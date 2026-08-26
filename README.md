# LLM Output Quality Scorer

A rubric-based LLM-as-judge scorer for AI-drafted customer support replies. Takes a customer
message + account/policy context + an AI-drafted reply, and scores the reply 1-5 on four
anchored dimensions (relevance, correctness, completeness, tone), with reasoning per dimension.

Status: core pipeline built and run end-to-end (rubric → draft generation → judge scoring).
Human-calibration step is set up but not yet completed — see "Calibration" below.

See [CLAUDE.md](./CLAUDE.md) for full scope and requirements. Part of a broader portfolio
initiative — see the parent [CLAUDE.md](../CLAUDE.md).

## Setup

Runs entirely against a local [Ollama](https://ollama.com) model — no API key, no billing, no
external service. Requires Ollama running locally with a model pulled:

```
ollama pull llama3.2
pip install -r requirements.txt
```

## Usage

```
python3 -m scorer.cli generate-replies     # draft replies for data/tickets.jsonl -> data/tickets_with_replies.jsonl
python3 -m scorer.cli score                # judge-score the drafts -> report.json + report.md
python3 -m scorer.make_worksheet           # build labeling_worksheet.md for human calibration
python3 -m scorer.cli calibrate            # compare report.json to data/human_labels.jsonl -> calibration_report.md
```

## Sample output

Real run against the 16-ticket set in `data/tickets.jsonl` (see `report.md` for full
per-example reasoning). Summary across all 16:

| dimension | mean | min | max |
|---|---|---|---|
| relevance | 4.12 | 4 | 5 |
| correctness | 4.50 | 2 | 5 |
| completeness | 4.12 | 4 | 5 |
| tone | 4.38 | 3 | 5 |

One representative example (`t04`, a login issue where the account was flagged for a bounced
verification email):

> **correctness: 2** — "The reply states that emails sent to j.torres@example.com have been
> bouncing since a typo was introduced during a profile edit, which is not accurate according to
> the provided context (unverified bounce flag set 2026-07-28)."

That's the judge correctly catching the draft reply over-stating an internal diagnosis as
confirmed fact to the customer — the kind of catch this tool exists to make.

## Tradeoffs

Required per [CLAUDE.md](./CLAUDE.md) — real decisions changed from the default, not left as
whatever the first generation produced:

1. **Local Ollama (`llama3.2`, ~3B) instead of a paid hosted API (GPT-4/Claude), for both
   drafting and judging.** Chosen specifically so the project runs at zero cost and is
   reproducible by anyone who clones the repo without needing an API key or billing — a real
   constraint for a portfolio project meant to be run, not just read. The cost: judge
   discrimination is visibly weaker than a frontier model would likely produce. Across all 16
   examples, **`relevance` never scored below 4 and `completeness` never scored below 4** —
   even for `t10`, a deliberately vague, low-context ticket where a stronger judge might
   reasonably score lower. `correctness` (2-5) and `tone` (3-5) showed real spread and the
   reasoning attached to each score was specific and grounded (see the `t04` example above), so
   the judge isn't just failing outright — but the tight clustering on two of four dimensions is
   a real, disclosed limitation of using a small local model here, not glossed over.
2. **All four dimensions scored in a single model call per example**, not one call per
   dimension (see `scorer/judge.py` docstring). Cheaper and faster at 3B-model speeds (this
   already took several minutes locally for 16 examples × 1 call; per-dimension calls would
   have taken ~4x longer), at the cost of true independence between dimension judgments. Worth
   revisiting if the rubric grows past ~4 dimensions.
3. **Generic Ollama JSON mode + Python-side shape validation with one retry**, instead of
   OpenAI-style strict JSON-schema structured outputs. `llama3.2` at this size doesn't reliably
   honor a strict schema, so `scorer/judge.py` validates dimension names/score ranges itself
   after parsing and raises clearly if the model still can't produce the right shape after a
   retry, rather than silently accepting malformed output.

## Calibration

Not yet run — `calibration_report.md` requires real human labels in `data/human_labels.jsonl`,
which is intentionally a manual step (see `labeling_worksheet.md`, generated from the same 16
examples). The whole point of calibration is checking the judge against a real person's
judgment, not another model's, so this step isn't something to fill in synthetically.
