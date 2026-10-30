# Local Phase 8H LOSO retraining parity — user-reported result (2026-10-30)

**Status:** PASS reported by the researcher from a local PowerShell execution. The underlying local report and full log have not yet been independently uploaded and inspected here.

## Input and scope

- Source ZIP SHA-256: `3cab021225bca327f61f46a4b67f47b2597bb37b4c94503ed057a44165450bcd`.
- Frozen prediction CSV SHA-256: `a15e10dc20bcfc61ac9b01ecb484275ac9113be65b277f7c31f3a0a6846d3787`.
- LOSO model retraining completed: 23 states, 87,335 test records.
- Matched rows: 87,335; left-only: 0; right-only: 0.
- Maximum absolute difference: 0.0 for `level_m`, `prev_level`, `loso_prediction`, `lower_90`, `upper_90`.
- `numerical_parity_pass`: true.
- LOSO MAE: 2.097133438517085 m.
- Persistence MAE: 2.2665031208849378 m.
- Nominal 90% interval coverage: 0.8949562031258945.
- Model features: `prev_level`, `lag_change`, `lag2_available`, `qsin`, `qcos`.
- Held-out state excluded from training and validation; source-state residuals used for calibration.

## Boundaries

This is strong evidence for **LOSO model retraining and prediction-level numerical parity**, not proof of the full paper's end-to-end reproduction. Pooled HGB model retraining, well-cluster bootstrap inference, alternative interval calibration, official well-ID authentication, and historical source-release timing were not verified by this local parity report.

No original CGWB data, prediction-level records, or manuscript files are included here. This file is a transcription of the user's reported local results, not a separately signed machine-generated provenance artifact.
