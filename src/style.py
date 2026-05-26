"""
style.py — Helfrich publication palette and matplotlib defaults.

Identity system documented in docs/style-guide.md.

Heritage palette drawn from Dr. Helfrich's institutions:
  CAROLINA_BLUE  UNC Chapel Hill primary
  CAROLINA_NAVY  UNC institutional navy
  OLD_GOLD       Georgia Tech Old Gold
  BSE_TEAL       Barcelona Graduate School of Economics aesthetic
  INDIANA_CRIMSON Indiana University Bloomington crimson
  PARCHMENT      warm cream background (scholarship over startup)
  SLATE          secondary text
  MIST           low-contrast separators

Palette is semantic, not decorative. Each color encodes a role.

Usage
-----
    from style import (helfrich_style,
                       CAROLINA_BLUE, CAROLINA_NAVY, OLD_GOLD,
                       BSE_TEAL, INDIANA_CRIMSON,
                       PARCHMENT, SLATE, MIST)

    @helfrich_style
    def fig_my_panel():
        fig, ax = plt.subplots()
        ax.plot(x, y, color=CAROLINA_BLUE)
        return fig

Backward-compatible aliases (INK, RUST, etc.) preserved so existing
figures continue to render. New work should use the heritage names.
"""
from __future__ import annotations

import functools
from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt

# ----------------------------------------------------------------------
# Heritage palette
# ----------------------------------------------------------------------

CAROLINA_BLUE   = "#4B9CD3"   # UNC primary  — dominant brand
CAROLINA_NAVY   = "#13294B"   # UNC navy     — body ink, headings
OLD_GOLD        = "#B3A369"   # GT Old Gold  — heritage accent, emphasis
BSE_TEAL        = "#2C7873"   # BGSE         — comparison, alternative
INDIANA_CRIMSON = "#990000"   # IU crimson   — warning, dissent (sparing)

PARCHMENT       = "#FAF8F3"   # warm cream background
SLATE           = "#4E5667"   # secondary text, axis labels
MIST            = "#E8E2D5"   # borders, dividers

# Sequential and diverging maps for heatmaps / continuous quantities
SEQ_BLUES = ["#E3EEF7", "#B8D3E8", "#7FB1D3", "#4B9CD3", CAROLINA_NAVY]
SEQ_GOLDS = ["#F4EFDC", "#E0D2A4", "#C7B97A", OLD_GOLD,  "#7E6F3B"]
DIV_BLUE_GOLD = [CAROLINA_NAVY, "#4B9CD3", "#B8D3E8", PARCHMENT,
                 "#E0D2A4", OLD_GOLD, "#7E6F3B"]

# Backward-compatible aliases (so existing figures keep rendering)
INK    = CAROLINA_NAVY        # was #1a4f7a; now Carolina Navy
RUST   = INDIANA_CRIMSON      # was #b85c38; now Indiana Crimson
SAGE   = BSE_TEAL             # was #5a7247; now BSE Teal
GOLD   = OLD_GOLD             # was #b8941e; now Old Gold
VIOLET = "#6a5acd"            # retained (not heritage but useful)
DIM    = SLATE                # was #8a8a8a; now Slate (warmer)
TEAL   = BSE_TEAL             # alias

# Re-export legacy sequence maps under the same names so existing imports
# keep working; the new heritage versions are SEQ_GOLDS and DIV_BLUE_GOLD.
SEQ_WARM      = SEQ_GOLDS
DIV_BLUE_RUST = DIV_BLUE_GOLD

PALETTE = {
    "CAROLINA_BLUE":   CAROLINA_BLUE,
    "CAROLINA_NAVY":   CAROLINA_NAVY,
    "OLD_GOLD":        OLD_GOLD,
    "BSE_TEAL":        BSE_TEAL,
    "INDIANA_CRIMSON": INDIANA_CRIMSON,
    "PARCHMENT":       PARCHMENT,
    "SLATE":           SLATE,
    "MIST":            MIST,
}

# Figure sizes in inches
FIG_SINGLE   = (5.5, 3.6)
FIG_FULL     = (9.0, 5.5)
FIG_SPREAD   = (12.0, 6.5)
FIG_TALL     = (6.0, 7.5)
FIG_SQUARE   = (7.0, 7.0)
FIG_NINEPANEL = (15.0, 11.0)

# Output directory
HERE = Path(__file__).resolve().parent.parent
FIG_OUTPUT = HERE / "figures"
FIG_OUTPUT.mkdir(parents=True, exist_ok=True)


def apply_defaults() -> None:
    """Apply Helfrich-publication matplotlib defaults."""
    matplotlib.rcParams.update({
        # PDF embedding
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "svg.fonttype": "none",

        # Typography
        "font.family": "sans-serif",
        "font.sans-serif": ["DejaVu Sans", "Helvetica", "Arial", "sans-serif"],
        "font.size": 11.5,
        "axes.titlesize": 12.5,
        "axes.titleweight": "regular",
        "axes.titlepad": 11,
        "axes.labelsize": 11,
        "axes.labelweight": "regular",
        "axes.labelpad": 6,
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
        "legend.fontsize": 10,
        "legend.frameon": False,
        "figure.titlesize": 14,

        "mathtext.fontset": "dejavusans",
        "mathtext.default": "regular",

        "lines.linewidth": 1.9,
        "lines.markersize": 5,
        "patch.linewidth": 0.7,

        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.linewidth": 0.9,
        "axes.edgecolor": "#444444",

        "xtick.direction": "out", "ytick.direction": "out",
        "xtick.major.size": 4, "ytick.major.size": 4,
        "xtick.major.width": 0.8, "ytick.major.width": 0.8,
        "xtick.color": "#444444", "ytick.color": "#444444",

        "axes.grid": True,
        "axes.grid.axis": "both",
        "grid.alpha": 0.22,
        "grid.linewidth": 0.6,
        "grid.color": "#888888",

        # Default color cycle uses the heritage palette in order of
        # narrative role: primary, contrast, comparison, emphasis,
        # then accents.
        "axes.prop_cycle": matplotlib.cycler(color=[
            CAROLINA_BLUE, INDIANA_CRIMSON, BSE_TEAL, OLD_GOLD,
            CAROLINA_NAVY, VIOLET, SLATE,
        ]),

        # Warm parchment background for figures (scholarship over startup)
        "figure.facecolor": PARCHMENT,
        "axes.facecolor":   PARCHMENT,

        "savefig.dpi": 300,
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.18,
        "savefig.transparent": False,
        "savefig.facecolor": PARCHMENT,
        "figure.dpi": 150,
        "figure.edgecolor": PARCHMENT,
    })


def helfrich_style(name=None, size=FIG_FULL, save=True, output_dir=None):
    """
    Decorator that styles a figure-producing function and saves the result.

    Usage:
        @helfrich_style                  # default size
        def fig_xxx(): return fig

        @helfrich_style(size=FIG_NINEPANEL)
        def fig_panel(): return fig
    """
    if callable(name):
        func = name
        return _wrap(func, name=None, size=FIG_FULL, save=True, output_dir=None)

    def decorator(func):
        return _wrap(func, name=name, size=size, save=save, output_dir=output_dir)

    return decorator


def _wrap(func, name, size, save, output_dir):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        apply_defaults()
        fig = func(*args, **kwargs)
        if fig is None:
            raise RuntimeError(
                f"Figure function {func.__name__!r} returned None."
            )
        if size is not None:
            fig.set_size_inches(*size)
        try:
            fig.tight_layout()
        except Exception:
            pass
        if save:
            outdir = Path(output_dir) if output_dir else FIG_OUTPUT
            outdir.mkdir(parents=True, exist_ok=True)
            stem = name or func.__name__
            fig.savefig(outdir / f"{stem}.png", dpi=300)
            fig.savefig(outdir / f"{stem}.pdf")
            print(f"  saved figures/{stem}.png + {stem}.pdf")
        return fig
    return wrapper


def clean_axes(ax, *, top=False, right=False, left=True, bottom=True):
    ax.spines["top"].set_visible(top)
    ax.spines["right"].set_visible(right)
    ax.spines["left"].set_visible(left)
    ax.spines["bottom"].set_visible(bottom)
    ax.tick_params(axis="x", direction="out", length=4)
    ax.tick_params(axis="y", direction="out", length=4)
    return ax


def panel_letter(ax, letter, title, *, x=-0.06, y=1.05):
    """
    Place a panel letter (a), (b), (c) and a title aligned to the axis.
    Letter is bold INK; title is regular in axis color.
    """
    ax.text(x, y, f"({letter})", transform=ax.transAxes,
            fontsize=12, color=INK, fontweight="bold",
            ha="left", va="bottom")
    ax.text(x + 0.04, y, title, transform=ax.transAxes,
            fontsize=11, color="#1F2937",
            ha="left", va="bottom")
