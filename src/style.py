"""
style.py — Dr. Ian Helfrich publication palette and matplotlib defaults.

Mirrors the Pictures of Inference styling (poi/style.py) so that figures
in this project share visual identity with the PoI textbook and other
Helfrich publications. Palette is semantic, not decorative: each color
encodes a story role.

Usage
-----
    from style import helfrich_style, INK, RUST, SAGE, GOLD, VIOLET, DIM, TEAL
    import matplotlib.pyplot as plt

    @helfrich_style
    def fig_my_panel():
        fig, ax = plt.subplots()
        ax.plot(x, y, color=INK)
        return fig

The decorator applies fonts, sizing, and saves to figures/<name>.pdf+png.
"""
from __future__ import annotations

import functools
from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt

# ----------------------------------------------------------------------
# Palette (semantic colors). Identical hex values to PoI.
# ----------------------------------------------------------------------

INK    = "#1a4f7a"   # primary  — pre-EO / baseline / dominant story
RUST   = "#b85c38"   # contrast — post-EO / treatment / alternative
SAGE   = "#5a7247"   # control  — placebo / comparison
GOLD   = "#b8941e"   # highlight — derived / synthesized
VIOLET = "#6a5acd"   # uncertain — predicted / posterior
DIM    = "#8a8a8a"   # background — support / muted
TEAL   = "#3a8a99"   # secondary contrast

# Sequential and diverging maps for heatmaps / continuous quantities
SEQ_BLUES = ["#d6e4f0", "#a8c5e0", "#6c9bc7", "#3a73a8", INK]
SEQ_WARM  = ["#f5dccb", "#e8b395", "#d68a64", RUST,     "#7a3a1f"]
DIV_BLUE_RUST = [INK, "#6c9bc7", "#d6e4f0", "#f5f5f5",
                 "#f5dccb", "#d68a64", RUST]

PALETTE = {"INK": INK, "RUST": RUST, "SAGE": SAGE, "GOLD": GOLD,
           "VIOLET": VIOLET, "DIM": DIM, "TEAL": TEAL}

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

        "axes.prop_cycle": matplotlib.cycler(color=[
            INK, RUST, SAGE, GOLD, VIOLET, TEAL, DIM,
        ]),

        "savefig.dpi": 300,
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.18,
        "savefig.transparent": False,
        "savefig.facecolor": "white",
        "figure.dpi": 150,
        "figure.facecolor": "white",
        "figure.edgecolor": "white",
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
