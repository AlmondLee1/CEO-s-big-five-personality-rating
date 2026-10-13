# CEO Big Five rating pilot

Run a ten-CEO example that requests individual Big Five ratings from a selected LLM and saves a record for every rating slot. The scores are model-generated impressions, not verified CEO traits. The [technical appendix](TECHNICAL_APPENDIX.pdf) explains the protocol and evidence.

## Contents

1. [Install](#install)
2. [Try the package without an API key](#try-the-package-without-an-api-key)
3. [Run a live pilot](#run-a-live-pilot)
4. [Inspect the output](#inspect-the-output)
5. [If a run stops](#if-a-run-stops)

## Install

Install Python 3.11 or newer. Open a terminal in this `submission` folder and run:

```powershell
python -m pip install -r requirements.txt
```

For Claude or Gemini, also run `python -m pip install -r requirements-optional.txt`.

## Try the package without an API key

On Windows, double-click `run_demo.bat`. On other systems, run:

```powershell
python score_ceos.py demo --output-dir outputs/demo --resume
```

Open `outputs/demo/ratings.xlsx`. The ten CEO names are real; the demonstration **scores are synthetic** and no API is called.

## Run a live pilot

1. Copy `.env.example` to `.env`. In `.env`, replace the placeholder for your selected provider with your own API key. Keep this file private.
2. Edit `pilot.toml`: choose `provider`, `dimension`, `iterations`, and, if needed, `input`. The supplied input is `data/ceo_pilot_10.csv`. Each repetition makes one rating request per CEO, so the supplied ten-person input creates `10 × iterations` rating slots.
3. Edit `config.toml` only if you need a different model ID, endpoint, output limit, timeout, retry count, delay, or temperature setting.
4. On Windows, double-click `run_pilot.bat`. Check the displayed provider, trait, total slots, and output folder; then type `YES` to start paid calls.

On other systems, run:

```powershell
python score_ceos.py pilot --check
python score_ceos.py pilot --resume --confirm-live-api
```

The default `output_dir` template in `pilot.toml` changes the folder automatically when you change the provider, trait, or repetition count. If you change the input CSV, model, or other settings without changing those three fields, choose a new `output_dir`. Custom input CSVs require `ceo_id,name,company` columns.

## Inspect the output

The console prints the current CEO, repetition, and progress. The output path is shown before the run starts. After completion, open `ratings.xlsx`: `Ratings` contains every score and `Summary` contains valid and failed counts. `ratings.jsonl` saves each completed slot during the run; `summary.csv` and `run.json` provide a text summary and run settings. Failed or nonconforming responses are coded `999.00` and excluded from the valid-score mean.

## If a run stops

- **Interrupted run:** Keep the same settings and double-click `run_pilot.bat` again. Saved slots are skipped.
- **Missing API key:** Check that `.env` is in this folder and contains the selected provider's key.
- **Different saved settings:** Restore the earlier settings to resume, or select a new output folder.
- **Missing Python package:** Repeat the installation command above.

The package contains no saved API results. `scripts/fetch_ceorater.py` and `scripts/build_ceorater_input.py` support rebuilding a dated CEO input from CEORater; `scripts/describe_ratings.py` summarizes completed live runs. These optional scripts are documented in the technical appendix.
