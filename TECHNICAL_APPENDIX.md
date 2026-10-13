# Technical appendix

## Contents

1. [Scope and implemented stage](#1-scope-and-implemented-stage)
2. [CEO input](#2-ceo-input)
3. [Rating protocol and model settings](#3-rating-protocol-and-model-settings)
4. [Records and reproducibility](#4-records-and-reproducibility)
5. [Prototype checks and evidential scope](#5-prototype-checks-and-evidential-scope)
6. [References](#6-references)

## 1. Scope and implemented stage

The artifact makes repeated, single-turn API requests for a named CEO, company, and one Big Five trait. A rating slot is one LLM × CEO ID × trait × repetition. Each slot sends the same template as a fresh request, without conversation history or earlier scores. The output is a model-generated rating under this protocol; it is not an observed measure of the CEO's personality or of public opinion.

One run handles one LLM and one trait. The supplied pilot input has ten CEOs. The proposed six-LLM, five-trait design with 500 repetitions per CEO would require separate runs for each LLM–trait pair. With the dated 513-record roster described below, that design implies 7,695,000 rating slots before any retries. The repository demonstrates the collection and export workflow on a small pilot; it does not report results for the full design.

## 2. CEO input

The input is a UTF-8 CSV with `ceo_id`, `name`, and `company`. The program rejects empty inputs, missing fields, and duplicate IDs. `name` and `company` enter the prompt; `ceo_id` links records across repetitions. The local study roster was derived from a download of the CEORater API, which returned 513 CEO records (CEORater 2026). `scripts/fetch_ceorater.py` retrieves a fresh snapshot; `scripts/build_ceorater_input.py` forms an ID from ticker and CEO name. The dated full roster is not redistributed in this package; the public `data/ceo_pilot_10.csv` supports inspection and independent test calls.

## 3. Rating protocol and model settings

The exact prompt template in `score_ceos.py` is:

```text
Please rate the {{dimension}} personality trait of {{ceo_name}}, CEO of {{company}}.

Rating range: 1 to 7 (1 is the lowest; 7 is the highest).

Requirements:
1. Output exactly one numeric score with two decimal places.
2. Do not output any explanation, analysis, or additional text.
3. The score must be between 1 and 7, inclusive.

Score:
```

`{{dimension}}` is one of `openness`, `conscientiousness`, `extraversion`, `agreeableness`, or `neuroticism`. All LLMs receive this English template and the same trait names. The program accepts only a response consisting of `1.00`–`6.99` or `7.00`, apart from surrounding whitespace. An explanation, refusal, other format, or out-of-range number is recorded as `invalid_response` with the sentinel score `999.00`; it is not retried. An API exception permits up to three attempts for the same slot. If all attempts fail, the slot is recorded as `api_error` with `999.00`. Neither failure type creates a replacement slot, and the run continues. `999.00` is excluded from valid-score means.

| LLM | Requested model ID | API client |
| --- | --- | --- |
| DeepSeek | `deepseek-flash` | OpenAI-compatible |
| Qwen | `qwen3.8-flash` | OpenAI-compatible |
| Doubao | `doubao-seed-2-1-turbo-260628` | OpenAI-compatible |
| Claude | `claude-haiku-5-5` | Anthropic |
| GPT | `gpt-6-luna` | OpenAI |
| Gemini | `gemini-3.8-flash` | Google Gen AI |

These are the configured IDs. Provider documentation for each ID appears in the References. The configured output cap is 1,024 tokens; the timeout is 30 seconds per request; and the delay between slots is one second. DeepSeek, Qwen, Doubao, and GPT use the `openai` Python client; Claude and Gemini use their providers' Python packages, listed in `requirements-optional.txt`.

## 4. Records and reproducibility

`pilot.toml` selects the provider, trait, repetitions, input, and output folder. `config.toml` holds model IDs, endpoints, and request settings. A local `.env` or system environment supplies the API key; the key is not written to output records. `README.md` gives the installation and run steps.

Each completed slot is immediately appended to `ratings.jsonl`, with CEO ID, requested and returned model IDs when available, repetition, score, status, error type, and number of API attempts. `run.json` records the input and prompt SHA-256 hashes plus the requested protocol settings. No random seed is specified, and a provider may change the service version behind a model ID; exact replay of a rating is therefore not guaranteed. `ratings.xlsx` arranges every repetition by CEO and adds valid-score means; `summary.csv` records valid and failed counts. The Excel and CSV summaries are written when the run finishes. Full API response text and per-call timestamps are not retained. Resuming a run skips saved slots only when the saved manifest matches the current input and settings; a changed run uses a new output folder.

`scripts/describe_ratings.py` produces per-CEO counts, failure rates, and descriptive statistics from live runs sharing the same input hash. It rejects synthetic demonstration data. The statistics describe the collected responses; they do not establish that the ratings measure personality or public stereotypes.

## 5. Prototype checks and evidential scope

Automated tests exercise the strict score parser, refusal and API-error handling, retries, resuming, output construction, and pilot path resolution. The repository includes the code and ten-CEO input needed to repeat the workflow, but no saved API results. The tests verify recording and export behavior. Cross-provider differences and construct validity have not been evaluated in this package.

## 6. References

- Alibaba Cloud. 2026. [*Qwen3.8 Flash model information*](https://help.aliyun.com/en/model-studio/qwen3-8-flash). Accessed 13 October 2026.
- Anthropic. 2026. [*Claude Haiku 5.5*](https://platform.claude.com/docs/en/models/haiku-5-5/overview). Accessed 13 October 2026.
- CEORater. 2026. [*The CEORater API*](https://www.ceorater.com/api-docs.html). Accessed 13 October 2026.
- DeepSeek. 2026a. [*DeepSeek-V4.1-Flash release*](https://api-docs.deepseek.com/updates/). Accessed 13 October 2026.
- DeepSeek. 2026b. [*Thinking mode*](https://api-docs.deepseek.com/guides/thinking_mode/). Accessed 13 October 2026.
- Google. 2026. [*Gemini 3.8 Flash*](https://ai.google.dev/gemini-api/docs/models/gemini-3.8-flash). Accessed 13 October 2026.
- OpenAI. 2026. [*GPT-6 Luna*](https://developers.openai.com/api/docs/models/gpt-6-luna). Accessed 13 October 2026.
- Volcengine. 2026. [*Ark model list*](https://docs.volcengine.com/docs/ark/model-list?lang=en). Accessed 13 October 2026.
