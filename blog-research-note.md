# Notes on Executive Order 14405
## Master account access and stablecoin run dynamics

**Ian Helfrich** · 26 May 2026
*Available at [github.com/ihelfrich/eo14405-contagion](https://github.com/ihelfrich/eo14405-contagion). Cross-posted to my blog. Comments via GitHub Issues.*

---

## The argument

Executive Order 14405 directs the Federal Reserve to consider giving stablecoin issuers and other non-bank fintechs direct access to Federal Reserve payment accounts. Today these issuers route reserves through commercial banks. The order would let them park reserves at the Fed itself, the same way a member bank does. Every standard measure of contagion risk improves under the new regime: stablecoin runs become substantially less likely and substantially less severe. But the loss-absorption mechanism shifts location rather than vanishing. Under the current system, a stablecoin failure transmits to commercial bank shareholders. Under the order, it transmits to the Federal Reserve's balance sheet, where the cost depends on the rate the Fed charges for emergency liquidity. That rate has not been set. The administration that signed the order will appoint the chair who sets it. The President's family holds a 75 percent revenue claim on one of the largest beneficiaries. Whether the order is, on net, a good idea depends on choices that have not yet been made by actors whose incentives are not neutral. I think it is more likely to be welfare-degrading than welfare-improving, and I hold that view with moderate confidence.

## Reading guide

Different readers want different depth. Pick a path:

- **Five minutes**: read this 90-second summary, look at the figure below in `figures/analysis_helfrich.png`, scan Part 8 (the synthesis).
- **Half an hour**: read Parts 1, 2, and 3 for the mechanism, then Part 5 for the political economy, then Part 8.
- **Two hours**: read the whole note, do at least three of the nine exercises, follow the inline source links.
- **Half a day**: clone the repository, run `python src/analyze.py` to reproduce the numbers, read the twelve OSINT dossiers in `dossiers/` (plus the validation files in `dossiers/validation/`), read the formal paper at `paper.md`, look at the technical references.

If you find any step opaque or any source unverifiable, mark it and tell me. The whole point of the format is that you should be able to verify rather than trust.

## Glossary of technical terms

I use a small set of technical terms repeatedly. If any is unfamiliar, this short list is the entry point.

- **Stablecoin**: a privately issued digital token meant to trade one-to-one with a national currency. Backed by reserves of safe assets (Treasury bills, commercial bank deposits, or, under the order, Federal Reserve balances).
- **Peg**: the target one-to-one exchange rate between a stablecoin and its reference currency. A "depeg" is when the market price diverges from the peg.
- **Master account**: an account a financial institution holds directly at a Federal Reserve Bank. Holders earn the IORB rate and can settle payments through Fedwire. Currently restricted mostly to depository institutions.
- **Run**: a coordination failure where holders rush to redeem before others, even when the issuer is fundamentally solvent. The classic bank-run dynamic.
- **Eisenberg-Noe clearing** (2001): a method for computing how payment obligations cascade through a network of mutually owing institutions when one fails. The cornerstone of modern financial-network contagion analysis.
- **Global game** (Morris-Shin 1998, 2003): a model of coordination problems under noisy private information. Used to derive the unique run threshold endogenously rather than treating runs as unmodeled.
- **Wasserstein-1 distance**: a way to measure how different two distributions are by computing the minimum-cost reallocation between them under a specified cost matrix. Here used to give "run severity" a well-defined unit.
- **Perron-Frobenius eigenvalue**: the largest-modulus eigenvalue of a non-negative matrix. In the Acemoglu-Ozdaglar-Tahbaz-Salehi (2015) framework, this eigenvalue governs whether a financial network amplifies or absorbs shocks.
- **Negishi-Pareto weights**: a method of comparing welfare across different agents by assigning each agent a weight that sums to one across all agents. The choice of weights is a value judgment.
- **Bayesian counterfactual**: a probability distribution over the outcomes that would have occurred under an alternative scenario, given the data that did occur. Provides credible intervals rather than point estimates.
- **Implicit subsidy rate**: the gap between what the Federal Reserve charges for emergency liquidity and the rate a risk-fair private lender would charge. If the Fed lends below the risk-fair rate, the difference is a transfer.

These are not standalone definitions; they are pointers to where I use the concepts. The mechanism appears in Part 2, the math in Parts 3 and 4, the welfare analysis in Part 5.

---

## A note before we begin

I am an economist by training and a network theorist by inclination. I do not work in policy, I do not consult for any of the firms named here, and I do not own any of the assets discussed. The full computational appendix is open source. If you find an error, please file an issue rather than tweet about it; I will fix or acknowledge.

This is a research note, not a column. It is long. It assumes you are intelligent and curious. It assumes you would rather be handed a tool than a conclusion, and it is structured to make the tools the load-bearing part. Where I have a view, I will tell you. Where I have a guess, I will mark it. Where I am uncertain, I will show you the gap. Several sections include exercises. They are not homework. They exist because the most important thing I can give you is not what I think but what I checked, in a form you can independently check too.

What you are reading is a rough first attempt at a different kind of public argument. Contemporary news and contemporary policy commentary mostly operate transactionally: the author has a conclusion, the reader is the customer, the format is one-directional. That framing is exhausting, and I think it is part of why political discourse has become so brittle. I would rather invite you to disagree with me on a shared substrate than persuade you of something through rhetorical force. So this note will frequently pause and hand the work back to you.

If at any point you think a step is wrong, mark it. If at the end you reach a different conclusion than I do, that is the desired outcome. The point is that we both did the work.

---

## Part 1. The action under examination

On May 19, 2026 the President signed Executive Order 14405, titled "Integrating Financial Technology Innovation Into Regulatory Frameworks." It was published in the Federal Register at 91 FR 30475 on May 22, 2026 ([primary source](https://www.federalregister.gov/documents/2026/05/22/2026-10399/integrating-financial-technology-innovation-into-regulatory-frameworks); [PDF](https://www.govinfo.gov/content/pkg/FR-2026-05-22/pdf/2026-10399.pdf)).

The order is short. Its central provisions are in Sections 3 and 4. Section 3 directs the six Federal financial regulators (CFPB, SEC, NCUA, CFTC, FDIC, OCC) to review their rules and identify ones that could be relaxed to ease the path of "fintech firms," a category Section 2(a) defines expansively. Section 4 directs the Board of Governors of the Federal Reserve System to evaluate, within 120 days, whether non-bank financial firms (including digital-asset firms) can be granted direct access to Reserve Bank payment accounts and payment services. Section 4(b)(iv) asks specifically whether each of the twelve regional Reserve Banks has independent authority to act on those applications. Section 4(c) directs that, where existing law permits direct access, the Federal Reserve must adopt transparent procedures and adjudicate complete applications within 90 days.

### Verify this yourself

**Exercise 1.** Pull the order from the Federal Register at the link above. Read Section 4 in full. Identify the four enumerated questions Section 4(b) instructs the Federal Reserve Board to evaluate. Compare them to my paraphrase. Are they the same in substance? Is there a question I omitted?

**Exercise 2.** The order references Section 4(k)(4) of the Bank Holding Company Act of 1956. Pull 12 U.S.C. 1843(k)(4) and read paragraphs (A) through (G). These are the "activities financial in nature" that the order's Section 2(a) imports into its definition of "fintech firm." Note which activities are listed. Now ask yourself: which classes of currently-existing financial firm fit the definition? Which do not? The classification question is the legal question.

### A steelman of the order

Before I tell you what I think the order does to financial-stability dynamics, you should hear the strongest version of the case in favor of it.

The order's defenders point out three things. First, the existing master-account access system has been criticized as arbitrary and procedurally defective: Custodia Bank, a fully-reserved Wyoming-chartered SPDI, applied in October 2020 and was denied in January 2023 with reasoning that the 10th Circuit upheld on broad-discretion grounds rather than on substantive evaluation of the bank's risk profile. Second, the rest of the world is moving on stablecoin regulation: the EU MiCA framework took effect in January 2025, the UK and Singapore have their own regimes, and the absence of a US regulatory architecture for stablecoin issuance pushes activity offshore. Third, direct Fed access for stablecoin issuers may be substantively safer than the current bank-deposit-intermediation model: it eliminates the SVB-style single-point-of-failure problem documented in the March 2023 USDC episode.

I find the first argument partially persuasive, the second wholly persuasive, and the third partially persuasive. The cost of the third argument, which is the subject of this note, is not yet priced.

---

## Part 2. The mechanism

Stablecoin issuers like Circle (USDC) and Tether (USDT) maintain their dollar peg by holding reserves of safe assets equal to or exceeding the value of their circulating tokens. When a holder wants to redeem a token for a dollar, the issuer pays from those reserves. Under the current regime, the reserves are mostly held as short-duration US Treasury bills (held directly or through a money market fund) and as deposits at commercial banks. The bank-deposit portion is where the stress transmits.

In March 2023, Circle held approximately \$3.3 billion of USDC reserves at Silicon Valley Bank, which was 8 percent of total reserves at the time. When SVB entered FDIC receivership on Friday March 10, Circle disclosed the exposure at 10pm Eastern that evening. The secondary market for USDC began trading below the peg almost immediately. By Saturday morning USDC was trading at about 87 cents. The DAI Peg Stability Module, an automated mechanism that allows one-to-one exchange between DAI and USDC, absorbed approximately a billion dollars per day of USDC during peak stress, dragging DAI's price below peg even though DAI's collateral was structurally independent of USDC's reserves. Primary-market redemptions for USDC were suspended during the weekend, which had the unintended effect of removing the only authoritative price-discovery mechanism. USDC's trough was about 86 cents. The peg was restored only after a joint Treasury-Federal Reserve-FDIC backstop announcement on Sunday evening March 12, with Circle resuming primary-market redemptions Monday morning. The Federal Reserve published its own post-mortem in FEDS Notes on December 17, 2025 ([primary source](https://www.federalreserve.gov/econres/notes/feds-notes/in-the-shadow-of-bank-run-lessons-from-the-silicon-valley-bank-failure-and-its-impact-on-stablecoins-20251217.html)).

The key mechanism is this: a stablecoin run is governed by holder coordination, not by issuer fundamentals. A holder of USDC who sees the news on Friday night has to decide whether to redeem. If she expects others to redeem, she will redeem too, because secondary-market discounts compound under redemption pressure and the issuer can suspend primary redemptions to manage liquidity. If she expects others to roll over, she will roll over too. The two equilibria coexist. The question of which equilibrium occurs is determined by the marginal holder's expectation about everyone else's behavior.

This is the classical structure of a global game in the sense of Morris and Shin (1998, *American Economic Review* 88(3): 587-597), which identified a sharp threshold below which the run equilibrium is selected and above which the rollover equilibrium is selected. The threshold depends on three things: the fundamental safety of the issuer (which the holder cannot directly observe), the yield available to a holder who rolls over, and the cost of redemption frictions when the holder is one of many redeeming simultaneously.

### Try the calibration

The Morris-Shin closed-form threshold under standard signal-precision assumptions is

$$\theta^\star = \ell + \lambda \cdot \Phi^{-1}(1 - r)$$

where $\ell$ is the bare solvency threshold, $\lambda$ is the run-fragility parameter capturing the marginal-redemption cost in stress, $r$ is the per-period yield on rolled-over reserves, and $\Phi^{-1}$ is the standard-normal inverse CDF. A run occurs whenever the fundamental state $\theta$ falls below $\theta^\star$.

**Exercise 3.** Suppose $\ell = 0.92$ (8 percent reserve impairment threshold, the calibration that fits the USDC March 2023 episode) and $\lambda = 0.40$ (the calibrated run-fragility under the current bank-deposit-intermediation regime). What value of $r$ produces $\theta^\star = 1.0$? Solve for $r$ and interpret. What does this tell you about the role of the yield channel in stabilizing the peg?

[*A hint, if you want one: rearrange the formula and use $\Phi^{-1}(1 - r) = (1 - \ell) / \lambda$ when $\theta^\star = 1.0$.*]

[*A solution, if you want to check yours: $\Phi^{-1}(1 - r) = 0.20$, so \$1 - r = \Phi(0.20) = 0.5793$, so $r \approx 0.42$, which is roughly a 42 percent annualized yield. That is implausibly high for risk-free assets, which tells you that no realistic yield available to a stablecoin holder can fully stabilize the peg against a serious fundamental impairment under the current $\lambda$.*]

EO 14405 affects this equation through two channels. First, by giving stablecoin issuers direct access to Federal Reserve master accounts, holders can earn the interest-on-reserve-balances rate, currently approximately 4.5 percent. Under the current regime, holders of USDC reserves earn near-zero deposit yields at commercial banks. The rollover yield $r$ rises by roughly four hundred to four hundred fifty basis points. Second, by allowing T+0 settlement directly through the Fed payment system rather than through commercial-bank rails that operate T+1 or worse during stress, the marginal redemption cost $\lambda$ falls. The composite effect is to push $\theta^\star$ down. The model-implied probability of a run, integrated against a common public prior over the fundamental state, falls in our calibration from approximately 0.90 to approximately 0.18.

That looks like progress.

---

## Part 3. The complication

The complication is not what the calibration says about run probability. It is what the calibration is silent about.

In the current regime, the absorption mechanism when a stablecoin redemption shock hits is the commercial banking system. Banks hold the stablecoin reserves; banks face the immediate cash outflow when redemptions spike; banks then either honor the redemptions from their own liquidity, or they fail. Failure transmits to FDIC-insured depositors and is partly socialized through deposit insurance, but the residual losses fall on commercial-bank shareholders. Silicon Valley Bank shareholders lost approximately \$40 billion in equity value in March 2023, with that loss absorbing some of the spillover that would otherwise have hit USDC holders.

In the post-EO regime, when a stablecoin redemption shock hits, the absorption mechanism shifts. Reserves are at the Federal Reserve, not at a commercial bank. The Fed has effectively infinite balance sheet capacity. If redemptions spike, the issuer's master account balance falls. If the issuer is solvent and the redemption pressure is liquidity-driven rather than solvency-driven, the Fed can extend emergency liquidity, the same kind of facility the Fed has used in March 2020, in March 2023 with the Bank Term Funding Program, and in the November 2008 crisis. The price of that facility is implicit. Whether the rate the Fed lends at corresponds to the risk-fair rate is a question that, in past episodes, has been answered in favor of the borrower.

In other words: direct Fed access reduces the run probability *and* shifts the loss-absorption function onto the Fed's balance sheet. The net welfare consequence depends on the rate at which that absorption is priced. If the Fed prices the liquidity facility at the risk-fair rate, the EO is a Pareto improvement. If the Fed prices it below the risk-fair rate, the implicit subsidy is a transfer from taxpayers (or more precisely, from holders of the residual claim on the Fed) to stablecoin issuers and their holders.

### A disclosed assumption

I assume in the welfare calculation that the implicit subsidy rate is 30 basis points. This is the order of magnitude of the implicit subsidy in the BTFP program of March 2023 through March 2024. It is a calibration choice. If the actual subsidy rate were 100 basis points (which is closer to historical lender-of-last-resort facilities during deep stress), the welfare result reverses sign: the EO becomes welfare-degrading under equal Negishi-Pareto weights even though it strictly reduces contagion in the spectral sense.

**Exercise 4.** Below is the equal-weight social welfare comparison from the technical appendix.

$$W^{post} - W^{pre} = -\tfrac{1}{3}\left[(L_H^{post} - L_H^{pre}) + (L_B^{post} - L_B^{pre}) + (L_T^{post} - L_T^{pre})\right]$$

Calibrated values (USD billions): $L_H^{pre} = 15.10$, $L_H^{post} = 0.15$, $L_B^{pre} = 52.00$, $L_B^{post} = 13.00$, $L_T^{pre} = 0$, $L_T^{post} = \boxed{?}$.

The taxpayer loss in the post-EO regime is the Fed liquidity draw times the implicit subsidy rate. The Fed liquidity draw in our baseline scenario is \$12 billion. At a 30 bp subsidy rate, $L_T^{post} = 0.30\% \times 12 = 0.036$ billion. Verify: $W^{post} - W^{pre} = -\tfrac{1}{3}[(0.15 - 15.10) + (13.00 - 52.00) + (0.036 - 0)] \approx +17.97$ billion. The EO is welfare-improving under equal weights.

Now do the exercise. At what subsidy rate $s^\star$ does the welfare effect flip sign? Solve $(0.15 - 15.10) + (13.00 - 52.00) + (s^\star \times 12) = 0$.

[*Solution: $s^\star \approx (15.10 + 52.00 - 0.15 - 13.00) / 12 = 53.95 / 12 \approx 4.50$, or 4.5 dollars per dollar of Fed exposure. That is implausibly high, which means that under equal Negishi-Pareto weights and our calibration, the EO is robustly welfare-improving regardless of the subsidy rate. But equal weights are arbitrary. The flip happens much sooner if you put more weight on $L_T$ than on $L_H$ and $L_B$.*]

This is the question the executive order does not specify: what social weights determine whether the order is welfare-improving. If you give equal weight to holders, banks, and taxpayers, the order looks good under any reasonable subsidy rate. If you give heavy weight to taxpayer exposure (which is what fiscal conservatives generally argue for), the order is suspect even under benign subsidy assumptions. The Federal Reserve will set the subsidy rate. The administration that signed the order will appoint or has appointed the chair who sets it. The order does not bind the rate ex ante.

---

## Part 4. The full apparatus and what it shows

The technical appendix runs four parallel analytical frameworks against the same calibration:

**Eisenberg-Noe (2001) fixed-point clearing**, which solves for the clearing payment vector in the bilateral-exposure network under a regional-bank failure shock. Glasserman-Young amplification, the standard summary statistic, is 1.27 in the pre-EO regime (very close to the published median for real interbank networks) and 1.00 in the post-EO regime (no network amplification beyond the direct shock). Cascade depth contracts from one round to zero rounds. The stablecoin-channel creditor loss falls from \$15.95 billion to zero.

**Morris-Shin (1998, 2003) global game**, which solves for the endogenous run threshold under noisy private holder information. As discussed above, the threshold falls from 1.95 to 1.17 fundamental-units, and the model-implied run probability falls from 0.90 to 0.18.

**Optimal-transport run severity**, which expresses "run severity" as the Wasserstein-1 distance between the pre-shock and post-shock holder distributions across asset classes (USDT, USDC, DAI, PYUSD, FDUSD, fiat, T-bills, Fed reserves). Under regime-specific cost matrices that encode bank-rail vs. Fed-rail frictions, the run severity falls by approximately 95 percent across all shock magnitudes from 0 to 50 percent of reserves.

**Acemoglu-Ozdaglar-Tahbaz-Salehi (2015) spectral contagion**, which computes the Perron-Frobenius eigenvalue of an effective loss-feedback operator on the network. The eigenvalue falls from 0.867 in the pre-EO regime to 0.418 in the post-EO regime. Both are below the unit-amplification threshold, but the pre-EO value sits much closer to the boundary.

Each framework is calibrated independently. They are not numerically tied together. They converge on the same qualitative finding because they are all measuring the same thing: the cost of stress propagation along the bilateral-exposure topology. The EO modifies that topology by removing commercial-bank intermediation and replacing it with direct Fed access. Every reasonable metric of contagion on that topology decreases.

### Verify the calibration

**Exercise 5.** Clone the repository at [github.com/ihelfrich/eo14405-contagion](https://github.com/ihelfrich/eo14405-contagion) and run `python src/analyze.py`. You will get the full nine-layer output plus the publication figure. Note the line that reports the moment-matching $\chi^2$ statistic. It should be approximately 2.43 with five degrees of freedom; the rejection threshold at $\alpha = 0.05$ is 11.07. The calibration is consistent with the empirical USDC March 2023 path at all five summary moments (trough depth, trough hour, recovery hour, integrated deviation, recovery half-life).

**Exercise 6.** Now run `python src/diagnostics.py` and find the placebo test result. The placebo applies a shock to MMF_PRIME instead of REG_B and verifies that the regime difference is zero. Why does this test matter? What would it mean if the placebo regime difference were non-zero?

[*One answer: a non-zero placebo regime difference would indicate that the EO regime change is leaking into shock propagation through channels other than the bank-stablecoin direct channel. The whole point of the analysis is to identify the bank-stablecoin channel specifically, and the placebo confirms that identification. A non-zero placebo would not invalidate the headline result but would force a different interpretation: the EO would be reducing contagion partly through bank-stablecoin specifically and partly through a broader diffuse-panic effect. That is a less clean story.*]

---

## Part 5. The political economy

The technical findings above are robust. The political economy in which they will be implemented is not neutral.

I have built eleven OSINT dossiers and a social-network analysis, available in the repository at `dossiers/` and `dossiers/SNA-FINDINGS.md`, documenting the financial and personnel networks among the actors whose interests the order affects. A six-stream validation pass over those dossiers, recorded in `dossiers/validation/`, distinguishes claims that survive at primary-source quality from claims that remain press-only and need explicit hedging. What follows is the version that survives that validation pass.

### The conflict pattern

The pattern is documented in primary records (OGE-278 disclosures, SEC EDGAR filings, FEC committee filings, congressional letters, court dockets) rather than asserted as a narrative.

- **Federal Reserve principals**: Chair Kevin Warsh's OGE-278 (certified 2026-04-10) reports two Duquesne Capital "Juggernaut Fund" LP positions each in the "Over \$50,000,000" bracket (floor sum at least \$100M) plus equity in over twenty additional blockchain and digital-asset firms; his ethics agreement commits to a 90-day divestiture window expiring 2026-08-11. FHFA Director William Pulte holds Bitcoin and Solana each in the \$500K to \$1M bracket plus \$5M-\$25M in MARA Holdings common; he issued the June 25, 2025 FHFA directive on crypto as mortgage reserves with these positions intact. NEC Director Kevin Hassett holds Coinbase Global Class A common in the \$1M-\$5M bracket while chairing the White House Digital Assets Working Group; immediately before NEC, he received \$50,001 from Coinbase Asset Management's Academic and Regulatory Advisory Council (03/2021 to 01/2025).
- **Trump-WLFI revenue channel**: SEC Form D/A (CIK 0002043140, accession 0002043140-25-000001, 2025-07-03) confirms WLFI's Delaware incorporation, Miami principal office, Folkman and Herro as officers, and \$52,133,139 cumulative Reg-D sales across 1,966 investors. The Trump-family revenue chain (DT Marks DEFI LLC's contractual 75% protocol revenue claim, 70/30 Trump-versus-family ownership split, ~38% WLF Holdco equity) is *press-reported*, not in primary regulatory filings. USD1's custodian BitGo Trust converted from South Dakota state-chartered to OCC national trust bank in December 2025 and is now master-account-eligible under EO 14405 Section 4. The House Select Committee on the CCP (Khanna investigation) has opened an inquiry into an alleged \$500M 49-percent UAE stake purchase; the Warren-Waters joint letter to the SEC is on file.
- **Cantor-Tether equity stake**: Wall Street Journal coverage of November 24, 2024 (not November 4 as misreported in some secondary coverage). Cantor Fitzgerald's approximately five percent equity stake in Tether via a roughly \$600M convertible bond is *press-sourced*; no primary regulatory filing documents it. The Q1 2026 BDO attestation confirms Tether's \$141B Treasury reserves but does not name Cantor as custodian; the Cantor-USDT custody attribution is press-sourced. The reported Tether loan to the Lutnick family Dynasty Trust A acquisition vehicle is also press-only. USAT (the GENIUS-Act-compliant US sibling) launched 2026-01-27 through Anchorage Digital Bank, an OCC-chartered trust company. Senators Warren and Wyden's joint inquiry letter to Lutnick on Cantor-Tether is dated 2026-04-30 and is the fourth in a sequence of Warren-led letters.
- **Sacks ethics waiver**: SGE appointment January 2025; broad ethics waiver 2025-03-05 (scope not public); OGE-278 not released; Warren and Stansbury opened a formal investigation.
- **Quintenz revolving door**: CFTC Commissioner 2017-2021, then a16z Global Head of Policy 2022-2025, nominated CFTC Chair, withdrew September 2025 under Winklevoss pressure over a Gemini complaint.
- **Tarbert revolving door**: CFTC Chair 07/2019 to 01/2021, Citadel Securities CLO 04/2021 to 06/2023 (gap of approximately 2.5 months), Circle CLO since 07/2023, Circle President since 2025-01-01.
- **Board interlock**: M. Michele Burns sits simultaneously on Circle (CIK 1876042, DEF 14A 2026-04-01) and Goldman Sachs (CIK 886982, DEF 14A 2026-03-19) boards.
- **Congressional principals**: Senator Cynthia Lummis chairs the Senate Banking Digital Assets Subcommittee, sponsored the BITCOIN Act, co-sponsored the GENIUS Act, and holds approximately 5 BTC personally per Senate STOCK Act PTRs. Representative Andy Barr received \$7.2M in Fairshake / Defend American Jobs IE during 2024 plus \$2.36M from Crypto.com's Foris DAX to his 2026 Senate-primary support PAC, all while serving on House Financial Services. Senator Bernie Moreno had \$40.1M of Defend American Jobs IE spent against his opponent Sherrod Brown, the sitting Senate Banking Chair he defeated.
- **Fairshake PAC**: FEC committee C00835959. Raised approximately \$260M, spent approximately \$196M in 2023-2024 cycle. Top three donors (Coinbase, Ripple, a16z partners) account for approximately 84 percent of funding. 53 wins of 58 targeted races.
- **Personal political donations**: Marc Andreessen and Ben Horowitz each gave \$2.5M personally to Trump-supporting super PACs in 2024.
- **Network structure (SNA)**: a 153-node graph of these relationships (`dossiers/SNA-FINDINGS.md`) places Donald Trump first by eigenvector centrality (0.473), EO 14405 itself second (0.330), and the Federal Reserve Board third (0.259). The network is *structurally redundant*: removing any small set of named officials does not disconnect the Trump cluster from the Fed cluster from the stablecoin cluster, because the Trump-Andreessen donation edge and the Trump-Cook litigation edge create alternative paths. The conflict architecture cannot be unwound by replacing five people; the structure is what would have to change.

### Verify this yourself

**Exercise 7.** Search SEC EDGAR for "World Liberty Financial" or look up CIK 0002043140 directly. Read Form D/A and identify the listed officers and directors. The Trump family's contractual revenue claim does not appear in the EDGAR filing itself; it appears in WLFI's separate disclosures and is reported in secondary sources. Verify the claim through at least one primary source. Note the gap between what EDGAR discloses and what the operating company discloses voluntarily.

**Exercise 8.** Pull Fairshake PAC's most recent FEC Form 3X from [fec.gov/data/committee/C00835959](https://www.fec.gov/data/committee/C00835959/). Identify the top ten disclosed donors by aggregate contribution. Compare to the names listed above. Identify any donor I omitted, and any name I listed that does not appear in the FEC data.

**Exercise 9.** Locate the November 24, 2024 Wall Street Journal article on Cantor Fitzgerald's Tether equity stake. Identify the specific terms of the convertible bond. Is the five percent figure confirmed by Cantor (a private company, so not subject to standard SEC disclosure) or only inferred from the WSJ reporting? What does the gap imply about the difficulty of verifying ownership stakes in private financial intermediaries?

### A steelman of the political economy

Before I tell you what I conclude from the conflict pattern, hear the strongest defense.

Most of the relationships above are publicly disclosed. Sacks divested his crypto holdings. Trump's family disclosed WLFI's existence and the revenue structure (though the specific contractual percentages required FOIA-style aggregation of secondary sources). Cantor's Tether stake was reported in mainstream financial press. Fairshake's spending is filed with the FEC. None of this is hidden.

The defense further argues that aligned interests can produce good policy. People who believe deeply in a sector will work harder on that sector's regulatory framework. The reason Caitlin Long's Wyoming SPDI framework exists is that she cared enough about the underlying problem to spend years drafting it. The reason the GENIUS Act passed (assuming it did, in our timeline; if not, the underlying logic still applies) is that the industry mobilized to get it passed. Activist constituencies move policy.

I find the disclosure argument partially persuasive. I find the aligned-interests-produce-good-policy argument unpersuasive in this context. The relevant question is not whether the policy is good in some abstract sense, but whether the rate at which the Federal Reserve will price emergency liquidity to non-bank master-account holders is set in the interest of the median taxpayer or in the interest of stablecoin issuers. The political economy of the rate-setting decision is what is at stake, and the rate-setting decision has not yet been made.

---

## Part 6. What I do not know

This section is not optional reading. The integrity of what I have argued depends on knowing where the seams are.

I do not know what subsidy rate the Federal Reserve will set when extending emergency liquidity to non-bank master-account holders. I have used 30 basis points based on the BTFP precedent. The actual rate could be higher or lower, and the welfare result depends on it.

I do not know whether the regional Reserve Banks will be granted independent authority to act on master-account applications. Section 4(b)(iv) of the order asks this question; the Federal Reserve Board's 120-day report will answer it. If the answer is yes, twelve regional decision-makers will determine the size and composition of the new non-bank master-account class. If the answer is no, the Federal Reserve Board centralizes the decision, with predictable institutional incentives.

I do not have a structurally identified counterfactual for the post-EO peg path. My Bayesian counterfactual integrates over a sensitivity-ratio mapping that is derived from the global-game mechanism but not empirically tested against post-EO data, because no such data exists yet. The 90 percent credible interval on the post-EO trough is [0.951, 0.985], but the coverage of the posterior predictive band on the historical USDC episode is only 0.44 against a nominal 0.90. That is reduced-form misspecification, and I have disclosed it.

I do not know the full text of the Sacks ethics waiver, because it has not been released. I do not know the specific terms of the Tether loan that reportedly financed part of the Lutnick family Cantor acquisition. I do not know what will happen if the Custodia certiorari petition is granted by the Supreme Court (it has not been docketed as of this writing). I do not know the full membership of Fairshake's affiliated PACs, because some affiliates do not appear in the obvious FEC searches.

If you would like to expand any of these, please do. I will incorporate verified additions in subsequent versions of this note and credit the source.

### Open questions for the reader

1. **The Fed reaction function.** What is the right rate at which the Federal Reserve should lend to a non-bank stablecoin issuer in stress, and what collateral haircut should apply? The order does not specify. What would you propose?

2. **The decentralization question.** If each of the twelve regional Reserve Banks can independently calibrate master-account access, what aggregation rule preserves coherent monetary policy implementation? Is there a precedent for this kind of federalized regulatory authority?

3. **The international competition question.** Other major-economy jurisdictions (EU, UK, Japan, Singapore, Hong Kong) explicitly do not give stablecoin issuers direct central-bank access. They require bank intermediation. The US is moving in a different direction. Is the US choice driven by considered policy or by regulatory capture? How would you distinguish empirically?

4. **The conflict-of-interest threshold.** At what level of personnel financial entanglement would a regulatory action like EO 14405 cross from legitimate policymaking into corrupt favor? Where do you place the documented relationships above on that spectrum?

5. **The MAGA-rhetoric question.** Direct master-account access for non-bank fintechs is an idea with serious intellectual defenders going back at least to the 2018 TNB USA narrow-bank case. It is not inherently a populist or partisan idea. Why has it become bundled with the broader political-economic alignment described in Part 5? Is the bundling load-bearing or coincidental?

---

## Part 7. How to disagree with me

I will list six specific ways the analysis above could be wrong. If you find any of them are right, I will revise.

**One.** The contagion model could be misspecified in ways the moment-matching diagnostic does not detect. The posterior predictive coverage is 0.44 against a nominal 0.90, which is a real warning sign. A richer model that captures plateau dynamics, primary-market suspension effects, and DAI-USDC PSM dynamics in continuous time would produce a different counterfactual. I have used a stylized model and disclosed its limitations.

**Two.** The placebo test could be confounded. I shocked MMF_PRIME and reported zero regime difference, which I interpret as confirming the bank-stablecoin channel identification. But a more aggressive placebo (a shock to the COINBASE node, or to a non-bank custodian) might produce a non-zero regime difference, indicating a broader diffuse-panic channel that I have not modeled.

**Three.** The welfare comparison depends on social weights and on the implicit subsidy rate. Both are policy choices, not facts. If you put very heavy weight on systemic-fiscal-risk-bearing, the order looks worse than I have presented it. If you assume the Fed will price the subsidy at the risk-fair rate (which is a defensible assumption if Federal Reserve operating discipline holds in stress, and an indefensible one if it does not), the order looks better.

**Four.** The conflict-of-interest pattern documented in Part 5 is largely about Trump-family and administration-aligned actors. A symmetric review of the previous administration's relationships with the same industry would also identify financial connections, including the largest crypto donor in the 2020 cycle (FTX's Sam Bankman-Fried, later convicted) and various ETF-issuance-related lobbying. The pattern of regulatory interest converging with industry interest is not partisan; what is partisan is which industry interests are aligned with which political coalition at a given moment.

**Five.** The Page-Gong (2016) endogenous-network-formation result that I cite in the methods appendix is fragile. The DSG framework requires equilibrium uniqueness for the comparative-statics claim to bind, and discounted-stochastic-game equilibria can be non-unique under realistic parameter sets. The qualitative conclusion (the pre-EO and post-EO networks are different DSG equilibria) is robust, but the specific equilibrium I solve for is one of several possible. A different equilibrium selection rule could change the result.

**Six.** I have not done an event-study analysis of the Kraken Financial Limited Purpose Master Account approval on March 4, 2026. That approval is a candidate natural experiment, and a difference-in-differences design with appropriate control firms would identify the local-average-treatment-effect of master-account access on observable risk metrics. I have not done that because the post-approval window is short and the data is limited, but it is feasible and should be done. If you do it before I do, I will cite you.

---

## Part 8. Synthesis

EO 14405 is a topology shift on the financial-network exposure graph. It systematically reduces stablecoin run risk in every standard contagion metric, by removing commercial-bank intermediation between stablecoin issuers and the Federal Reserve. The reduction is real and large. The Wasserstein-1 run severity falls by 95 percent. The Eisenberg-Noe amplification falls from 1.27 to 1.00. The global-game run probability falls from 0.90 to 0.18. The spectral radius falls from 0.87 to 0.42. The technical case for the order's contagion-reducing effects is solid.

The complication is that absorption of stress shifts location rather than vanishing. The Federal Reserve's balance sheet replaces the commercial banking system as the counterparty whose policy choices determine whether a stablecoin redemption shock produces a depeg. Whether this is a net welfare improvement depends on the rate at which the Federal Reserve will price the implicit liquidity backstop, which the order does not specify and which has not yet been determined. Under my baseline calibration the order is welfare-improving under equal Negishi-Pareto weights. Under heavy taxpayer weighting it is welfare-degrading.

The political-economy facts documented in Part 5 do not invalidate the technical analysis. They do situate the implementing decisions in an institutional environment in which several of the actors who will set the operative parameters have direct financial relationships with the policy beneficiaries. The 120-day Section 4(b) report will be drafted under a Federal Reserve chair appointed by the same administration that signed the order. That is not corruption per se. It is a pattern that should be disclosed alongside the welfare analysis, because the welfare conclusion is sensitive to choices that those institutional actors will make.

I think the order is, on net, more likely to be welfare-degrading than welfare-improving in the medium term. I hold this view with moderate confidence. I could be persuaded otherwise by (a) a credible ex-ante framework from the Federal Reserve specifying the conditions under which it will extend emergency liquidity to non-bank master-account holders, (b) evidence that the regional Reserve Banks are calibrating master-account decisions to risk profile rather than to political-economy pressure, and (c) demonstration that the welfare loss to taxpayers from implicit subsidy is empirically small in the relevant range. None of those conditions are yet met. If they become met, I will update.

Even if my view is wrong, the more important point is that you now have the tools to form your own view. The code is open. The dossiers are open. The calibration is documented. The verification exercises are concrete. If your conclusion is different from mine, I would like to hear it, and I would like to know which step in the chain you stopped agreeing with me.

---

## Method appendix

The full computational appendix is at [github.com/ihelfrich/eo14405-contagion](https://github.com/ihelfrich/eo14405-contagion). The structure:

- `paper.md`: the formal working paper version of this note with propositions, proofs, and full references
- `src/`: Python modules for the four analytical frameworks (`clearing.py`, `global_game.py`, `ot_dynamics.py`, `spectral.py`), the Bayesian module (`bayes.py`), the welfare module (`welfare.py`), the Page-Gong endogenous-network module (`page_gong.py`), the diagnostics module (`diagnostics.py`), and the orchestrator (`analyze.py`)
- `src/figures.jl`: the Julia/CairoMakie figure pipeline (Helfrich palette)
- `dossiers/`: six OSINT files on the principals (Trump-WLFI, Sacks-a16z-Quintenz, Circle-Coinbase, Tether-iFinex, Custodia-Wyoming-SPDI, Fairshake-PAC) plus the synthesis (`SYNTHESIS.md`)
- `data/canonical_citations.md`: pinned source list

To reproduce the analysis:

```bash
git clone https://github.com/ihelfrich/eo14405-contagion
cd eo14405-contagion
pip install matplotlib networkx numpy scipy POT
python src/analyze.py        # produces figure + numerical output
python src/diagnostics.py    # moment-match + placebo + robustness
python src/page_gong.py      # endogenous-network DSG check
```

If you build a derivative analysis from this code, please credit it. If you find a bug, file an issue at [github.com/ihelfrich/eo14405-contagion/issues](https://github.com/ihelfrich/eo14405-contagion/issues).

---

## A closing note about how I wrote this

You may have noticed that I have repeatedly invited you to disagree with me. That is not a rhetorical flourish. It is the central design choice of this note.

Contemporary public argument is mostly transactional. The author has a conclusion. The reader is asked to accept the conclusion. The author signals authority through credentials, tone, and selective citation. The reader's role is to be persuaded.

I think this format is exhausting and corrosive. It is also part of why political discourse in the era of populist rhetoric has become so brittle. When everything you read is trying to sell you a conclusion, you learn either to accept conclusions uncritically (and become a follower of someone) or to reject conclusions reflexively (and become unable to learn from anyone). Neither is a healthy intellectual posture.

The alternative I am trying to model here is a research note in which the author shows the work, marks the seams, hands the reader concrete tools to verify or disagree, and treats the reader as a colleague rather than a customer. This is not a new format. It is the format of good scientific papers, good investigative journalism, and a small handful of public intellectuals who have managed to maintain it. I am not claiming to have done it well. I am claiming that the attempt is worthwhile.

If the format works for you, please tell me, and tell me what could be better. If the format does not work, please tell me that too. The point of public writing is not to produce agreement; it is to produce shared understanding, which is a different thing.

If you take one thing from this note, take the exercises. They are the part that actually transfers competence. The arguments will become obsolete; the practice of verifying primary sources will not.

Thank you for reading.

---

*This research note is released under CC BY 4.0. The underlying code is MIT-licensed. Cite as: Helfrich, Ian. 2026. "Direct Federal Reserve Access for Stablecoins, Considered Slowly: A Research Note on EO 14405." Available at github.com/ihelfrich/eo14405-contagion.*
