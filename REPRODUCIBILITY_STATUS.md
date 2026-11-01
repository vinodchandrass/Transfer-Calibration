# Reproducibility status and release gate

**Assessment: partially verified research evidence; NOT complete end-to-end reproduction.**

## Evidence levels

1. **Automated, public summary consistency:** `python scripts/verify_evidence.py` checks fixed archived figures and arithmetic; GitHub Actions has passed. This does not recompute predictions or statistical inference.
2. **Recovered source declarations:** The previously inspected Phase8H/Phase8L code declared features `prev_level`, `lag_change`, `lag2_available`, `qsin`, `qcos`; HGB `max_iter=150`, `learning_rate=0.07`, `l2_regularization=1.0`, `random_state=2026`, with depth selected using validation MAE. These declarations are recorded in `audits/recovered_pipeline_audit.md`; original scripts are not in this public repository.
3. **Researcher-reported LOSO parity:** A local run reportedly reproduced 23 held-out states and 87,335 matched test records, with numerical differences of zero for the recorded prediction and interval columns. The machine-generated report and full log have not been independently inspected in this repository. See `audits/phase8h_local_parity_2026-10-30.md`.
4. **Unverified components:** Pooled HGB retraining, bootstrap resampling and inference, independent calibration re-execution beyond the reported LOSO parity, official well identity, and historical source-release timing.

## Conditions for a complete reproduction claim

- [ ] Publish verified author-owned original pooled and LOSO training/inference code with deterministic preprocessing and matching.
- [ ] Record a tested environment/dependency lock and all model-selection decisions.
- [ ] Provide a reproducible path to authorized source acquisition **without** uploading original CGWB datasets.
- [ ] Recompute pooled and LOSO matched-row outputs and reconcile checksums and numerical metrics.
- [ ] Recompute the well-cluster bootstrap and nominal 90% interval calibration, with machine-readable verification reports.
- [ ] Inspect and preserve the underlying local parity report and environment information, with no observation-level or identifying records exposed.
- [ ] Obtain explicit author approval for the exact public release contents; then tag a versioned release.

**Do not substitute the existing GitHub Actions PASS for any unchecked item.** A limited code/evidence-availability statement is appropriate; an end-to-end reproducibility claim is not.

## Interpretation caveats

- Well keys are provisional; authenticated CGWB well IDs are unavailable.
- Observation-date retrospective evaluation is not historical source-release validation.
- State holdout is not aquifer-level generalization.
- LOSO may use target-well antecedent measurements; it is not unseen-well forecasting.
- Source-field inventory is not certification of physical measurement conventions.

## Public-release boundaries

Do not upload the manuscript, journal PDF, original CGWB datasets, or individual prediction-level records. Any additional code or aggregate outputs must be authenticated and approved before public release.
