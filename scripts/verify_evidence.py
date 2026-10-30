#!/usr/bin/env python3
"""Check consistency of published Phase 8M/8N evidence summaries.
This script does NOT reproduce model training or bootstrap estimates.
Only Python standard library is required.
"""
from pathlib import Path
import json
import math

root = Path(__file__).resolve().parents[1]
m = json.loads((root / "evidence/phase8m_summary.json").read_text())
n = json.loads((root / "evidence/phase8n_source_summary.json").read_text())
assert m["records"] == 87335 and m["states"] == 23
assert m["provisional_wells"] == 19579
assert math.isclose(m["loso_mae"] - m["pooled_mae"], m["loso_minus_pooled"], abs_tol=1e-12)
assert 0 <= m["coverage_90"] <= 1
assert m["bootstrap_replicates_per_state"] == 2000
assert m["states_loso_worse_than_pooled"] <= m["states"]
assert m["states_loso_worse_than_persistence"] <= m["states"]
assert n["csv_files"] == 51 and n["source_rows"] == 1368883 and n["states"] == 26
assert len(n["source_zip_sha256"]) == 64
print("PASS: archived evidence summary consistency checks")
print("NOT TESTED: original model training, matched-row recomputation, well identity, release-time leakage")
