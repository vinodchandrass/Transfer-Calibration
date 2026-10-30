# Fast local parity workflow (no raw-data upload)

Run from PowerShell in the cloned repository:

```powershell
git pull
python scripts/find_source_archive.py --root D:\gw --out source_archive_location.txt
```

If the archive is found, run the original recovered parity kit *locally* with the archive path and original frozen predictions. The expected archive SHA-256 is `3cab021225bca327f61f46a4b67f47b2597bb37b4c94503ed057a44165450bcd`.

This locator does not read raw observation contents, change source files, or upload anything. A filename match is insufficient: only the exact SHA-256 is accepted. If no match is found, search the larger original project directory with `--root` pointing to that directory. Do not bypass the hash gate.

The frozen prediction output can be extracted locally from the provided Phase 8H results ZIP. Until retraining and prediction parity are demonstrated, do not claim an independently reproduced model.
