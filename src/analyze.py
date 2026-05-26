"""
analyze.py — orchestrator that composes the six analytical layers and
produces the full set of tables and figures referenced in paper.md.

Run order:
  1. Build the stylized 13-node financial network for each regime.
  2. Compute Eisenberg-Noe clearing under the SVB-class bank shock.
  3. Solve the global-game run threshold for each regime.
  4. Compute Wasserstein run severity W_1(mu_0, mu_1) for each regime.
  5. Spectral analysis: lambda_max, Katz centrality, super-spreaders.
  6. Posterior credible bands on counterfactual peg via MCMC.
  7. Welfare comparison with explicit SWF.
  8. Render a 9-panel publication figure.
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, str(Path(__file__).parent))

from bayes import (USDC_EMPIRICAL, counterfactual_band, metropolis_hastings,
                   posterior_predictive_diagnostics)
from clearing import stress_clear, cascade_depth
from global_game import proposition_1_check, regime_comparison
from model import build_network, simulate
from ot_dynamics import severity_metric, severity_trajectory, topology_distance
from spectral import spectral_report_from_matrix
from welfare import (compute_welfare, losses_from_simulation,
                     proposition_2_verdict)


ASSET_EDGE_KINDS = {
    "deposit", "tbill", "master_account", "rrp", "cp", "custody", "psm",
}

SPECTRAL_TRANSMISSIBILITY = {
    "deposit": 0.85,
    "tbill": 0.01,
    "master_account": 0.00,
    "rrp": 0.00,
    "cp": 0.05,
    "custody": 0.03,
    "psm": 0.25,
}


def _absorptive_capacity(nodes: dict, nm: str, *, purpose: str) -> float:
    node = nodes[nm]
    if node.kind == "fed":
        return 1e9
    if purpose == "spectral" and node.kind == "stablecoin":
        # For local run-feedback analysis the relevant buffer is the stock of
        # immediately pledgeable liquid reserves, not only accounting equity.
        return max(node.assets * 0.25, node.cash_buffer)
    if purpose == "spectral" and node.kind == "mmf":
        return node.assets * 0.05
    return node.equity + node.cash_buffer


def build_LK(
    regime: str,
    *,
    exclude_fed: bool = False,
    purpose: str = "clearing",
) -> tuple[np.ndarray, np.ndarray, list[str]]:
    """Convert reserve-placement graph edges into a liability matrix.

    The graph in model.py stores asset placement edges as asset owner ->
    counterparty. Eisenberg-Noe needs the opposite convention: L[i,j] is what
    node i owes node j. Thus a stablecoin deposit at REG_B is a REG_B liability
    to the stablecoin issuer, not a stablecoin liability to REG_B.
    """
    g, nodes = build_network(regime)
    names = list(nodes.keys())
    if exclude_fed:
        names = [n for n in names if nodes[n].kind != "fed"]
    n = len(names)
    idx = {nm: i for i, nm in enumerate(names)}
    L = np.zeros((n, n))
    for u, v, data in g.edges(data=True):
        if u in idx and v in idx:
            if data.get("kind") in ASSET_EDGE_KINDS:
                L[idx[v], idx[u]] += data["weight"]
            else:
                L[idx[u], idx[v]] += data["weight"]
    if purpose == "clearing":
        # In Eisenberg-Noe, e_i is external asset value available to meet the
        # modeled network obligations. Since the graph contains only a subset
        # of each institution's balance sheet, a solvent unshocked node should
        # be able to pay those modeled obligations in full.
        bar_p = L.sum(axis=1)
        e = np.array([nodes[nm].equity for nm in names]) + bar_p
        e = np.where(np.isfinite(e), e, 1e9)
        return L, e, names
    k = np.array([_absorptive_capacity(nodes, nm, purpose=purpose) for nm in names])
    return L, k, names


def spectral_feedback_matrix(regime: str) -> tuple[np.ndarray, list[str]]:
    """Effective loss-feedback matrix for spectral contagion.

    Nominal claims are first converted into expected loss-transmission weights
    using stress transmissibility coefficients, then symmetrized to capture
    funding feedback. This avoids the nilpotent-DAG artifact in the raw
    one-way reserve-placement graph.
    """
    g, nodes = build_network(regime)
    names = [n for n in nodes if nodes[n].kind not in {"fed", "mmf"}]
    idx = {nm: i for i, nm in enumerate(names)}
    E = np.zeros((len(names), len(names)))
    for u, v, data in g.edges(data=True):
        if u not in idx or v not in idx:
            continue
        tau = SPECTRAL_TRANSMISSIBILITY.get(data.get("kind"), 0.0)
        w = data["weight"] * tau
        E[idx[u], idx[v]] += w
        E[idx[v], idx[u]] += w
    k = np.array([_absorptive_capacity(nodes, nm, purpose="spectral") for nm in names])
    B = E / np.where(k > 0, k, 1.0)[:, None]
    return B, names


def creditor_losses_by_kind(L: np.ndarray, result, names: list[str], kinds: set[str]) -> float:
    _, nodes = build_network("pre_eo")
    bar_p = result.bar_p
    out = 0.0
    for i in range(len(names)):
        if result.losses[i] <= 0 or bar_p[i] <= 0:
            continue
        creditor_shares = L[i] / bar_p[i]
        for j, share in enumerate(creditor_shares):
            if share > 0 and nodes[names[j]].kind in kinds:
                out += result.losses[i] * share
    return float(out)


def placebo_mmf_shock() -> dict:
    L_pre, k_pre, names = build_LK("pre_eo")
    L_post, k_post, _ = build_LK("post_eo")
    mmf_idx = names.index("MMF_PRIME")
    pre = stress_clear(L_pre, k_pre, mmf_idx, shock_amount=60.0)
    post = stress_clear(L_post, k_post, mmf_idx, shock_amount=60.0)
    return {
        "pre_amplification": pre.amplification,
        "post_amplification": post.amplification,
        "delta_amplification": post.amplification - pre.amplification,
        "pre_defaults": int(pre.defaulted.sum()),
        "post_defaults": int(post.defaulted.sum()),
    }


def topology_robustness(seed: int = 41) -> list[dict]:
    rng = np.random.default_rng(seed)
    out = []
    for topology in ("erdos_renyi", "core_periphery", "scale_free"):
        n_banks, n_stables = 18, 5
        bank_k = rng.lognormal(mean=np.log(45), sigma=0.55, size=n_banks)
        stable_assets = np.array([140.0, 42.0, 5.0, 1.5, 3.0])
        stable_k = stable_assets * 0.25
        k = np.concatenate([bank_k, stable_k])
        B_pre = np.zeros((n_banks + n_stables, n_banks + n_stables))
        B_post = np.zeros_like(B_pre)

        for s_idx, assets in enumerate(stable_assets):
            sc = n_banks + s_idx
            if topology == "erdos_renyi":
                mask = rng.uniform(size=n_banks) < 0.28
                weights = rng.uniform(0.5, 1.5, size=n_banks) * mask
            elif topology == "core_periphery":
                weights = np.r_[rng.uniform(2.0, 4.0, 4),
                                rng.uniform(0.0, 0.5, n_banks - 4)]
            else:
                weights = rng.pareto(1.8, size=n_banks) + 0.1
            if weights.sum() == 0:
                weights[rng.integers(0, n_banks)] = 1.0
            weights = weights / weights.sum()
            pre_exposure = assets * 0.80 * weights * SPECTRAL_TRANSMISSIBILITY["deposit"]
            post_exposure = np.zeros(n_banks)
            post_exposure[0] = assets * 0.10 * SPECTRAL_TRANSMISSIBILITY["deposit"]
            for b in range(n_banks):
                for B, exposure in ((B_pre, pre_exposure[b]), (B_post, post_exposure[b])):
                    B[sc, b] += exposure / k[sc]
                    B[b, sc] += exposure / k[b]
        lam_pre = max(abs(np.linalg.eigvals(B_pre)))
        lam_post = max(abs(np.linalg.eigvals(B_post)))
        out.append({
            "topology": topology,
            "lambda_pre": float(lam_pre),
            "lambda_post": float(lam_post),
            "reduction_pct": float(100 * (1 - lam_post / lam_pre)),
        })
    return out


def run_all() -> dict:
    print("=" * 72)
    print("EO 14405 contagion analysis — full multi-layer evaluation")
    print("=" * 72)

    results: dict = {}

    # --- Build the networks ---
    L_pre,  k_pre,  names = build_LK("pre_eo", purpose="clearing")
    L_post, k_post, _     = build_LK("post_eo", purpose="clearing")
    results["names"] = names

    # --- Layer 1: Eisenberg-Noe clearing under SVB-class shock ---
    print("\n[1] Eisenberg-Noe clearing vector")
    print("-" * 72)
    reg_b_idx = names.index("REG_B")
    # SVB-class shock: wipe ~$60B of bank assets (peak SVB loss)
    en_pre  = stress_clear(L_pre,  k_pre,  reg_b_idx, shock_amount=60.0)
    en_post = stress_clear(L_post, k_post, reg_b_idx, shock_amount=60.0)
    cd_pre  = cascade_depth(L_pre,  k_pre  - np.eye(len(names))[reg_b_idx] * 60.0)
    cd_post = cascade_depth(L_post, k_post - np.eye(len(names))[reg_b_idx] * 60.0)
    print(f"  Pre-EO:  amplification={en_pre.amplification:.2f}  "
          f"defaults={int(en_pre.defaulted.sum())}  cascade_depth={cd_pre}")
    print(f"  Post-EO: amplification={en_post.amplification:.2f}  "
          f"defaults={int(en_post.defaulted.sum())}  cascade_depth={cd_post}")
    sc_loss_pre = creditor_losses_by_kind(L_pre, en_pre, names, {"stablecoin", "exchange"})
    sc_loss_post = creditor_losses_by_kind(L_post, en_post, names, {"stablecoin", "exchange"})
    print(f"  Stablecoin-channel creditor loss: pre=${sc_loss_pre:.2f}B  "
          f"post=${sc_loss_post:.2f}B")
    results["en"] = {"pre": en_pre, "post": en_post,
                     "cd_pre": cd_pre, "cd_post": cd_post,
                     "stablecoin_loss_pre": sc_loss_pre,
                     "stablecoin_loss_post": sc_loss_post}

    # --- Layer 2: Global-game run threshold ---
    print("\n[2] Global-game equilibrium (Morris-Shin 2003)")
    print("-" * 72)
    gg_pre, gg_post = regime_comparison()
    prop1 = proposition_1_check(gg_pre, gg_post)
    print(f"  Pre-EO  theta* = {gg_pre.theta_star:.4f}   P(run|y_prior) = {gg_pre.p_run:.4f}")
    print(f"  Post-EO theta* = {gg_post.theta_star:.4f}   P(run|y_prior) = {gg_post.p_run:.4f}")
    print(f"  Delta theta*: {prop1['delta']:+.4f}    "
          f"Proposition 1 holds: {prop1['stability_improved']}")
    results["gg"] = {"pre": gg_pre, "post": gg_post, "prop1": prop1}

    # --- Layer 3: Optimal-transport run severity ---
    print("\n[3] Optimal-transport run severity (Wasserstein-1)")
    print("-" * 72)
    ot_pre  = severity_metric("USDC", 0.20, "pre_eo")
    ot_post = severity_metric("USDC", 0.20, "post_eo")
    sevs_pre,  W_pre  = severity_trajectory("USDC", "pre_eo")
    sevs_post, W_post = severity_trajectory("USDC", "post_eo")
    print(f"  Pre-EO  W_1(mu_0, mu_1) = {ot_pre.W1:.4f}  bp-mass")
    print(f"  Post-EO W_1(mu_0, mu_1) = {ot_post.W1:.4f}  bp-mass")
    print(f"  Ratio (post/pre) = {ot_post.W1 / ot_pre.W1:.3f}")
    print(f"  Topology distance ||c_pre - c_post||_F = "
          f"{topology_distance('pre_eo', 'post_eo'):.2f}")
    results["ot"] = {"pre": ot_pre, "post": ot_post,
                     "sev_pre":  (sevs_pre,  W_pre),
                     "sev_post": (sevs_post, W_post)}

    # --- Layer 4: Spectral contagion ---
    print("\n[4] Spectral contagion (Acemoglu-Ozdaglar-Tahbaz-Salehi 2015)")
    print("-" * 72)
    B_pre_sp, names_sp = spectral_feedback_matrix("pre_eo")
    B_post_sp, _ = spectral_feedback_matrix("post_eo")
    sp_pre  = spectral_report_from_matrix(B_pre_sp, names_sp, regime="pre_eo")
    sp_post = spectral_report_from_matrix(B_post_sp, names_sp, regime="post_eo")
    print(f"  Pre-EO  lambda_max = {sp_pre.lambda_max:.4f}   "
          f"spectral_gap = {sp_pre.spectral_gap:.4f}   "
          f"amplifying = {sp_pre.is_amplifying}")
    print(f"  Post-EO lambda_max = {sp_post.lambda_max:.4f}   "
          f"spectral_gap = {sp_post.spectral_gap:.4f}   "
          f"amplifying = {sp_post.is_amplifying}")
    print(f"  Pre-EO  super-spreaders: {sp_pre.super_spreaders}")
    print(f"  Post-EO super-spreaders: {sp_post.super_spreaders}")
    print(f"  Pre-EO  Fiedler value: {sp_pre.fiedler:.4f}")
    print(f"  Post-EO Fiedler value: {sp_post.fiedler:.4f}")
    results["sp"] = {"pre": sp_pre, "post": sp_post,
                     "B_pre": B_pre_sp, "B_post": B_post_sp}

    # --- Layer 5: Bayesian counterfactual ---
    print("\n[5] Bayesian counterfactual (MCMC, USDC March 2023 likelihood)")
    print("-" * 72)
    print("    Sampling ~8000 iterations (Metropolis-Hastings)...")
    post = metropolis_hastings(n_iter=8000, burn_in=2000)
    print(f"    Acceptance rate: {post.acceptance:.2%}")
    s_med, rho_med, tau_med = np.median(post.samples, axis=0)
    s_lo, _, _       = np.quantile(post.samples, 0.05, axis=0)
    s_hi, _, _       = np.quantile(post.samples, 0.95, axis=0)
    print(f"    s   posterior: {s_med:.3f}  [90% CI: {s_lo:.3f}, {s_hi:.3f}]")
    sens_ratio = 0.45 / 1.75
    band = counterfactual_band(post, sens_ratio)
    pp_diag = posterior_predictive_diagnostics(post)
    print(f"    Counterfactual post-EO trough median: "
          f"{np.median(band['trough_post_dist']):.4f}")
    print(f"    90% CI: [{np.quantile(band['trough_post_dist'], 0.05):.4f}, "
          f"{np.quantile(band['trough_post_dist'], 0.95):.4f}]")
    print(f"    Posterior predictive 90% coverage: {pp_diag['coverage_90']:.2f}; "
          f"median RMSE={pp_diag['rmse_median']:.4f}")
    results["bayes"] = {"posterior": post, "band": band, "sens_ratio": sens_ratio,
                        "moment_diagnostics": pp_diag}

    # --- Layer 6: Welfare analysis ---
    print("\n[6] Welfare analysis with explicit SWF")
    print("-" * 72)
    sim_pre  = simulate("pre_eo")
    sim_post = simulate("post_eo")
    L_pre_vec  = losses_from_simulation(
        sim_pre.peg["USDC"], bank_equity_drawdown=52.0,
        fed_draw=0.0, stablecoin_size_bn=42.0
    )
    L_post_vec = losses_from_simulation(
        sim_post.peg["USDC"], bank_equity_drawdown=13.0,
        fed_draw=max(sim_post.fed_master_redemptions),
        stablecoin_size_bn=42.0
    )
    welfare = compute_welfare(L_pre_vec, L_post_vec)
    print(proposition_2_verdict(welfare))
    results["welfare"] = {"pre": L_pre_vec, "post": L_post_vec, "report": welfare,
                          "sim_pre": sim_pre, "sim_post": sim_post}

    # --- Layer 7: Channel-identification diagnostics ---
    print("\n[7] Robustness and placebo diagnostics")
    print("-" * 72)
    placebo = placebo_mmf_shock()
    robust = topology_robustness()
    print(f"  MMF placebo delta amplification: "
          f"{placebo['delta_amplification']:+.4f}")
    for row in robust:
        print(f"  {row['topology']:14s} lambda pre={row['lambda_pre']:.3f}  "
              f"post={row['lambda_post']:.3f}  "
              f"reduction={row['reduction_pct']:.1f}%")
    results["diagnostics"] = {"placebo": placebo, "robustness": robust}

    print("\n" + "=" * 72)
    print("Analysis complete. Composing figure...")
    print("=" * 72)
    return results


def make_paper_figure(results: dict, out_path: Path) -> None:
    fig = plt.figure(figsize=(15, 11))
    gs = fig.add_gridspec(3, 3, hspace=0.38, wspace=0.30)

    ACCENT = "#1F3864"
    WARN   = "#B45309"
    DANGER = "#B91C1C"
    GOOD   = "#047857"
    GRAY   = "#6B7280"

    plt.rcParams.update({
        "font.family": "DejaVu Sans", "font.size": 10,
        "axes.spines.top": False, "axes.spines.right": False,
        "axes.grid": True, "grid.color": "#E5E7EB", "grid.linewidth": 0.6,
        "axes.edgecolor": "#374151", "axes.labelcolor": "#374151",
        "xtick.color": "#374151", "ytick.color": "#374151",
    })

    # (a) USDC peg path (deterministic, both regimes)
    ax = fig.add_subplot(gs[0, 0])
    sim_pre  = results["welfare"]["sim_pre"]
    sim_post = results["welfare"]["sim_post"]
    ax.plot(sim_pre.hours,  sim_pre.peg["USDC"],  color=DANGER, lw=2,
            label="Pre-EO")
    ax.plot(sim_post.hours, sim_post.peg["USDC"], color=GOOD,   lw=2,
            label="Post-EO")
    ax.axhline(1.0, color=GRAY, lw=0.7, ls="--")
    ax.scatter(USDC_EMPIRICAL["hours"], USDC_EMPIRICAL["peg"],
               s=18, color="black", marker="o", zorder=5,
               label="USDC Mar 2023")
    ax.set_ylim(0.83, 1.02); ax.set_xlim(0, 96)
    ax.set_xlabel("hours since shock")
    ax.set_ylabel("USDC peg (USD)")
    ax.set_title("(a) Calibration: USDC peg path", loc="left",
                 fontsize=10.5, fontweight="bold", color=ACCENT)
    ax.legend(fontsize=8, loc="lower right", frameon=False)

    # (b) Bayesian credible band on counterfactual
    ax = fig.add_subplot(gs[0, 1])
    band = results["bayes"]["band"]
    hrs = np.arange(len(band["median"]))
    ax.fill_between(hrs, band["lower"], band["upper"], color=GOOD, alpha=0.25,
                    label="90% CI")
    ax.plot(hrs, band["median"], color=GOOD, lw=2, label="posterior median")
    ax.plot(sim_pre.hours[:73], sim_pre.peg["USDC"][:73],
            color=DANGER, lw=1.6, ls="--", alpha=0.7, label="pre-EO (calibrated)")
    ax.axhline(1.0, color=GRAY, lw=0.7, ls="--")
    ax.set_ylim(0.83, 1.02); ax.set_xlim(0, 72)
    ax.set_xlabel("hours since shock")
    ax.set_ylabel("USDC peg (USD)")
    ax.set_title("(b) Bayesian counterfactual (MCMC)", loc="left",
                 fontsize=10.5, fontweight="bold", color=ACCENT)
    ax.legend(fontsize=8, loc="lower right", frameon=False)

    # (c) Wasserstein run severity vs. shock magnitude
    ax = fig.add_subplot(gs[0, 2])
    sevs_pre,  W_pre  = results["ot"]["sev_pre"]
    sevs_post, W_post = results["ot"]["sev_post"]
    ax.plot(sevs_pre  * 100, W_pre,  color=DANGER, lw=2, label="Pre-EO")
    ax.plot(sevs_post * 100, W_post, color=GOOD,   lw=2, label="Post-EO")
    ax.set_xlabel("shock severity (% of USDC reserves)")
    ax.set_ylabel(r"$W_1(\mu_0,\mu_1)$ (bp · mass)")
    ax.set_title("(c) Optimal-transport run severity", loc="left",
                 fontsize=10.5, fontweight="bold", color=ACCENT)
    ax.legend(fontsize=8, loc="upper left", frameon=False)

    # (d) Global-game run threshold + comparative statics
    ax = fig.add_subplot(gs[1, 0])
    gg = results["gg"]
    # Plot theta_star as a function of r for both regimes
    rs = np.linspace(0.001, 0.06, 200)
    from scipy.stats import norm
    theta_pre  = 0.92 + 0.40 * norm.ppf(1.0 - rs)
    theta_post = 0.92 + 0.15 * norm.ppf(1.0 - rs)
    ax.plot(rs * 100, theta_pre,  color=DANGER, lw=2, label="Pre-EO")
    ax.plot(rs * 100, theta_post, color=GOOD,   lw=2, label="Post-EO")
    ax.scatter([0.5,  4.5], [gg["pre"].theta_star, gg["post"].theta_star],
               color="black", zorder=5, s=30)
    ax.set_xlabel("rollover yield r (%)")
    ax.set_ylabel(r"run threshold $\theta^*$")
    ax.set_title(r"(d) Global-game $\theta^*(r;\lambda)$", loc="left",
                 fontsize=10.5, fontweight="bold", color=ACCENT)
    ax.legend(fontsize=8, frameon=False)

    # (e) Spectral signature
    ax = fig.add_subplot(gs[1, 1])
    sp_pre  = results["sp"]["pre"]
    sp_post = results["sp"]["post"]
    labels  = [r"$\lambda_{\max}$", r"$\lambda_{2}$", "spectral gap", "Fiedler"]
    pre_vals  = [sp_pre.lambda_max,  sp_pre.lambda_2,  sp_pre.spectral_gap,  sp_pre.fiedler]
    post_vals = [sp_post.lambda_max, sp_post.lambda_2, sp_post.spectral_gap, sp_post.fiedler]
    x = np.arange(len(labels)); w = 0.36
    ax.bar(x - w/2, pre_vals,  width=w, color=DANGER, label="Pre-EO")
    ax.bar(x + w/2, post_vals, width=w, color=GOOD,   label="Post-EO")
    ax.axhline(1.0, color=GRAY, ls="--", lw=0.7)
    ax.text(0.02, 0.96, r"AOT-S threshold: $\lambda_{\max} < 1$",
            transform=ax.transAxes, fontsize=8, color=GRAY,
            verticalalignment="top")
    ax.set_xticks(x); ax.set_xticklabels(labels, fontsize=9)
    ax.set_ylabel("eigenvalue")
    ax.set_title("(e) Spectral contagion metrics", loc="left",
                 fontsize=10.5, fontweight="bold", color=ACCENT)
    ax.legend(fontsize=8, loc="upper right", frameon=False)

    # (f) Katz super-spreaders (top-6 per regime)
    ax = fig.add_subplot(gs[1, 2])
    pre_top  = sp_pre.super_spreaders[:6]
    post_top = sp_post.super_spreaders[:6]
    pre_katz  = [sp_pre.katz_centrality[n]  for n in pre_top]
    post_katz = [sp_post.katz_centrality[n] for n in post_top]
    labels = list(dict.fromkeys(pre_top + post_top))[:6]
    y = np.arange(len(labels))
    pre_full  = [sp_pre.katz_centrality.get(n, 0)  for n in labels]
    post_full = [sp_post.katz_centrality.get(n, 0) for n in labels]
    ax.barh(y - 0.18, pre_full,  height=0.36, color=DANGER, label="Pre-EO")
    ax.barh(y + 0.18, post_full, height=0.36, color=GOOD,   label="Post-EO")
    ax.set_yticks(y); ax.set_yticklabels(labels, fontsize=9)
    ax.set_xlabel(r"Katz centrality $\kappa_i$")
    ax.set_title("(f) Super-spreader ranking", loc="left",
                 fontsize=10.5, fontweight="bold", color=ACCENT)
    ax.legend(fontsize=8, loc="lower right", frameon=False)

    # (g) Welfare decomposition
    ax = fig.add_subplot(gs[2, 0])
    L_pre  = results["welfare"]["pre"]
    L_post = results["welfare"]["post"]
    classes = ["Holders", "Banks", "Taxpayers"]
    pre_vals  = [L_pre.holders,  L_pre.banks,  L_pre.taxpayers]
    post_vals = [L_post.holders, L_post.banks, L_post.taxpayers]
    x = np.arange(len(classes)); w = 0.36
    ax.bar(x - w/2, pre_vals,  width=w, color=DANGER, label="Pre-EO")
    ax.bar(x + w/2, post_vals, width=w, color=GOOD,   label="Post-EO")
    ax.set_xticks(x); ax.set_xticklabels(classes, fontsize=9)
    ax.set_ylabel("loss (USD bn)")
    ax.set_title("(g) Welfare incidence", loc="left",
                 fontsize=10.5, fontweight="bold", color=ACCENT)
    ax.legend(fontsize=8, frameon=False)

    # (h) EN amplification + cascade depth
    ax = fig.add_subplot(gs[2, 1])
    en = results["en"]
    metrics = ["Glasserman-Young\namplification", "cascade\ndepth (rounds)", r"defaulted nodes"]
    pre_v  = [en["pre"].amplification,  en["cd_pre"],  int(en["pre"].defaulted.sum())]
    post_v = [en["post"].amplification, en["cd_post"], int(en["post"].defaulted.sum())]
    x = np.arange(len(metrics)); w = 0.36
    ax.bar(x - w/2, pre_v,  width=w, color=DANGER, label="Pre-EO")
    ax.bar(x + w/2, post_v, width=w, color=GOOD,   label="Post-EO")
    ax.set_xticks(x); ax.set_xticklabels(metrics, fontsize=8.5)
    ax.set_title("(h) Eisenberg-Noe cascade structure", loc="left",
                 fontsize=10.5, fontweight="bold", color=ACCENT)
    ax.legend(fontsize=8, frameon=False)

    # (i) Indifference-weight surface (2-D projection)
    ax = fig.add_subplot(gs[2, 2])
    rep = results["welfare"]["report"]
    d = np.array([rep.delta.holders, rep.delta.banks, rep.delta.taxpayers])
    # Plot the indifference line in (omega_H, omega_T) space with
    # omega_B = 1 - omega_H - omega_T constraint
    omH = np.linspace(0, 1, 100)
    omT = np.linspace(0, 1, 100)
    OH, OT = np.meshgrid(omH, omT)
    OB = 1 - OH - OT
    welfare_change = -(OH * d[0] + OB * d[1] + OT * d[2])
    mask = OB < 0
    welfare_change_masked = np.where(mask, np.nan, welfare_change)
    cf = ax.contourf(OH, OT, welfare_change_masked, levels=15, cmap="RdYlGn")
    plt.colorbar(cf, ax=ax, label="welfare gain (USD bn)")
    ax.contour(OH, OT, welfare_change_masked, levels=[0], colors="black",
               linewidths=1.5, linestyles="--")
    ax.scatter([1/3], [1/3], color="black", marker="*", s=90, zorder=5)
    ax.text(1/3 + 0.02, 1/3 + 0.02, "equal weights", fontsize=8)
    ax.set_xlabel(r"holder weight $\omega_H$")
    ax.set_ylabel(r"taxpayer weight $\omega_T$")
    ax.set_title("(i) Welfare gain surface", loc="left",
                 fontsize=10.5, fontweight="bold", color=ACCENT)

    # Title and footer
    fig.suptitle(
        "EO 14405 contagion analysis: nine-layer evaluation under the "
        "Acemoglu-Ozdaglar-Tahbaz-Salehi (2015) framework",
        fontsize=12.5, color=ACCENT, fontweight="bold", y=0.995,
    )
    fig.text(0.5, 0.005,
             "Calibration: USDC March 2023 episode (Fed FEDS Notes 17 Dec 2025). "
             "Methods: Eisenberg-Noe clearing, Morris-Shin global game, "
             "optimal transport ($W_1$), Acemoglu-Ozdaglar-Tahbaz-Salehi spectral, "
             "Metropolis-Hastings MCMC, Negishi welfare. "
             "Source: github.com/ihelfrich/eo14405-contagion",
             ha="center", fontsize=8, color=GRAY, style="italic")

    plt.savefig(out_path, dpi=160, bbox_inches="tight", facecolor="white")
    plt.close()
    print(f"\nFigure → {out_path}")


def main() -> None:
    results = run_all()
    here = Path(__file__).resolve().parent.parent
    out = here / "figures" / "analysis_nine_panel.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    make_paper_figure(results, out)


if __name__ == "__main__":
    main()
