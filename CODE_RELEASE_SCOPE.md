# Paper B recovered code: scope and limitations

The recovered code-only package contains seven original Python scripts. Their original byte-level hashes and archive provenance are listed in `audits/authenticated_source_inventory_2026-11-01.md` and the separately prepared `SOURCE_MANIFEST.json`.

**Important:** Source-file syntax checks are not model reproduction. The original scripts depend on specific input archives and paths; they are not a self-contained, tested installation. `requirements-experiments.txt` names imported third-party packages but intentionally does not invent original dependency versions.

## Reproduction checklist

- Archived summary consistency: verified by the public CI workflow.
- Recovered script syntax: checked in the code-only package.
- LOSO numerical parity: researcher-reported local pass; machine-generated report not independently authenticated here.
- Pooled HGB, bootstrap and full interval calibration: not independently verified.
- Official well IDs, physical datum consistency, and historical source release times: not established.

No CGWB raw data, observation-level predictions, manuscript, or PDF may be committed. Do not describe a release as end-to-end reproducible until the outstanding evidence checks have passed.
