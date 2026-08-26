import argparse
import json
import statistics


def _pearson(xs: list[float], ys: list[float]) -> float | None:
    n = len(xs)
    if n < 2 or len(set(xs)) == 1 or len(set(ys)) == 1:
        return None
    mx, my = statistics.fmean(xs), statistics.fmean(ys)
    cov = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    sx = (sum((x - mx) ** 2 for x in xs)) ** 0.5
    sy = (sum((y - my) ** 2 for y in ys)) ** 0.5
    if sx == 0 or sy == 0:
        return None
    return cov / (sx * sy)


def calibrate(report_path: str, human_labels_path: str, dim_names: list[str]) -> dict:
    with open(report_path) as f:
        scored = {r["id"]: r["scores"] for r in json.load(f)}

    human = {}
    with open(human_labels_path) as f:
        for line in f:
            line = line.strip()
            if line:
                row = json.loads(line)
                human[row["id"]] = row["scores"]

    common_ids = sorted(set(scored) & set(human))
    if not common_ids:
        raise SystemExit("No overlapping ids between scored report and human labels.")

    per_dim = {}
    disagreements = []
    for dim in dim_names:
        model_vals, human_vals = [], []
        for eid in common_ids:
            if dim not in human.get(eid, {}):
                continue
            mv = scored[eid][dim]["score"]
            hv = human[eid][dim]
            model_vals.append(mv)
            human_vals.append(hv)
            if abs(mv - hv) >= 2:
                disagreements.append(
                    {
                        "id": eid,
                        "dimension": dim,
                        "model_score": mv,
                        "human_score": hv,
                        "model_reasoning": scored[eid][dim]["reasoning"],
                    }
                )
        if not model_vals:
            continue
        exact = sum(1 for m, h in zip(model_vals, human_vals) if m == h) / len(model_vals)
        within_1 = sum(1 for m, h in zip(model_vals, human_vals) if abs(m - h) <= 1) / len(model_vals)
        mae = statistics.fmean(abs(m - h) for m, h in zip(model_vals, human_vals))
        per_dim[dim] = {
            "n": len(model_vals),
            "exact_match_rate": round(exact, 2),
            "within_1_rate": round(within_1, 2),
            "mae": round(mae, 2),
            "pearson_r": round(r, 2) if (r := _pearson(model_vals, human_vals)) is not None else None,
        }

    return {"n_examples": len(common_ids), "per_dimension": per_dim, "disagreements": disagreements}


def write_report(result: dict, output_path: str, title: str = "Calibration Report"):
    lines = [f"# {title}\n", f"Compared against {result['n_examples']} labeled examples.\n"]
    lines.append("| dimension | n | exact match | within ±1 | MAE | Pearson r |")
    lines.append("|---|---|---|---|---|---|")
    for dim, stats in result["per_dimension"].items():
        r_str = f"{stats['pearson_r']}" if stats["pearson_r"] is not None else "n/a (no variance)"
        lines.append(
            f"| {dim} | {stats['n']} | {stats['exact_match_rate']} | {stats['within_1_rate']} | {stats['mae']} | {r_str} |"
        )

    lines.append("\n## Disagreements of 2+ points (model vs. label)\n")
    if result["disagreements"]:
        for d in result["disagreements"]:
            lines.append(
                f"- **{d['id']} / {d['dimension']}**: model={d['model_score']}, label={d['human_score']}\n"
                f"  - model reasoning: {d['model_reasoning']}"
            )
    else:
        lines.append("None — largest disagreement was within 1 point on every scored dimension.")

    with open(output_path, "w") as f:
        f.write("\n".join(lines))

    print(f"Wrote report to {output_path}")
    print(json.dumps(result["per_dimension"], indent=2))


def main():
    parser = argparse.ArgumentParser(description="Calibrate scorer output against human labels")
    parser.add_argument("--report", default="report.json")
    parser.add_argument("--human-labels", default="data/human_labels.jsonl")
    parser.add_argument("--rubric", default="rubric.yaml")
    parser.add_argument("--output", default="calibration_report.md")
    args = parser.parse_args()

    from scorer.rubric import load_rubric

    rubric = load_rubric(args.rubric)
    result = calibrate(args.report, args.human_labels, rubric.dimension_names())
    write_report(result, args.output)


if __name__ == "__main__":
    main()
