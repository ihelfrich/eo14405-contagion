"""
clearing.py — Eisenberg–Noe (2001) payment-system clearing vector.

Solves the fixed-point problem for a financial network in which each node i
has obligations L_ij to other nodes j, an exogenous cash buffer e_i, and a
liquidation value of its non-cash assets. The clearing vector p* is the
maximal solution of

    p_i = min( bar_p_i ,  e_i + sum_j (p_j * pi_ji) )

where bar_p_i is total nominal obligations of i and pi_ji = L_ji / bar_p_j
is the relative-share matrix. Eisenberg & Noe (2001, Mgmt Sci 47(2)) prove
that this fixed point exists, is unique under mild conditions, and is
attainable by Picard iteration starting from p = bar_p.

We additionally compute the Glasserman–Young (2015, J. Banking & Finance)
contagion amplification index

    Gamma = (sum_i s_i) / (sum_i s_i^{direct})

where s_i is total loss to node i in clearing equilibrium and s_i^{direct}
is i's loss in a counterfactual where only the initial defaulting shock
propagates (no further amplification). Gamma > 1 means the network amplifies
the initial shock; Gamma = 1 means no network amplification.

Reference:
    Eisenberg, L. and T. Noe (2001). "Systemic Risk in Financial Systems."
        Management Science 47(2): 236-249.
    Glasserman, P. and H. P. Young (2015). "How likely is contagion in
        financial networks?" Journal of Banking & Finance 50: 383-399.
    Acemoglu, D., A. Ozdaglar, and A. Tahbaz-Salehi (2015). "Systemic Risk
        and Stability in Financial Networks." American Economic Review
        105(2): 564-608.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass
class ClearingResult:
    p_star: np.ndarray          # clearing vector
    bar_p: np.ndarray           # nominal obligations
    defaulted: np.ndarray       # bool: True if i defaulted (p_i < bar_p_i)
    iterations: int
    losses: np.ndarray          # bar_p - p_star
    amplification: float        # Gamma (Glasserman-Young)


def clear(
    L: np.ndarray,
    e: np.ndarray,
    *,
    direct_loss: float | None = None,
    shock_node: int | None = None,
    tol: float = 1e-10,
    max_iter: int = 200,
) -> ClearingResult:
    """
    Compute the Eisenberg-Noe clearing vector.

    Parameters
    ----------
    L : (n,n) liability matrix.  L[i,j] is what i owes j.
    e : (n,) exogenous cash buffer of each node.

    Returns
    -------
    ClearingResult with p_star, default flags, iteration count,
    and Glasserman-Young amplification index.
    """
    L = np.asarray(L, dtype=float)
    e = np.asarray(e, dtype=float).flatten()
    n = L.shape[0]
    assert L.shape == (n, n)

    bar_p = L.sum(axis=1)                       # total each node owes
    safe = np.where(bar_p > 0, bar_p, 1.0)      # avoid /0
    Pi = (L.T / safe).T                          # rel-share Pi[i,j]=L_ij/bar_p_i
    # Iteration: p^{k+1} = min(bar_p, e + Pi^T p^k)
    p = bar_p.copy()
    for k in range(max_iter):
        p_new = np.maximum(0.0, np.minimum(bar_p, e + Pi.T @ p))
        if np.max(np.abs(p_new - p)) < tol:
            p = p_new
            break
        p = p_new
    else:
        k = max_iter

    losses = bar_p - p
    defaulted = losses > 1e-8

    # Glasserman-Young amplification is a ratio to the direct asset shock,
    # not to the amount by which the shocked node's buffer happens to go
    # negative. Network amplification is creditor loss outside the shocked
    # node, scaled by the initial direct loss.
    if direct_loss is None:
        direct_loss = max(0.0, -e.min())
        propagated_loss = losses.sum()
    else:
        # losses are unpaid obligations to creditors. The shocked node's row
        # is precisely the first-round creditor loss, so it belongs in the
        # amplification numerator.
        propagated_loss = max(0.0, losses.sum())

    if direct_loss and direct_loss > 0:
        amplification = 1.0 + propagated_loss / direct_loss
    else:
        amplification = 1.0

    return ClearingResult(
        p_star=p,
        bar_p=bar_p,
        defaulted=defaulted,
        iterations=k + 1,
        losses=losses,
        amplification=amplification,
    )


def stress_clear(
    L: np.ndarray,
    e: np.ndarray,
    shock_node: int,
    shock_amount: float,
    **kwargs,
) -> ClearingResult:
    """
    Apply a negative cash shock to a single node and recompute clearing.
    Used to evaluate the cascade triggered by one bank failure.
    """
    e_shocked = e.copy().astype(float)
    e_shocked[shock_node] -= shock_amount
    return clear(
        L,
        e_shocked,
        direct_loss=shock_amount,
        shock_node=shock_node,
        **kwargs,
    )


def cascade_depth(L: np.ndarray, e: np.ndarray) -> int:
    """
    Number of rounds of default propagation: how many iterations until the
    set of defaulted nodes stabilizes. A proxy for contagion path length.
    """
    L = np.asarray(L, dtype=float)
    e = np.asarray(e, dtype=float)
    n = L.shape[0]
    bar_p = L.sum(axis=1)
    safe = np.where(bar_p > 0, bar_p, 1.0)
    Pi = (L.T / safe).T
    p = bar_p.copy()
    prev_default = np.zeros(n, dtype=bool)
    depth = 0
    for _ in range(50):
        p = np.maximum(0.0, np.minimum(bar_p, e + Pi.T @ p))
        cur_default = (bar_p - p) > 1e-8
        if np.array_equal(cur_default, prev_default):
            break
        prev_default = cur_default.copy()
        depth += 1
    return depth


if __name__ == "__main__":
    # Sanity check: a tiny 3-node ring.
    L = np.array([
        [0, 5, 0],
        [0, 0, 5],
        [5, 0, 0],
    ], dtype=float)
    e = np.array([3.0, 3.0, 3.0])
    r = clear(L, e)
    print("p* =", r.p_star)
    print("defaulted:", r.defaulted)
    print("iterations:", r.iterations)
    print("amplification:", r.amplification)
