#!/usr/bin/env python3
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
matrix = ROOT / "02_problem_definition_evidence/traceability_matrix.csv"

if not matrix.exists():
    print("No traceability matrix found.")
    raise SystemExit(1)

with matrix.open(encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

print("# Traceability Summary")
for row in rows:
    print(f"- {row.get('Requirement ID')}: {row.get('Business Goal')} -> {row.get('Status')}")
