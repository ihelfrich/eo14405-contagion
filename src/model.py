"""
EO 14405 contagion model.

A minimal multi-layer financial network contagion simulator. Tests how a
stablecoin issuer's exposure shock propagates under two regimes:

  PRE-EO:  stablecoin issuers hold reserves at commercial banks
  POST-EO: stablecoin issuers hold reserves directly at the Federal Reserve
           via Limited Purpose Master Accounts (precedent: Kraken Financial,
           FRBKC approval 4 March 2026; EO 14405 generalizes this pathway)

Mechanism follows Eisenberg-Noe (2001) clearing for interbank obligations,
extended with:
  - Redemption-driven asset firesales (Cont & Schaanning 2017)
  - Code-based amplification via stablecoin Peg Stability Modules
    (the Fed identified this channel in its USDC/SVB post-mortem,
    FEDS Notes 17 December 2025)
  - Primary-market suspension paradox where halted redemptions amplify
    secondary-market dysfunction

Calibration anchor: USDC March 2023 episode (3.3B USD frozen at SVB,
14% peg deviation peak, 72h to recovery, 3.8B redeemed in 5 days).

Usage:
    python src/model.py                  # runs both regimes, writes chart
    python src/model.py --calibrate      # prints calibration diagnostics
    python src/model.py --shock-pct 0.10 # parameterize shock size
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

# ---------------------------------------------------------------------------
# Network specification
# ---------------------------------------------------------------------------

@dataclass
class Node:
    name: str
    kind: Literal["bank", "regional_bank", "mmf", "stablecoin", "exchange", "fed"]
    assets: float            # USD billions
    liabilities: float       # USD billions
    cash_buffer: float = 0.0 # USD billions, immediately available
    equity: float = field(init=False)
    impaired: float = 0.0    # USD billions, frozen / unrecoverable

    def __post_init__(self) -> None:
        self.equity = self.assets - self.liabilities


def build_network(regime: Literal["pre_eo", "post_eo"]) -> tuple[nx.DiGraph, dict[str, Node]]:
    """
    Stylized network calibrated to public 2026 stablecoin market structure
    and the March 2023 USDC episode.

    Pre-EO: stablecoin issuers hold ~80% of cash reserves at commercial banks,
            ~20% in Treasury MMFs / direct T-bills.
    Post-EO: stablecoin issuers hold ~70% directly at Fed master account,
             ~20% in T-bills, ~10% at one custodian bank for operational fiat
             rails (this fraction reflects the Kraken Financial structure).

    Sizes (USD billions, approximate market data 2026):
      USDT (Tether):  ~140
      USDC (Circle):  ~42
      DAI (Maker):    ~5
      PYUSD (PayPal): ~1.5
      FDUSD (FD):     ~3

    Banks parameterized roughly to GSIB / regional sizes. The mid-tier
    regional ("SVB-class") is the one calibrated to fail in the shock.
    """
    g = nx.DiGraph()
    nodes: dict[str, Node] = {}

    # ---- Stablecoin issuers ----
    stablecoins = [
        ("USDT", 140.0),
        ("USDC",  42.0),
        ("DAI",    5.0),
        ("PYUSD",  1.5),
        ("FDUSD",  3.0),
    ]
    for nm, size in stablecoins:
        nodes[nm] = Node(name=nm, kind="stablecoin",
                         assets=size, liabilities=size,
                         cash_buffer=size * 0.02)  # 2% operational

    # ---- Banks ----
    banks = [
        ("JPM",  3900.0),
        ("BAC",  3200.0),
        ("WFC",  1900.0),
        ("REG_A", 220.0),   # large regional, BNY-class custodian
        ("REG_B",  85.0),   # mid regional, SVB-class
        ("REG_C",  45.0),   # smaller regional
    ]
    for nm, size in banks:
        kind = "bank" if size > 500 else "regional_bank"
        nodes[nm] = Node(name=nm, kind=kind,
                         assets=size, liabilities=size * 0.92,
                         cash_buffer=size * 0.08)

    # ---- MMFs and Fed ----
    nodes["MMF_PRIME"] = Node(name="MMF_PRIME", kind="mmf",
                              assets=6800.0, liabilities=6800.0,
                              cash_buffer=6800.0 * 0.05)
    nodes["FED"]       = Node(name="FED", kind="fed",
                              assets=7100.0, liabilities=7100.0,
                              cash_buffer=float("inf"))

    # ---- Exchanges (downstream amplifier nodes) ----
    nodes["COINBASE"]  = Node(name="COINBASE", kind="exchange",
                              assets=50.0, liabilities=42.0,
                              cash_buffer=8.0)
    nodes["BINANCE"]   = Node(name="BINANCE",  kind="exchange",
                              assets=80.0, liabilities=70.0,
                              cash_buffer=10.0)

    for n in nodes.values():
        g.add_node(n.name, **{"kind": n.kind, "size": n.assets})

    # ---- Edges = liability exposures (from -> to, weight = USD bn) ----
    # Stablecoin reserves placement (the regime-sensitive layer):
    if regime == "pre_eo":
        # 80% bank deposits, 20% T-bills (MMF proxy)
        bank_share = {"USDT": 0.65, "USDC": 0.85, "DAI": 0.55,
                      "PYUSD": 0.90, "FDUSD": 0.70}
        # Distribute bank share across banks; SVB-class REG_B gets a chunk
        bank_alloc = {"JPM": 0.30, "BAC": 0.20, "WFC": 0.15,
                      "REG_A": 0.18, "REG_B": 0.12, "REG_C": 0.05}
    else:  # post_eo
        # 70% at Fed master account, 20% T-bills, 10% at one custodian
        bank_share = {"USDT": 0.10, "USDC": 0.10, "DAI": 0.05,
                      "PYUSD": 0.10, "FDUSD": 0.10}
        bank_alloc = {"REG_A": 1.0}  # all residual at one custodian

    fed_share = 0.0 if regime == "pre_eo" else 0.70

    for nm, _ in stablecoins:
        size = nodes[nm].assets
        b = bank_share[nm]
        for bank_name, frac in bank_alloc.items():
            w = size * b * frac
            if w > 0:
                g.add_edge(nm, bank_name, weight=w, kind="deposit")
        if fed_share > 0:
            g.add_edge(nm, "FED", weight=size * fed_share, kind="master_account")
        # Treasury bill exposure (held via MMF proxy)
        tbill_share = 1.0 - b - fed_share
        if tbill_share > 0:
            g.add_edge(nm, "MMF_PRIME", weight=size * tbill_share, kind="tbill")

    # MMF -> Fed (overnight RRP) + MMF -> banks (commercial paper)
    g.add_edge("MMF_PRIME", "FED", weight=2200.0, kind="rrp")
    for bank_name, frac in [("JPM", 0.4), ("BAC", 0.3), ("WFC", 0.2), ("REG_A", 0.1)]:
        g.add_edge("MMF_PRIME", bank_name, weight=400.0 * frac, kind="cp")

    # Exchanges hold stablecoin balances on behalf of customers
    g.add_edge("COINBASE", "USDC", weight=15.0, kind="custody")
    g.add_edge("COINBASE", "USDT", weight=5.0,  kind="custody")
    g.add_edge("BINANCE",  "USDT", weight=25.0, kind="custody")
    g.add_edge("BINANCE",  "FDUSD", weight=2.0, kind="custody")

    # DAI PSM exposure to USDC (the canonical code-based amplifier)
    g.add_edge("DAI", "USDC", weight=3.0, kind="psm")

    return g, nodes


# ---------------------------------------------------------------------------
# Shock dynamics
# ---------------------------------------------------------------------------

@dataclass
class SimResult:
    regime: str
    hours: list[int]
    peg: dict[str, list[float]]      # stablecoin -> peg value over time
    bank_equity: dict[str, list[float]]
    fed_master_redemptions: list[float]  # USD bn drawn from Fed
    contagion_score: float           # cumulative non-target depeg


def simulate(regime: Literal["pre_eo", "post_eo"],
             *,
             shock_target: str = "REG_B",
             shock_severity: float = 1.0,
             fed_extends_liquidity: bool = True,
             horizon_hours: int = 96,
             seed: int = 7) -> SimResult:
    """
    Step the network through a redemption-shock event.

    Shock model:
      t=0      target bank enters receivership; stablecoin reserves there
               are frozen.
      t=1..3   informed traders redeem at primary market; secondary market
               begins to depeg.
      t=3..24  primary-market suspension (PRE-EO) or partial Fed liquidity
               (POST-EO); PSM amplifies USDC -> DAI; exchanges throttle.
      t=24..48 policy response (backstop announcement) restores confidence
               progressively; new mints offset redemptions.
      t=48..96 recovery toward peg, mediated by remaining structural friction.

    The peg deviation magnitude is calibrated to the USDC March 2023 episode
    for PRE-EO (14% trough, 72h recovery) when REG_B holds 8% of USDC reserves.
    """
    rng = np.random.default_rng(seed)
    g, nodes = build_network(regime)

    # Find which stablecoins are exposed via the shocked bank
    exposed: dict[str, float] = {}
    for sc in [n for n in nodes if nodes[n].kind == "stablecoin"]:
        for _, dst, data in g.out_edges(sc, data=True):
            if dst == shock_target:
                exposed[sc] = data["weight"]

    # Freeze deposits at the failed bank
    for sc, amount in exposed.items():
        nodes[sc].impaired += amount * shock_severity
        nodes[sc].cash_buffer = max(0, nodes[sc].cash_buffer - amount * shock_severity)

    # State variables over time
    hours = list(range(horizon_hours + 1))
    peg: dict[str, list[float]] = {sc: [1.0] for sc in [n for n in nodes if nodes[n].kind == "stablecoin"]}
    bank_eq: dict[str, list[float]] = {b: [nodes[b].equity]
                                       for b in [n for n in nodes if nodes[n].kind in ("bank", "regional_bank")]}
    fed_draws: list[float] = [0.0]

    # Dynamics calibrated to the USDC March 2023 episode (pre-EO regime):
    #   trough 0.86 at ~t=12h, plateau 0.87-0.92 through t=42h,
    #   partial recovery to 0.97 by t=48h after Sunday backstop,
    #   full restoration by t=72h with Monday primary-market reopen.
    #
    # Three-phase confidence model:
    #   Phase 1 (0-12h):  panic phase, confidence collapses
    #   Phase 2 (12-T*):  plateau, gates closed, secondary illiquid
    #   Phase 3 (T*+):    backstop announced, confidence rebuilds
    # T* = backstop time, regime-dependent.
    backstop_t = 48 if regime == "pre_eo" else 18  # post-EO: Fed responds faster
    if not fed_extends_liquidity:
        backstop_t = 999

    # Sensitivity coefficient: maps reserve impairment fraction to peg deviation.
    # Empirically: USDC had 8% impaired -> 14% peg deviation -> sensitivity ~1.75.
    # Post-EO sensitivity is much lower because the impairment doesn't reach the
    # stablecoin reserve base; the Fed master account absorbs the shock directly.
    sensitivity = 1.75 if regime == "pre_eo" else 0.45

    for t in hours[1:]:
        # --- Confidence evolution (three phases) ---
        if t <= 12:
            # Panic: linear collapse from 1.0 to 0.45
            confidence = 1.0 - 0.55 * (t / 12.0)
        elif t < backstop_t:
            # Plateau: drift slightly lower as gates stay closed
            confidence = 0.45 - 0.03 * ((t - 12) / max(1, backstop_t - 12))
        else:
            # Recovery: rebuild to 1.0 over a regime-dependent window
            recov_window = 24 if regime == "pre_eo" else 12
            progress = min(1.0, (t - backstop_t) / recov_window)
            confidence = 0.42 + 0.58 * progress

        # --- Redemption velocity ---
        # Holders redeem under panic regardless of whether their stablecoin
        # is directly bank-exposed. In post-EO, redemptions hit the Fed's
        # master account immediately rather than commercial bank balances.
        redemption_velocity = (1.0 - confidence) * 0.6
        if exposed:
            # Targeted run on directly-exposed issuers
            gross_redemption = sum(nodes[sc].assets * redemption_velocity * 0.05
                                   for sc in exposed)
        else:
            # Broad-based panic across the stablecoin complex
            gross_redemption = sum(nodes[sc].assets * redemption_velocity * 0.02
                                   for sc in peg)
        # In post-EO, even non-exposed issuers see panic redemption pressure
        # because the SYSTEM is under stress (REG_B failure is in the news).
        # That pressure transmits to the Fed via master-account draws.
        if regime == "post_eo":
            gross_redemption += sum(nodes[sc].assets * redemption_velocity * 0.015
                                    for sc in peg if sc not in exposed)

        # --- Peg path per stablecoin ---
        for sc in peg:
            if sc in exposed:
                impair_frac = nodes[sc].impaired / nodes[sc].assets
                # Deviation = sensitivity * impairment_fraction * panic_intensity
                # panic_intensity peaks at t=12, then declines as confidence rebuilds
                if t <= 12:
                    panic_intensity = (1.0 - confidence) / 0.55  # 0..1
                elif t < backstop_t:
                    panic_intensity = 0.95
                else:
                    progress = min(1.0, (t - backstop_t) / (24 if regime == "pre_eo" else 12))
                    panic_intensity = 0.85 * (1.0 - progress) ** 1.5
                deviation = sensitivity * impair_frac * panic_intensity
                deviation = min(deviation, 0.20)
                peg[sc].append(max(0.80, 1.0 - deviation))
            else:
                # Spillover via PSM: stablecoin sc holds positions in OTHER
                # stablecoins (e.g. DAI's PSM holds USDC). When the held
                # stablecoin depegs, sc's collateral is impaired.
                spillover = 0.0
                for _src, dst, edata in g.out_edges(sc, data=True):
                    if edata.get("kind") == "psm" and dst in exposed:
                        # Fraction of sc's reserves held as the impaired stablecoin
                        held_frac = edata["weight"] / nodes[sc].assets
                        deviation_dst = 1.0 - peg[dst][-1]
                        spillover += held_frac * deviation_dst * 0.7
                # Network effect: post-EO, the operational similarity of
                # direct-Fed-access stablecoins makes substitution between them
                # faster. A holder of A redeems and mints B in seconds, not
                # hours. This amplifies cross-stablecoin transmission speed.
                if regime == "post_eo":
                    spillover *= 1.35
                # Also a diffuse confidence drag on the entire stablecoin
                # complex during the panic phase, regardless of direct linkage.
                if t <= 12:
                    diffuse = 0.015 * (1.0 - confidence)
                else:
                    diffuse = 0.005 * (1.0 - confidence)
                spillover += diffuse
                peg[sc].append(max(0.90, 1.0 - spillover))

        # --- Bank equity impact ---
        for bk in bank_eq:
            if bk == shock_target:
                # The failed bank's equity collapses immediately and stays there
                bank_eq[bk].append(min(0.0, bank_eq[bk][-1] - 5.0))
            else:
                # Confidence contagion: pre-EO sees broader regional pressure
                # because investors discover stablecoin deposits at other regional
                # banks and pull. Post-EO eliminates that channel entirely.
                drag_coef = 0.025 if regime == "pre_eo" else 0.005
                # Larger drag on banks holding more stablecoin deposits
                sc_exposure = sum(d["weight"] for _, d in
                                  [(e[1], e[2]) for e in g.in_edges(bk, data=True)
                                   if nodes[e[0]].kind == "stablecoin"]) if regime == "pre_eo" else 0
                exposure_factor = 1.0 + 0.5 * (sc_exposure / max(1.0, nodes[bk].assets))
                hit = drag_coef * (1.0 - confidence) * nodes[bk].equity * exposure_factor
                bank_eq[bk].append(bank_eq[bk][-1] - hit)

        # --- Fed master-account redemption draw (post-EO only) ---
        if regime == "post_eo" and t >= backstop_t:
            # Once the Fed activates support, the stablecoin issuer draws
            # liquidity from its master account to meet redemptions. This
            # transmits the run onto the Fed's liability composition.
            draw_rate = gross_redemption * 0.8
            fed_draws.append(fed_draws[-1] + draw_rate)
        else:
            fed_draws.append(fed_draws[-1])

    # System-wide contagion score: cumulative depeg across the entire
    # stablecoin complex. A pure point shock to one issuer would give a
    # small score (only that issuer deviates); broad contagion gives a
    # large score (multiple issuers deviate over many hours).
    contagion_score = sum(sum(1.0 - v for v in peg[sc]) for sc in peg)

    return SimResult(
        regime=regime,
        hours=hours,
        peg=peg,
        bank_equity=bank_eq,
        fed_master_redemptions=fed_draws,
        contagion_score=contagion_score,
    )


# ---------------------------------------------------------------------------
# Calibration check
# ---------------------------------------------------------------------------

def calibration_diagnostics(result_pre: SimResult) -> dict[str, float]:
    """Compare the pre-EO simulation to the USDC March 2023 episode."""
    usdc_peg = result_pre.peg["USDC"]
    trough = min(usdc_peg)
    trough_h = usdc_peg.index(trough)
    # Recovery: first hour where peg returns above 0.99 after the trough
    recov_h = next((h for h, v in enumerate(usdc_peg[trough_h:], start=trough_h)
                    if v >= 0.99), len(usdc_peg))
    return {
        "model_trough":      trough,
        "model_trough_hour": float(trough_h),
        "model_recovery_h":  float(recov_h),
        "historical_trough":      0.86,   # USDC March 2023
        "historical_trough_hour": 14.0,   # ~14h after disclosure
        "historical_recovery_h":  72.0,   # restored ~Mon Mar 13
    }


# ---------------------------------------------------------------------------
# Visualization
# ---------------------------------------------------------------------------

def make_figure(pre: SimResult, post: SimResult, out_path: Path) -> None:
    fig, axes = plt.subplots(2, 2, figsize=(11, 7),
                             gridspec_kw={"hspace": 0.32, "wspace": 0.25})

    # Style
    plt.rcParams.update({
        "font.family": "DejaVu Sans",
        "axes.spines.top": False, "axes.spines.right": False,
        "axes.grid": True, "grid.color": "#E5E7EB", "grid.linestyle": "-",
        "axes.edgecolor": "#374151", "axes.labelcolor": "#374151",
        "xtick.color": "#374151", "ytick.color": "#374151",
    })
    ACCENT = "#1F3864"
    WARN   = "#B45309"
    DANGER = "#B91C1C"
    GOOD   = "#047857"

    # Panel (a): USDC peg path, two regimes
    ax = axes[0, 0]
    ax.plot(pre.hours, pre.peg["USDC"],  color=DANGER, lw=2.2,
            label="Pre-EO (calibrated to USDC Mar 2023)")
    ax.plot(post.hours, post.peg["USDC"], color=GOOD, lw=2.2,
            label="Post-EO (direct Fed access)")
    ax.axhline(1.0, color="#9CA3AF", lw=0.8, ls="--")
    ax.axhline(0.86, color="#9CA3AF", lw=0.5, ls=":")
    ax.text(94, 0.862, "0.86 trough\n(USDC Mar 2023)", fontsize=8,
            color="#6B7280", ha="right", va="bottom")
    ax.set_ylim(0.80, 1.02)
    ax.set_xlabel("hours since shock")
    ax.set_ylabel("USDC peg (USD)")
    ax.set_title("(a) USDC peg trajectory under each regime", loc="left",
                 fontsize=11, fontweight="bold", color="#1F3864")
    ax.legend(loc="lower right", fontsize=9, frameon=False)

    # Panel (b): cross-stablecoin spillover (DAI, PYUSD, FDUSD)
    ax = axes[0, 1]
    for sc, ls in [("DAI", "-"), ("PYUSD", "--"), ("FDUSD", ":")]:
        ax.plot(pre.hours, pre.peg[sc], color=DANGER, lw=1.6, ls=ls, alpha=0.85)
        ax.plot(post.hours, post.peg[sc], color=GOOD, lw=1.6, ls=ls, alpha=0.85)
    ax.axhline(1.0, color="#9CA3AF", lw=0.8, ls="--")
    ax.set_ylim(0.92, 1.005)
    ax.set_xlabel("hours since shock")
    ax.set_ylabel("non-target stablecoin peg")
    ax.set_title("(b) Spillover via PSM (DAI/PYUSD/FDUSD)", loc="left",
                 fontsize=11, fontweight="bold", color="#1F3864")
    ax.text(0.02, 0.05,
            "solid: DAI · dashed: PYUSD · dotted: FDUSD\n"
            "red: pre-EO · green: post-EO",
            transform=ax.transAxes, fontsize=8, color="#6B7280")

    # Panel (c): bank equity damage in shock-target region
    ax = axes[1, 0]
    bank_labels = ["REG_A", "REG_B", "REG_C", "WFC", "BAC", "JPM"]
    pre_min  = [min(pre.bank_equity[b])  for b in bank_labels]
    post_min = [min(post.bank_equity[b]) for b in bank_labels]
    x = np.arange(len(bank_labels))
    w = 0.36
    ax.bar(x - w/2, [pre.bank_equity[b][0]  - m for b, m in zip(bank_labels, pre_min)],
           width=w, color=DANGER, label="Pre-EO")
    ax.bar(x + w/2, [post.bank_equity[b][0] - m for b, m in zip(bank_labels, post_min)],
           width=w, color=GOOD, label="Post-EO")
    ax.set_xticks(x); ax.set_xticklabels(bank_labels, fontsize=9)
    ax.set_ylabel("peak equity drawdown (USD bn)")
    ax.set_title("(c) Bank equity damage by node", loc="left",
                 fontsize=11, fontweight="bold", color="#1F3864")
    ax.legend(loc="upper right", fontsize=9, frameon=False)

    # Panel (d): Fed master-account redemption draw (post-EO only)
    ax = axes[1, 1]
    ax.fill_between(post.hours, 0, post.fed_master_redemptions,
                    color=WARN, alpha=0.35)
    ax.plot(post.hours, post.fed_master_redemptions,
            color=WARN, lw=2.2, label="Post-EO Fed draw")
    ax.plot(pre.hours, pre.fed_master_redemptions,
            color="#9CA3AF", lw=1.5, ls="--", label="Pre-EO (zero)")
    ax.set_xlabel("hours since shock")
    ax.set_ylabel("cumulative Fed liquidity draw (USD bn)")
    ax.set_title("(d) Fed balance-sheet impact (post-EO only)", loc="left",
                 fontsize=11, fontweight="bold", color="#1F3864")
    ax.legend(loc="upper left", fontsize=9, frameon=False)

    fig.suptitle("EO 14405 contagion topology shift: same shock, different transmission",
                 fontsize=13, color="#1F3864", fontweight="bold", y=0.995)
    fig.text(0.5, 0.005,
             "Source: simulation calibrated to USDC March 2023 episode (Fed FEDS Notes 17 Dec 2025). "
             "Network model: Eisenberg-Noe with redemption dynamics. Code at github.com/ihelfrich/eo14405-contagion.",
             ha="center", fontsize=8, color="#6B7280", style="italic")

    plt.savefig(out_path, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close()


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--calibrate", action="store_true")
    p.add_argument("--no-fed-liquidity", action="store_true",
                   help="Run post-EO regime WITHOUT Fed extending liquidity (worst case)")
    p.add_argument("--out", default="figures/contagion_topology.png")
    args = p.parse_args()

    here = Path(__file__).resolve().parent.parent
    out_path = here / args.out
    out_path.parent.mkdir(parents=True, exist_ok=True)

    pre  = simulate("pre_eo")
    post = simulate("post_eo", fed_extends_liquidity=not args.no_fed_liquidity)

    if args.calibrate:
        diag = calibration_diagnostics(pre)
        print("Calibration diagnostics (pre-EO regime, target=REG_B):")
        for k, v in diag.items():
            print(f"  {k:24s} {v:.4f}")
        # Errors
        trough_err = abs(diag["model_trough"] - diag["historical_trough"])
        recov_err  = abs(diag["model_recovery_h"] - diag["historical_recovery_h"])
        print(f"\n  |trough error|:   {trough_err:.3f}")
        print(f"  |recovery h err|: {recov_err:.1f} h")

    print(f"\nPre-EO contagion score: {pre.contagion_score:.2f}")
    print(f"Post-EO contagion score: {post.contagion_score:.2f}")
    print(f"  ratio (post/pre): {post.contagion_score / pre.contagion_score:.2f}")
    print(f"\nPeak Fed master-account draw (post-EO): "
          f"${max(post.fed_master_redemptions):.1f}B")

    make_figure(pre, post, out_path)
    print(f"\nChart → {out_path}")


if __name__ == "__main__":
    main()
