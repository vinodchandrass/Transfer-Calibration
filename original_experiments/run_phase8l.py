import argparse, hashlib, io, json, zipfile, datetime, platform, sklearn
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.metrics import mean_absolute_error

p=argparse.ArgumentParser(description='LOSO national groundwater transfer, frozen Phase8F feature protocol')
p.add_argument('--audit-zip',required=True);p.add_argument('--out',required=True);p.add_argument('--max-states',type=int,default=0,help='Optional smoke test; 0 runs all states')
a=p.parse_args();out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
with zipfile.ZipFile(a.audit_zip) as z:
    key=next((n for n in z.namelist() if n.replace('\\','/').endswith('conservative_national/conservative_observations.csv')),None)
    if key is None: raise RuntimeError('Missing conservative_observations.csv')
    df=pd.read_csv(z.open(key),usecols=['provisional_well_id','state','date','level_m'],low_memory=False)
df['date']=pd.to_datetime(df.date,errors='coerce');df['level_m']=pd.to_numeric(df.level_m,errors='coerce')
df=df.dropna(subset=['date','level_m','state','provisional_well_id']).copy()
df['period']=df.date.dt.to_period('Q');df=df.sort_values(['provisional_well_id','period','date'])
counts=df.groupby(['provisional_well_id','period'],sort=False).size().rename('n')
df=df.join(counts,on=['provisional_well_id','period']);df=df[df.n==1].copy()
g=df.groupby('provisional_well_id',sort=False)
df['prev_level']=g.level_m.shift();df['prev_period']=g.period.shift();df['prev_level2']=g.level_m.shift(2);df['prev_period2']=g.period.shift(2)
df['quarter_gap']=df.period.astype('int64')-df.prev_period.astype('int64');pairs=df[df.quarter_gap==1].copy()
pairs['target_year']=pairs.date.dt.year;pairs['target_quarter']=pairs.date.dt.quarter
pairs['prev2_valid']=(pairs.prev_period.astype('int64')-pairs.prev_period2.astype('int64')==1)
pairs['lag_change']=np.where(pairs.prev2_valid,pairs.prev_level-pairs.prev_level2,0.)
pairs['lag2_available']=pairs.prev2_valid.astype(int)
pairs['qsin']=np.sin(2*np.pi*pairs.target_quarter/4);pairs['qcos']=np.cos(2*np.pi*pairs.target_quarter/4)
features=['prev_level','lag_change','lag2_available','qsin','qcos']
pairs=pairs.dropna(subset=['prev_level','level_m']);pairs['split']=np.select([pairs.target_year<=2018,pairs.target_year.between(2019,2021),pairs.target_year>=2022],['train','validation','test'],default='exclude')
c=pairs.groupby(['state','split']).size().unstack(fill_value=0)
eligible=sorted(c.index[(c.get('train',0)>=100)&(c.get('validation',0)>=30)&(c.get('test',0)>=30)].tolist())
pairs=pairs[pairs.state.isin(eligible)].copy()
if a.max_states: eligible=eligible[:a.max_states]
results=[];predictions=[];logs=[]; fit_provenance=[]
def fingerprint(frame):
    keys=frame[['state','provisional_well_id','date','level_m','prev_level']].copy()
    keys['date']=keys['date'].dt.strftime('%Y-%m-%dT%H:%M:%S')
    keys=keys.sort_values(['state','provisional_well_id','date','level_m','prev_level'])
    payload=keys.to_csv(index=False,float_format='%.12g',lineterminator='\n').encode('utf-8')
    return hashlib.sha256(payload).hexdigest()

for i,target in enumerate(eligible,1):
    source=pairs[pairs.state!=target]
    tr=source[source.split=='train'];va=source[source.split=='validation'];te=pairs[(pairs.state==target)&(pairs.split=='test')].copy()
    if min(len(tr),len(va),len(te))==0:raise RuntimeError('Empty partition for '+target)
    assert not (tr.state==target).any() and not (va.state==target).any(), 'LOSO source-state leakage'
    assert (tr.target_year<=2018).all() and va.target_year.between(2019,2021).all() and (te.target_year>=2022).all(), 'Chronological leakage'
    assert tr[features].notna().all().all() and va[features].notna().all().all() and te[features].notna().all().all(), 'Nonfinite or missing features'
    tr_hash=fingerprint(tr); va_hash=fingerprint(va); te_hash=fingerprint(te)
    selection=[]
    for depth in (3,5,7):
        m=HistGradientBoostingRegressor(max_depth=depth,max_iter=150,learning_rate=.07,l2_regularization=1.,random_state=2026)
        fit_started=datetime.datetime.now(datetime.timezone.utc).isoformat()
        m.fit(tr[features],tr.level_m)
        fit_finished=datetime.datetime.now(datetime.timezone.utc).isoformat()
        fit_provenance.append({'held_out_state':target,'depth':depth,'fit_started_utc':fit_started,'fit_finished_utc':fit_finished,'training_count':len(tr),'validation_count':len(va),'test_count':len(te),'training_state_count':int(tr.state.nunique()),'held_out_in_training':int((tr.state==target).sum()),'held_out_in_validation':int((va.state==target).sum()),'training_partition_sha256':tr_hash,'validation_partition_sha256':va_hash,'test_partition_sha256':te_hash,'model_class':'HistGradientBoostingRegressor','max_iter':150,'learning_rate':0.07,'l2_regularization':1.0,'random_state':2026,'features':features,'sklearn_version':sklearn.__version__,'python_version':platform.python_version()})
        valpred=m.predict(va[features]);selection.append((mean_absolute_error(va.level_m,valpred),depth,m,valpred))
    selection.sort(key=lambda x:(x[0],x[1]));score,depth,model,valpred=selection[0]
    residual=np.abs(va.level_m.to_numpy()-valpred)
    # Split-conformal order statistic, finite-sample corrected; source-state calibration only.
    rank=min(len(residual),int(np.ceil((len(residual)+1)*0.90)))
    q=float(np.partition(residual,rank-1)[rank-1]);pred=model.predict(te[features]);truth=te.level_m.to_numpy();persist=te.prev_level.to_numpy()
    abs_hgb=np.abs(truth-pred);abs_persist=np.abs(truth-persist)
    coverage=float(np.mean(abs_hgb<=q))
    results.append({'state':target,'n_test':len(te),'test_wells':te.provisional_well_id.nunique(),'source_train_n':len(tr),'source_validation_n':len(va),'selected_depth':depth,'source_validation_mae':score,'LOSO_HGB_MAE':float(abs_hgb.mean()),'persistence_MAE':float(abs_persist.mean()),'delta_MAE_HGB_minus_persistence':float((abs_hgb-abs_persist).mean()),'source_conformal_q90_m':q,'LOSO_coverage_90':coverage,'LOSO_interval_width_m':2*q})
    predictions.append(pd.DataFrame({'state':target,'provisional_well_id':te.provisional_well_id.to_numpy(),'date':te.date.to_numpy(),'level_m':truth,'prev_level':persist,'loso_prediction':pred,'abs_error_hgb':abs_hgb,'abs_error_persistence':abs_persist,'lower_90':pred-q,'upper_90':pred+q}))
    logs.append({'state':target,'depth_validation_scores':{str(d):float(s) for s,d,_,_ in selection}})
    print(f'[{i}/{len(eligible)}] {target}: MAE {abs_hgb.mean():.4f}, persistence {abs_persist.mean():.4f}, coverage {coverage:.3f}',flush=True)
res=pd.DataFrame(results);res.to_csv(out/'loso_state_metrics.csv',index=False)
allpred=pd.concat(predictions,ignore_index=True);allpred.to_csv(out/'loso_test_predictions.csv',index=False)
summary={'source_zip_sha256':hashlib.sha256(Path(a.audit_zip).read_bytes()).hexdigest(),'protocol':'LOSO state exclusion from training and validation; target-state test 2022+; features and model grid frozen to Phase8F','feature_columns':features,'states_completed':len(eligible),'fit_provenance_records':len(fit_provenance),'fit_time_instrumentation':True,'partial_smoke_test':bool(a.max_states),'test_predictions':len(allpred),'pooled_LOSO_MAE':float(allpred.abs_error_hgb.mean()),'pooled_persistence_MAE':float(allpred.abs_error_persistence.mean()),'pooled_90_coverage':float(((allpred.level_m>=allpred.lower_90)&(allpred.level_m<=allpred.upper_90)).mean()),'limitations':['Station IDs provisional','Conformal exchangeability across source and held-out target states is not assumed','Calibration uses pooled source-state validation residuals','No target-state labels used for model selection or calibration','Measurement conventions and source release timing unverified','No multiplicity-adjusted inference or bootstrap in this script']}
(out/'fit_provenance.json').write_text(json.dumps(fit_provenance,indent=2),encoding='utf-8');(out/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8');(out/'selection_log.json').write_text(json.dumps(logs,indent=2),encoding='utf-8')
print(json.dumps(summary,indent=2))
