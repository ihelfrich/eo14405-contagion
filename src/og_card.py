"""
og_card.py - the LinkedIn / Twitter / OG preview card.

Output: figures/og_card.png at 1200x627 (1.91:1 LinkedIn preview aspect),
heritage palette, large bold serif headline. The card a Senate aide sees
before they decide whether to click through.

Design rules:
- Headline is the single thing the reader takes away. Set huge.
- Eyebrow tag locates the piece (research note / policy analysis).
- Subhead carries the catch (the "but" that makes this not just a number).
- Footer carries the byline and the canonical URL.
- A small "iH" seal in the corner mirrors the favicon and signals brand
  continuity across surfaces.
- Heritage palette only. No off-brand colors.
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import FancyBboxPatch

sys.path.insert(0, str(Path(__file__).parent))

from style import (CAROLINA_BLUE, CAROLINA_NAVY, OLD_GOLD, INDIANA_CRIMSON,
                   BSE_TEAL, PARCHMENT, SLATE, MIST)


def make_og_card(out_path: Path) -> None:
    # 1200x627 at 100dpi
    fig = plt.figure(figsize=(12, 6.27), dpi=100)
    fig.patch.set_facecolor(PARCHMENT)

    # Full-canvas axis with no ticks
    ax = fig.add_axes((0, 0, 1, 1))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 6.27)
    ax.set_facecolor(PARCHMENT)
    ax.axis("off")

    # Carolina Blue thin top border (signature line)
    ax.add_patch(mpatches.Rectangle(
        (0, 6.10), 12, 0.06, color=CAROLINA_BLUE, zorder=2))

    # Old Gold accent stripe just below
    ax.add_patch(mpatches.Rectangle(
        (0, 6.04), 4, 0.025, color=OLD_GOLD, zorder=2))

    # ------------------------------------------------------------------
    # Eyebrow (small uppercase, gold)
    # ------------------------------------------------------------------
    ax.text(0.55, 5.55, "RESEARCH NOTE  ·  HELFRICH  ·  27 MAY 2026",
            fontsize=13.5, color=OLD_GOLD,
            family="Helvetica Neue", weight="bold",
            ha="left", va="bottom",
            transform=ax.transData)

    # ------------------------------------------------------------------
    # Headline (large Georgia bold, Carolina Navy with one Old Gold accent)
    #
    # Positioning the multi-color "95%" requires real width measurement
    # because Georgia's metrics are hard to predict from character count.
    # We render each segment, query its actual rendered extent via the
    # canvas renderer, then place the next segment immediately after.
    # ------------------------------------------------------------------
    HEADLINE_FONT = dict(fontsize=52, family="Georgia", weight="bold",
                         ha="left", va="baseline",
                         transform=ax.transData)

    # Line 1: full string, single color
    ax.text(0.55, 4.20,
            "EO 14405 cuts stablecoin",
            color=CAROLINA_NAVY, linespacing=1.05,
            **HEADLINE_FONT)

    # Line 2: place segments in sequence, measure each, advance the
    # cursor by the rendered width before placing the next.
    fig.canvas.draw()           # required so get_window_extent() works
    renderer = fig.canvas.get_renderer()

    def place(x_data: float, y_data: float, s: str, color: str) -> float:
        """Render text at (x_data, y_data) and return the right edge in
        data coordinates so the next segment can start there."""
        t = ax.text(x_data, y_data, s, color=color, **HEADLINE_FONT)
        bbox_disp = t.get_window_extent(renderer=renderer)
        # Convert the right edge from display pixels back to data coords
        right_data = ax.transData.inverted().transform((bbox_disp.x1, 0))[0]
        return right_data

    cursor = 0.55
    cursor = place(cursor, 3.30, "contagion by ", CAROLINA_NAVY)
    cursor = place(cursor, 3.30, "95",            CAROLINA_NAVY)
    cursor = place(cursor, 3.30, "%",             OLD_GOLD)
    cursor = place(cursor, 3.30, ".",             CAROLINA_NAVY)

    # ------------------------------------------------------------------
    # Subhead (slate gray, Helvetica, two lines)
    # ------------------------------------------------------------------
    ax.text(0.55, 2.45,
            "Then relocates the loss to the Federal Reserve,",
            fontsize=20, color=SLATE,
            family="Helvetica Neue", weight="normal",
            ha="left", va="baseline",
            transform=ax.transData)
    ax.text(0.55, 1.95,
            "at a rate the Fed has not yet specified.",
            fontsize=20, color=SLATE,
            family="Helvetica Neue", weight="normal",
            ha="left", va="baseline",
            transform=ax.transData)

    # ------------------------------------------------------------------
    # Gold horizontal rule above the footer
    # ------------------------------------------------------------------
    ax.add_line(Line2D([0.55, 9.5], [1.30, 1.30],
                       color=OLD_GOLD, linewidth=2, zorder=2))

    # ------------------------------------------------------------------
    # Footer: author left, URL right (both small sans)
    # ------------------------------------------------------------------
    ax.text(0.55, 0.78,
            "DR. IAN HELFRICH",
            fontsize=12, color=CAROLINA_NAVY,
            family="Helvetica Neue", weight="bold",
            ha="left", va="baseline",
            transform=ax.transData)
    ax.text(0.55, 0.42,
            "Ph.D. Economics, Georgia Tech 2024  ·  Independent researcher",
            fontsize=10.5, color=SLATE,
            family="Helvetica Neue",
            ha="left", va="baseline",
            transform=ax.transData)
    ax.text(9.5, 0.78,
            "READ THE FULL ANALYSIS",
            fontsize=10.5, color=OLD_GOLD,
            family="Helvetica Neue", weight="bold",
            ha="right", va="baseline",
            transform=ax.transData)
    ax.text(9.5, 0.42,
            "ihelfrich.github.io/eo14405-contagion",
            fontsize=12, color=CAROLINA_NAVY,
            family="Helvetica Neue", weight="bold",
            ha="right", va="baseline",
            transform=ax.transData)

    # ------------------------------------------------------------------
    # "iH" seal in the bottom-right corner (mirrors the favicon)
    # ------------------------------------------------------------------
    seal_x, seal_y, seal_r = 11.1, 5.45, 0.45
    # Background circle in Carolina Navy
    seal_bg = mpatches.Circle((seal_x, seal_y), seal_r,
                              facecolor=CAROLINA_NAVY,
                              edgecolor=OLD_GOLD, linewidth=2,
                              zorder=3)
    ax.add_patch(seal_bg)
    # "iH" in Old Gold
    ax.text(seal_x, seal_y - 0.04, "iH",
            fontsize=22, color=OLD_GOLD,
            family="Georgia", weight="bold",
            ha="center", va="center",
            transform=ax.transData, zorder=4)
    # Tiny Indiana Crimson dot (signature flourish, mirrors favicon)
    crimson_dot = mpatches.Circle((seal_x - 0.16, seal_y + 0.20), 0.04,
                                  color=INDIANA_CRIMSON, zorder=5)
    ax.add_patch(crimson_dot)

    # ------------------------------------------------------------------
    # Save (no padding, exact 1200x627)
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
