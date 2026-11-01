# Transfer–Calibration: Groundwater Paper B

Evidence and reproducibility-support repository for **“Geographic Heterogeneity in Transfer Performance and Prediction-Interval Calibration in Retrospective Groundwater Forecasting Across 23 Indian States.”**

**Status: partial verification; not a complete end-to-end reproducibility release.** This repository contains archived aggregate evidence, source-audit notes, an evidence-consistency checker, and a wrapper for running a separately recovered LOSO retraining/parity kit on the researcher's machine. It does **not** contain the original complete model-training pipeline, raw CGWB observations, or individual well-level predictions.

## Verified and reported evidence

| Check | Status | Evidence |
| --- | --- | --- |
| Archived summary arithmetic and structure | Automated consistency check; GitHub Actions passed | `scripts/verify_evidence.py`, `evidence/`, workflow |
| Recovered LOSO training configuration and prediction-file hashes | Inspected in an earlier audit; originals not published here | `audits/recovered_pipeline_audit.md` |
| LOSO retraining on 23 states, 87,335 matched records | Researcher-reported local numerical parity PASS; underlying machine-generated log/report not independently inspected here | `audits/phase8h_local_parity_2026-10-30.md` |
| Pooled HGB training and predictions | Not independently reproduced here | `REPRODUCIBILITY_STATUS.md` |
| Bootstrap confidence intervals and full calibration analysis | Not independently reproduced here | `REPRODUCIBILITY_STATUS.md` |
| Authenticated CGWB well identities and historical source-release timing | Not established | `REPRODUCIBILITY_STATUS.md` |

The summary checker **does not retrain models**. A green GitHub Actions check must not be described as experimental reproduction.

## Local verification

To check the archived public summaries (Python 3.11; standard library only):

```bash
python scripts/verify_evidence.py
```

To run LOSO numerical parity using **existing local source archives and the separately recovered parity kit**, follow [RUN_LOCAL_PARITY.md](RUN_LOCAL_PARITY.md). The wrapper checks the expected archive SHA-256 before invoking the kit. The underlying archive and recovered parity kit are **not included** in this repository; an external reader cannot reproduce the experiment from this checkout alone.

## Scientific boundaries

- Well identities are provisional composite keys, not authenticated official CGWB well IDs.
- LOSO evaluates transfer to a held-out state **while permitting antecedent target-well measurements**; it does not evaluate previously unmonitored wells.
- The retrospective split is based on observation dates, not independently verified historical data-release dates.
- Administrative states are not hydrogeological basin boundaries.
- Data-source inventory checks do not establish measurement-datum equivalence across states.

## Data, scope and release

Original CGWB data, manuscript/PDF, and individual prediction-level records are **not redistributed**. Only author-owned experimental code, protocols, derived aggregate evidence, integrity manifests and audit instructions may be published after verification and author approval.

No versioned research release has been approved or tagged. Do not cite this repository as proof of complete independent reproduction. See [REPRODUCIBILITY_STATUS.md](REPRODUCIBILITY_STATUS.md) for outstanding gates.
