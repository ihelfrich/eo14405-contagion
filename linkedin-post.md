# Notes on Executive Order 14405
## Master account access and stablecoin run dynamics

*For LinkedIn. The first three lines below are what appears before "see more." Graphic markers in [BRACKETS]. Tag placeholders marked with [@] where the actual LinkedIn @-handle should go before posting.*

---

**Trump signed Executive Order 14405 on May 19, 2026.**

It directs the Federal Reserve to consider giving stablecoin issuers and other non-bank fintechs direct access to its payment system. Every standard contagion metric in my model improves substantially.

Then I checked who's writing the rules.

---

To give the economist in me room to breathe, I'm starting with the academic. If you'd rather watch paint dry than read a researcher whinging, the takeaway is at the bottom under "TL;DR." No harm. I just find that clickbait titles and damnable Bottom-Line-Up-Front communication have eroded the average person's ability to read beyond the headline, and I'd rather be long-winded than dishonest.

For the five of you still here:

**Executive Order 14405**, signed on May 19, 2026 and published at **91 FR 30475** (that is the Federal *Register* citation, volume 91, page 30475, not the Federal Reserve, yes I know that is confusing, and yes I almost made the same mistake), directs the Federal Reserve to evaluate direct master-account access for non-bank fintech firms and stablecoin issuers within 120 days, with a 90-day adjudication clock for individual applications.

It is being presented as a deregulatory action favoring the crypto industry. That framing is incomplete and, I would argue, deliberately incurious. The structural picture is more interesting.

Over the past two weeks I built a four-framework network-contagion model calibrated against the USDC depeg of March 2023, running the same shock under two regimes:

1. the current bank-deposit-intermediation system, and
2. the regime EO 14405 moves us toward, in which stablecoin issuers hold reserves directly at the Federal Reserve.

All four frameworks converged on a single finding.

**Direct master-account access reduces stablecoin run risk along every standard metric.**

For the empirically-inclined, the verified numbers:

- Wasserstein-1 run severity falls by approximately **95 percent** (0.82 to 0.04 bp-mass)
- Eisenberg-Noe contagion-amplification index falls from **1.27 to 1.00**
- Model-implied run probability falls from **0.90 to 0.18** under a common public prior
- Perron-Frobenius spectral radius of the loss-feedback operator falls from **0.87 to 0.42**

The reduction is both large and uniform.

**[GRAPHIC 1: `figures/linkedin_hero.png`, the four-metric bar chart in the heritage palette. This is what readers see in the LinkedIn preview card. Insert here.]**

I'm proud of that headline because it is mine, incomplete, and entirely misleading.

Why? Because the same model shows that the absorption mechanism does not vanish under the new regime. It changes its mailing address.

In the current system, a stablecoin redemption shock transmits to commercial bank shareholders. SVB shareholders lost approximately \$40 billion in March 2023, and that loss absorbed a substantial share of the spillover that would otherwise have hit USDC holders. Under EO 14405's new regime, that absorption transfers to the Federal Reserve's balance sheet, where the cost depends entirely on the rate the Fed charges for emergency liquidity to non-bank master-account holders.

In plain English: fintech bro messes up, fintech bank goes boom, and *the Federal Reserve* now eats the spillover directly instead of bank shareholders.

In my baseline calibration that subsidy is small (approximately 30 basis points on \$12 billion of exposure, or \$36 million). If the actual subsidy rate is 100 basis points, which is closer to historical lender-of-last-resort facilities during stress, the welfare conclusion under equal Negishi-Pareto weights flips. The order does not specify the rate. The Federal Reserve Board sets it.

**[GRAPHIC 2: `figures/analysis_helfrich.png`, the nine-panel publication figure showing all four analytical frameworks side by side. Insert here so the empirically-inclined reader sees the apparatus.]**

So who sets the rate?

**Kevin Warsh.** Confirmed Federal Reserve Chair on May 13, 2026.

His OGE-278 disclosure of April 10, 2026, with an amended ethics agreement of April 17, reports two Duquesne Capital "Juggernaut Fund" limited-partnership positions each in the "Over \$50,000,000" bracket. That is a floor sum of \$100 million. He also discloses equity in over twenty additional blockchain and digital-asset firms.

The OGE's verbatim compliance language reads: *"in compliance for all lines except [enumerated lines]; once the filer divests these assets, he will be in compliance."* His ethics agreement commits him to divest "as soon as practicable but not later than ninety days after my confirmation." That deadline is **August 11, 2026**.

Between his confirmation on May 13 and his divestiture deadline on August 11, any Federal Reserve Board vote on master-account access under Section 4 of the order is being taken by a chair holding disclosed equity in the directly affected sector.

He is not alone.

**William Pulte**, FHFA Director. Holds Bitcoin and Solana each in the \$500,001 to \$1,000,000 bracket plus MARA Holdings common stock in the \$5,000,001 to \$25,000,000 bracket. He issued the June 25, 2025 FHFA directive ordering Fannie Mae and Freddie Mac to consider crypto as eligible mortgage reserves while holding those positions. No recusal endnote.

**Kevin Hassett**, NEC Director. Holds \$1,000,001 to \$5,000,000 in Coinbase Class A common stock while chairing the White House Digital Assets Working Group. Immediately before NEC, he received \$50,001 from Coinbase Asset Management's Academic and Regulatory Advisory Council from March 2021 to January 2025.

**Cynthia Lummis**, Senate Banking Digital Assets Subcommittee Chair. Holds approximately 5 BTC personally per her Senate STOCK Act periodic transaction reports. Sponsored the BITCOIN Act. Co-sponsored GENIUS.

**Andy Barr**, House Financial Services. Fairshake and its affiliate Defend American Jobs spent \$7.2 million in independent expenditures supporting his 2024 reelection. Crypto.com's Foris DAX entity contributed \$2.36 million to his "Keep America Great PAC" for the 2026 Kentucky Senate primary. Concurrent service. Disclosed.

**Bernie Moreno**, who defeated the sitting Senate Banking Committee Chair Sherrod Brown with \$40.1 million in Defend American Jobs spend against Brown.

**Howard Lutnick**, Commerce Secretary. Per the Wall Street Journal of November 24, 2024, Cantor Fitzgerald, the Lutnick family investment bank, acquired an approximately 5 percent equity stake in Tether via a roughly \$600 million convertible bond and reportedly financed part of the Lutnick family Cantor acquisition (through Dynasty Trust A) with a Tether loan. The Q1 2026 BDO attestation confirms Tether's reported \$141 billion in U.S. Treasury reserves; the Cantor-custodian attribution is press-sourced. Tether's US-compliant sibling **USAT** launched January 27, 2026 through Anchorage Digital Bank, the OCC-chartered trust company whose charter is itself the pathway to master-account eligibility under EO 14405.

**World Liberty Financial**, issuer of the USD1 stablecoin. Per SEC Form D/A (CIK 0002043140), Delaware-incorporated, Miami office, \$52,133,139 cumulative Reg-D sales across 1,966 investors. USD1's custodian BitGo Trust converted from South Dakota state-chartered to OCC national trust bank in December 2025 and is master-account-eligible under Section 4. The Trump-family revenue chain through DT Marks DEFI LLC (a reported 75 percent protocol-revenue claim) is press-sourced, not in primary SEC filings.

I built a 153-node social network of these documented relationships. The full analysis is at github.com/ihelfrich/eo14405-contagion. I expected to find a small minimum-cut spine, meaning that removing four or five named officials would disconnect the Trump cluster from the Federal Reserve cluster from the stablecoin-issuer cluster. **I was wrong.**

The network is structurally redundant. Removing Warsh, Pulte, Hassett, Lutnick, and Quintenz would not fragment it. Marc Andreessen and Ben Horowitz each personally gave \$2.5 million to Trump-supporting super-PACs in 2024. The Trump v. Cook litigation at the Supreme Court connects Trump directly to a sitting Fed Governor. These edges create alternative paths between the three clusters that survive removal of the named officials.

**The conflict architecture cannot be unwound by replacing five people. The structure of the edges is what would have to change.**

That finding is the most uncomfortable thing the analysis produced and the most important.

**[GRAPHIC 3: `figures/sna_nexus.png`, the Trump-Fed-Stablecoin spine subgraph. This is your viral image. Insert here.]**

None of these facts invalidates the technical contagion finding. The contagion analysis is robust to deltas in the initial conditions. The political-economy context affects how the welfare conclusion should be interpreted by an institutional actor, Federal Reserve staff, congressional staff, the press, you, me, who has to decide whether the order is, on net, a good idea.

I think it is more likely to be welfare-degrading than welfare-improving in the medium term, with the loss falling on taxpayers and the gain accruing to a narrow set of well-connected issuers. I hold this view with moderate confidence.

Most Americans have not been given a working model of how the monetary system operates. That is not a failure of the public. It is an asymmetry that benefits whoever is making the decisions, and the decisions are about to be made.

I could be persuaded otherwise by:

1. A credible ex-ante framework from the Federal Reserve specifying the conditions under which it will extend emergency liquidity to non-bank master-account holders, at what rate, against what collateral, with what disclosure.
2. Evidence that the regional Reserve Banks are calibrating master-account decisions to risk profile rather than political-economy pressure.
3. Demonstration that the welfare loss to taxpayers from implicit subsidy is empirically small in the relevant range.

I won't hold my breath.

To **[@Federal Reserve Board]**, **[@Kevin Warsh]**, **[@U.S. Senate Committee on Banking, Housing, and Urban Affairs]**, **[@U.S. House Committee on Financial Services]**: the work below is open. If the analysis is wrong, the data are reproducible and I will fix what is wrong. If the analysis is right, the framework I am asking for is what comes next, and waiting until after the first stablecoin redemption event to specify it is the worst available outcome.

---

**TL;DR**

EO 14405 measurably reduces stablecoin run risk by every standard contagion metric. It does this by relocating the loss-absorption mechanism from commercial bank shareholders to the Federal Reserve's balance sheet, where the implicit subsidy depends on a rate the Fed has not yet specified. That rate will be set by a chair confirmed under his own \$100M+ divestiture timeline, in an administration whose family financial interests run directly through the largest beneficiary. The conflict architecture is structurally redundant, meaning removing any small set of named officials does not fix it.

**The Federal Reserve must publish its ex-ante liquidity-extension framework before the first non-bank master account is operational. Not after.**

Full technical paper, twelve source-cited OSINT dossiers, six independent validation files, a 153-node social-network analysis, and a fully reproducible computational appendix in Python and Julia are at **ihelfrich.github.io/eo14405-contagion**. All code and data are open. If you find an error, please file an issue. I will fix or acknowledge.

*Ian Helfrich, Ph.D. Economics, Georgia Tech 2024. Independent researcher. No financial interest in any entity discussed.*

#FederalReserve #StablecoinPolicy #EO14405 #FinancialStability #MonetaryPolicy
