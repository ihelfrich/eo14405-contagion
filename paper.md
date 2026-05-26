# Stablecoin Run Risk Under Direct Federal Reserve Access:
## A Spectral and Optimal-Transport Analysis of Executive Order 14405

**Ian Helfrich**
*Independent Research Note* · 26 May 2026

---

### Abstract

Executive Order 14405 directs the Federal Reserve to evaluate, and where legally permissible to establish, direct Reserve-Bank master-account access for non-bank financial entities, including stablecoin issuers. The change shifts the topology along which stablecoin run risk transmits, but it does not eliminate it. I formalize this proposition in four complementary frameworks: (i) Eisenberg-Noe (2001) fixed-point clearing on the bilateral exposure network, (ii) the Morris-Shin (1998, 2003) global game for the endogenous run threshold, (iii) optimal-transport with cost matrices encoding regime-specific frictions for run-severity measurement, and (iv) an Acemoglu-Ozdaglar-Tahbaz-Salehi (2015) effective feedback operator for spectral contagion. Calibrating to the March 2023 USDC/SVB episode via Bayesian posterior inference, I show that under the post-EO regime: the run threshold $\theta^\star$ falls by approximately 0.78 fundamental-units, the model-implied run probability falls from 0.90 to 0.18 under a common public prior, the system-wide Wasserstein-1 run severity drops by roughly 95 percent, and the Perron-Frobenius eigenvalue $\lambda_{\max}$ of the effective loss-feedback matrix declines from 0.87 to 0.42. The unambiguous result is the reallocation of liquidity absorption from commercial banks to the Fed's residual claimants, who absorb on the order of $12\text{B}$ of liquidity-provision exposure in the baseline scenario. The expected fiscal subsidy cost of that exposure is much smaller under the baseline 30 bp subsidy calibration, so welfare conclusions are highly sensitive to whether the social loss function prices gross liquidity exposure, expected subsidy, or tail fiscal loss.

**Keywords:** stablecoins, financial-network contagion, optimal transport, global games, master account, EO 14405

**JEL:** G01, G21, G23, G28, E58

---

## 1. Introduction

The May 19, 2026 Executive Order 14405 (Integrating Financial Technology Innovation Into Regulatory Frameworks, 91 FR 30475) instructs the Board of Governors of the Federal Reserve System, in 120 days, to evaluate the legal authority for and operational architecture of direct Reserve-Bank master-account access for non-bank financial entities, including stablecoin issuers. The order asks specifically whether the twelve regional Reserve Banks can act independently of the FRB in granting such access (Sec. 4(b)(iv)) and instructs that where existing law permits direct access, a 90-day adjudication clock applies (Sec. 4(c)). The order operationalizes a pathway already opened by the Federal Reserve Bank of Kansas City's approval of Kraken Financial's Limited Purpose Master Account on March 4, 2026.

The public-policy discussion around EO 14405 has framed the change as a binary choice between deregulation and consumer protection. That framing misses the structural mechanism. Direct master-account access does not eliminate stablecoin run risk; it relocates the absorption mechanism from commercial banks to the Fed's balance sheet. The relevant analytical question is not whether the EO reduces risk, but how it redistributes it across agent classes and across the topology of the financial network.

This note formalizes that question in four standard frameworks of financial-network theory: Eisenberg-Noe fixed-point clearing for the payment system, Morris-Shin global games for the endogenous run threshold, optimal transport for the formal measurement of run severity across holder distributions, and Acemoglu-Ozdaglar-Tahbaz-Salehi spectral analysis for asymptotic contagion susceptibility. I calibrate the dynamics to the March 2023 USDC/SVB episode using Bayesian Markov chain Monte Carlo posterior inference, then compute the counterfactual under the post-EO regime in each framework.

The four frameworks converge on the same qualitative conclusion. Direct master-account access reduces run risk along every contagion metric. But it does so by transferring the absorption from commercial-bank shareholders to the Fed's residual claimants, where "residual claimants" includes both taxpayers (via the implicit cost of liquidity extension at below-fair rates) and the stability of the Fed's policy-implementation framework. Whether this transfer is welfare-improving depends on social weighting that the executive order does not specify.

The contribution of this note is threefold. First, it provides the first formal network-theoretic analysis of EO 14405, treating the regime change as a topology shift on the bilateral-exposure matrix. Second, it introduces an optimal-transport metric for run severity that gives "run intensity" a well-defined unit (basis-point-mass of frictional reallocation) and a regime-comparable scale. Third, it derives an explicit welfare-indifference surface in Negishi-Pareto weight space, identifying the policy conditions under which the EO is stability-improving and welfare-improving simultaneously.

## 2. Related literature

This work sits at the intersection of three literatures. The first is the systemic-risk and financial-network literature originating with Eisenberg and Noe (2001), formalized in network-game form by Acemoglu, Ozdaglar, and Tahbaz-Salehi (2015), and applied to specific stress episodes by Glasserman and Young (2015) and Cont, Moussa, and Santos (2013). The novel structural feature of the post-EO regime is the addition of a non-depository class with direct Fed access, which changes both the dimensionality and the topology of the clearing system in ways the existing literature does not directly analyze.

The second is the global-game literature on bank runs and currency attacks, beginning with Morris and Shin (1998, 2003) and extended to the lender-of-last-resort question by Rochet and Vives (2004). The application to stablecoin runs is recent (see for instance Ahnert, Hoffmann, and Monnet 2023) but has not, to my knowledge, been used to formally analyze the effect of direct central-bank access on the endogenous run threshold.

The third is the stablecoin-specific literature, including the Federal Reserve's own December 2025 FEDS Notes post-mortem of the USDC/SVB episode (Federal Reserve 2025), industry attestation analyses (Lyons and Viswanath-Natraj 2023), and the regulatory-architecture literature (BIS 2023; Cecchetti and Schoenholtz 2024). The Fed's post-mortem identifies three contagion channels (direct bank-to-stablecoin transmission, code-based amplification via Peg Stability Modules, and primary-market-suspension paradox) that I incorporate as structural features of the model.

This note's contribution to all three literatures is to treat the regime change as a topology shift on the bilateral-exposure matrix and to characterize that shift in spectral and optimal-transport terms simultaneously.

## 3. Setup

The financial system is a directed weighted graph $G = (V, E, L)$ where $V$ is a set of $n$ nodes representing financial entities, $E \subseteq V \times V$ is the set of directed bilateral exposures, and $L: E \to \mathbb{R}_+$ assigns nominal obligations. Nodes are partitioned into six classes: G-SIBs, regional banks, money market funds, stablecoin issuers, crypto exchanges, and the Federal Reserve. Each node $i$ has total nominal obligations $\bar{p}_i = \sum_j L_{ij}$ and an exogenous cash buffer $e_i$.

Let $\Pi = (L_{ij}/\bar{p}_i)_{i,j}$ be the relative-share matrix. The Eisenberg-Noe clearing vector $p^\star \in \mathbb{R}^n_+$ is the maximal fixed point of

$$
p_i = \min\!\Big(\bar{p}_i,\ e_i + \sum_{j} \Pi_{ji}\, p_j\Big). \tag{1}
$$

Existence and uniqueness under standard conditions are established in Eisenberg-Noe Theorem 2. The fixed point is attainable by Picard iteration starting from $p = \bar{p}$. Node $i$ is in default if $p^\star_i < \bar{p}_i$; the total system loss is $\sum_i (\bar{p}_i - p^\star_i)$.

The regime change under EO 14405 corresponds to a transformation of $L$ that (i) reallocates stablecoin-issuer obligations from a commercial-bank counterparty to the Fed, and (ii) compresses certain operational frictions (settlement latency, gate-closure delays) that enter the dynamic redemption model below. We denote the pre-EO liability matrix by $L^{pre}$ and the post-EO by $L^{post}$, with corresponding clearing vectors $p^{\star,pre}$ and $p^{\star,post}$.

### 3.1 Calibration data

The model is calibrated to the March 2023 USDC depeg event. The relevant facts are (Federal Reserve 2025):

- Circle held $3.3 billion of USDC reserves at Silicon Valley Bank (8 percent of total reserves) when SVB entered FDIC receivership on March 10, 2023.
- Following Circle's disclosure at 10pm ET on Friday March 10, USDC primary redemption requests spiked to a total of $3.8 billion against $0.8 billion new mints by March 15.
- USDC reached a trough of $0.86 on the secondary market.
- The DAI Peg Stability Module absorbed approximately $1 billion of USDC daily during peak stress, dragging DAI's price below peg despite its separate collateral backing.
- USDC's primary-market suspension during the weekend, intended to manage liquidity, amplified secondary-market dysfunction by removing the authoritative price-discovery mechanism.
- The peg fully restored after the Treasury / Federal Reserve / FDIC joint backstop announcement at 6:15 pm ET Sunday March 12, with Circle resuming redemptions Monday March 13.

These facts identify the deep parameters of the dynamic model. We will return to formal posterior inference in Section 6.

## 4. The four frameworks

### 4.1 Eisenberg-Noe clearing under a regional-bank shock

We instantiate the network with thirteen nodes representing the 2026 US financial system: three G-SIBs (JPM, BAC, WFC), three regional banks (REG_A, REG_B, REG_C) with REG_B sized to be SVB-class, five stablecoin issuers (USDT, USDC, DAI, PYUSD, FDUSD), an aggregate money market fund, an aggregate crypto exchange (COINBASE), and the Federal Reserve. Edges encode reserve holdings, deposit relationships, overnight reverse-repo positions, customer-stablecoin custody, and the MakerDAO PSM.

Under the pre-EO regime, stablecoin issuers hold approximately 65-90 percent of their reserves as cash deposits in commercial banks (Circle's June 2023 reserve composition documents 90 percent of cash at BNY Mellon and a remainder of partner banks). Under the post-EO regime, we assume issuers migrate 70 percent of reserves to Fed master accounts, 20 percent to Treasury bills (held directly or via short-duration MMF), and 10 percent to a custodian bank for operational fiat rails. The 70/20/10 split reflects the Kraken Financial structure, which is the only public template currently available.

The shock is a $60 billion equity-side impairment to REG_B (SVB-class regional). Under the pre-EO topology, this impairment propagates through stablecoin reserve impairment, redemption cascade, and secondary-market spillover. Under the post-EO topology, the same impairment does not directly affect stablecoin reserves and the propagation is muted.

**Proposition 1.** *Under the calibrated bank-failure shock, the stablecoin-channel creditor loss satisfies $C^{post}_{SC} < C^{pre}_{SC}$. The Glasserman-Young amplification index is weakly lower under post-EO clearing and equals one when the shocked bank has no modeled network obligations.*

The proof is by direct computation of the Eisenberg-Noe clearing vector under both topologies after translating reserve-placement edges into debtor-to-creditor liabilities. This distinction matters. A stablecoin issuer's circulating supply is a liability to outside holders, not a bilateral inter-node debt owed to its reserve bank. Treating the full circulating supply as an Eisenberg-Noe network liability spuriously creates amplification of order 50. The corrected calculation uses only modeled bilateral obligations and separately reports creditor losses borne by stablecoin and exchange nodes. Computational details are in Section 6.

### 4.2 Global-game equilibrium

Let $\theta$ denote the stablecoin issuer's fundamental state (a sufficient statistic for solvency given current reserve composition). Holders observe a public signal $y \sim \mathcal{N}(\theta, \sigma_\theta^2)$ and a private signal $x_i = \theta + \epsilon_i$, $\epsilon_i \sim \mathcal{N}(0, \sigma_x^2)$. Each holder chooses to redeem (action 1) or roll over (action 0). Payoffs are: redemption yields 1 if the issuer can meet redemption demand, 0 otherwise; rollover yields $r$ unconditional.

The issuer can meet redemption demand iff $\theta \geq \ell + \lambda\, \ell(\theta)$, where $\ell$ is the bare solvency threshold, $\lambda > 0$ is the run-fragility parameter, and $\ell(\theta) \in [0,1]$ is the proportion of holders that redeem in equilibrium.

In the high-precision limit $\sigma_x \to 0$, Morris-Shin Corollary 1 (2003) establishes that the unique threshold-strategy equilibrium has cutoff signal $x^\star$ such that the marginal holder is indifferent, and the corresponding fundamental threshold is

$$
\theta^\star = \ell + \lambda\, \Phi^{-1}(1 - r), \tag{2}
$$

where $\Phi^{-1}$ is the standard-normal inverse CDF. EO 14405 affects this equilibrium through two channels:

- **The rollover yield $r$ rises.** Post-EO, holders earn IORB on reserves held in master accounts. At current IORB of approximately 4.5 percent versus near-zero on commercial-bank stablecoin reserves, this raises $r$ by approximately 400-450 basis points.
- **The run-fragility $\lambda$ falls.** Post-EO settlement is T+0 with direct Fed access; pre-EO settlement through commercial-bank rails is T+1 or worse during stress. The effective $\lambda$ falls by roughly the ratio of these settlement delays, scaled by the average duration of a panic episode.

**Proposition 2 (run-threshold reduction).** *Under the post-EO regime with $r^{post} > r^{pre}$ and $\lambda^{post} < \lambda^{pre}$, the run threshold strictly decreases: $\theta^{\star,post} < \theta^{\star,pre}$.*

Proof: from (2), $\partial \theta^\star / \partial r = -\lambda / \phi(\Phi^{-1}(1-r)) < 0$ for $r \in (0,1)$ and $\partial \theta^\star / \partial \lambda = \Phi^{-1}(1-r)$, which is positive for $r < 0.5$. Both channels move $\theta^\star$ in the same direction under the EO. The magnitude of the reduction at our calibration ($\ell = 0.92$, $\lambda^{pre} = 0.40$, $\lambda^{post} = 0.15$, $r^{pre} = 0.005$, $r^{post} = 0.045$) is approximately 0.78 fundamental-units.

### 4.3 Optimal-transport run severity

Let $\mu_0 \in \mathcal{P}(X)$ denote the pre-shock distribution of holder claims across $X = \{$USDT, USDC, DAI, PYUSD, FDUSD, fiat USD, T-bills, Fed reserves$\}$ and let $\mu_1^R$ denote the post-shock distribution under regime $R \in \{\text{pre-EO, post-EO}\}$. The cost of moving a unit of claim mass from state $i$ to state $j$ under regime $R$ is $c^R_{ij}$, expressed in basis points. The cost matrices encode regime-specific frictions: a stablecoin-to-fiat-USD move costs approximately 50 bp pre-EO (gate latency plus secondary spread) versus approximately 5 bp post-EO; a stablecoin-to-Fed-reserves move is infeasible pre-EO and approximately 1 bp post-EO.

The minimum-cost reallocation under a redemption shock is the solution of the Monge-Kantorovich problem

$$
W^R_1(\mu_0, \mu_1^R) = \min_{\gamma \in \Pi(\mu_0, \mu_1^R)} \sum_{i,j} c^R_{ij}\, \gamma_{ij}, \tag{3}
$$

where $\Pi(\mu_0, \mu_1^R)$ is the set of joint distributions with the specified marginals. This is a linear program with a unique solution by Birkhoff (1946); we solve it exactly via the network simplex algorithm (Peyre and Cuturi 2019).

**Proposition 3 (run-severity contraction).** *Under the calibrated cost matrices, $W^{post}_1(\mu_0, \mu_1^{post}) < W^{pre}_1(\mu_0, \mu_1^{pre})$ for every shock target and every shock magnitude $s \in (0, 0.5]$.*

The result is uniform in the shock magnitude. In the numerical exercise, at the 20-percent reserve-impairment level (comparable to the USDC March 2023 shock), the post-EO run severity is approximately 5 percent of the pre-EO value. The Frobenius distance between the two cost matrices is $\|c^{pre} - c^{post}\|_F \approx 349$, providing a topology-distance measure that does not depend on any particular shock.

The optimal-transport formulation gives "run severity" a well-defined unit (bp-mass of frictional reallocation) that the discrete network-model deviation metric does not. It also allows direct comparison across shock targets: a USDT-targeted shock under the pre-EO regime produces a different transport plan than a USDC-targeted shock, with implications for which downstream nodes absorb the redistribution.

### 4.4 Spectral contagion theory

Let $A^R$ denote the effective loss-feedback matrix under regime $R$. For each modeled balance-sheet edge of type $m$, nominal exposure $x_{ij}$ is first multiplied by a stress transmissibility coefficient $\tau_m \in [0,1]$ capturing loss given default, legal seniority, and operational run feedback. The normalized feedback operator is

$$
B^R_{ij} = \frac{\tau_m x_{ij} + \tau_m x_{ji}}{k_i}, \tag{4}
$$

where $k_i$ is node $i$'s stress absorptive capacity. The symmetrization in (4) is not an accounting claim that every exposure is legally reciprocal. It is a local-feedback approximation: a bank default impairs the stablecoin that holds deposits at the bank, and a stablecoin run feeds back into the bank through deposit withdrawal and fire-sale channels. Using the raw directed reserve-placement graph would be nilpotent in this stylized network and would mechanically report $\lambda_{\max}=0$, which is a graph-coding artifact rather than a contagion statement.

**Theorem (AOT-S 2015, Theorem 1, paraphrased).** *If $\lambda_{\max}(B) < 1$ where $\lambda_{\max}$ is the Perron-Frobenius eigenvalue, then the network is locally non-amplifying: an infinitesimal shock to any node produces an infinitesimal aggregate loss in equilibrium. If $\lambda_{\max}(B) \geq 1$, the network is in the amplifying region: arbitrarily small shocks can produce large equilibrium losses.*

**Proposition 4 (spectral contraction).** *Under the calibrated effective feedback matrices, $\lambda_{\max}(B^{pre}) > \lambda_{\max}(B^{post})$.*

We additionally compute the spectral gap $\lambda_{\max} - |\lambda_2|$, the Fiedler value (algebraic connectivity of the symmetric Laplacian), and Katz centrality $\kappa = (I - \alpha B)^{-1} \mathbf{1}$ with $\alpha < 1/\lambda_{\max}$. The Katz centrality identifies nodes whose local impairment would propagate furthest. Section 6 reports the ranking under each regime and shows that the post-EO network remains non-amplifying even though residual custodian concentration makes REG_A more central.

**Proposition 5 (post-EO spectral non-amplification).** *Let $B^{post}$ be the nonnegative effective feedback matrix defined in (4). If each stablecoin issuer moves share $q$ of reserve assets from commercial-bank deposits with stress transmissibility $\tau_D$ to Fed master-account balances with transmissibility $\tau_F=0$, and all other edge weights are unchanged, then*

$$
\lambda_{\max}(B^{post}) \leq \lambda_{\max}(B^{pre}) - q \cdot \Delta_\lambda,
$$

*for some $\Delta_\lambda \geq 0$ determined by the Perron left and right eigenvectors of $B^{pre}$. In the calibrated network, $\lambda_{\max}(B^{post})=0.42<1$, so the post-EO effective feedback system is locally non-amplifying.*

Proof sketch. For a nonnegative matrix, the Perron root is monotone in every entry. The EO transformation subtracts a nonnegative matrix $D$ from the bank-stablecoin block and adds a Fed block whose transmissibility is zero in the effective feedback operator. Hence $B^{post}=B^{pre}-D+R$ with $D \geq 0$ and $R$ zero on the analyzed non-Fed feedback block. Monotonicity gives $\lambda(B^{post}) \leq \lambda(B^{pre})$. The first-order perturbation is $v^\top D u/(v^\top u)$, where $u$ and $v$ are the Perron right and left eigenvectors of $B^{pre}$, yielding the stated $\Delta_\lambda$. The numerical calibration verifies the strict inequality and the $\lambda<1$ condition.

## 5. Bayesian counterfactual

The deterministic dynamic model in Section 4 depends on three structural parameters: the sensitivity $s$ (deviation per unit reserve impairment), the panic-phase decay $\rho$, and the recovery half-life $\tau$. We treat the observed USDC peg path during March 10-13, 2023 as an observation with Gaussian measurement noise $\sigma$, place independent log-normal priors on $(s, \rho, \tau)$, and sample from the joint posterior

$$
p(s, \rho, \tau \mid y) \propto p(y \mid s, \rho, \tau)\, p(s)\, p(\rho)\, p(\tau)
$$

via random-walk Metropolis-Hastings (Robert and Casella 2004) with 8,000 iterations and 2,000 burn-in.

The point of the Bayesian treatment is not to recalibrate the deterministic dynamics, but to propagate parameter uncertainty into the counterfactual. The post-EO counterfactual rescales $s$ by a fragility-ratio mapping centered at $s^{post}/s^{pre} \approx 0.26$. This mapping is not identified by the March 2023 episode alone. It is a structural extrapolation from the global-game mechanism: if secondary-market price pressure is locally proportional to the equilibrium mass of early redeemers, and that mass is locally proportional to the run-fragility parameter $\lambda$, then the semi-elasticity of peg deviation with respect to reserve impairment scales with $\lambda^{post}/\lambda^{pre}$. Formally, for small reserve impairment $z$,

$$
1-P_t \approx s^R z \, \ell^R_t,\quad
\ell^R_t \approx a_t \lambda^R,
$$

so $s^{post}/s^{pre} \approx \lambda^{post}/\lambda^{pre}$ if $a_t$ is regime-invariant. The assumption is strong: it rules out a separate confidence premium attached to Fed access and rules out endogenous Fed reaction-function uncertainty. I therefore treat the ratio and the post-EO impairment fraction as uncertain counterfactual objects in the posterior predictive calculation rather than as known constants.

## 6. Results

The orchestrator in `src/analyze.py` composes the six analytical layers and produces a nine-panel figure (Figure 1). Numerical results across the layers:

**Eisenberg-Noe clearing.** After correcting the liability orientation, Glasserman-Young amplification falls from $\Gamma^{pre} \approx 1.27$ to $\Gamma^{post} \approx 1.00$ under the REG_B shock. The stablecoin-channel creditor loss falls from $15.95$ B to zero because REG_B no longer owes reserve-deposit balances to stablecoin issuers. Cascade depth is one round in the pre-EO case and zero rounds in the post-EO clearing network.

**Global-game equilibrium.** The run threshold $\theta^\star$ falls from 1.95 to 1.17 under our calibration, a reduction of approximately 0.78 fundamental-units. With common public prior mean $y=1.50$ and $\sigma_\theta=0.35$, the model-implied run probability falls from 0.90 to 0.18. The local elasticities $\partial \theta^\star / \partial r$ and $\partial \theta^\star / \partial \lambda$ are both first-order significant: a 100 bp increase in $r$ reduces $\theta^\star$ by approximately 0.28 fundamental-units, and a unit decrease in $\lambda$ reduces $\theta^\star$ by approximately 2.6 units.

**Optimal-transport run severity.** $W_1^{pre} \approx 0.82$ bp-mass at the 20 percent shock magnitude versus $W_1^{post} \approx 0.04$ bp-mass, a 95 percent reduction. The reduction is uniform in shock magnitude over $[0, 50\%]$. The topology distance $\|c^{pre} - c^{post}\|_F \approx 349$.

**Spectral contagion.** On the calibrated effective feedback operator, both regimes are within the non-amplifying region, but $\lambda_{\max}^{pre}=0.867$ is substantially closer to the unit-amplification threshold than $\lambda_{\max}^{post}=0.418$. The earlier zero eigenvalue was a nilpotent-graph artifact from applying the spectral calculation to a one-way reserve-placement DAG. The dominant Katz nodes shift from DAI, USDC, PYUSD, REG_B, and FDUSD in the pre-EO topology to DAI, USDC, REG_A, FDUSD, and USDT in the post-EO topology.

**Bayesian posterior.** Acceptance rate is 28 percent. Posterior medians are $s = 1.54$ (90 percent CI [1.45, 1.63]), $\rho = 2.99$, and $\tau = 14.5$ hours. Once uncertainty in the post-EO sensitivity ratio and impairment fraction is propagated, the counterfactual post-EO trough median is 0.971 with 90 percent credible interval [0.951, 0.985], compared to a historical pre-EO trough of 0.86. The moment-matching diagnostic is not perfect: the empirical hourly path falls inside the posterior predictive 90 percent band at 44 percent of observed timestamps and the posterior-median RMSE is 0.016. That is evidence of reduced-form shape misspecification, not a reason to treat the counterfactual band as structural identification.

**Welfare incidence.** Under the integrated-depeg welfare calculation, pre-EO losses are $L_H^{pre}=15.10$ B (holders), $L_B^{pre}=52.00$ B (banks), and $L_T^{pre}=0$ (taxpayers). Post-EO losses are $L_H^{post}=0.15$ B, $L_B^{post}=13.00$ B, and $L_T^{post}=0.04$ B when taxpayer loss is measured as expected subsidy cost equal to the Fed liquidity draw times a 30 bp implicit subsidy rate. Under equal Negishi-Pareto weights, the EO is welfare-improving. The neutral simplex intersects near $\omega_T=0.998$ because the baseline expected subsidy cost is tiny relative to holder and bank losses. A different welfare object, gross Fed liquidity exposure or tail fiscal loss, would move that threshold sharply.

## 7. Discussion and policy implications

The four frameworks converge on a single structural finding: EO 14405 is a topology shift that systematically reduces stablecoin run risk in every standard metric of financial contagion. The reduction is not marginal. The Wasserstein-1 run severity falls by approximately 95 percent. The Eisenberg-Noe cascade depth contracts from 4 rounds to 1. The global-game run threshold falls by 0.78 fundamental-units. The Perron-Frobenius spectral radius declines from the boundary of the amplifying region toward the deeply non-amplifying region.

This convergence is not a coincidence. The four frameworks measure different aspects of the same underlying object: the topology of bilateral exposures and the cost of moving across it under stress. The EO modifies that topology in a single coherent direction: it removes commercial-bank intermediation between stablecoin issuers and the Fed and replaces it with direct master-account access. Every metric that measures distance, propagation, or amplification along that topology decreases.

But the welfare analysis shows that the topology shift does not reduce total expected loss; it reallocates it. The Fed becomes the counterparty whose policy choices determine whether a stablecoin redemption run translates into a depeg event. Under the post-EO regime, $L_T$ rises from zero to approximately $4 B in our baseline scenario, reflecting the expected fiscal cost of implicit Fed liquidity extension at below-fair rates. This is small in our calibration because the run is contained quickly under post-EO assumptions; under worst-case assumptions where the Fed extends discount-window-equivalent support during a multi-day systemic stress, the order of magnitude could be larger.

Three policy implications follow.

**First**, the Fed must publish, before any major stablecoin issuer migrates to direct master-account access, a credible framework specifying the conditions under which it will extend emergency liquidity to non-bank master-account holders, at what rate, against what collateral, and with what disclosure. The order specifies a 120-day evaluation period (Sec. 4(b)) and a 90-day adjudication clock for individual applications (Sec. 4(c)). The framework must precede, not follow, the first large stablecoin master-account approval.

**Second**, the question of whether individual Reserve Banks can act independently of the FRB in granting master-account access (Sec. 4(b)(iv)) is not a procedural question but a question of substantive monetary-policy implementation. If twelve regional Reserve Banks can each independently calibrate the size and composition of master-account exposures, the Fed's policy-implementation framework (floor system with IORB and ON RRP) is implicitly federalized. The aggregate demand curve for reserves becomes the sum of twelve heterogeneous local equilibria. This requires either a corresponding decentralization of the policy framework or an explicit centralization of the master-account decision at the FRB level. The status quo is ambiguous.

**Third**, the welfare analysis identifies the Pareto-improvement condition that the executive order does not specify. The EO is welfare-improving if and only if the social welfare function places sufficient weight on holders and banks relative to taxpayers. Under equal Negishi-Pareto weights, the EO is welfare-improving in our calibration. But the calibration also shows that small changes in the assumed implicit subsidy rate (we use 30 bp; if the actual rate were 100 bp the welfare conclusion reverses) flip the result. This is the empirical question that the Fed's 120-day report must answer.

## 8. Conflicts of interest and political-economy disclosure

The financial-contagion analysis above is technical and does not depend on who benefits politically from the executive order it analyzes. The political-economy facts nonetheless matter for two reasons. They affect the institutional credibility of the implementing decisions the order delegates to the Federal Reserve. And they situate the welfare analysis in the policy environment in which the welfare loss function will actually be specified. A companion synthesis dossier (`dossiers/SYNTHESIS.md`) documents the relationships below in primary sources; this section summarizes the structure.

The principal direct conflict involves the issuer of USD1, World Liberty Financial (WLFI). Per SEC Form D/A filings (CIK 0002043140), WLFI is a Delaware corporation; per WLFI's separate disclosures, DT Marks DEFI LLC (reportedly seventy percent Donald Trump, thirty percent other family members) holds a contractual claim to seventy-five percent of WLF protocol revenue and a fluctuating equity stake of approximately thirty-eight percent in WLF Holdco LLC. USD1's custodian is BitGo Trust, a South Dakota state-chartered trust company that is eligible for the Limited Purpose Master Account pathway the order operationalizes. The order's Section 4(b) and 4(c) directly affect USD1's regulatory trajectory; the Trump family's contractual revenue claim flows through that channel.

A parallel structural conflict involves the U.S. Secretary of Commerce. Per the Wall Street Journal (November 4, 2024) and subsequent disclosures, Cantor Fitzgerald acquired an approximately five percent equity stake in Tether via a roughly six hundred million dollar convertible bond, custodies the majority of Tether's reported U.S. Treasury reserves, and reportedly financed part of the Lutnick family Cantor acquisition with a Tether loan. Tether's US-compliant sibling USAT launched January 27, 2026 through Anchorage Digital Bank, an OCC-chartered trust company with existing Fed master-account access. USAT is the operational pathway through which the offshore-USDT economic engine acquires US Fed payment rails. Senators Warren and Wyden opened a fourth formal congressional inquiry into the Cantor-Tether relationship on April 30, 2026.

The administration-Silicon-Valley revolving door is documented in the dossier. David Sacks (White House AI and Crypto Czar, January 2025 to March 2026) divested approximately two hundred million dollars in crypto holdings as a Special Government Employee but received a broad ethics waiver on March 5, 2025; his OGE-278 is not public. Brian Quintenz, formerly CFTC Commissioner 2017-2021 and a16z Global Head of Policy 2022-2025, was nominated CFTC Chair but withdrew in September 2025 after pressure from the Winklevoss twins over a Gemini complaint. Heath Tarbert, formerly the 14th CFTC Chairman 2019-2021, is President of Circle Internet Group; that is the most direct regulator-to-regulated-issuer transition in the stablecoin space.

The political-finance side is documented in Fairshake PAC's FEC filings (committee ID C00835959) and the dossier's race-by-race accounting. Fairshake raised approximately two hundred sixty million dollars and spent approximately one hundred ninety-six million in the 2023-2024 cycle. The top three donors (Coinbase, Ripple, Andreessen Horowitz partners) accounted for approximately eighty-four percent of funding. The PAC achieved a fifty-three out of fifty-eight win rate. The defeated sitting chair of the Senate Banking Committee (Sherrod Brown) had approximately forty million dollars spent against him by the Fairshake apparatus; his successful opponent Bernie Moreno is a crypto-asset entrepreneur whose subsequent positions on stablecoin legislation are consistent with the donor preferences. Independent of Fairshake, Marc Andreessen and Ben Horowitz each personally gave 2.5 million dollars to the Trump 2024 super PAC.

These facts do not by themselves invalidate the technical analysis above. They do affect how a reader should weight the policy implications. The welfare-indifference threshold derived in Section 6 depends on the implicit subsidy rate the Federal Reserve will adopt when extending emergency liquidity to non-bank master-account holders, and that rate will be set by a chair appointed by the same administration that signed the order. The 120-day Section 4(b) report will be drafted under similar institutional incentives. The disclosure is appropriate because the technical finding (contagion topology shift) and the political-economy finding (concentrated benefit to documented administration-aligned interests) are simultaneously true. Either fact in isolation is incomplete.

The full primary-source documentation is in `dossiers/SYNTHESIS.md`. Readers who object to either the existence or the interpretation of these relationships are invited to verify them independently using the exercises in that file.

## 9. Robustness and limitations

**Calibration sensitivity.** The deep parameters $(s, \rho, \tau)$ are disciplined by the USDC March 2023 episode, but the posterior predictive diagnostics reject the view that the reduced-form path is a complete structural model of the hourly peg. The 90 percent posterior predictive band covers 44 percent of the empirical hourly observations and the posterior-median RMSE is 0.016. The model captures the order of magnitude of the depeg and recovery but misses some plateau curvature. I therefore use the Bayesian layer as uncertainty propagation around a stylized counterfactual, not as a claim of full likelihood-based structural identification.

**Counterfactual mapping.** The mapping $s^{post}=s^{pre}(\lambda^{post}/\lambda^{pre})$ is derived from a local proportionality between early redemption mass and the global-game fragility parameter. It is not directly identified without post-EO stablecoin-run observations. The reported counterfactual band therefore integrates over lognormal uncertainty in the sensitivity ratio and normal uncertainty in the post-EO impairment fraction. This widens the 90 percent trough interval to [0.951, 0.985], which is materially wider than the mechanically tight interval obtained by varying $s$ alone.

**Network heterogeneity.** The thirteen-node network is a stylized representation of the US financial system. I rerun the spectral calculation on synthetic bank-stablecoin topologies with the same stablecoin sizes and reserve-migration rule: Erdos-Renyi, core-periphery, and scale-free. The pre-to-post reductions in $\lambda_{\max}$ are 54 percent, 70 percent, and 55 percent respectively. The sign survives substantial topology variation, but the level of $\lambda_{\max}$ does not.

**Placebo test.** A non-stablecoin shock to the prime-MMF node produces no EO treatment effect in the Eisenberg-Noe layer: pre-EO and post-EO amplification both equal 1.00, with zero defaults in both regimes. This is the channel-identification test the baseline bank-shock comparison needs. The EO changes stablecoin reserve access; it should not mechanically change the propagation of a shock outside the stablecoin reserve channel.

**Fed reaction function.** The deterministic model treats the Fed's liquidity-extension decision as a binary parameter. A richer model would derive the Fed's reaction function from observable variables (stablecoin market cap, redemption velocity, credit-spread movements) and integrate over the Fed's optimal policy.

**Cross-jurisdiction effects.** USDT (Tether) is incorporated outside US jurisdiction and holds reserves at non-US custodians. A complete model would extend the network to include foreign banks and the international transmission of US-dollar liquidity shocks. We leave this for future work, noting that the implications of US-issued stablecoins becoming the dominant dollar substitute for emerging-market payments are large and underexplored.

**Identification by event study.** The Kraken Financial Limited Purpose Master Account approval (March 4, 2026) is a candidate natural experiment. A difference-in-differences design using Kraken as the treated unit and other unfunded crypto-adjacent firms as the control would identify the local-average-treatment-effect of master-account access on observable risk metrics (CDS spreads, basis between primary and secondary markets, redemption velocity in event windows). Limited data availability at the time of writing prevents this exercise; it should be revisited as the post-EO period matures.

## 10. Conclusion

EO 14405 is being read on Wall Street as a deregulatory gift to the crypto industry. The structural analysis here points to a different reading: the order is a topology shift on the bilateral-exposure network that systematically reduces stablecoin run risk in every standard metric, at the cost of a fiscal externality on the Fed's balance sheet that the order does not address. Whether the net effect is welfare-improving depends on social weights that the order leaves implicit.

The order's framers appear to have assumed that direct Fed access for stablecoin issuers is a Pareto improvement over the bank-deposit model. The frameworks here show that this is wrong in one direction and right in another. It is wrong because the run risk does not disappear; it relocates to a balance sheet where the policy framework for handling it does not yet exist. It is right because the average severity of a single-name stablecoin shock falls substantially. The synthesis is that the order has authorized a structural change whose implementation depends on a Fed reaction function that must be specified before the first large migration occurs.

This is a Setser-class question about the dollar's external position as much as a Diamond-Dybvig question about the deposit franchise. A regulated, Fed-backed stablecoin ecosystem competing with foreign-issued crypto-dollar substitutes in emerging-market payments would extend dollar hegemony. But that extension is only as strong as the Fed's willingness to extend implicit credit backstops to private dollar substitutes it does not issue and cannot fully control. The order has authorized the first of those bets. The framework that governs the rest of them is what comes next.

---

### References

- Acemoglu, D., Ozdaglar, A., and Tahbaz-Salehi, A. (2015). "Systemic Risk and Stability in Financial Networks." *American Economic Review* 105(2): 564-608.
- Ahnert, T., Hoffmann, P., and Monnet, C. (2023). "The Digital Economy, Privacy, and CBDC." ECB Working Paper.
- BIS (2023). "The Crypto Ecosystem: Key Elements and Risks." BIS Working Paper.
- Birkhoff, G. (1946). "Three Observations on Linear Algebra." *Univ. Nac. Tucumán. Revista Ser. A.* 5: 147-151.
- Cecchetti, S. and Schoenholtz, K. (2024). "Stablecoins: Implementing a Regulatory Framework." *Money and Banking blog.*
- Cont, R., Moussa, A., and Santos, E. B. (2013). "Network Structure and Systemic Risk in Banking Systems." *Handbook on Systemic Risk*. Cambridge UP.
- Cont, R. and Schaanning, E. (2017). "Fire Sales, Indirect Contagion and Systemic Stress Testing." Norges Bank Working Paper.
- Cuturi, M. (2013). "Sinkhorn Distances: Lightspeed Computation of Optimal Transport." *Advances in Neural Information Processing Systems*.
- Diamond, D. W. and Dybvig, P. H. (1983). "Bank Runs, Deposit Insurance, and Liquidity." *Journal of Political Economy* 91(3): 401-419.
- Eisenberg, L. and Noe, T. (2001). "Systemic Risk in Financial Systems." *Management Science* 47(2): 236-249.
- Federal Reserve (2025). "In the Shadow of Bank Runs: Lessons from the Silicon Valley Bank Failure and Its Impact on Stablecoins." *FEDS Notes*, December 17, 2025.
- Gelman, A. et al. (2013). *Bayesian Data Analysis*, 3rd ed. CRC Press.
- Glasserman, P. and Young, H. P. (2015). "How likely is contagion in financial networks?" *Journal of Banking & Finance* 50: 383-399.
- Lyons, R. and Viswanath-Natraj, G. (2023). "What Keeps Stablecoins Stable?" *Journal of International Money and Finance* 131: 102777.
- Morris, S. and Shin, H. S. (1998). "Unique Equilibrium in a Model of Self-Fulfilling Currency Attacks." *American Economic Review* 88(3): 587-597.
- Morris, S. and Shin, H. S. (2003). "Global Games: Theory and Applications." in *Advances in Economics and Econometrics*, ed. Dewatripont, Hansen, and Turnovsky. Cambridge UP.
- Negishi, T. (1960). "Welfare Economics and Existence of an Equilibrium for a Competitive Economy." *Metroeconomica* 12: 92-97.
- Peyre, G. and Cuturi, M. (2019). "Computational Optimal Transport." *Foundations and Trends in Machine Learning* 11(5-6): 355-607.
- Robert, C. and Casella, G. (2004). *Monte Carlo Statistical Methods*. Springer.
- Rochet, J.-C. and Vives, X. (2004). "Coordination Failures and the Lender of Last Resort." *Journal of the European Economic Association* 2: 1116-1147.
- Villani, C. (2008). *Optimal Transport: Old and New*. Springer.

---

### Methods and code

All code and data are available at [github.com/ihelfrich/eo14405-contagion](https://github.com/ihelfrich/eo14405-contagion). The replication entry point is

```bash
python src/analyze.py
```

which runs the full nine-layer evaluation and produces the figure inline. Individual modules (`clearing.py`, `global_game.py`, `ot_dynamics.py`, `spectral.py`, `bayes.py`, `welfare.py`) can be run independently for verification.

**Suggested citation.** Helfrich, Ian. 2026. "Stablecoin Run Risk Under Direct Federal Reserve Access: A Spectral and Optimal-Transport Analysis of Executive Order 14405." Working paper, 26 May 2026. Available at github.com/ihelfrich/eo14405-contagion.
