"""
linkedin_hero.py - LinkedIn hero graphic: 4-metric pre/post comparison.

Output: figures/linkedin_hero.png at 1200x627 (LinkedIn preview-card
aspect ratio), heritage palette, large readable type.
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, str(Path(__file__).parent))

from style import (CAROLINA_NAVY, INDIANA_CRIMSON, OLD_GOLD, PARCHMENT,
                   SLATE, MIST, apply_defaults)


def make_hero(out_path: Path) -> None:
    apply_defaults()

    metrics = [
        "Wasserstein-1\nrun severity\n(bp-mass)",
        "Eisenberg-Noe\namplification\nindex",
        "Model-implied\nrun probability",
        "Spectral radius\n(loss-feedback\noperator)",
    ]
    pre_vals  = [0.82, 1.27, 0.90, 0.87]
    post_vals = [0.04, 1.00, 0.18, 0.42]

    fig, ax = plt.subplots(figsize=(12, 6.27), dpi=200)
    fig.patch.set_facecolor(PARCHMENT)
    ax.set_facecolor(PARCHMENT)

    x = np.arange(len(metrics))
    w = 0.36

    bars_pre  = ax.bar(x - w/2, pre_vals, width=w,
                       color=CAROLINA_NAVY, label="Pre-EO (current regime)",
                       zorder=3)
    bars_post = ax.bar(x + w/2, post_vals, width=w,
                       color=INDIANA_CRIMSON, label="Post-EO (direct Fed access)",
                       zorder=3)

    # Value labels on top of each bar
    for b, v in zip(bars_pre, pre_vals):
        ax.text(b.get_x() + b.get_width()/2, b.get_height() + 0.03,
                f"{v:.2f}", ha="center", va="bottom",
                fontsize=12, color=CAROLINA_NAVY, fontweight="bold")
    for b, v in zip(bars_post, post_vals):
        ax.text(b.get_x() + b.get_width()/2, b.get_height() + 0.03,
                f"{v:.2f}", ha="center", va="bottom",
                fontsize=12, color=INDIANA_CRIMSON, fontweight="bold")

    # Percent-change annotations between paired bars
    deltas = [
        (0, "-95%", -0.07),
        (1, "-21%", -0.07),
        (2, "-80%", -0.07),
        (3, "-52%", -0.07),
    ]
    for i, txt, y in deltas:
        ax.annotate(txt, xy=(x[i], 0.0), xytext=(x[i], y),
                    ha="center", va="top",
                    fontsize=11, color=OLD_GOLD, fontweight="bold",
                    annotation_clip=False)

    ax.set_xticks(x)
    ax.set_xticklabels(metrics, fontsize=10.5, color=CAROLINA_NAVY)
    ax.set_ylim(0, 1.6)
    ax.set_ylabel("metric value", fontsize=11, color=SLATE)
    ax.tick_params(axis="y", labelsize=10, colors=SLATE)
    ax.tick_params(axis="x", labelsize=10.5)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["bottom"].set_color(SLATE)
    ax.spines["left"].set_color(SLATE)

    ax.set_axisbelow(True)
    ax.grid(axis="y", alpha=0.22, color=SLATE, linewidth=0.6, zorder=1)

    ax.set_title(
        "EO 14405 reduces stablecoin contagion across all four frameworks",
        fontsize=15, color=CAROLINA_NAVY, fontweight="bold",
        loc="left", pad=14,
    )

    fig.text(0.5, 0.04,
             "Ian Helfrich, Ph.D. (Georgia Tech 2024). Calibration: USDC March 2023 episode "
             "(Fed FEDS Notes 17 Dec 2025). Full analysis: ihelfrich.github.io/eo14405-contagion",
             ha="center", fontsize=9, color=SLATE, style="italic")

    ax.legend(loc="upper right", fontsize=11, frameon=False)

    plt.tight_layout(rect=(0.01, 0.07, 0.99, 0.97))
    plt.savefig(out_path, dpi=200, bbox_inches="tight",
                facecolor=PARCHMENT)
    plt.close()
    print(f"saved {out_path}")


if __name__ == "__main__":
    here = Path(__file__).resolve().parent.parent
    out = here / "figures" / "linkedin_hero.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    make_hero(out)
