#!/usr/bin/env python3
"""One-command local Phase8H retraining parity. Original datasets never leave this machine."""
import argparse, hashlib, os, subprocess, sys, tempfile, zipfile
from pathlib import Path
EXPECTED="3cab021225bca327f61f46a4b67f47b2597bb37b4c94503ed057a44165450bcd"
p=argparse.ArgumentParser()
p.add_argument("--root",default=r"D:\gw",help="Search root for original source ZIP and Phase8H results ZIP")
p.add_argument("--archive",help="Optional explicit original source ZIP path")
p.add_argument("--results",help="Optional explicit Phase8H results ZIP path")
p.add_argument("--kit",help="Local PaperB_Numerical_Parity_Kit directory (from audit bundle)")
p.add_argument("--out",default="local_parity_output")
a=p.parse_args()
root=Path(a.root)
if not root.exists():sys.exit(f"Root does not exist: {root}")
def digest(path):
 h=hashlib.sha256()
 with path.open("rb") as f:
  for block in iter(lambda:f.read(8*1024*1024),b""):h.update(block)
 return h.hexdigest()
def candidates():
 for folder,_,names in os.walk(root):
  for name in names:
   if name.lower().endswith(".zip"):yield Path(folder)/name
archive=Path(a.archive) if a.archive else None
results=Path(a.results) if a.results else None
if archive and digest(archive)!=EXPECTED:sys.exit("Explicit source archive SHA-256 mismatch; aborting")
for path in ([] if archive and results else candidates()):
 if results is None and path.name.lower()=="gw_phase8h_results.zip":results=path
 if archive is None:
  try:
   with zipfile.ZipFile(path) as z:
    if not any(x.replace(chr(92),"/").endswith("conservative_national/conservative_observations.csv") for x in z.namelist()):continue
   print("Checking candidate archive hash:",path,flush=True)
   if digest(path)==EXPECTED:archive=path
  except (OSError,zipfile.BadZipFile):pass
 if archive and results:break
if not archive:sys.exit("BLOCKED: exact source archive not found. Pass --archive or broaden --root.")
if not results:sys.exit("BLOCKED: GW_Phase8H_Results.zip not found. Pass --results.")
kit=Path(a.kit) if a.kit else root/"PaperB_Numerical_Parity_Kit"
if not (kit/"verify.py").is_file():sys.exit(f"BLOCKED: missing original parity kit {kit}/verify.py; extract PaperB_Reproduction_Audit.zip first.")
out=Path(a.out).resolve();out.mkdir(parents=True,exist_ok=True)
with tempfile.TemporaryDirectory() as d:
 with zipfile.ZipFile(results) as z:
  matches=[x for x in z.namelist() if x.replace(chr(92),"/").endswith("loso_test_predictions.csv")]
  if len(matches)!=1:sys.exit(f"Expected one frozen prediction CSV; found {len(matches)}")
  frozen=Path(d)/"loso_test_predictions.csv"
  frozen.write_bytes(z.read(matches[0]))
 print("Verified original source SHA256:",EXPECTED,flush=True)
 print("Running recovered retraining and numerical parity; this may take substantial CPU time.",flush=True)
 cmd=[sys.executable,str(kit/"verify.py"),"--archive",str(archive),"--frozen",str(frozen),"--out",str(out)]
 completed=subprocess.run(cmd,check=False)
 if completed.returncode:sys.exit(completed.returncode)
import json
report=json.loads((out/"numerical_parity_report.json").read_text())
if report.get("numerical_parity_pass") is True:
 print("PASS: independent retraining matches frozen predictions within 1e-8")
else:
 sys.exit("FAIL: retraining numerical parity not demonstrated; inspect "+str(out))
