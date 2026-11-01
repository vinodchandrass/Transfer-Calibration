import argparse,zipfile,io,json,hashlib
from pathlib import Path
import numpy as np,pandas as pd
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.metrics import mean_absolute_error,mean_squared_error
p=argparse.ArgumentParser();p.add_argument('--audit-zip',required=True);p.add_argument('--out',required=True);a=p.parse_args()
out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
with zipfile.ZipFile(a.audit_zip) as z:
 names=z.namelist(); key=next((n for n in names if n.replace('\\','/').endswith('conservative_national/conservative_observations.csv')),None)
 if key is None: raise RuntimeError('conservative observations absent')
 df=pd.read_csv(z.open(key),usecols=['provisional_well_id','state','date','year_quarter','level_m'],dtype={'provisional_well_id':'string','state':'string'},low_memory=False)
df['date']=pd.to_datetime(df.date,errors='coerce');df['level_m']=pd.to_numeric(df.level_m,errors='coerce');df=df.dropna(subset=['date','level_m','state','provisional_well_id'])
df['period']=df.date.dt.to_period('Q'); df=df.sort_values(['provisional_well_id','period','date'])
# Quarter with multiple days is ambiguous for a quarterly target: exclude rather than silently select a reading.
counts=df.groupby(['provisional_well_id','period'],sort=False).size().rename('n');ambig=int((counts>1).sum());df=df.join(counts,on=['provisional_well_id','period']);df=df.loc[df.n==1].copy()
df=df.sort_values(['provisional_well_id','period']);g=df.groupby('provisional_well_id',sort=False)
df['prev_level']=g.level_m.shift();df['prev_period']=g.period.shift();df['prev_date']=g.date.shift();df['prev_level2']=g.level_m.shift(2);df['prev_period2']=g.period.shift(2)
df['quarter_gap']=(df.period.astype('int64')-df.prev_period.astype('int64'));pairs=df.loc[df.quarter_gap==1].copy()
pairs['target_year']=pairs.date.dt.year;pairs['target_quarter']=pairs.date.dt.quarter
pairs['prev2_valid']=(pairs.prev_period.astype('int64')-pairs.prev_period2.astype('int64')==1)
pairs['lag_change']=np.where(pairs.prev2_valid,pairs.prev_level-pairs.prev_level2,0.)
pairs['lag2_available']=pairs.prev2_valid.astype(int)
pairs['qsin']=np.sin(2*np.pi*pairs.target_quarter/4);pairs['qcos']=np.cos(2*np.pi*pairs.target_quarter/4)
features=['prev_level','lag_change','lag2_available','qsin','qcos'];pairs=pairs.dropna(subset=['prev_level','level_m'])
pairs['split']=np.select([pairs.target_year<=2018,pairs.target_year.between(2019,2021),pairs.target_year>=2022],['train','validation','test'],default='exclude')
summary={'source_zip_sha256':hashlib.sha256(Path(a.audit_zip).read_bytes()).hexdigest(),'quarter_groups_with_multiple_days_excluded':ambig,'pair_count':int(len(pairs)),'feature_columns':features,'split_counts':pairs.split.value_counts().to_dict(),'limitations':['Station IDs remain provisional','One observation per well-quarter required; ambiguous quarters excluded','No rainfall/aquifer variables','Contemporaneous cross-state pooling is not leave-one-state-out','Source publication timing and measurement datum not verified']}
counts=pairs.groupby(['state','split']).size().unstack(fill_value=0);counts.to_csv(out/'pair_eligibility_by_state.csv');eligible=counts.index[(counts.get('train',0)>=100)&(counts.get('validation',0)>=30)&(counts.get('test',0)>=30)].tolist();summary['eligible_by_conservative_pair_thresholds']=eligible
pairs=pairs[pairs.state.isin(eligible)].copy();train=pairs[pairs.split=='train'];val=pairs[pairs.split=='validation'];test=pairs[pairs.split=='test']
if min(len(train),len(val),len(test))==0:raise RuntimeError('Insufficient split data')
models=[]
for depth in [3,5,7]:
 m=HistGradientBoostingRegressor(max_depth=depth,max_iter=150,learning_rate=.07,l2_regularization=1.,random_state=2026)
 m.fit(train[features],train.level_m);score=mean_absolute_error(val.level_m,m.predict(val[features]));models.append((score,depth,m))
models.sort(key=lambda x:x[0]);best=models[0];summary['validation_depth_selection']=[{'depth':int(d),'mae':float(s)} for s,d,_ in models];summary['selected_depth']=int(best[1]);m=best[2]
# All selection occurs on validation. Test is evaluated once after depth selection.
test=test.copy();test['prediction']=m.predict(test[features]);test['persistence']=test.prev_level
results=[]
for state,grp in test.groupby('state'):
 for name,col in [('HGB', 'prediction'),('persistence','persistence')]:
  results.append({'state':state,'model':name,'n':len(grp),'wells':grp.provisional_well_id.nunique(),'MAE':mean_absolute_error(grp.level_m,grp[col]),'RMSE':np.sqrt(mean_squared_error(grp.level_m,grp[col]))})
pd.DataFrame(results).to_csv(out/'chronological_test_metrics.csv',index=False)
test[['state','provisional_well_id','date','level_m','prev_level','prediction','persistence']].to_csv(out/'chronological_test_predictions.csv',index=False)
# No conformal calibration here: would require explicitly designed calibration partitions.
summary['national_chronological_model_trained']=True;summary['LOSO_trained']=False;summary['interval_calibration_performed']=False
(out/'summary.json').write_text(json.dumps(summary,indent=2,default=str),encoding='utf-8')
print(json.dumps({'eligible_states':len(eligible),'test_rows':len(test),'selected_depth':best[1],'output':str(out)},indent=2))
