#!/usr/bin/env python3
"""Locate the required original Phase8F source archive by SHA-256, without uploading it."""
import argparse, hashlib, os, sys, zipfile
from pathlib import Path
EXPECTED="3cab021225bca327f61f46a4b67f47b2597bb37b4c94503ed057a44165450bcd"
ap=argparse.ArgumentParser()
ap.add_argument("--root",default=r"D:\\gw")
ap.add_argument("--out",default="source_archive_location.txt")
a=ap.parse_args()
root=Path(a.root)
if not root.is_dir(): sys.exit(f"Directory not found: {root}")
matches=[]; scanned=0; candidates=0
for folder,_,names in os.walk(root):
 for name in names:
  if not name.lower().endswith(".zip"):continue
  p=Path(folder)/name; scanned+=1
  try:
   with zipfile.ZipFile(p) as z:
    if not any(x.replace("\\","/").endswith("conservative_national/conservative_observations.csv") for x in z.namelist()):continue
   candidates+=1
   h=hashlib.sha256()
   with p.open("rb") as f:
    for b in iter(lambda:f.read(8*1024*1024),b""):h.update(b)
   digest=h.hexdigest()
   print(f"Candidate: {p} SHA256={digest}",flush=True)
   if digest==EXPECTED:matches.append(str(p.resolve()))
  except (OSError,zipfile.BadZipFile,PermissionError) as e:print(f"SKIP {p}: {e}",file=sys.stderr)
Path(a.out).write_text("\\n".join(matches)+("\\n" if matches else ""),encoding="utf-8")
print(f"Scanned {scanned} ZIP files; {candidates} contain expected member; exact matches={len(matches)}")
if matches: print("FOUND:",*matches,sep="\\n");sys.exit(0)
sys.exit("Required exact source archive not found under selected root")
