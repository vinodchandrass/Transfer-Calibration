# Reproducibility status and release gate

**Current level: summary-level verification only. Not an end-to-end reproduction.**

The repository contains transcribed, provenance-labeled summaries from existing Phase 8M and Phase 8N evidence packages and a standard-library Python script checking arithmetic and structural consistency. These are *not* independent re-executions of the original forecasting models.

## Run
```bash
python scripts/verify_evidence.py
```

## Required for complete reproduction
1. Original training and inference code for pooled HGB, leave-one-state-out HGB, and persistence.
2. Authenticated feature list, HGB hyperparameters, model-selection decisions, random seeds and dependency versions.
3. Deterministic preprocessing and matching protocol; original prediction-level outputs and well-cluster assignments.
4. Bootstrap and interval-calibration implementation with input-output hash reconciliation.
5. Re-execution against the specified source archives without distributing raw CGWB datasets.

## Scientific caveats
- Well keys are provisional; official CGWB well IDs have not been authenticated.
- Observation-date retrospective validation is not historical source-release validation.
- Administrative-state holdout does not establish aquifer-level generalization.
- LOSO predictions may use target-well antecedent measurements.
- The Phase 8N source audit does not certify measurement datum or conventions.

Do not claim complete reproducibility, independent model replication, or verified training code on the basis of this repository.
