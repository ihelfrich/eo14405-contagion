"""
welfare.py — explicit social welfare comparison across regimes.

Setup
-----
Three classes of agent:
    H : stablecoin holders (mass = total circulating supply)
    B : commercial banks (mass = banking sector by aggregate equity)
    T : taxpayers / Fed-balance-sheet residual claimants

Per-period flow utility under a stress event:
    U_H = - L_H (peg loss + redemption-delay cost)
    U_B = - L_B (deposit-franchise impairment from stablecoin outflow)
    U_T = - L_T (expected fiscal cost of Fed liquidity extension)

Aggregate welfare with Negishi-Pareto weights (omega_H, omega_B, omega_T)
that sum to 1:
    W = - (omega_H L_H + omega_B L_B + omega_T L_T)

The regime change EO 14405 shifts loss MASS across the three classes
without necessarily changing total system loss. Whether it is welfare-
improving depends on the weights AND on the loss-shift magnitudes.

Welfare proposition (Proposition 2 of the paper)
------------------------------------------------
Define Delta_L_X = L_X^{post} - L_X^{pre} for X in {H, B, T}.
The EO is welfare-improving iff

    omega_H Delta_L_H + omega_B Delta_L_B + omega_T Delta_L_T < 0.

We compute Delta_L_X from the simulation outputs and characterize the
welfare-neutral surface in (omega_H, omega_B, omega_T) space.

Reference:
    Negishi, T. (1960). "Welfare Economics and Existence of an Equilibrium
        for a Competitive Economy." Metroeconomica 12: 92-97.
    Diamond, D. and P. Dybvig (1983). "Bank Runs, Deposit Insurance, and
        Liquidity." JPE 91(3): 401-419.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass
class LossVector:
    holders:    float   # USD bn equivalent
    banks:      float
    taxpayers:  float   # = expected fiscal cost of Fed liquidity extension


@dataclass
class WelfareReport:
    pre:  LossVector
    post: LossVector
    delta: LossVector
    indifferent_weights: tuple[float, float, float]
    improvement_under_equal_weights: bool


def losses_from_simulation(
    peg_path: list[float],
    bank_equity_drawdown: float,
    fed_draw: float,
    stablecoin_size_bn: float,
    *,
    fed_liquidity_subsidy_rate: float = 0.003,
) -> LossVector:
    """
    Convert simulation outputs into welfare losses in $bn.

    holder loss = sum_t (1 - peg_t) * size  (integrated peg deviation)
    bank loss   = bank_equity_drawdown      (direct equity impairment)
    taxpayer    = fed_draw * subsidy_rate   (expected fiscal cost of
                                              implicit Fed support, where
                                              subsidy_rate captures the
                                              gap between the lending rate
                                              and the risk-fair rate)

    The subsidy_rate of 30 bp is the order-of-magnitude calibration from
    BTFP usage (March 2023 - March 2024), where the program lent below the
    risk-fair rate to depository institutions.
    """
    # Integrated peg deviation, in $bn-hours, normalized to $bn by dividing
    # by 24 (one day's worth)
    holder_loss = (sum(1.0 - p for p in peg_path) / 24.0) * stablecoin_size_bn
    return LossVector(
        holders=holder_loss,
        banks=bank_equity_drawdown,
        taxpayers=fed_draw * fed_liquidity_subsidy_rate,
    )


def compute_welfare(pre: LossVector, post: LossVector) -> WelfareReport:
    delta = LossVector(
        holders   = post.holders   - pre.holders,
        banks     = post.banks     - pre.banks,
        taxpayers = post.taxpayers - pre.taxpayers,
    )
    # Indifference-surface direction: the unit-norm weight vector w
    # orthogonal to (Delta_H, Delta_B, Delta_T) such that w . Delta = 0
    # AND w sums to 1 in the simplex. We pick the boundary intersection
    # by symmetric projection.
    d = np.array([delta.holders, delta.banks, delta.taxpayers])
    # Find weights on the simplex that make w . d = 0 if possible;
    # otherwise return the closest feasible weights.
    n = np.linalg.norm(d)
    if n > 0:
        # Project the centroid (1/3, 1/3, 1/3) onto the hyperplane w.d = 0
        centroid = np.array([1/3, 1/3, 1/3])
        proj = centroid - (centroid @ d) / (d @ d) * d
        # Clip to simplex
        proj = np.clip(proj, 0.0, 1.0)
        if proj.sum() > 0:
            proj /= proj.sum()
        indiff = tuple(proj.tolist())
    else:
        indiff = (1/3, 1/3, 1/3)

    # Equal-weight verdict
    equal_w = np.array([1/3, 1/3, 1/3])
    welfare_change_equal = -float(equal_w @ d)
    improvement_equal = welfare_change_equal > 0

    return WelfareReport(
        pre=pre,
        post=post,
        delta=delta,
        indifferent_weights=indiff,
        improvement_under_equal_weights=improvement_equal,
    )


def proposition_2_verdict(report: WelfareReport) -> str:
    d = report.delta
    sign = lambda x: "+" if x >= 0 else "-"
    msg = (
        f"Pre-EO  losses: holders ${report.pre.holders:.2f}B, "
        f"banks ${report.pre.banks:.2f}B, taxpayers ${report.pre.taxpayers:.2f}B\n"
        f"Post-EO losses: holders ${report.post.holders:.2f}B, "
        f"banks ${report.post.banks:.2f}B, taxpayers ${report.post.taxpayers:.2f}B\n"
        f"Delta L:        H {sign(d.holders)}${abs(d.holders):.2f}B, "
        f"B {sign(d.banks)}${abs(d.banks):.2f}B, "
        f"T {sign(d.taxpayers)}${abs(d.taxpayers):.2f}B\n"
    )
    if report.improvement_under_equal_weights:
        msg += "Equal-weight verdict: EO is welfare-IMPROVING.\n"
    else:
        msg += "Equal-weight verdict: EO is welfare-DEGRADING.\n"
    msg += (
        f"Indifference weights (omega_H, omega_B, omega_T) on the "
        f"closest simplex point: ({report.indifferent_weights[0]:.3f}, "
        f"{report.indifferent_weights[1]:.3f}, "
        f"{report.indifferent_weights[2]:.3f})"
    )
    return msg


if __name__ == "__main__":
    # Demo using stylized numbers
    pre  = LossVector(holders=12.0, banks=52.0, taxpayers=0.0)
    post = LossVector(holders=0.5,  banks=13.0, taxpayers=4.0)
    rep = compute_welfare(pre, post)
    print(proposition_2_verdict(rep))
