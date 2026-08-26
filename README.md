# LLM Output Quality Scorer

A scorer that uses an LLM as judge to score AI generated customer support replies. Takes a
customer message, the account and policy context, and a draft reply, then scores the reply on a
scale of 1 to 5 across four anchored dimensions (relevance, correctness, completeness, tone),
with reasoning attached to every score.

Status: core pipeline built and run end to end (rubric, then draft generation, then judge
scoring). The human calibration step is set up but not yet completed; see "Calibration" below.

See [CLAUDE.md](./CLAUDE.md) for full scope and requirements. Part of a broader portfolio
initiative; see the parent [CLAUDE.md](../CLAUDE.md).

## Overview

This project turns "is this AI output good enough to ship" from a vibe check into a measurement:
a rubric based scorer with human calibration, for AI drafted customer support replies.

**The problem it solves.** Every team shipping an AI feature eventually asks "is the output good
enough?" and usually answers it by eyeballing a few examples. That doesn't scale, isn't
consistent across people, and isn't defensible in a launch review. This is the artifact a PM
would actually hand to engineering and design to make that measurable.

**How it works, step by step.**

1. We wrote the rubric first, before any code: 4 dimensions (relevance, correctness,
   completeness, tone), each scored 1 to 5, and for each score we wrote out what a 2 looks like
   versus a 4. That anchoring matters: without it, an LLM judge gives inconsistent scores for the
   same quality of output.
2. We built a test dataset: 16 realistic customer support tickets, written by hand, spanning easy
   cases, ambiguous ones, angry customers, and multi part complaints, deliberately varied so
   there would be real quality variance to measure.
3. We generated draft replies using a deliberately lightweight, minimally prompted AI agent,
   standing in for a "first version" draft reply feature a team might actually be evaluating
   before shipping.
4. We built the judge: an LLM scores each draft against the rubric, one call per example,
   returning a score plus a written reason for each dimension.
5. We ran it for real and looked at the results critically instead of just accepting them. That's
   where we found something interesting: two of the four dimensions, relevance and completeness,
   never scored below a 4 across all 16 examples, even on a ticket that was intentionally vague.
   That's a real weakness in the judge, and we wrote it up rather than hiding it.
6. We built calibration tooling, because a rubric score means nothing until it is checked against
   real human judgment. It computes agreement rate, mean error, and correlation, and specifically
   surfaces any case where the model and the human disagreed by 2 or more points.
7. We ran a stand in check ourselves and caught a real miss: on one ticket, the judge gave a
   reply a perfect correctness score, but the reply had actually hedged on a fact ("we cannot
   confirm if this was a duplicate charge") that the source data had already confirmed. We
   caught that; the judge didn't.

**The judgment calls worth knowing about.**

We originally planned to use OpenAI's API. We hit a real billing wall mid build: no credits.
Rather than fake it, we rearchitected the whole thing to run on a free local model (Ollama),
which turned out to be a better story: it proves the tool is reproducible by anyone without a
paid key, at the honest cost of weaker judge quality, which we then measured and disclosed.

We explicitly did not let our own labels count as "real calibration." We kept them in a
separate, clearly named file, because one LLM checking another isn't the same as checking
against genuine human judgment, and we say that plainly rather than implying otherwise.

## Setup

Runs entirely against a local [Ollama](https://ollama.com) model. No API key, no billing, no
external service. Requires Ollama running locally with a model pulled:

```
ollama pull llama3.2
pip install -r requirements.txt
```

## Usage

```
python3 -m scorer.cli generate-replies     # draft replies for data/tickets.jsonl -> data/tickets_with_replies.jsonl
python3 -m scorer.cli score                # judge score the drafts -> report.json + report.md
python3 -m scorer.make_worksheet           # build labeling_worksheet.md for human calibration
python3 -m scorer.cli calibrate            # compare report.json to data/human_labels.jsonl -> calibration_report.md
```

## Test data

16 hand written support tickets in [data/tickets.jsonl](data/tickets.jsonl), each with a
customer message and the account and policy context a real agent would have. Chosen to span a
real difficulty range, not just easy cases: straightforward requests (refunds, policy
questions), an angry escalation after several unanswered emails, a deliberately vague message
with no diagnosable issue, a customer stacking three complaints in one message, and cases with a
subtle trap in the context (for example, a promo code that looks expired but was actually shown
as valid due to a confirmed bug, which the reply is supposed to catch).

Four examples, with the real draft reply generated for each and how the judge scored it:

**`t01`**: *"Hi, I was charged $49.99 twice this month for my Pro plan. Can you refund the
duplicate charge?"* (context: confirmed billing retry bug, policy is an automatic refund within
5 to 7 days)
→ scores: relevance=4, correctness=5, completeness=4, **tone=3**. The judge noted the reply
"reads as templated / impersonal" and never acknowledges the customer's frustration, even though
nothing it says is wrong.

**`t07`**: *"This is the third email I've sent about my billing issue and NO ONE has responded.
I'm about to cancel..."* (context: a confirmed $75 pricing error, plus 2 prior unanswered
emails)
→ scores: relevance=5, correctness=4, **completeness=5**, tone=4. The highest completeness
score in the set; the judge credited the reply for addressing both the refund and the customer's
stated intent to cancel "with roughly proportionate attention."

**`t10`**: *"hey so i think i need help with something but not sure who to ask, my account is
kind of messed up"* (context: nothing wrong on the account at all, no diagnosable issue)
→ scores: relevance=4, correctness=5, completeness=4, tone=5. The right response here is to ask
for more detail rather than guess, which the draft did. Included specifically to test whether
the judge would penalize a reply for not inventing an answer to an unanswerable ticket. It
didn't.

**`t15`**: *"I was double billed AND my export feature is broken AND nobody has responded to my
last email in 4 days."* (context: the billing charge was not actually duplicated, the export
outage is a known incident, and the 4 day old unanswered email is real)
→ scores: relevance=4, correctness=**5**, completeness=4, tone=5. This is the example flagged
in Calibration below: the judge gave this a perfect correctness score despite the reply hedging
on a fact ("we cannot confirm whether the charge is indeed a duplicate") that the context had
already confirmed. A real judge miss, caught by checking the output again instead of trusting
the score.

Full set of 16, generated replies, and full per example reasoning: `data/tickets.jsonl`,
`data/tickets_with_replies.jsonl`, `report.md`.

## Sample output

Real run against the 16 ticket set in `data/tickets.jsonl` (see `report.md` for full per
example reasoning). Summary across all 16:

| dimension | mean | min | max |
|---|---|---|---|
| relevance | 4.12 | 4 | 5 |
| correctness | 4.50 | 2 | 5 |
| completeness | 4.12 | 4 | 5 |
| tone | 4.38 | 3 | 5 |

One representative example (`t04`, a login issue where the account was flagged for a bounced
verification email):

> **correctness: 2**: "The reply states that emails sent to j.torres@example.com have been
> bouncing since a typo was introduced during a profile edit, which is not accurate according to
> the provided context (unverified bounce flag set 2026-07-28)."

That's the judge correctly catching the draft reply overstating an internal diagnosis as
confirmed fact to the customer, the kind of catch this tool exists to make.

## Tradeoffs

Required per [CLAUDE.md](./CLAUDE.md): real decisions changed from the default, not left as
whatever the first generation produced.

1. **Local Ollama (`llama3.2`, about 3B parameters) instead of a paid hosted API (OpenAI or
   Anthropic), for both drafting and judging.** Chosen specifically so the project runs at zero
   cost and is reproducible by anyone who clones the repo without needing an API key or billing.
   A real constraint for a portfolio project meant to be run, not just read. The cost: judge
   discrimination is visibly weaker than a frontier model would likely produce. Across all 16
   examples, **`relevance` never scored below 4 and `completeness` never scored below 4**, even
   for `t10`, a deliberately vague ticket with almost no context, where a stronger judge might
   reasonably score lower. `correctness` (2 to 5) and `tone` (3 to 5) showed real spread, and the
   reasoning attached to each score was specific and grounded (see the `t04` example above), so
   the judge isn't just failing outright. But the tight clustering on two of four dimensions is a
   real, disclosed limitation of using a small local model here, not glossed over.
2. **All four dimensions scored in a single model call per example**, not one call per
   dimension (see `scorer/judge.py` docstring). Cheaper and faster at 3B model speeds (this
   already took several minutes locally for 16 examples times one call each; per dimension calls
   would have taken about four times as long), at the cost of true independence between
   dimension judgments. Worth revisiting if the rubric grows past about four dimensions.
3. **Generic Ollama JSON mode plus Python side shape validation with one retry**, instead of
   OpenAI style strict JSON schema structured outputs. `llama3.2` at this size doesn't reliably
   honor a strict schema, so `scorer/judge.py` validates dimension names and score ranges itself
   after parsing, and raises clearly if the model still can't produce the right shape after a
   retry, rather than silently accepting malformed output.

## Calibration

**Real human calibration is not done yet.** `data/human_labels.jsonl` (the file the CLAUDE.md
definition of done actually asks for) is still empty; see `labeling_worksheet.md` to fill it in.
The point of calibration is checking the judge against a real person's judgment, not another
model's, so this step can't be satisfied synthetically, and the corresponding checkbox in
[CLAUDE.md](./CLAUDE.md) stays unchecked until it's done.

**What *is* in this repo (`claude_self_check_report.md`, `data/claude_labels.jsonl`) is a
different, weaker thing: Claude independently reread all 16 (ticket, context, draft reply)
triples, without looking at the judge's scores first, and produced its own scores. That's one
LLM checking another, not calibration against human judgment, and it's kept in separately named
files specifically so it never gets mistaken for the real thing.**

Results of that check:

| dimension | exact match | within ±1 | MAE | Pearson r |
|---|---|---|---|---|
| relevance | 0.31 | 1.00 | 0.69 | 0.23 |
| correctness | 0.50 | 0.94 | 0.56 | 0.62 |
| completeness | 0.38 | 1.00 | 0.62 | 0.18 |
| tone | 0.31 | 0.94 | 0.75 | 0.29 |

Every score was within 1 point on relevance and completeness (weak correlation, but no wild
misses), while correctness had the strongest correlation (r=0.62), consistent with correctness
being the most fact checkable dimension against the provided context. The one real disagreement
(2 or more points) was **`t15`**, a reply juggling three complaints at once: the independent
check caught that the reply hedges on the billing question ("we cannot confirm whether the
charge is indeed a duplicate") when the context already **confirms no duplicate was found**. The
judge scored that reply correctness=5 and missed the hedge; the independent check scored it 3.
That's exactly the kind of miss real human calibration exists to catch, and it's a plausible
preview of what a real human labeler might also flag, but it isn't a substitute for one.
