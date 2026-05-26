"""
global_game.py — Morris-Shin (1998, 2003) coordination-game equilibrium
for stablecoin runs.

Setup
-----
A continuum of holders of mass 1 each decide whether to redeem (action 1)
or roll over (action 0). The stablecoin's fundamental state is theta ~ N(y, sigma_theta^2)
where y is a public signal (e.g., a published reserve attestation). Each
holder i observes a private signal x_i = theta + epsilon_i, epsilon_i ~ N(0, sigma_x^2).

Payoffs (per holder):
    redeem:     1  if theta >= ell (issuer can meet redemption)
                0  otherwise
    rollover:   r  unconditional yield (e.g., IORB if direct Fed access)

The aggregate proportion of redeemers is l(theta) = Pr(x_i < x_star | theta).
The issuer can meet redemptions iff theta >= ell + lambda * l(theta), where
lambda parameterizes the issuer's funding fragility. ell is the bare
solvency threshold and the lambda * l term captures the run-amplified
liquidity demand.

Equilibrium
-----------
Under sigma_x -> 0 limit (high signal precision, Morris-Shin 2003 Cor. 1),
the unique threshold-strategy equilibrium has cutoff signal x_star such
that the marginal holder is indifferent:

    Pr(theta >= theta_star | x_i = x_star) = r

where the run threshold theta_star satisfies the consistency condition

    theta_star = ell + lambda * Phi( -(x_star - theta_star)/sigma_x ).

In the high-precision limit and with diffuse public prior, the closed-form
threshold is

    theta_star = ell + lambda * Phi^{-1}( 1 - r ).      (*)

EO 14405 enters via two channels:
    1. The yield r changes: post-EO holders earn IORB directly via the
       master account, raising r by ~30bp at current rates.
    2. The fragility lambda shrinks: with Fed direct access, the issuer's
       liquidity need per unit of redemption falls because reserves are
       T+0 settleable rather than commercial-deposit T+1.

We solve (*) numerically; the analytical solution is the closed form above.
We also compute the comparative-statics derivatives d theta_star / d r and
d theta_star / d lambda which give the local elasticity of the run
threshold to each policy lever.

Reference:
    Morris, S. and H. S. Shin (1998). "Unique Equilibrium in a Model of
        Self-Fulfilling Currency Attacks." AER 88(3): 587-597.
    Morris, S. and H. S. Shin (2003). "Global Games: Theory and
        Applications." in Advances in Economics and Econometrics, ed.
        Dewatripont, Hansen, Turnovsky.
    Rochet, J.-C. and X. Vives (2004). "Coordination Failures and the
        Lender of Last Resort." JEEA 2: 1116-1147.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.stats import norm


@dataclass
class RunEquilibrium:
    theta_star: float           # run threshold on fundamental
    x_star: float               # cutoff signal
    p_run: float                # ex-ante probability of run given public prior
    elasticity_r: float         # d theta_star / d r
    elasticity_lambda: float    # d theta_star / d lambda
    regime: str


def equilibrium(
    ell: float,
    lam: float,
    r: float,
    *,
    y_prior: float | None = None,
    sigma_theta: float = 1.0,
    regime: str = "",
) -> RunEquilibrium:
    """
    Compute the unique threshold-strategy equilibrium.

    Parameters
    ----------
    ell        : bare solvency threshold (fundamental value below which the
                 issuer is technically insolvent even with no run).
    lam        : run-fragility parameter. lambda*l(theta) is the extra
                 liquidity drawn by a run of proportion l.
    r          : opportunity cost of redemption (yield on holding).
                 Post-EO this rises because IORB > commercial deposit rate.
    y_prior    : public-prior mean for fundamental. Default ell + lam/2.
    sigma_theta: prior std-dev of fundamental.

    Returns
    -------
    RunEquilibrium with theta_star and run probability.
    """
    if y_prior is None:
        y_prior = ell + lam / 2.0
    # High-precision-limit closed form
    theta_star = ell + lam * norm.ppf(1.0 - r)
    # Run probability under public prior
    p_run = norm.cdf((theta_star - y_prior) / sigma_theta)
    # Comparative statics
    # d theta_star / d r = -lam * phi(Phi^{-1}(1-r))^{-1}     (chain rule on ppf)
    z = norm.ppf(1.0 - r)
    elasticity_r = -lam / norm.pdf(z) if norm.pdf(z) > 1e-12 else -np.inf
    elasticity_lambda = z
    return RunEquilibrium(
        theta_star=theta_star,
        x_star=theta_star,  # in high-precision limit
        p_run=p_run,
        elasticity_r=elasticity_r,
        elasticity_lambda=elasticity_lambda,
        regime=regime,
    )


def regime_comparison(
    *,
    ell: float = 0.92,           # 8% reserve-impairment threshold (USDC 2023 analog)
    lam_pre: float = 0.40,        # commercial-bank rails fragility
    lam_post: float = 0.15,       # Fed master account, T+0 settlement
    r_pre: float = 0.005,         # 50 bp deposit-equivalent yield
    r_post: float = 0.045,        # 4.5% IORB
    sigma_theta: float = 0.05,
) -> tuple[RunEquilibrium, RunEquilibrium]:
    """
    Solve the run equilibrium under both regimes with policy-relevant
    calibration. Defaults reflect 2026 conditions: pre-EO holders earn
    near-zero deposit yields and face commercial-bank intermediation
    fragility; post-EO holders earn IORB and face Fed-direct fragility.
    """
    pre = equilibrium(ell, lam_pre, r_pre,
                      sigma_theta=sigma_theta, regime="pre_eo")
    post = equilibrium(ell, lam_post, r_post,
                       sigma_theta=sigma_theta, regime="post_eo")
    return pre, post


def proposition_1_check(pre: RunEquilibrium, post: RunEquilibrium) -> dict:
    """
    Proposition 1 (text Eq. 3): theta_star_post < theta_star_pre is necessary
    and sufficient for EO 14405 to be locally Pareto-improving on financial
    stability. Returns the gap and which direction.
    """
    delta = post.theta_star - pre.theta_star
    return {
        "theta_star_pre": pre.theta_star,
        "theta_star_post": post.theta_star,
        "delta": delta,
        "stability_improved": delta < 0,   # lower threshold = run less likely
        "delta_run_prob": post.p_run - pre.p_run,
    }


if __name__ == "__main__":
    pre, post = regime_comparison()
    print(f"PRE-EO:  theta* = {pre.theta_star:.4f}   P(run) = {pre.p_run:.4f}")
    print(f"POST-EO: theta* = {post.theta_star:.4f}   P(run) = {post.p_run:.4f}")
    print(f"\nElasticity dtheta*/dr      (pre): {pre.elasticity_r:+.3f}")
    print(f"Elasticity dtheta*/dlambda (pre): {pre.elasticity_lambda:+.3f}")
    check = proposition_1_check(pre, post)
    print(f"\nProposition 1 verdict: stability improved = {check['stability_improved']}")
    print(f"  Delta theta*     = {check['delta']:+.4f}")
    print(f"  Delta P(run)     = {check['delta_run_prob']:+.4f}")
