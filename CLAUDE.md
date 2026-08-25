# LLM Output Quality Scorer

**Category:** Evaluation & Testing · **Source #22** · **Skill it proves:** Quality standards

## Why this matters for senior/principal AI PM
"Quality" for an AI feature is meaningless until it's a rubric someone can apply consistently.
This project proves you can turn a fuzzy quality bar into a reusable, documented scoring system
— the artifact a senior AI PM hands to eng/design so "is this good enough to ship" stops being
a debate and becomes a measurement.

## What to build (MVP scope)
A standalone scorer (library + CLI) that takes an LLM output (and its input context) and
returns a multi-dimensional quality score against a documented rubric — reusable across
different projects/tasks, not hardcoded to one use case.

- Rubric definition file (YAML/JSON): dimensions (e.g. relevance, correctness, completeness,
  tone/format compliance), each with a 1-5 scale and explicit anchor descriptions per level
  (what a 2 looks like vs. a 4 — vague rubrics produce inconsistent scores).
- Scorer: LLM-as-judge implementation that scores each dimension independently with reasoning,
  not one blended number.
- Calibration check: run the scorer against a small hand-labeled set (you label 15-20 examples
  yourself) and report agreement (e.g. correlation or exact-match rate) between the scorer and
  your human labels — this is the part that proves the tool is trustworthy, not just plausible.
- CLI: `score --input output.json --rubric rubric.yaml` → scored report.

## Suggested stack
Python, LLM API for judging, a small hand-labeled calibration set checked into the repo.

## Core requirements
- Rubric has explicit per-level anchors, not just dimension names.
- Calibration against human labels is real and reported honestly, including where the scorer
  disagreed with you and why (this is more credible than claiming perfect agreement).
- Scorer output includes reasoning per dimension, not just numbers — usable for debugging.

## Tradeoffs (required — do not skip)
Change at least one of these from whatever an AI would default to, and document why in a
`## Tradeoffs` section in the README:
- Whether dimensions are weighted equally or not in any composite score, and why.
- A specific rubric anchor you rewrote after seeing it produce a wrong verdict, and what you
  changed.
- What you did when the scorer disagreed with your human label — did you fix the rubric, the
  prompt, or accept the disagreement, and why.

## Definition of done
- [ ] Rubric file + scorer run end-to-end on real LLM outputs
- [ ] README reports calibration results against your hand-labeled set, including disagreements
- [ ] Documents how the rubric would change for a different task/domain
- [ ] README has a `## Tradeoffs` section documenting a real decision you changed and why
- [ ] `.env.example`; no secrets committed

## Portfolio pitch
"Built a quality scorer with an anchored rubric and reported human-calibration results,
including where it disagreed with me — turning 'is this good enough' into a measurement."
