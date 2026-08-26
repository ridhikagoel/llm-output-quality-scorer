"""LLM-as-judge scoring against an anchored rubric.

Design decision (documented in README Tradeoffs): all dimensions for a given example are
scored in a SINGLE model call rather than one call per dimension. Cheaper and faster, at the
cost of true independence between dimension scores (the model sees all dimensions at once and
could let one judgment bleed into another). For a 4-dimension, 16-example eval this tradeoff
is worth it; it would need revisiting for a rubric with many more dimensions or where
independence matters more than cost.

Uses Ollama's generic JSON mode (not a strict schema, which Ollama's small local models handle
unreliably) plus explicit shape validation in Python with one retry on malformed output.
"""
from scorer.llm import chat_json
from scorer.rubric import Rubric


def _build_prompt(rubric: Rubric, customer_message: str, context: str, draft_reply: str) -> str:
    dim_blocks = []
    for d in rubric.dimensions:
        anchor_lines = "\n".join(f"    {level}: {text}" for level, text in sorted(d.anchors.items()))
        dim_blocks.append(f"- {d.name}: {d.description.strip()}\n{anchor_lines}")
    dims_text = "\n".join(dim_blocks)
    names = rubric.dimension_names()

    example_shape = {
        "scores": [{"dimension": n, "score": 3, "reasoning": "one to two sentence reason"} for n in names]
    }

    return f"""Task: {rubric.task.strip()}

Score the DRAFT REPLY below on each of these dimensions, using the 1-5 anchor descriptions as
your scoring guide. Give an integer score AND a one-to-two sentence reasoning per dimension that
cites specifics from the reply or context, not a generic justification.

{dims_text}

--- Customer message ---
{customer_message}

--- Account/policy context (ground truth) ---
{context}

--- Draft reply to score ---
{draft_reply}

Respond with ONLY valid JSON in exactly this shape (one entry per dimension, dimension names
must be exactly: {", ".join(names)}):
{example_shape}
"""


def score_example(rubric: Rubric, customer_message: str, context: str, draft_reply: str) -> dict:
    prompt = _build_prompt(rubric, customer_message, context, draft_reply)
    parsed = chat_json(rubric.judge_model, prompt, temperature=0)

    scores = {}
    for item in parsed.get("scores", []):
        dim = item.get("dimension")
        if dim not in rubric.dimension_names():
            continue
        try:
            score = int(item["score"])
        except (KeyError, TypeError, ValueError):
            continue
        score = max(1, min(5, score))
        scores[dim] = {"score": score, "reasoning": item.get("reasoning", "")}

    missing = set(rubric.dimension_names()) - set(scores)
    if missing:
        raise ValueError(f"Judge response missing dimensions: {missing}. Raw: {parsed}")

    return scores
