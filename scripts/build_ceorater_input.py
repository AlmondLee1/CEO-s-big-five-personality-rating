"""Create a fixed CEO input from a saved CEORater API response."""
import argparse
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--sample", type=Path)
    args = parser.parse_args()
    payload = json.loads(args.source.read_text(encoding="utf-8"))
    source_rows = payload["items"]
    if payload["total"] != len(source_rows):
        raise ValueError("The downloaded response is incomplete")
    counts = Counter((r["ticker"], r["ceo"]) for r in source_rows)
    if any(value > 1 for value in counts.values()):
        raise ValueError("A ticker and CEO pair occurs more than once")
    rows = [{"ceo_id": f"{r['ticker']}|{r['ceo']}", "name": r["ceo"],
             "company": r["company"], "ticker": r["ticker"],
             "tenure_years": r["tenure_years"]} for r in source_rows]
    rows.sort(key=lambda r: (r["ticker"], r["name"]))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    for path, selected in ((args.output, rows), (args.sample, rows[:2])):
        if path is None:
            continue
        with path.open("w", encoding="utf-8-sig", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(selected)
    manifest = {"source_url": "https://api.ceorater.com/api/v1/ceos",
                "source_file": str(args.source), "source_sha256": hashlib.sha256(args.source.read_bytes()).hexdigest(),
                "record_count": len(rows), "input_file": str(args.output),
                "input_sha256": hashlib.sha256(args.output.read_bytes()).hexdigest(),
                "co_ceo_tickers": {ticker: count for ticker, count in Counter(r["ticker"] for r in rows).items() if count > 1},
                "repeated_names": {name: count for name, count in Counter(r["name"] for r in rows).items() if count > 1}}
    args.output.with_suffix(".manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
