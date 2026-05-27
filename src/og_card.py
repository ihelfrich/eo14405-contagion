"""
og_card.py - the LinkedIn / Twitter / OG preview card.

Output: figures/og_card.png at 1200x627 (LinkedIn preview aspect),
heritage palette.

DESIGN INTENT
=============
A LinkedIn user scrolls past 60 posts per minute. The card has roughly
three seconds to deliver the WHOLE story arc. Four escalating beats:

  1. THE GAIN     - EO 14405 cuts stablecoin contagion by 95%.
  2. THE TRANSFER - The Federal Reserve eats the loss.
  3. THE EXPOSURE - The Fed Chair owns $100M+ of the affected sector.
  4. THE DEADLINE - His divestiture clock runs out August 11.

Each line raises the stakes. The headline is the hook (good news).
The next three lines turn the hook into the story (it's not).

Composition:
- Top:    Carolina Blue rule + Old Gold accent stripe
- Eyebrow: HELFRICH RESEARCH · EO 14405 · 27 MAY 2026
- iH seal top-right (mirrors the favicon)
- Left-aligned typographic stack:
    huge Carolina Navy serif for the headline ("95%" accented Old Gold)
    medium navy serif for beat 2 (transfer)
    medium navy serif for beat 3 (exposure, with "$100M+" bold)
    medium INDIANA CRIMSON serif for beat 4 (deadline, the alarm beat)
- Gold rule above the footer
- Footer: author left, canonical URL right

The crimson final beat is the single color shift that signals "this is
the part the reader should be alarmed about." Used once, with restraint.
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

sys.path.insert(0, str(Path(__file__).parent))

from style import (CAROLINA_BLUE, CAROLINA_NAVY, OLD_GOLD, INDIANA_CRIMSON,
                   BSE_TEAL, PARCHMENT, SLATE, MIST)


def make_og_card(out_path: Path) -> None:
    # 1200x627 at 100dpi
    fig = plt.figure(figsize=(12, 6.27), dpi=100)
    fig.patch.set_facecolor(PARCHMENT)

    ax = fig.add_axes((0, 0, 1, 1))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 6.27)
    ax.set_facecolor(PARCHMENT)
    ax.axis("off")

    # ------------------------------------------------------------------
    # Top frame: thin Carolina Blue rule + Old Gold accent
    # ------------------------------------------------------------------
    ax.add_patch(mpatches.Rectangle((0, 6.20), 12, 0.07, color=CAROLINA_BLUE, zorder=2))
    ax.add_patch(mpatches.Rectangle((0, 6.13), 3.5, 0.025, color=OLD_GOLD, zorder=2))

    # ------------------------------------------------------------------
    # Eyebrow
    # ------------------------------------------------------------------
    ax.text(0.55, 5.78,
            "HELFRICH  RESEARCH    ·    EO 14405    ·    27 MAY 2026",
            fontsize=12.5, color=OLD_GOLD,
            family="Helvetica Neue", weight="bold",
            ha="left", va="bottom",
            transform=ax.transData)

    # ------------------------------------------------------------------
    # iH seal (top right, mirrors favicon)
    # ------------------------------------------------------------------
    seal_x, seal_y, seal_r = 11.30, 5.55, 0.42
    ax.add_patch(mpatches.Circle((seal_x, seal_y), seal_r,
                                 facecolor=CAROLINA_NAVY,
                                 edgecolor=OLD_GOLD, linewidth=1.6,
                                 zorder=3))
    ax.text(seal_x, seal_y - 0.04, "iH",
            fontsize=20, color=OLD_GOLD,
            family="Georgia", weight="bold",
            ha="center", va="center", zorder=4)
    ax.add_patch(mpatches.Circle((seal_x - 0.155, seal_y + 0.18), 0.038,
                                 color=INDIANA_CRIMSON, zorder=5))

    # ------------------------------------------------------------------
    # Headline (the gain), with measurement-based "%" Old Gold accent
    # Two short lines so the headline doesn't collide with the iH seal.
    # ------------------------------------------------------------------
    HEAD_FONT = dict(fontsize=44, family="Georgia", weight="bold",
                     ha="left", va="baseline",
                     transform=ax.transData)

    # Line 1
    ax.text(0.55, 5.05,
            "EO 14405 cuts stablecoin",
            color=CAROLINA_NAVY, **HEAD_FONT)

    # Force a draw so we can measure rendered widths for line 2
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()

    def place(x_data: float, y_data: float, s: str, color: str,
              font_kwargs: dict) -> float:
        t = ax.text(x_data, y_data, s, color=color, **font_kwargs)
        bbox = t.get_window_extent(renderer=renderer)
        return ax.transData.inverted().transform((bbox.x1, 0))[0]

    # Line 2: "contagion by 95%." with the % in Old Gold
    cursor = 0.55
    cursor = place(cursor, 4.22, "contagion by ", CAROLINA_NAVY, HEAD_FONT)
    cursor = place(cursor, 4.22, "95",            CAROLINA_NAVY, HEAD_FONT)
    cursor = place(cursor, 4.22, "%",             OLD_GOLD,      HEAD_FONT)
    cursor = place(cursor, 4.22, ".",             CAROLINA_NAVY, HEAD_FONT)

    # ------------------------------------------------------------------
    # Three escalating beats. Each raises the stakes.
    # ------------------------------------------------------------------
    BEAT_FONT = dict(fontsize=20, family="Georgia", weight="normal",
                     ha="left", va="baseline",
                     transform=ax.transData)
    BEAT_BOLD = dict(fontsize=20, family="Georgia", weight="bold",
                     ha="left", va="baseline",
                     transform=ax.transData)

    # Beat 2: THE TRANSFER  (where does the loss go?)
    ax.text(0.55, 3.40,
            "The loss moves to the Federal Reserve balance sheet.",
            color=CAROLINA_NAVY, **BEAT_FONT)

    # Beat 3: THE EXPOSURE  (who sets the rate?)  - $100M+ bolded
    cursor = 0.55
    cursor = place(cursor, 2.80, "The chair who will set the rate holds ",
                   CAROLINA_NAVY, BEAT_FONT)
    cursor = place(cursor, 2.80, "$100M+",
                   CAROLINA_NAVY, BEAT_BOLD)
    cursor = place(cursor, 2.80, " in the affected sector.",
                   CAROLINA_NAVY, BEAT_FONT)

    # Beat 4: THE DEADLINE  - crimson, the alarm beat
    cursor = 0.55
    cursor = place(cursor, 2.20, "His divestiture deadline: ",
                   CAROLINA_NAVY, BEAT_FONT)
    cursor = place(cursor, 2.20, "August 11, 2026",
                   INDIANA_CRIMSON, BEAT_BOLD)
    cursor = place(cursor, 2.20, ".",
                   CAROLINA_NAVY, BEAT_FONT)

    # ------------------------------------------------------------------
    # Synthesis line + gold rule
    # ------------------------------------------------------------------
    ax.add_line(Line2D([0.55, 11.45], [1.50, 1.50],
                       color=OLD_GOLD, linewidth=2, zorder=2))

    ax.text(0.55, 1.05,
            "EO 14405 solved one risk and created another.",
            fontsize=15.5, color=CAROLINA_NAVY,
            family="Georgia", weight="bold", style="italic",
            ha="left", va="baseline",
            transform=ax.transData)

    # ------------------------------------------------------------------
    # Footer (author + URL)
    # ------------------------------------------------------------------
    ax.text(0.55, 0.42,
            "DR. IAN HELFRICH   ·   Ph.D. Economics, Georgia Tech 2024   ·   Independent researcher",
            fontsize=10.5, color=SLATE,
            family="Helvetica Neue", weight="normal",
            ha="left", va="baseline",
            transform=ax.transData)
    ax.text(11.45, 0.42,
            "READ  »  ihelfrich.github.io/eo14405-contagion",
            fontsize=10.5, color=CAROLINA_NAVY,
            family="Helvetica Neue", weight="bold",
            ha="right", va="baseline",
            transform=ax.transData)

    # ------------------------------------------------------------------
    # Save
    # ------------------------------------------------------------------
    plt.savefig(out_path, dpi=100, facecolor=PARCHMENT,
                bbox_inches="tight", pad_inches=0)
    plt.close()
    print(f"saved {out_path}")


if __name__ == "__main__":
    here = Path(__file__).resolve().parent.parent
    out = here / "figures" / "og_card.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    make_og_card(out)
