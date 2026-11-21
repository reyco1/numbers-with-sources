"""Check every number an agent reports against the data it says it used."""
import csv
import json
from pathlib import Path

VERIFIED = "Verified"
MISMATCH = "Mismatch"
NOT_VERIFIED = "Not verified"


def lookup(source, data_dir):
    """Return (found_value, note). found_value is None if it can't be read.

    A source looks like "file.csv:row_key". The CSV needs a `key` column
    and a `value` column.
    """
    if not source or ":" not in source:
        return None, "no source given"
    file_name, row_key = source.rsplit(":", 1)
    root = Path(data_dir).resolve()
    path = (root / file_name).resolve()
    if root not in path.parents:
        return None, "source is outside the data folder"
    if not path.is_file():
        return None, f"file not found: {file_name}"
    with path.open(newline="") as f:
        for row in csv.DictReader(f):
            if row.get("key") == row_key:
                try:
                    return float(row["value"]), ""
                except (KeyError, TypeError, ValueError):
                    return None, f"row {row_key} has no usable value"
    return None, f"row not found: {row_key}"


def check_claim(claim, data_dir, tolerance=0.0):
    """Return a result dict for one claim."""
    found, note = lookup(claim.get("source"), data_dir)
    result = {
        "claim": claim.get("claim", ""),
        "reported": claim.get("value"),
        "source": claim.get("source"),
        "found": found,
        "note": note,
    }
    if found is None:
        result["status"] = NOT_VERIFIED
    elif abs(found - claim["value"]) <= tolerance:
        result["status"] = VERIFIED
    else:
        result["status"] = MISMATCH
        result["note"] = f"agent said {claim['value']:g}, source says {found:g}"
    return result


def check_answer(answer, data_dir, tolerance=0.0):
    """Check a list of claims. `answer` is the parsed JSON list."""
    return [check_claim(c, data_dir, tolerance) for c in answer]


def load_answer(path):
    with open(path) as f:
        return json.load(f)
