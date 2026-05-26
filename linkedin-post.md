# Notes on Executive Order 14405
## Master account access and stablecoin run dynamics

*~700 words. For LinkedIn or other short-form contexts. Companion long-form research note at [github.com/ihelfrich/eo14405-contagion](https://github.com/ihelfrich/eo14405-contagion). Single image: `figures/analysis_helfrich.png`.*

---

Executive Order 14405, signed May 19, 2026 and published at 91 FR 30475, directs the Federal Reserve to evaluate direct master-account access for non-bank fintech firms and stablecoin issuers. The order is being read as a deregulatory action favoring the crypto industry. The structural picture is more interesting.

I spent the last two weeks building a network-contagion model calibrated against the USDC depeg of March 2023. The model runs the same shock under two regimes: the current bank-deposit-intermediation system and the regime the order operationalizes, in which stablecoin issuers hold reserves directly at the Federal Reserve. Four analytical frameworks converged on a single finding.

Direct master-account access reduces stablecoin run risk along every standard metric. The Wasserstein-1 run severity falls by approximately 95 percent. The Eisenberg-Noe contagion-amplification index falls from 1.27 to 1.00. The model-implied run probability falls from 0.90 to 0.18. The Perron-Frobenius spectral radius of the loss-feedback operator falls from 0.87 to 0.42. The reduction is large and uniform.

This is the headline finding. It is also incomplete.

The same model shows that the absorption mechanism does not disappear under the new regime. It moves. In the current system, a stablecoin redemption shock transmits to commercial bank shareholders. SVB shareholders lost approximately \$40 billion in March 2023, and that loss absorbed a substantial share of the spillover that would otherwise have hit USDC holders. Under the post-EO regime, the absorption transfers to the Federal Reserve's balance sheet, where the implicit subsidy depends on the rate the Fed charges for emergency liquidity. In my baseline calibration this subsidy is small (approximately 30 basis points on \$12 billion of exposure, or \$36 million). If the actual subsidy rate is 100 basis points, which is closer to historical lender-of-last-resort facilities during stress, the welfare conclusion under equal Negishi-Pareto weights flips.

The political-economy context matters here, and the validation-pass primary sources are stronger than I initially thought. Chair Kevin Warsh's OGE-278 disclosure documents two Duquesne "Juggernaut Fund" LP positions each in the "Over \$50,000,000" bracket plus equity in over twenty additional blockchain firms, divestiture due 2026-08-11. FHFA Director William Pulte holds Bitcoin and Solana while having issued the June 25, 2025 directive on crypto as mortgage reserves. NEC Director Kevin Hassett holds \$1-5M in Coinbase Class A common while chairing the White House Digital Assets Working Group. The principal direct beneficiary of EO 14405 is a stablecoin issuer in which the President's family holds the contractually-reported (press-sourced) majority revenue claim, with USD1's custodian BitGo converted to OCC trust-bank status in December 2025. The Commerce Secretary's family investment bank holds an approximately five percent equity stake in Tether per WSJ reporting of November 24, 2024. The Fairshake PAC complex and its affiliates spent approximately \$196 million in the 2023-2024 cycle (\$260M raised), achieving 53 wins of 58 targeted races, including the defeat of the sitting Senate Banking Committee chair.

None of these facts invalidates the technical finding. The contagion analysis is robust. The political-economy context affects how the welfare conclusion should be interpreted by an institutional actor (Federal Reserve staff, congressional staff, the press, or you) who has to decide whether the order is, on net, a good idea.

I think the order is more likely to be welfare-degrading than welfare-improving in the medium term. I hold this view with moderate confidence. I could be persuaded otherwise by a credible ex-ante framework from the Federal Reserve specifying the conditions under which it will extend emergency liquidity to non-bank master-account holders, evidence that the regional Reserve Banks are calibrating master-account decisions to risk profile rather than political-economy pressure, and demonstration that the welfare loss to taxpayers from implicit subsidy is empirically small in the relevant range.

Full technical paper, six source-cited OSINT dossiers on the principals, computational appendix in Python and Julia, and an interactive blog research note with reader exercises are at the link above. All code and data are open. If you find an error, please file an issue rather than tweet about it; I will fix or acknowledge.

---

*Ian Helfrich, Ph.D. Economics, Georgia Tech 2024. Independent researcher. No financial interest in any entity discussed.*
