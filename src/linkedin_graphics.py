"""
linkedin_graphics.py - Redesigned LinkedIn-ready graphics.

Three images, each optimized for the 3-second-scroll test on mobile.
Heritage palette. No technical jargon required to understand the
headline. Big readable type.

Output:
  figures/li_mechanism.png   - "Where does the loss go?" flow diagram
  figures/li_scorecard.png   - Conflict-of-interest scorecard
  figures/li_spine.png       - Simplified 12-node SNA spine
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, str(Path(__file__).parent))

from style import (CAROLINA_BLUE, CAROLINA_NAVY, INDIANA_CRIMSON, OLD_GOLD,
                   BSE_TEAL, PARCHMENT, SLATE, MIST)

# Common LinkedIn preview aspect: 1200x627 (1.91:1)
LI_FIG_SIZE = (12, 6.27)
LI_DPI = 200


def make_mechanism(out_path: Path) -> None:
    """
    Hero image: where the loss lands, before vs after EO 14405.

    No technical terms. Two side-by-side flow diagrams. Big arrows,
    big absorbed-by labels. Each tells the story in 3 seconds.
    """
    fig, ax = plt.subplots(figsize=LI_FIG_SIZE, dpi=LI_DPI)
    fig.patch.set_facecolor(PARCHMENT)
    ax.set_facecolor(PARCHMENT)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 6.27)
    ax.axis("off")

    # Title
    ax.text(6, 5.85, "Where does the loss go when a stablecoin fails?",
            ha="center", va="top", fontsize=18,
            color=CAROLINA_NAVY, fontweight="bold")
    ax.text(6, 5.45, "EO 14405 reduces run risk, but the absorption mechanism moves to a different balance sheet",
            ha="center", va="top", fontsize=11, color=SLATE, style="italic")

    # Vertical divider
    ax.plot([6, 6], [0.6, 4.85], color=MIST, lw=1.5)

    def panel(x_center: float, title: str, accent: str,
              flow_label: str, absorber: str, absorber_sub: str,
              dollar: str) -> None:
        # Panel title
        ax.text(x_center, 4.65, title, ha="center", va="top",
                fontsize=15, color=accent, fontweight="bold")

        # Three boxes stacked: Stablecoin → Intermediary → Failure → Absorber
        # Top box: stablecoin holder (Carolina Blue)
        b1 = mpatches.FancyBboxPatch(
            (x_center - 1.7, 3.45), 3.4, 0.7,
            boxstyle="round,pad=0.04,rounding_size=0.12",
            linewidth=1.5, edgecolor=CAROLINA_BLUE, facecolor="white", zorder=2)
        ax.add_patch(b1)
        ax.text(x_center, 3.80, "Stablecoin holder", ha="center", va="center",
                fontsize=11, color=CAROLINA_NAVY, fontweight="bold")

        # Arrow down
        ax.annotate("", xy=(x_center, 3.05), xytext=(x_center, 3.40),
                    arrowprops=dict(arrowstyle="->", color=SLATE, lw=1.4))
        ax.text(x_center + 0.18, 3.22, "reserves", fontsize=9.5,
                color=SLATE, ha="left", va="center", style="italic")

        # Middle box: intermediary
        b2 = mpatches.FancyBboxPatch(
            (x_center - 1.7, 2.30), 3.4, 0.7,
            boxstyle="round,pad=0.04,rounding_size=0.12",
            linewidth=1.5, edgecolor=accent, facecolor="white", zorder=2)
        ax.add_patch(b2)
        ax.text(x_center, 2.65, flow_label, ha="center", va="center",
                fontsize=11, color=CAROLINA_NAVY, fontweight="bold")

        # Arrow down with "FAILURE" label
        ax.annotate("", xy=(x_center, 1.90), xytext=(x_center, 2.25),
                    arrowprops=dict(arrowstyle="->", color=INDIANA_CRIMSON, lw=2))
        ax.text(x_center + 0.20, 2.07, "failure", fontsize=9.5,
                color=INDIANA_CRIMSON, ha="left", va="center", style="italic",
                fontweight="bold")

        # Bottom box: who absorbs (the kicker)
        b3 = mpatches.FancyBboxPatch(
            (x_center - 1.85, 0.92), 3.7, 1.0,
            boxstyle="round,pad=0.04,rounding_size=0.14",
            linewidth=2.2, edgecolor=accent, facecolor=accent, zorder=2)
        ax.add_patch(b3)
        ax.text(x_center, 1.62, absorber, ha="center", va="center",
                fontsize=13, color="white", fontweight="bold")
        ax.text(x_center, 1.22, absorber_sub, ha="center", va="center",
                fontsize=10, color="white", style="italic")

        # Dollar tag
        ax.text(x_center, 0.55, dollar, ha="center", va="center",
                fontsize=14, color=accent, fontweight="bold")

    # LEFT: Before EO 14405
    panel(
        x_center=3.0,
        title="Before EO 14405 (today)",
        accent=CAROLINA_NAVY,
        flow_label="Commercial bank\n(e.g., Silicon Valley Bank)",
        absorber="BANK SHAREHOLDERS",
        absorber_sub="absorb the loss",
        dollar="≈ $40 billion at SVB, March 2023",
    )

    # RIGHT: After EO 14405
    panel(
        x_center=9.0,
        title="After EO 14405 (the order)",
        accent=INDIANA_CRIMSON,
        flow_label="Federal Reserve\nmaster account",
        absorber="FEDERAL RESERVE",
        absorber_sub="absorbs the loss (at a rate not yet set)",
        dollar="≈ $12 billion in baseline model",
    )

    # Footer
    fig.text(0.5, 0.025,
             "Ian Helfrich, Ph.D. (Georgia Tech 2024). Full analysis: ihelfrich.github.io/eo14405-contagion",
             ha="center", fontsize=9, color=SLATE, style="italic")

    plt.savefig(out_path, dpi=LI_DPI, bbox_inches="tight",
                facecolor=PARCHMENT)
    plt.close()
    print(f"saved {out_path}")


def make_scorecard(out_path: Path) -> None:
    """
    Conflict-of-interest scorecard. Six rows: name, position, dollar
    amount of relevant disclosed asset, the one-line "what this
    affects" framing. Reads at a glance.
    """
    fig, ax = plt.subplots(figsize=LI_FIG_SIZE, dpi=LI_DPI)
    fig.patch.set_facecolor(PARCHMENT)
    ax.set_facecolor(PARCHMENT)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 6.27)
    ax.axis("off")

    # Title
    ax.text(6, 5.95, "Who is writing the rules for stablecoin-Fed access?",
            ha="center", va="top", fontsize=17,
            color=CAROLINA_NAVY, fontweight="bold")
    ax.text(6, 5.55, "Disclosed financial interests of US officials with direct authority over EO 14405 implementation",
            ha="center", va="top", fontsize=10.5,
            color=SLATE, style="italic")

    # Column headers
    headers = ["Name", "Position", "Disclosed financial interest", "Source"]
    col_x =   [0.45, 2.85, 5.65, 10.55]
    for x, h in zip(col_x, headers):
        ax.text(x, 4.95, h, ha="left", va="bottom",
                fontsize=10, color=OLD_GOLD, fontweight="bold")
    ax.plot([0.3, 11.7], [4.85, 4.85], color=OLD_GOLD, lw=1.2)

    rows = [
        ("Kevin Warsh",      "Federal Reserve Chair",
         "$100M+ Duquesne 'Juggernaut' LP\n+ equity in 20+ blockchain firms",
         "OGE-278\n04/10/2026"),
        ("William Pulte",    "FHFA Director",
         "$500K-$1M BTC, $500K-$1M SOL,\n$5M-$25M MARA Holdings common",
         "OGE-278"),
        ("Kevin Hassett",    "NEC Director",
         "$1M-$5M Coinbase Class A common\nchairs WH Digital Assets WG",
         "OGE-278"),
        ("Cynthia Lummis",   "Sen. Banking, Digital\nAssets Subcom. Chair",
         "~5 BTC personal\nsponsors BITCOIN Act + GENIUS",
         "Senate STOCK\nAct PTRs"),
        ("Andy Barr",        "House Financial Services",
         "$7.2M Fairshake / DAJ IE,\n$2.36M Crypto.com to 2026 KY-Sen PAC",
         "FEC"),
        ("Howard Lutnick",   "Commerce Secretary",
         "Family Cantor Fitzgerald: ~5% Tether equity\n(per WSJ Nov 24, 2024)",
         "Press"),
    ]

    y0 = 4.55
    row_h = 0.66
    for i, (name, pos, fin, src) in enumerate(rows):
        y = y0 - i * row_h
        if i % 2 == 0:
            bg = mpatches.Rectangle((0.3, y - row_h + 0.06), 11.4, row_h - 0.03,
                                    facecolor=MIST, alpha=0.32,
                                    edgecolor="none", zorder=0)
            ax.add_patch(bg)
        ax.text(col_x[0], y - 0.10, name, ha="left", va="top",
                fontsize=11, color=CAROLINA_NAVY, fontweight="bold")
        ax.text(col_x[1], y - 0.10, pos, ha="left", va="top",
                fontsize=10, color=CAROLINA_NAVY)
        ax.text(col_x[2], y - 0.10, fin, ha="left", va="top",
                fontsize=10, color=INDIANA_CRIMSON, fontweight="bold")
        ax.text(col_x[3], y - 0.10, src, ha="left", va="top",
                fontsize=9, color=SLATE, style="italic")

    # Footer
    fig.text(0.5, 0.04,
             "All figures verified at primary sources where marked OGE-278 / FEC / STOCK Act. Press-sourced claims marked. "
             "Full validation pass at ihelfrich.github.io/eo14405-contagion",
             ha="center", fontsize=8.5, color=SLATE, style="italic")

    plt.savefig(out_path, dpi=LI_DPI, bbox_inches="tight",
                facecolor=PARCHMENT)
    plt.close()
    print(f"saved {out_path}")


def make_spine_simple(out_path: Path) -> None:
    """
    Simplified network spine: 12 nodes max, hand-positioned, big labels,
    no overlapping. Shows the redundancy finding: removing any small set
    of named officials does not disconnect the three clusters because the
    Trump–Andreessen donation edge and the Trump–Cook litigation edge
    create alternative paths.
    """
    fig, ax = plt.subplots(figsize=LI_FIG_SIZE, dpi=LI_DPI)
    fig.patch.set_facecolor(PARCHMENT)
    ax.set_facecolor(PARCHMENT)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 6.27)
    ax.axis("off")

    # Title and subtitle pinned at the top; full graph workspace is
    # 0..4.6 vertical for nodes (leaving title room above 4.85, legend
    # room below 0.10).
    ax.text(6, 6.10, "The conflict architecture is structurally redundant",
            ha="center", va="top", fontsize=16,
            color=CAROLINA_NAVY, fontweight="bold")
    ax.text(6, 5.65,
            "Removing any five named officials does not disconnect the network. The donation and litigation edges create alternative paths.",
            ha="center", va="top", fontsize=9.5, color=SLATE, style="italic")

    # 12 nodes laid out in workspace y in [1.10, 4.50], with stablecoin
    # row well above the legend (at y=0.05-0.45).
    nodes = {
        # Admin / Trump cluster (left)
        "Donald Trump":               (1.6, 3.15, CAROLINA_NAVY, "admin"),
        "World Liberty\nFinancial":   (1.2, 1.70, CAROLINA_NAVY, "admin"),
        "Howard Lutnick\n(Commerce)": (1.4, 4.45, CAROLINA_NAVY, "admin"),
        # Bridge nodes (middle, gold)
        "Marc Andreessen\n(a16z)":    (5.2, 4.10, OLD_GOLD, "bridge"),
        "Lisa Cook\n(Fed Gov.)":      (5.5, 2.55, OLD_GOLD, "bridge"),
        # Fed cluster (right side, upper)
        "Kevin Warsh\n(Fed Chair)":   (10.0, 4.45, INDIANA_CRIMSON, "fed"),
        "Federal Reserve\nBoard":     (10.7, 3.25, INDIANA_CRIMSON, "fed"),
        "Kevin Hassett\n(NEC)":       (8.4, 3.95, INDIANA_CRIMSON, "fed"),
        # Stablecoin cluster: a single tidy row at y around 1.40, with
        # Tether sitting slightly higher and USAT slightly lower to make
        # the right-side label stack readable.
        "Tether / USDT":              (10.4, 2.15, BSE_TEAL, "stablecoin"),
        "USDC / Circle":              (8.4, 1.55, BSE_TEAL, "stablecoin"),
        "Coinbase":                   (6.8, 1.55, BSE_TEAL, "stablecoin"),
        "USAT / Anchorage":           (10.4, 1.15, BSE_TEAL, "stablecoin"),
    }

    edges = [
        ("Donald Trump",      "World Liberty\nFinancial",   "family",      INDIANA_CRIMSON),
        ("Donald Trump",      "Howard Lutnick\n(Commerce)", "appointed",   SLATE),
        ("Donald Trump",      "Kevin Warsh\n(Fed Chair)",   "appointed",   SLATE),
        ("Donald Trump",      "Kevin Hassett\n(NEC)",       "appointed",   SLATE),
        ("Donald Trump",      "Marc Andreessen\n(a16z)",    "$2.5M donation", OLD_GOLD),
        ("Donald Trump",      "Lisa Cook\n(Fed Gov.)",      "litigation",  OLD_GOLD),
        ("Howard Lutnick\n(Commerce)", "Tether / USDT",     "Cantor 5% equity", SLATE),
        ("Marc Andreessen\n(a16z)",    "Coinbase",          "board / VC",       SLATE),
        ("Marc Andreessen\n(a16z)",    "USDC / Circle",     "a16z portfolio",   SLATE),
        ("Kevin Warsh\n(Fed Chair)",   "Federal Reserve\nBoard", "chairs",  SLATE),
        ("Kevin Hassett\n(NEC)",       "USDC / Circle",     "$1-5M COIN",  INDIANA_CRIMSON),
        ("Federal Reserve\nBoard",     "Tether / USDT",     "EO 14405 §4", SLATE),
        ("Federal Reserve\nBoard",     "USDC / Circle",     "EO 14405 §4", SLATE),
        ("Federal Reserve\nBoard",     "USAT / Anchorage",  "EO 14405 §4", SLATE),
        ("Tether / USDT",     "USAT / Anchorage",          "subsidiary",  SLATE),
    ]

    # Draw edges first
    for src, dst, label, color in edges:
        x1, y1, _, _ = nodes[src]
        x2, y2, _, _ = nodes[dst]
        lw = 1.8 if color == OLD_GOLD else 1.0
        alpha = 1.0 if color == OLD_GOLD else 0.55
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="-", color=color,
                                    lw=lw, alpha=alpha,
                                    connectionstyle="arc3,rad=0.05"),
                    zorder=1)

    # Per-node label-offset overrides. Stablecoin-cluster labels
    # pushed to the right or above to avoid colliding with each other
    # and with the legend at the bottom.
    label_offsets = {
        "Donald Trump":               (0.0, -0.55),
        "World Liberty\nFinancial":   (0.0, -0.55),
        "Howard Lutnick\n(Commerce)": (0.0, 0.50),
        "Marc Andreessen\n(a16z)":    (0.0, 0.50),
        "Lisa Cook\n(Fed Gov.)":      (-0.55, 0.0),
        "Kevin Warsh\n(Fed Chair)":   (0.0, 0.50),
        "Federal Reserve\nBoard":     (0.55, 0.0),
        "Kevin Hassett\n(NEC)":       (0.0, 0.50),
        "Tether / USDT":              (0.55, 0.0),
        "USDC / Circle":              (0.55, 0.0),
        "Coinbase":                   (0.0, 0.50),
        "USAT / Anchorage":           (0.55, 0.0),
    }

    # Draw nodes on top
    for name, (x, y, color, _) in nodes.items():
        circle = mpatches.Circle((x, y), 0.28, facecolor=color,
                                 edgecolor="white", linewidth=2.5, zorder=3)
        ax.add_patch(circle)
        dx, dy = label_offsets.get(name, (0.0, 0.55))
        ha = "left"   if dx > 0 else ("right" if dx < 0 else "center")
        va = "center" if dx != 0 else ("top" if dy < 0 else "bottom")
        ax.text(x + dx, y + dy, name, ha=ha, va=va,
                fontsize=8.5, color=CAROLINA_NAVY, fontweight="bold",
                zorder=4)

    # Legend box: centered across the full width, well below the
    # stablecoin cluster. Wider so the chips don't crowd each other.
    legend_box = mpatches.FancyBboxPatch(
        (0.5, 0.05), 11.0, 0.40,
        boxstyle="round,pad=0.04,rounding_size=0.08",
        linewidth=1.0, edgecolor=MIST, facecolor="white", zorder=2)
    ax.add_patch(legend_box)
    legend_items = [
        (1.10, "Trump admin",          CAROLINA_NAVY),
        (3.60, "Federal Reserve",      INDIANA_CRIMSON),
        (6.40, "Stablecoin issuers",   BSE_TEAL),
        (9.30, "Bridge (redundancy)",  OLD_GOLD),
    ]
    for x_pos, label, color in legend_items:
        ax.scatter(x_pos, 0.25, s=100, color=color, edgecolor="white",
                   linewidth=1.5, zorder=4)
        ax.text(x_pos + 0.22, 0.25, label, ha="left", va="center",
                fontsize=9, color=SLATE, zorder=4)

    # Footer
    fig.text(0.5, 0.025,
             "Ian Helfrich, Ph.D. (Georgia Tech 2024). "
             "Full 153-node SNA + validation: ihelfrich.github.io/eo14405-contagion",
             ha="center", fontsize=9, color=SLATE, style="italic")

    plt.savefig(out_path, dpi=LI_DPI, bbox_inches="tight",
                facecolor=PARCHMENT)
    plt.close()
    print(f"saved {out_path}")


def main() -> None:
    here = Path(__file__).resolve().parent.parent
    fig_dir = here / "figures"
    fig_dir.mkdir(parents=True, exist_ok=True)
    make_mechanism(fig_dir / "li_mechanism.png")
    make_scorecard(fig_dir / "li_scorecard.png")
    make_spine_simple(fig_dir / "li_spine.png")


if __name__ == "__main__":
    main()
