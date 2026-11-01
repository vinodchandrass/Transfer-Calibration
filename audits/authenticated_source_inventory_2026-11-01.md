# Authenticated source-code inventory (2026-11-01)

These hashes were independently recalculated from the user-provided project archives during the current repository-completion review. **Hash matching establishes byte identity, not successful execution or scientific validity.**

| Archive | Member | SHA-256 |
|---|---|---|
| PaperB_Reproduction_Audit.zip | GW_Phase8H_Kit/run_phase8h.py | `47873ea78fe6c66fd64220486d5e129c54bf0d6e0d2c22a38cbc1bc3349033da` |
| PaperB_Reproduction_Audit.zip | GW_Phase8L_Kit/run_phase8l.py | `e6be4462b8426a029fa3a5b2a79c5a5e735e481a6cd42b5e5cb38da0f92104bf` |
| PaperB_Reproduction_Audit.zip | PaperB_Numerical_Parity_Kit/frozen_phase8h_reproduction.py | `47873ea78fe6c66fd64220486d5e129c54bf0d6e0d2c22a38cbc1bc3349033da` |
| PaperB_Reproduction_Audit.zip | PaperB_Numerical_Parity_Kit/verify.py | `81043797b4e15de833abe51c128e8b432adecc83cbed755794ba9ce0c8e63463` |
| PaperB_Final_Reproduction_Scripts.zip | GW_Phase8F_Kit/run_phase8f.py | `19d06866cd0e6913e4c97b96b619dc2347e71effc8918b0eb17fe9eab12dc08d` |
| PaperB_Final_Reproduction_Scripts.zip | GW_Phase8L_Kit/run_phase8l.py | `e6be4462b8426a029fa3a5b2a79c5a5e735e481a6cd42b5e5cb38da0f92104bf` |
| PaperB_Final_Reproduction_Scripts.zip | PaperB_Final_Source_Calibration_Audit.py | `14794f53970f6793d61d34eac9443720b08c5132a09290f2a3b2d168d736a4e5` |
| PaperB_Final_Reproduction_Scripts.zip | PaperB_Final_Validity_Inference_Audit.py | `2a5708efcfe567b1eb53fc0dc445ca0e923bd9234ade07231ba91188e800d797` |

**Source archive identity:** the locally available `CGWB_National_28_State_Original_CSVs(1).zip` has SHA-256 `23e67d1a9dc66a52c4e04f56fc024b7089ff62903e17b4e6ebad351e62a73b0f`, agreeing with the Phase 8N source inventory. This is **different** from the Phase8H processed-input archive required by `run_local_parity.py` (`3cab021225bca327f61f46a4b67f47b2597bb37b4c94503ed057a44165450bcd`). They must not be interchanged.

No raw observations, prediction rows, or manuscript files are included in this inventory. A complete release remains contingent on source-code publication and independent checks.
