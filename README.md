# LLM Output Quality Scorer

## For recruiters / hiring managers

**The problem:** every team shipping an AI feature eventually has to answer "is this output
actually good enough to ship?" Most teams answer that by eyeballing a handful of examples, which
doesn't scale and isn't consistent from person to person. This project is a working tool that
turns that judgment call into a measurable, repeatable score.

**What I built:** an AI "judge" that scores draft customer-support replies against a rubric I
wrote myself — four specific dimensions (does it answer the right question, is it factually
accurate, does it cover everything the customer asked, is the tone right), each with a written
description of what a weak answer looks like versus a strong one. I ran it against 16 realistic
support tickets I wrote to cover a real range of difficulty, then checked the judge's scores
against independent judgment to find out where it could be trusted and where it couldn't.

**Why this is a PM signal, not just an engineering exercise:** the easy version of this project
is to call an API, get some scores back, and call it done. I didn't stop there — I found a real
blind spot in my own tool (it was too generous on two of the four dimensions, confirmed by
testing, not assumed) and wrote that up instead of hiding it. I also drew a hard line between a
quick self-check I ran myself and genuine human calibration, which the project is explicit about
still needing rather than quietly pretending to have. That distinction — knowing when a result
is trustworthy versus when it just looks trustworthy — is the actual skill this project is meant
to demonstrate.

**Try it in under 5 minutes:** see [Setup](#setup) below — it runs entirely on a free local
model, no API key or billing required.

---

A rubric-based LLM-as-judge scorer for AI-drafted customer support replies. Takes a customer
message + account/policy context + an AI-drafted reply, and scores the reply 1-5 on four
anchored dimensions (relevance, correctness, completeness, tone), with reasoning per dimension.

Status: core pipeline built and run end-to-end (rubric → draft generation → judge scoring).
Human-calibration step is set up but not yet completed — see "Calibration" below.

See [CLAUDE.md](./CLAUDE.md) for full scope and requirements. Part of a broader portfolio
initiative — see the parent [CLAUDE.md](../CLAUDE.md).

**What this demonstrates:** the rubric is written and anchored *before* any scoring happens; the
judge's output was checked critically rather than trusted on the first run, which surfaced a
real weakness (see Tradeoffs below); and the calibration step is honest about its own limits —
a self-check against a second model is clearly labeled as *not* a substitute for real human
calibration, rather than being dressed up as one.

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

## Test data

16 hand-written support tickets in [data/tickets.jsonl](data/tickets.jsonl), each with a
customer message and the account/policy context a real agent would have — chosen to span a
real difficulty range, not just easy cases: straightforward requests (refunds, policy
questions), an angry multi-email escalation, a deliberately vague message with no diagnosable
issue, a customer stacking three complaints in one message, and cases with a subtle trap in the
context (e.g. a promo code that looks expired but was actually shown as valid due to a confirmed
bug, which the reply is supposed to catch).

Four examples, with the real draft reply generated for each and how the judge scored it:

**`t01`** — *"Hi, I was charged $49.99 twice this month for my Pro plan. Can you refund the
duplicate charge?"* (context: confirmed billing-retry bug, policy = auto-refund in 5-7 days)
→ scores: relevance=4, correctness=5, completeness=4, **tone=3** — judge noted the reply "reads
as templated/impersonal" and never acknowledges the customer's frustration, even though nothing
it says is wrong.

**`t07`** — *"This is the third email I've sent about my billing issue and NO ONE has responded.
I'm about to cancel..."* (context: a confirmed $75 pricing error, 2 prior unanswered emails)
→ scores: relevance=5, correctness=4, **completeness=5**, tone=4 — the highest-completeness
score in the set; judge credited the reply for addressing both the refund and the customer's
stated intent to cancel "with roughly proportionate attention."

**`t10`** — *"hey so i think i need help with something but not sure who to ask, my account is
kind of messed up"* (context: nothing wrong on the account — no diagnosable issue at all)
→ scores: relevance=4, correctness=5, completeness=4, tone=5 — the "right" response here is to
ask for more detail rather than guess, which the draft did; included specifically to test
whether the judge would penalize a reply for *not* inventing an answer to an unanswerable ticket
(it didn't).

**`t15`** — *"I was double billed AND my export feature is broken AND nobody has responded to my
last email in 4 days."* (context: billing charge was NOT actually duplicated, export outage is a
known incident, the 4-day-old email is real) → scores: relevance=4, correctness=**5**,
completeness=4, tone=5 — this is the example flagged in Calibration below: the judge gave this a
perfect correctness score despite the reply hedging on a fact ("we cannot confirm whether the
charge is indeed a duplicate") that the context had already confirmed. A real judge miss, caught
by re-checking the output instead of trusting the score.

Full set of 16, generated replies, and full per-example reasoning: `data/tickets.jsonl`,
`data/tickets_with_replies.jsonl`, `report.md`.

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

**Real human calibration is not done yet.** `data/human_labels.jsonl` (the file the CLAUDE.md
definition-of-done actually asks for) is still empty — see `labeling_worksheet.md` to fill it in.
The point of calibration is checking the judge against a real person's judgment, not another
model's, so this step can't be satisfied synthetically, and the corresponding checkbox in
[CLAUDE.md](./CLAUDE.md) stays unchecked until it's done.

**What *is* in this repo (`claude_self_check_report.md`, `data/claude_labels.jsonl`) is a
different, weaker thing: Claude independently re-read all 16 (ticket, context, draft reply)
triples — without looking at the judge's scores first — and produced its own scores. That's an
LLM-vs-LLM consistency check, not calibration against human judgment, and it's kept in
separately-named files specifically so it never gets mistaken for the real thing.**

Results of that self-check:

| dimension | exact match | within ±1 | MAE | Pearson r |
|---|---|---|---|---|
| relevance | 0.31 | 1.00 | 0.69 | 0.23 |
| correctness | 0.50 | 0.94 | 0.56 | 0.62 |
| completeness | 0.38 | 1.00 | 0.62 | 0.18 |
| tone | 0.31 | 0.94 | 0.75 | 0.29 |

Every score was within 1 point on relevance and completeness (weak correlation, but no wild
misses), while correctness had the strongest correlation (r=0.62) — consistent with correctness
being the most fact-checkable dimension against the provided context. The one real disagreement
(2+ points) was **`t15`**, a reply juggling three complaints at once: Claude's independent read
caught that the reply hedges on the billing question ("we cannot confirm whether the charge is
indeed a duplicate") when the context already **confirms no duplicate was found** — the judge
scored that reply correctness=5 and missed the hedge; Claude scored it 3. That's exactly the
kind of miss real human calibration exists to catch, and it's a plausible preview of what a real
human labeler might also flag — but it isn't a substitute for one.
