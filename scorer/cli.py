import argparse

from scorer import generate_replies, run_score
from scorer.calibrate import calibrate
from scorer.rubric import load_rubric


def main():
    parser = argparse.ArgumentParser(prog="scorer", description="LLM output quality scorer")
    sub = parser.add_subparsers(dest="command", required=True)

    p_gen = sub.add_parser("generate-replies", help="Generate draft replies for the ticket set")
    p_gen.add_argument("--input", default="data/tickets.jsonl")
    p_gen.add_argument("--output", default="data/tickets_with_replies.jsonl")

    p_score = sub.add_parser("score", help="Score draft replies against the rubric")
    p_score.add_argument("--input", default="data/tickets_with_replies.jsonl")
    p_score.add_argument("--rubric", default="rubric.yaml")
    p_score.add_argument("--output", default="report.json")

    p_cal = sub.add_parser("calibrate", help="Compare scorer output to human labels")
    p_cal.add_argument("--report", default="report.json")
    p_cal.add_argument("--human-labels", default="data/human_labels.jsonl")
    p_cal.add_argument("--rubric", default="rubric.yaml")
    p_cal.add_argument("--output", default="calibration_report.md")

    args = parser.parse_args()

    if args.command == "generate-replies":
        generate_replies.run(args.input, args.output)
    elif args.command == "score":
        run_score.run(args.input, args.rubric, args.output)
    elif args.command == "calibrate":
        rubric = load_rubric(args.rubric)
        result = calibrate(args.report, args.human_labels, rubric.dimension_names())
        print(result)


if __name__ == "__main__":
    main()
