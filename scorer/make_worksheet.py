"""Build a human-labeling worksheet from the generated draft replies.

The calibration step needs a real person's judgment, not another model's — that's the whole
point of calibrating. This script just lays out each (ticket, context, draft reply) for a human
to score by hand; it does not call any model.
"""
import argparse
import json


def build_worksheet(input_path: str, rubric_path: str, output_path: str):
    from scorer.rubric import load_rubric

    rubric = load_rubric(rubric_path)
    dim_names = rubric.dimension_names()

    rows = []
    with open(input_path) as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))

    lines = ["# Human Labeling Worksheet\n"]
    lines.append(
        "For each example, read the customer message, the context, and the draft reply, then "
        "score each dimension 1-5 using the anchors in `rubric.yaml`. Put your scores into "
        "`data/human_labels.jsonl` — one line per example, format:\n"
    )
    lines.append("```")
    lines.append(
        json.dumps({"id": rows[0]["id"], "scores": {d: 3 for d in dim_names}})
    )
    lines.append("```\n")
    lines.append(f"Dimensions to score: {', '.join(dim_names)} (each 1-5)\n")
    lines.append("---\n")

    for row in rows:
        lines.append(f"## {row['id']}\n")
        lines.append(f"**Customer message:**\n> {row['customer_message']}\n")
        lines.append(f"**Context:**\n> {row['context']}\n")
        lines.append(f"**Draft reply:**\n> {row['draft_reply']}\n")
        lines.append("Your scores: " + ", ".join(f"{d}=__" for d in dim_names) + "\n")
        lines.append("---\n")

    with open(output_path, "w") as f:
        f.write("\n".join(lines))

    print(f"Wrote worksheet for {len(rows)} examples to {output_path}")
    print("Fill in your scores, then save them to data/human_labels.jsonl (see format above).")


def main():
    parser = argparse.ArgumentParser(description="Build the human-labeling worksheet")
    parser.add_argument("--input", default="data/tickets_with_replies.jsonl")
    parser.add_argument("--rubric", default="rubric.yaml")
    parser.add_argument("--output", default="labeling_worksheet.md")
    args = parser.parse_args()
    build_worksheet(args.input, args.rubric, args.output)


if __name__ == "__main__":
    main()
