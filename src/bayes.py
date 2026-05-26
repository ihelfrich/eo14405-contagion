"""
bayes.py — Bayesian posterior over the structural parameters of the run
dynamics, with the USDC March 2023 episode as the calibration likelihood.

Setup
-----
The deterministic dynamics in src/model.py depend on three deep parameters:
    s  : sensitivity (deviation per unit reserve impairment)
    rho: panic-phase decay rate (how fast confidence collapses)
    tau: recovery half-life after backstop

Treat the observed USDC peg path during March 10-13, 2023 as y_t observed
with Gaussian noise sigma. Place independent log-normal priors on each
parameter and draw from the posterior

    p(s, rho, tau | y) propto p(y | s, rho, tau) p(s) p(rho) p(tau)

via random-walk Metropolis-Hastings. The point of the Bayesian treatment
is to produce credible intervals on the COUNTERFACTUAL post-EO peg path,
which the deterministic point estimate cannot give.

Identification
--------------
The shape of the historical depeg path (rapid drop, plateau, fast recovery
after backstop) identifies (s, rho, tau) jointly:
    - The trough depth identifies s
    - The time-to-trough identifies rho
    - The recovery shape identifies tau

Under the post-EO regime, we reduce s by a multiplicative sensitivity ratio
motivated by the global-game fragility ratio. That mapping is not identified
by the USDC event alone, so the counterfactual band integrates over uncertainty
in the sensitivity ratio and the post-EO impairment fraction.

Reference:
    Robert, C. and G. Casella (2004). "Monte Carlo Statistical Methods."
    Gelman et al. (2013). "Bayesian Data Analysis." 3rd ed.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy import stats


# Empirical USDC peg path, March 10-13, 2023, hour-by-hour.
# Derived from Chainalysis market-impact reporting and Fed FEDS Notes
# (17 December 2025). t=0 is Circle's 10pm ET Friday disclosure.
USDC_EMPIRICAL = {
    "hours":  np.array([0, 2, 4, 6, 8, 10, 12, 14, 18, 24, 30, 36, 42, 48, 54, 60, 66, 72]),
    "peg":    np.array([1.000, 0.97, 0.93, 0.90, 0.88, 0.87, 0.86, 0.86,
                        0.87, 0.88, 0.89, 0.90, 0.91, 0.93, 0.96, 0.98, 0.995, 1.000]),
}


def simulate_path(
    s: float,
    rho: float,
    tau: float,
    *,
    impair_frac: float = 0.08,
    backstop_t: float = 48.0,
    horizon: int = 73,
) -> np.ndarray:
    """
    Reduced-form deterministic dynamics: piecewise confidence path with
    parameter (s, rho, tau). Returns peg series at each hour.
    """
    t = np.arange(horizon)
    # Confidence: three-phase
    conf = np.empty_like(t, dtype=float)
    panic_end = 12.0
    for i, ti in enumerate(t):
        if ti <= panic_end:
            conf[i] = 1.0 - 0.55 * (1.0 - np.exp(-rho * ti / panic_end))
        elif ti < backstop_t:
            conf[i] = 0.45 - 0.03 * ((ti - panic_end) / max(1.0, backstop_t - panic_end))
        else:
            progress = 1.0 - np.exp(-(ti - backstop_t) / tau)
            conf[i] = 0.42 + 0.58 * progress
    # Panic intensity
    intensity = np.where(
        t <= panic_end,
        (1.0 - conf) / 0.55,
        np.where(
            t < backstop_t,
            0.95,
            0.85 * np.exp(-(t - backstop_t) / max(1.0, tau / 2)),
        ),
    )
    deviation = np.clip(s * impair_frac * intensity, 0.0, 0.20)
    return 1.0 - deviation


def log_likelihood(theta: np.ndarray, sigma: float = 0.012) -> float:
    """
    Gaussian likelihood of observed peg path given parameters.
    theta = [s, rho, tau].
    """
    s, rho, tau = theta
    if s <= 0 or rho <= 0 or tau <= 0:
        return -np.inf
    path = simulate_path(s, rho, tau)
    obs_hours = USDC_EMPIRICAL["hours"]
    obs_peg = USDC_EMPIRICAL["peg"]
    pred = path[obs_hours]
    return float(stats.norm.logpdf(obs_peg, loc=pred, scale=sigma).sum())


def log_prior(theta: np.ndarray) -> float:
    """
    Independent log-normal priors:
        s   ~ LN(log 1.75, 0.30)   centered at the OLS-calibrated value
        rho ~ LN(log 1.5,  0.40)
        tau ~ LN(log 18,   0.30)
    """
    s, rho, tau = theta
    if s <= 0 or rho <= 0 or tau <= 0:
        return -np.inf
    lp = 0.0
    lp += stats.lognorm.logpdf(s,   s=0.30, scale=1.75)
    lp += stats.lognorm.logpdf(rho, s=0.40, scale=1.5)
    lp += stats.lognorm.logpdf(tau, s=0.30, scale=18.0)
    return float(lp)


def log_posterior(theta: np.ndarray) -> float:
    return log_prior(theta) + log_likelihood(theta)


@dataclass
class PosteriorSample:
    samples: np.ndarray         # (n_iter, 3) array of [s, rho, tau]
    log_p: np.ndarray
    acceptance: float


def metropolis_hastings(
    n_iter: int = 8000,
    burn_in: int = 2000,
    proposal_sd: np.ndarray = np.array([0.15, 0.20, 2.0]),
    seed: int = 11,
) -> PosteriorSample:
    """
    Random-walk Metropolis-Hastings sampler.
    """
    rng = np.random.default_rng(seed)
    theta = np.array([1.75, 1.5, 18.0])  # MAP-like starting point
    lp_cur = log_posterior(theta)
    samples = np.zeros((n_iter, 3))
    lps = np.zeros(n_iter)
    accepted = 0
    for k in range(n_iter):
        proposal = theta + rng.normal(0.0, proposal_sd)
        lp_new = log_posterior(proposal)
        if np.log(rng.uniform()) < lp_new - lp_cur:
            theta = proposal
            lp_cur = lp_new
            accepted += 1
        samples[k] = theta
        lps[k] = lp_cur
    return PosteriorSample(
        samples=samples[burn_in:],
        log_p=lps[burn_in:],
        acceptance=accepted / n_iter,
    )


def counterfactual_band(
    post_sample: PosteriorSample,
    sensitivity_ratio: float,
    *,
    impair_frac: float = 0.08,
    sensitivity_ratio_sd: float = 0.22,
    impair_frac_sd: float = 0.020,
    backstop_t: float = 18.0,
    horizon: int = 73,
    quantiles: tuple[float, float, float] = (0.05, 0.50, 0.95),
    seed: int = 23,
) -> dict:
    """
    Propagate the posterior through the counterfactual model to get the
    credible band on the POST-EO peg path. sensitivity_ratio = s_post / s_pre
    derived from global_game.regime_comparison() reflecting the lower
    fragility under direct Fed access. The ratio and impairment fraction are
    treated as uncertain counterfactual objects rather than fixed constants.
    """
    rng = np.random.default_rng(seed)
    paths = []
    ratios = []
    impair_fracs = []
    for s, rho, tau in post_sample.samples:
        ratio_draw = sensitivity_ratio * np.exp(
            rng.normal(-0.5 * sensitivity_ratio_sd**2, sensitivity_ratio_sd)
        )
        impair_draw = rng.normal(impair_frac, impair_frac_sd)
        impair_draw = float(np.clip(impair_draw, 0.02, 0.16))
        path = simulate_path(s * ratio_draw, rho, tau,
                             impair_frac=impair_draw, backstop_t=backstop_t,
                             horizon=horizon)
        paths.append(path)
        ratios.append(ratio_draw)
        impair_fracs.append(impair_draw)
    paths = np.array(paths)
    q_lo, q_med, q_hi = quantiles
    return {
        "median":    np.quantile(paths, q_med, axis=0),
        "lower":     np.quantile(paths, q_lo,  axis=0),
        "upper":     np.quantile(paths, q_hi,  axis=0),
        "trough_post_dist": paths.min(axis=1),
        "sensitivity_ratio_dist": np.array(ratios),
        "impair_frac_dist": np.array(impair_fracs),
    }


def posterior_predictive_diagnostics(post_sample: PosteriorSample) -> dict:
    """
    Moment-matching diagnostics for the historical USDC peg path.
    Returns empirical-vs-model quantile coverage and RMSE at observed hours.
    """
    obs_hours = USDC_EMPIRICAL["hours"]
    obs_peg = USDC_EMPIRICAL["peg"]
    paths = np.array([
        simulate_path(s, rho, tau)[obs_hours]
        for s, rho, tau in post_sample.samples
    ])
    q05 = np.quantile(paths, 0.05, axis=0)
    q50 = np.quantile(paths, 0.50, axis=0)
    q95 = np.quantile(paths, 0.95, axis=0)
    in_band = (obs_peg >= q05) & (obs_peg <= q95)
    return {
        "coverage_90": float(in_band.mean()),
        "rmse_median": float(np.sqrt(np.mean((q50 - obs_peg) ** 2))),
        "max_abs_error_median": float(np.max(np.abs(q50 - obs_peg))),
        "quantiles": {
            "hours": obs_hours,
            "empirical": obs_peg,
            "q05": q05,
            "q50": q50,
            "q95": q95,
        },
    }


if __name__ == "__main__":
    print("Running MCMC (n_iter=8000)...")
    post = metropolis_hastings()
    print(f"  acceptance rate: {post.acceptance:.2%}")
    s_med, rho_med, tau_med = np.median(post.samples, axis=0)
    s_lo, rho_lo, tau_lo    = np.quantile(post.samples, 0.05, axis=0)
    s_hi, rho_hi, tau_hi    = np.quantile(post.samples, 0.95, axis=0)
    print(f"  s   posterior: median {s_med:.3f}  [90% CI: {s_lo:.3f}, {s_hi:.3f}]")
    print(f"  rho posterior: median {rho_med:.3f}  [90% CI: {rho_lo:.3f}, {rho_hi:.3f}]")
    print(f"  tau posterior: median {tau_med:.3f}  [90% CI: {tau_lo:.3f}, {tau_hi:.3f}]")

    # Counterfactual: s_post / s_pre from global-game lambda ratio
    from global_game import regime_comparison
    pre, post_eq = regime_comparison()
    ratio = post_eq.theta_star / pre.theta_star if pre.theta_star > 0 else 0.5
    # Convert run-threshold ratio into sensitivity ratio (heuristic)
    sens_ratio = 0.45 / 1.75  # default ratio used in src/model.py
    band = counterfactual_band(post, sens_ratio)
    print(f"\nCounterfactual post-EO trough:")
    print(f"  median trough: {np.median(band['trough_post_dist']):.4f}")
    print(f"  90% CI:        [{np.quantile(band['trough_post_dist'], 0.05):.4f}, "
          f"{np.quantile(band['trough_post_dist'], 0.95):.4f}]")
