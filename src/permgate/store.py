"""A records store with two access paths: trusting and scoped.

The scoped accessor is the whole point of this repo: restricted fields are
stripped AT THE DATA LAYER, before any model-shaped component ever sees them.
A credential that cannot fetch a field cannot leak it - no matter what the
prompt says, and no matter how the model behaves.
"""
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
RESTRICTED_FIELDS = {"gov_id", "case_notes"}


def load_records():
    return {r["user"]: r for r in
            (json.loads(l) for l in (ROOT / "data" / "records.jsonl").read_text().splitlines() if l.strip())}


def fetch_trusting(user):
    """Full record. Security is delegated to whatever reads it (i.e. the prompt)."""
    return dict(load_records().get(user, {}))


def fetch_scoped(user):
    """Field-level permission enforcement: restricted fields never leave the store."""
    rec = load_records().get(user, {})
    return {k: v for k, v in rec.items() if k not in RESTRICTED_FIELDS}


def restricted_values():
    """Ground truth for leak detection: every value that must never appear in output."""
    vals = set()
    for rec in load_records().values():
        for f in RESTRICTED_FIELDS:
            if f in rec:
                vals.add(str(rec[f]))
    return vals
