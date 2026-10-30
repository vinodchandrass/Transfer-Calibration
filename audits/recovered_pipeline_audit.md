# Recovered experimental evidence audit — 2026-10-30

The user-provided `PaperB_Reproduction_Audit.zip` was inspected without running model training.

## Recovered executable sources
- `GW_Phase8H_Kit/run_phase8h.py`: SHA-256 `47873ea78fe6c66fd64220486d5e129c54bf0d6e0d2c22a38cbc1bc3349033da`.
- `GW_Phase8L_Kit/run_phase8l.py`: SHA-256 `e6be4462b8426a029fa3a5b2a79c5a5e735e481a6cd42b5e5cb38da0f92104bf`.
- `PaperB_Numerical_Parity_Kit/frozen_phase8h_reproduction.py`: byte-identical to Phase8H script.
- `PaperB_Numerical_Parity_Kit/verify.py`: SHA-256 `81043797b4e15de833abe51c128e8b432adecc83cbed755794ba9ce0c8e63463`.

## Recovered training configuration
- HGB feature columns: `prev_level`, `lag_change`, `lag2_available`, `qsin`, `qcos`.
- `HistGradientBoostingRegressor`: `max_iter=150`, `learning_rate=0.07`, `l2_regularization=1.0`, `random_state=2026`.
- Depth selected using validation MAE; held-out state excluded from LOSO training and validation.
- Conformal intervals calibrated on source-state validation residuals.

These are *source-code declarations*, not a claim that a fresh model training run has passed.

## Frozen-output identity
`loso_test_predictions.csv` from Phase8H, Phase8L, and final prediction linkage are byte-identical:
SHA-256 `a15e10dc20bcfc61ac9b01ecb484275ac9113be65b277f7c31f3a0a6846d3787` (15,467,837 bytes).

## Blocking dependency
The retraining/parity scripts require the archive with SHA-256
`3cab021225bca327f61f46a4b67f47b2597bb37b4c94503ed057a44165450bcd`,
containing `conservative_national/conservative_observations.csv`.
That archive was not included in the audit bundle, so no retraining was performed.

The original CGWB dataset and manuscript must not be published here. All well identifiers remain provisional.
