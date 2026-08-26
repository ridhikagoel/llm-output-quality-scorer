import argparse
import json

from scorer.judge import score_example
from scorer.rubric import load_rubric


def run(input_path: str, rubric_path: str, output_path: str) -> list[dict]:
    rubric = load_rubric(rubric_path)

    rows = []
    with open(input_path) as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))

    results = []
    for row in rows:
        scores = score_example(rubric, row["customer_message"], row["context"], row["draft_reply"])
        result = {"id": row["id"], "draft_reply": row["draft_reply"], "scores": scores}
        results.append(result)
        summary = ", ".join(f"{k}={v['score']}" for k, v in scores.items())
        print(f"[{row['id']}] {summary}")

    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)

    _write_markdown_report(results, rubric, output_path.replace(".json", ".md"))
    print(f"\nWrote {len(results)} scored examples to {output_path}")
    return results


def _write_markdown_report(results: list[dict], rubric, md_path: str):
    dim_names = rubric.dimension_names()
    lines = ["# Quality Scoring Report\n"]
    lines.append("| id | " + " | ".join(dim_names) + " |")
    lines.append("|---|" + "---|" * len(dim_names))
    for r in results:
        row_scores = [str(r["scores"][d]["score"]) for d in dim_names]
        lines.append(f"| {r['id']} | " + " | ".join(row_scores) + " |")

    lines.append("\n## Per-example reasoning\n")
    for r in results:
        lines.append(f"### {r['id']}")
        lines.append(f"> {r['draft_reply'][:300]}{'...' if len(r['draft_reply']) > 300 else ''}\n")
        for d in dim_names:
            s = r["scores"][d]
            lines.append(f"- **{d}** ({s['score']}/5): {s['reasoning']}")
        lines.append("")

    with open(md_path, "w") as f:
        f.write("\n".join(lines))


def main():
    parser = argparse.ArgumentParser(description="Run the LLM-judge quality scorer")
    parser.add_argument("--input", default="data/tickets_with_replies.jsonl")
    parser.add_argument("--rubric", default="rubric.yaml")
    parser.add_argument("--output", default="report.json")
    args = parser.parse_args()
    run(args.input, args.rubric, args.output)


if __name__ == "__main__":
    main()
