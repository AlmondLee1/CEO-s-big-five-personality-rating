"""Download a local CEORater snapshot for research input preparation."""
import argparse
import json
import urllib.request
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=Path("outputs/ceorater_snapshot"))
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    for route, name in (("ceos", "ceorater_ceos.json"), ("meta", "ceorater_meta.json")):
        with urllib.request.urlopen(f"https://api.ceorater.com/api/v1/{route}", timeout=30) as response:
            payload = response.read()
        json.loads(payload)
        (args.output_dir / name).write_bytes(payload)
    print(f"Downloaded CEO records and metadata into {args.output_dir}")


if __name__ == "__main__":
    main()
