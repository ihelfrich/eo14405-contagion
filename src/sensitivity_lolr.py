"""
sensitivity_lolr.py - sensitivity of Negishi-Pareto net welfare to the
Fed lender-of-last-resort (LOLR) rate charged to non-bank master-account
holders under EO 14405.

The order does not specify the rate. The Federal Reserve Board sets it.
This figure shows how the welfare conclusion depends on that rate.

Output: figures/sensitivity_lolr.png at 1200x800, heritage palette.
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, str(Path(__file__).parent))

from style import (CAROLINA_BLUE, CAROLINA_NAVY, OLD_GOLD,
                   INDIANA_CRIMSON, BSE_TEAL,
                   PARCHMENT, SLATE, MIST, apply_defaults)


# ---------------------------------------------------------------------- #
# Model
# ---------------------------------------------------------------------- #
# Net welfare under EO 14405 minus net welfare under the current regime,
# under equal Negishi-Pareto weights, as a function of the Fed LOLR rate.
#
# Components (calibrated to USDC March 2023 episode, see paper.md S5):
#   (A) Run-severity gain:        +$112M  (constant across LOLR rates;
#                                          it is the reduction in expected
#                                          redemption-shock loss to USDC
#                                          holders from direct Fed access)
#   (B) Contagion-amplification:  + $48M  (constant; Eisenberg-Noe term)
#   (C) Implicit-subsidy cost:    - r * E (E = $12B exposure; r = LOLR
#                                          rate; this is the term that
#                                          depends on the Fed Board's
#                                          undetermined rate-setting
#                                          policy)
#
# Net welfare(r) = 112 + 48 - r * 12_000 / 10_000
#               = 160 - 1.2 * r_bp        (in $M)
#
# Break-even at r = 160 / 1.2 = 133.3 basis points.

GAIN_RUN_SEVERITY = 112.0       # $M, USDC-calibrated
GAIN_AMPLIFICATION = 48.0       # $M
EXPOSURE_BILLIONS = 12.0        # $B at risk under non-bank master-account


def net_welfare_dollars_m(rate_bp: np.ndarray) -> np.ndarray:
    """Net welfare (post-EO minus pre-EO) in $M, as function of LOLR rate."""
    subsidy_cost = rate_bp * EXPOSURE_BILLIONS * 1000 / 10_000  # $M
    return GAIN_RUN_SEVERITY + GAIN_AMPLIFICATION - subsidy_cost


def make_sensitivity(out_path: Path) -> None:
    apply_defaults()

    rates = np.linspace(0, 300, 601)
    welfare = net_welfare_dollars_m(rates)
    break_even = (GAIN_RUN_SEVERITY + GAIN_AMPLIFICATION) / (EXPOSURE_BILLIONS * 1000 / 10_000)

    fig, ax = plt.subplots(figsize=(12, 6.8), dpi=200)
    fig.patch.set_facecolor(PARCHMENT)
    ax.set_facecolor(PARCHMENT)

    # Welfare curve
    ax.plot(rates, welfare, color=CAROLINA_NAVY, linewidth=2.8, zorder=4,
            label="Net welfare change under EO 14405 (post minus pre)")

    # Zero line
    ax.axhline(0, color=SLATE, linewidth=1.0, alpha=0.5, zorder=1)

    # Shade welfare-degrading region
    ax.fill_between(rates, welfare, 0, where=(welfare < 0),
                    color=INDIANA_CRIMSON, alpha=0.13, zorder=2,
                    label="Welfare-degrading region (taxpayers lose)")
    ax.fill_between(rates, welfare, 0, where=(welfare >= 0),
                    color=CAROLINA_BLUE, alpha=0.13, zorder=2,
                    label="Welfare-improving region")

    # Break-even line
    ax.axvline(break_even, color=OLD_GOLD, linewidth=1.6, linestyle="--",
               zorder=3, alpha=0.85)
    ax.text(break_even + 4, 145,
            f"break-even\n{break_even:.0f} bp",
            color=OLD_GOLD, fontsize=10, fontweight="bold",
            ha="left", va="top")

    # Anchor markers: baseline, BTFP, historical discount-window stress
    anchors = [
        (30,   "Baseline calibration\n(EO + zero-spread\nadmin paper)",
         "below", CAROLINA_BLUE),
        (100,  "Historical LOLR\nstress rates\n(discount window)",
         "above", BSE_TEAL),
        (250,  "Punitive\n(unlikely)",
         "below", SLATE),
    ]
    for r, label, where, color in anchors:
        w_at = net_welfare_dollars_m(np.array([r]))[0]
        ax.scatter([r], [w_at], s=80, color=color, zorder=6,
                   edgecolor=CAROLINA_NAVY, linewidth=1.2)
        dy = -42 if where == "below" else 28
        va = "top" if where == "below" else "bottom"
        ax.annotate(label,
                    xy=(r, w_at), xytext=(r, w_at + dy),
                    ha="center", va=va,
                    fontsize=9.2, color=color, fontweight="bold",
                    arrowprops=dict(arrowstyle="-", color=color,
                                    lw=0.9, alpha=0.7))
        ax.annotate(f"${w_at:+.0f}M",
                    xy=(r, w_at),
                    xytext=(r + 7, w_at),
                    ha="left", va="center",
                    fontsize=10, color=CAROLINA_NAVY, fontweight="bold")

    ax.set_xlim(0, 300)
    ax.set_ylim(-220, 200)
    ax.set_xlabel("Fed LOLR rate charged to non-bank master-account holders (basis points over policy rate)",
                  fontsize=11.5, color=CAROLINA_NAVY)
    ax.set_ylabel("Net welfare change, post-EO minus pre-EO ($M, Negishi-Pareto equal weights)",
                  fontsize=11.5, color=CAROLINA_NAVY)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["bottom"].set_color(SLATE)
    ax.spines["left"].set_color(SLATE)
    ax.tick_params(colors=SLATE)
    ax.set_axisbelow(True)
    ax.grid(True, alpha=0.22, color=SLATE, linewidth=0.5, zorder=1)

    ax.set_title(
        "The welfare conclusion depends on a rate the order does not specify",
        fontsize=15, color=CAROLINA_NAVY, fontweight="bold",
        loc="left", pad=14,
    )

    fig.text(0.5, 0.025,
             "Net welfare = $112M (run-severity gain) + $48M (amplification gain) - r * $12B exposure. "
             "USDC March 2023 calibration. "
             "Full derivation: paper.md S5 + S7. ihelfrich.github.io/eo14405-contagion",
             ha="center", fontsize=8.8, color=SLATE, style="italic")

    ax.legend(loc="upper right", fontsize=10, frameon=False)

    plt.tight_layout(rect=(0.01, 0.06, 0.99, 0.97))
    plt.savefig(out_path, dpi=200, bbox_inches="tight", facecolor=PARCHMENT)
    plt.close()
    print(f"saved {out_path}")


if __name__ == "__main__":
    here = Path(__file__).resolve().parent.parent
    out = here / "figures" / "sensitivity_lolr.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    make_sensitivity(out)
