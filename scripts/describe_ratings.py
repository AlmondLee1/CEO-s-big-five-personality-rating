"""Describe valid-score distributions and failure rates across saved runs."""
import argparse
import csv
import json
import statistics
from collections import defaultdict
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runs", type=Path, nargs="+", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    groups = defaultdict(list)
    input_hashes = set()
    for directory in args.runs:
        metadata = json.loads((directory / "run.json").read_text(encoding="utf-8"))
        if metadata["mode"] != "live_api":
            raise ValueError(f"Synthetic data cannot enter a research summary: {directory}")
        input_hashes.add(metadata["input_sha256"])
        for line in (directory / "ratings.jsonl").read_text(encoding="utf-8").splitlines():
            row = json.loads(line)
            key = (str(directory), metadata["provider"], metadata["model_requested"],
                   metadata["dimension"], row["ceo_id"], row["ceo_name"])
            groups[key].append(row)
    if len(input_hashes) != 1:
        raise ValueError("Runs use different CEO input snapshots")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["run_directory", "provider", "model", "dimension", "ceo_id", "ceo_name",
                         "recorded", "valid", "failed", "failure_rate", "mean", "median", "sd", "minimum", "maximum"])
        for key, rows in sorted(groups.items()):
            valid = [float(r["score"]) for r in rows if r["status"] == "ok"]
            if any(value < 1 or value > 7 for value in valid):
                raise ValueError(f"Out-of-range valid score: {key}")
            writer.writerow([*key, len(rows), len(valid), len(rows) - len(valid),
                             round((len(rows) - len(valid)) / len(rows), 4),
                             round(statistics.mean(valid), 4) if valid else "",
                             round(statistics.median(valid), 4) if valid else "",
                             round(statistics.stdev(valid), 4) if len(valid) > 1 else "",
                             min(valid) if valid else "", max(valid) if valid else ""])
    print(f"Wrote {args.output} for {len(groups)} CEO/provider/dimension groups")


if __name__ == "__main__":
    main()
