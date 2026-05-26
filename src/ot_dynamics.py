"""
ot_dynamics.py — optimal-transport formulation of stablecoin run dynamics.

Setup
-----
Let mu_0 in P(X) be the pre-shock distribution of holder claims across
"states" X = {USDT, USDC, DAI, PYUSD, FDUSD, fiat, T-bills, USD reserves}.
A run is a transformation mu_0 -> mu_1 driven by perceived risk shifts.

The cost of a holder moving claim mass from state i to state j is c_ij,
a regime-specific friction matrix. Pre-EO, moving USDC -> fiat at a
commercial bank costs ~50 bp (gate latency, redemption queue, secondary-
market spread). Post-EO, the same move via Fed master account costs ~5 bp.

The minimum-cost reallocation under a redemption shock is the solution
of the Monge-Kantorovich problem

    W_c(mu_0, mu_1) = min_{gamma in Pi(mu_0, mu_1)} sum_{i,j} c_ij gamma_ij

with gamma row/column-summing to mu_0, mu_1. We solve via Sinkhorn for
speed (Cuturi 2013) with epsilon = 0.01 entropic regularization, or via
exact LP for the small instances here.

Run severity metric
-------------------
We define the run severity at time t under regime R as

    S^R(t) = W_{c^R}(mu_0, mu_t^R)

so the trajectory t -> S^R(t) is a regime-specific run path expressed
in units of "total holder-frictional cost." A useful summary is the
integrated path Int_0^T S^R(t) dt, which we report.

This connects the discrete network model to a continuous Wasserstein
metric on holder distributions and makes "run severity" a quantity with
well-defined units (dollars of frictional cost).

Reference:
    Villani, C. (2008). "Optimal Transport: Old and New."
    Cuturi, M. (2013). "Sinkhorn Distances: Lightspeed Computation of
        Optimal Transport." NeurIPS.
    Peyre and Cuturi (2019). "Computational Optimal Transport." FnT.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import ot

STATES = ["USDT", "USDC", "DAI", "PYUSD", "FDUSD",
          "fiat_USD", "Tbills", "Fed_reserves"]
N = len(STATES)


def cost_matrix(regime: str) -> np.ndarray:
    """
    Construct the cost matrix c_ij of transitioning a unit of claim mass.
    Diagonal is zero (no move). Off-diagonal entries are basis points of
    frictional cost, calibrated to:
      - Stablecoin <-> stablecoin: ~10-50 bp (PSM/swap spread)
      - Stablecoin -> fiat: pre-EO 50 bp gate + spread, post-EO 5 bp
      - Stablecoin -> Tbills: pre-EO 20 bp (MMF entry), post-EO 5 bp
      - Stablecoin -> Fed reserves: pre-EO infeasible (set high), post-EO 1 bp
      - fiat -> Fed reserves: pre-EO bank settlement T+1, post-EO real-time
    Costs are in BPS of moved mass.
    """
    c = np.full((N, N), 50.0)
    np.fill_diagonal(c, 0.0)
    # Inter-stablecoin moves (DEX swap / PSM)
    stablecoin_idx = [STATES.index(s) for s in ("USDT", "USDC", "DAI", "PYUSD", "FDUSD")]
    for i in stablecoin_idx:
        for j in stablecoin_idx:
            if i != j:
                c[i, j] = 15.0
    fiat = STATES.index("fiat_USD")
    tbill = STATES.index("Tbills")
    reserves = STATES.index("Fed_reserves")
    if regime == "pre_eo":
        # Stablecoin -> fiat: 50 bp gate + spread
        for i in stablecoin_idx:
            c[i, fiat] = 50.0
            c[fiat, i] = 50.0
            c[i, tbill] = 20.0
            c[tbill, i] = 20.0
            c[i, reserves] = 1e6           # infeasible (no direct access)
            c[reserves, i] = 1e6
        c[fiat, reserves] = 30.0           # bank settlement to Fed
        c[reserves, fiat] = 30.0
    elif regime == "post_eo":
        for i in stablecoin_idx:
            c[i, fiat] = 5.0
            c[fiat, i] = 5.0
            c[i, tbill] = 5.0
            c[tbill, i] = 5.0
            c[i, reserves] = 1.0           # direct master account access
            c[reserves, i] = 1.0
        c[fiat, reserves] = 5.0
        c[reserves, fiat] = 5.0
    else:
        raise ValueError(f"unknown regime: {regime}")
    return c


def baseline_distribution() -> np.ndarray:
    """
    Pre-shock holder distribution, calibrated to approximate 2026 market
    weights of mass across the 8 states. Stablecoin shares mirror current
    circulating supply; fiat / Tbills / reserves represent the broader
    USD claim universe at scaled proportions for analytic clarity.
    """
    # Approximate 2026 weights (in mass units, sum to 1.0)
    mu = np.array([
        0.30,   # USDT
        0.10,   # USDC
        0.012,  # DAI
        0.004,  # PYUSD
        0.008,  # FDUSD
        0.18,   # fiat USD (operational balances)
        0.30,   # Tbills (held via MMFs etc)
        0.086,  # Fed reserves
    ])
    return mu / mu.sum()


def shock_distribution(
    target: str,
    severity: float,
    regime: str,
) -> np.ndarray:
    """
    Post-shock distribution: mass migrates AWAY from `target` (e.g., "USDC"
    if Circle's reserves are partially impaired) toward safer states.
    The redistribution favors fiat under pre-EO, Fed reserves under post-EO.
    """
    mu = baseline_distribution()
    mu1 = mu.copy()
    t_idx = STATES.index(target)
    moved = mu[t_idx] * severity
    mu1[t_idx] -= moved
    # Direction of flight depends on regime
    if regime == "pre_eo":
        # In pre-EO, holders fly to fiat (and slightly to T-bills via MMFs).
        mu1[STATES.index("fiat_USD")] += moved * 0.70
        mu1[STATES.index("Tbills")]   += moved * 0.20
        mu1[STATES.index("USDT")]     += moved * 0.10  # cross-stablecoin
    else:
        # In post-EO, the operational similarity of direct-Fed-access
        # stablecoins makes substitution faster; some flight to Fed
        # reserves through the master account.
        mu1[STATES.index("USDT")]        += moved * 0.40  # cross-substitution
        mu1[STATES.index("Fed_reserves")] += moved * 0.40
        mu1[STATES.index("fiat_USD")]    += moved * 0.15
        mu1[STATES.index("Tbills")]      += moved * 0.05
    return mu1


@dataclass
class OTResult:
    regime: str
    target: str
    severity: float
    W1: float                          # Wasserstein-1 distance
    transport_plan: np.ndarray         # optimal gamma
    cost_matrix: np.ndarray


def severity_metric(
    target: str = "USDC",
    severity: float = 0.20,
    regime: str = "pre_eo",
    *,
    epsilon: float = 0.0,
) -> OTResult:
    """
    Compute Wasserstein-1 distance between the baseline holder distribution
    and the post-shock distribution under a given regime. epsilon > 0 uses
    Sinkhorn entropic regularization; epsilon = 0 uses exact LP via
    ot.emd (network simplex).
    """
    mu = baseline_distribution()
    nu = shock_distribution(target, severity, regime)
    # Numerical mass balance
    nu = nu * (mu.sum() / nu.sum())
    c = cost_matrix(regime)
    if epsilon > 0:
        gamma = ot.sinkhorn(mu, nu, c, reg=epsilon)
    else:
        gamma = ot.emd(mu, nu, c)
    w1 = float((gamma * c).sum())
    return OTResult(
        regime=regime,
        target=target,
        severity=severity,
        W1=w1,
        transport_plan=gamma,
        cost_matrix=c,
    )


def severity_trajectory(
    target: str = "USDC",
    regime: str = "pre_eo",
    severities: np.ndarray | None = None,
) -> tuple[np.ndarray, np.ndarray]:
    """
    Return (severities, W1_path) so one can plot W1 as a function of
    shock magnitude. The shape of this curve characterizes regime-
    specific robustness: a steeper curve is more fragile.
    """
    if severities is None:
        severities = np.linspace(0.0, 0.50, 51)
    w = np.array([severity_metric(target, s, regime).W1 for s in severities])
    return severities, w


def topology_distance(regime_a: str, regime_b: str) -> float:
    """
    Wasserstein distance between the COST MATRICES themselves (Frobenius
    norm of c_a - c_b, treating each entry as a transport-cost coordinate).
    Quantifies how different the regime topologies are; pre-EO vs post-EO
    differ most strongly in the stablecoin <-> Fed-reserves entries.
    """
    ca = cost_matrix(regime_a)
    cb = cost_matrix(regime_b)
    # Clip the infeasibility-sentinel so it doesn't dominate
    ca = np.clip(ca, 0, 100)
    cb = np.clip(cb, 0, 100)
    return float(np.linalg.norm(ca - cb))


if __name__ == "__main__":
    pre  = severity_metric("USDC", 0.20, "pre_eo")
    post = severity_metric("USDC", 0.20, "post_eo")
    print(f"PRE-EO  W1 = {pre.W1:.3f}  bp-mass")
    print(f"POST-EO W1 = {post.W1:.3f}  bp-mass")
    print(f"Ratio (post/pre) = {post.W1/pre.W1:.3f}")
    print(f"Topology distance |c_pre - c_post|_F = {topology_distance('pre_eo','post_eo'):.2f}")
