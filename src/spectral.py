"""
spectral.py — spectral measures of contagion susceptibility on the
financial network.

Theory
------
Acemoglu, Ozdaglar, and Tahbaz-Salehi (2015) characterize systemic risk
on financial networks in terms of the spectral radius of the bilateral
exposure matrix B normalized by absorptive capacity. Define

    B_{ij} = L_{ji} / k_i

where L_{ji} is i's exposure to j (j's liability to i) and k_i is i's
absorptive capacity (equity + cash buffer). The Perron-Frobenius
eigenvalue lambda_max(B) controls the asymptotic propagation gain of an
infinitesimal shock to any node.

Result (AOT-S Thm 1 paraphrased): If lambda_max(B) < 1, the network is
locally non-amplifying. If lambda_max(B) >= 1, an arbitrarily small shock
can in principle propagate to large losses.

Katz centrality
---------------
With damping factor alpha < 1/lambda_max, the Katz centrality vector

    kappa = (I - alpha B)^{-1} 1

ranks nodes by their cumulative "reachability" via all walks. A node
with high Katz centrality is a contagion super-spreader. We compute
Katz centrality under both regimes and identify nodes whose rank
changes meaningfully.

We additionally compute:
  - spectral gap |lambda_1| - |lambda_2|: a small gap signals near-
    degenerate dynamics with multiple plausible propagation directions
  - algebraic connectivity (Fiedler value of the Laplacian): low values
    indicate the network is close to disconnection, which paradoxically
    can be either good (firewalled) or bad (broker-dependent)
  - assortativity coefficient: do high-degree nodes connect to other
    high-degree nodes (core-periphery patterns)
"""
from __future__ import annotations

from dataclasses import dataclass

import networkx as nx
import numpy as np


@dataclass
class SpectralReport:
    regime: str
    lambda_max: float           # Perron-Frobenius
    lambda_2: float             # second-largest in modulus
    spectral_gap: float
    is_amplifying: bool         # lambda_max >= 1
    fiedler: float              # algebraic connectivity
    katz_centrality: dict[str, float]
    super_spreaders: list[str]  # top-5 by Katz
    assortativity: float


def exposure_matrix(L: np.ndarray, k: np.ndarray) -> np.ndarray:
    """
    Build the normalized exposure matrix B for AOT-S analysis.
    L[i,j] = liability of i to j; B[i,j] = L[j,i] / k_i.
    """
    n = L.shape[0]
    B = np.zeros((n, n))
    safe_k = np.where(k > 0, k, 1.0)
    for i in range(n):
        for j in range(n):
            B[i, j] = L[j, i] / safe_k[i]
    return B


def spectral_report(
    L: np.ndarray,
    k: np.ndarray,
    node_names: list[str],
    *,
    regime: str = "",
) -> SpectralReport:
    """
    Compute the full spectral characterization of the network.
    """
    B = exposure_matrix(L, k)
    eigvals = np.linalg.eigvals(B)
    abs_eig = np.abs(eigvals)
    order = np.argsort(-abs_eig)
    l1 = float(abs_eig[order[0]])
    l2 = float(abs_eig[order[1]]) if len(order) > 1 else 0.0

    # Fiedler value (algebraic connectivity) on the symmetric undirected
    # exposure graph
    A = (B + B.T) / 2
    deg = A.sum(axis=1)
    Lap = np.diag(deg) - A
    lap_eigs = np.sort(np.linalg.eigvalsh(Lap))
    # The 0 eigenvalue corresponds to the all-ones vector; the next is Fiedler
    fiedler = float(lap_eigs[1]) if len(lap_eigs) > 1 else 0.0

    # Katz centrality (uses 1 / (lambda_max + 1) as a safe alpha)
    alpha = 1.0 / (l1 + 1.0)
    try:
        kappa = np.linalg.solve(np.eye(B.shape[0]) - alpha * B, np.ones(B.shape[0]))
    except np.linalg.LinAlgError:
        kappa = np.zeros(B.shape[0])
    katz = {n: float(kappa[i]) for i, n in enumerate(node_names)}
    top5 = sorted(katz, key=katz.get, reverse=True)[:5]

    # Assortativity on the directed weighted graph
    g = nx.DiGraph()
    g.add_nodes_from(node_names)
    for i, ni in enumerate(node_names):
        for j, nj in enumerate(node_names):
            if i != j and B[i, j] > 0:
                g.add_edge(ni, nj, weight=B[i, j])
    try:
        assort = float(nx.degree_assortativity_coefficient(g, weight="weight"))
    except Exception:
        assort = float("nan")

    return SpectralReport(
        regime=regime,
        lambda_max=l1,
        lambda_2=l2,
        spectral_gap=l1 - l2,
        is_amplifying=(l1 >= 1.0),
        fiedler=fiedler,
        katz_centrality=katz,
        super_spreaders=top5,
        assortativity=assort,
    )


def shock_propagation_path(
    B: np.ndarray,
    seed_node: int,
    horizon: int = 12,
) -> np.ndarray:
    """
    Trace shock propagation as iterated matrix-vector product:
    x_{t+1} = B @ x_t starting from a unit shock to seed_node. Returns
    an (horizon, n) array of magnitudes at each step. Useful for
    visualizing contagion expansion in time.
    """
    n = B.shape[0]
    x = np.zeros(n)
    x[seed_node] = 1.0
    path = np.zeros((horizon, n))
    for t in range(horizon):
        path[t] = x
        x = B @ x
    return path


if __name__ == "__main__":
    # Small toy: 4-node directed network
    L = np.array([
        [0, 5, 0, 0],
        [3, 0, 4, 0],
        [0, 2, 0, 6],
        [4, 0, 0, 0],
    ], dtype=float)
    k = np.array([8.0, 6.0, 6.0, 4.0])
    rep = spectral_report(L, k, ["A", "B", "C", "D"], regime="toy")
    print("lambda_max:", rep.lambda_max)
    print("amplifying:", rep.is_amplifying)
    print("Katz:", rep.katz_centrality)
    print("super-spreaders:", rep.super_spreaders)
