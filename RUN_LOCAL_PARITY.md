# Single-command local LOSO retraining parity

The repository cannot access the user's D: drive. This wrapper locates the **exact SHA-256-matched** source archive, extracts frozen predictions locally, and runs the original recovered parity kit. It does not upload raw data.

1. Extract `PaperB_Reproduction_Audit.zip` into `D:\gw\PaperB_Reproduction_Audit` (or another folder).
2. In PowerShell, from `D:\gw\Transfer-Calibration`:

```powershell
git pull
python scripts/run_local_parity.py --root D:\gw --kit D:\gw\PaperB_Reproduction_Audit\PaperB_Numerical_Parity_Kit --out D:\gw\PaperB_Parity_Output
```

If the source archive is outside `D:\gw`, pass its path with `--archive`. If the results ZIP is elsewhere, pass `--results`.

The run may be computationally expensive. A green GitHub Actions evidence-consistency check is **not** a substitute for this run. The script fails closed if the source hash does not match or the recovered kit is absent. Do not publish original CGWB observations or provisional well-level records.
