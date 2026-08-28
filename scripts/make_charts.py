"""Regenerate the README charts from report.json + claude_self_check_report.md, without
re-running the judge (which needs a local Ollama model).

    python3 scripts/make_charts.py

Writes:
  outputs/score_spread.png    — where the judge discriminates and where it doesn't
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "outputs"
DIMS = ["relevance", "correctness", "completeness", "tone"]


def main() -> None:
    import matplotlib.pyplot as plt
    import numpy as np

    rows = json.loads((ROOT / "report.json").read_text())
    scores = {d: [r["scores"][d]["score"] for r in rows] for d in DIMS}

    fig, ax = plt.subplots(figsize=(7.5, 4.2))
    rng = np.random.default_rng(0)
    for i, d in enumerate(DIMS):
        ys = np.array(scores[d], dtype=float)
        xs = i + (rng.random(len(ys)) - 0.5) * 0.28
        ax.scatter(xs, ys, s=42, alpha=0.75,
                   color=("#e6550d" if ys.min() < 4 else "#9ecae1"))
        ax.plot([i - 0.22, i + 0.22], [ys.mean(), ys.mean()], color="#333", lw=2)
        ax.text(i, 5.35, f"range {int(ys.min())}–{int(ys.max())}", ha="center", fontsize=9,
                weight=("bold" if ys.min() < 4 else "normal"))

    ax.set_xticks(range(len(DIMS)))
    ax.set_xticklabels(DIMS)
    ax.set_yticks([1, 2, 3, 4, 5])
    ax.set_ylim(0.7, 5.7)
    ax.set_ylabel("judge score (1–5)")
    ax.set_title("Where the local judge discriminates — and where it's stuck\n"
                 "(each dot = one of 16 support replies; bar = mean)", fontsize=10)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    fig.tight_layout()
    OUT.mkdir(exist_ok=True)
    fig.savefig(OUT / "score_spread.png", dpi=130)
    plt.close(fig)
    print(f"wrote {OUT/'score_spread.png'}")


if __name__ == "__main__":
    main()
