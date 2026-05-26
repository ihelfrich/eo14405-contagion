# Outreach kit

*For readers who want to share this work and for me to keep track of who needs to see it. Everything below is open. Reuse without attribution if it helps. Modify the templates freely; they are starting points, not scripts.*

---

## What this is

A research artifact on Executive Order 14405 and what direct Federal Reserve master-account access means for stablecoin contagion risk and for the political-economy of who sets the rules. Three layers:

1. The [research note](index.html) (~5,700 words, Socratic, designed for a colleague)
2. The [working paper](paper.html) (~7,000 words, formal, with proofs)
3. The [LinkedIn-format short version](short.html) (~1,400 words, designed to travel)

Plus twelve OSINT dossiers, a 153-node social-network analysis, a six-stream validation pass, and a fully reproducible computational appendix.

The [verification table](verify.html) maps every numeric and factual claim in the short version to a primary-source URL. If you want to check a claim, start there.

---

## Pull quotes (use anywhere)

**On the headline finding:**
> Direct master-account access reduces stablecoin run risk along every standard metric. The reduction is both large and uniform.

**On the catch:**
> The absorption mechanism does not vanish under the new regime. It changes its mailing address.

**On the rate-setting problem:**
> The welfare conclusion depends on a rate the order does not specify. The Federal Reserve Board sets it.

**On the timing:**
> Between his confirmation on May 13 and his divestiture deadline on August 11, any Federal Reserve Board vote on master-account access under Section 4 of the order is being taken by a chair holding disclosed equity in the directly affected sector.

**On the structural problem:**
> The conflict architecture cannot be unwound by replacing five people. The structure of the edges is what would have to change.

**On the institutional ask:**
> The Federal Reserve must publish its ex-ante liquidity-extension framework before the first non-bank master account is operational. Not after.

---

## Tag list (LinkedIn @-handles to include)

Confirmed institutional handles (verified existing on LinkedIn as of 2026-05-26):

- **@Federal Reserve Board**, the rule-setter
- **@Federal Reserve Bank of New York**, operational counterparty for master accounts
- **@U.S. Senate Committee on Banking, Housing, and Urban Affairs**, Chair Scott
- **@U.S. House Committee on Financial Services**, Chair French Hill
- **@U.S. Government Accountability Office**, GAO has open work on stablecoin oversight
- **@Office of Financial Research**, OFR has a published interest in stablecoin contagion
- **@Federal Deposit Insurance Corporation**
- **@Office of the Comptroller of the Currency**

Individual handles to consider tagging (use sparingly; tag the institution, not the person, when uncertain):

- **@Kevin Warsh**, Fed Chair, has a public LinkedIn presence
- **@Sherrod Brown**, former Senate Banking Chair, may amplify
- **@Elizabeth Warren**, Senate Banking, has already opened a parallel investigation

Press and research handles for amplification:

- **@Bloomberg** / **@Bloomberg Opinion**
- **@The Wall Street Journal**
- **@Financial Times**
- **@Reuters**
- **@The Wharton School** (Wharton Public Policy Initiative writes on this)
- **@Brookings** (Hutchins Center on Fiscal & Monetary Policy)
- **@Peterson Institute for International Economics**

Do not auto-tag every name on this list in a single post. Pick the three or four most relevant for the specific angle you are sharing.

---

## Hashtag strategy

Primary (use on every post):
`#FederalReserve` `#StablecoinPolicy` `#EO14405` `#FinancialStability` `#MonetaryPolicy`

Secondary (rotate based on the specific finding being highlighted):
`#Crypto` `#CentralBanking` `#MasterAccount` `#ConflictOfInterest` `#PoliticalEconomy` `#NetworkAnalysis` `#PublicChoice`

Do not use more than seven hashtags on a single LinkedIn post. The platform downranks posts with eight or more.

---

## Share copy variants

### LinkedIn long-form
Use the full [short.html](short.html) version. Already optimized for LinkedIn preview cards (1200x627 hero image, three-line above-the-fold hook).

### LinkedIn short-form (text-only update)
> EO 14405 measurably reduces stablecoin run risk on every standard contagion metric. It does this by relocating loss absorption from commercial bank shareholders to the Federal Reserve. The implicit subsidy depends on a rate the Fed has not yet specified.
>
> The chair who will set the rate was confirmed on May 13 holding \$100M+ in directly affected positions, with a divestiture deadline of August 11.
>
> Full analysis, twelve dossiers, 153-node network, reproducible code: ihelfrich.github.io/eo14405-contagion

### X / Twitter (280 chars)
> EO 14405 cuts stablecoin run risk by 95%. It does so by moving the loss to the Fed's balance sheet at a rate the Fed has not specified. The chair who sets the rate holds disclosed positions in the affected sector through Aug 11.
>
> ihelfrich.github.io/eo14405-contagion

### Bluesky / Mastodon (300 chars)
> New research: EO 14405 reduces stablecoin run risk by every standard contagion metric, but the welfare conclusion flips at a Fed lender-of-last-resort rate the order does not specify. The chair who will set that rate is in his divestiture window.
>
> Full code + data: ihelfrich.github.io/eo14405-contagion

### Text-message version (for one-to-one sharing)
> EO 14405: technical finding holds (it does reduce contagion), but the absorption mechanism moves to the Fed at a rate the Fed sets, and the chair who will set the rate is mid-divestiture. ihelfrich.github.io/eo14405-contagion

---

## Email draft: Fed Reserve Bank or Board staff

Subject: `EO 14405 contagion analysis, request for Federal Reserve ex-ante LOLR framework`

> Dear [staff name],
>
> I am Dr. Ian Helfrich, an independent researcher with a 2024 Georgia Tech economics PhD. I have completed a four-framework contagion analysis of EO 14405 calibrated against the USDC March 2023 episode and posted the full reproducible artifact at ihelfrich.github.io/eo14405-contagion.
>
> The headline finding is that direct Federal Reserve master-account access for non-bank issuers reduces stablecoin run risk on every standard metric. The Wasserstein-1 run severity falls by approximately 95 percent in the calibrated counterfactual.
>
> The second-order finding is that the loss-absorption mechanism does not disappear under the new regime. It transfers to the Federal Reserve's balance sheet, where the welfare cost depends on the rate the Federal Reserve charges for emergency liquidity to non-bank master-account holders. The order does not specify that rate. At 30 basis points the net welfare conclusion is mildly positive; at 100 basis points it flips. The figure at [figures/sensitivity_lolr.png](figures/sensitivity_lolr.png) shows the break-even at approximately 133 basis points.
>
> I am writing to ask whether the Federal Reserve plans to publish an ex-ante framework specifying the conditions under which it will extend emergency liquidity to non-bank master-account holders, at what rate, against what collateral, with what disclosure, before the first such account is operational.
>
> If the framework already exists in a non-public form, I would be grateful for any pointer to the publication timeline. If the framework does not yet exist, the request in the attached short version of my work is that the Federal Reserve publish one before the first non-bank master account becomes operational.
>
> The full computational appendix is open. If any of my numerical results disagree with Federal Reserve internal calibrations I would be grateful to know how, and I will correct any error.
>
> Best,
> Ian
> ianthelfrich@gmail.com · ianhelfrich.com

### Email draft: Senate Banking or House Financial Services staff

Subject: `EO 14405 contagion analysis, for committee record`

> Dear [staff name],
>
> I am Dr. Ian Helfrich, an independent economist. I have completed an analysis of EO 14405's effect on stablecoin run risk and the political-economy structure surrounding its implementation. The full work is at ihelfrich.github.io/eo14405-contagion.
>
> Three findings I think are relevant to the committee:
>
> 1. The contagion-reduction claim made by EO 14405 supporters is correct. Direct Federal Reserve master-account access reduces stablecoin run risk substantially.
>
> 2. The implicit-subsidy cost depends on a Federal Reserve emergency-liquidity rate that the order does not specify. The break-even rate above which the welfare conclusion flips is approximately 133 basis points, well within the historical range for stress-period discount-window facilities.
>
> 3. The principals who will set the rate hold disclosed equity in the directly affected sector. The Federal Reserve Chair is in a 90-day divestiture window that closes 2026-08-11. The FHFA Director, NEC Director, and Commerce Secretary have parallel disclosed positions. Removing any small set of officials does not fragment the conflict-of-interest network; the structural redundancy is documented in the 153-node social-network analysis in the repository.
>
> The verification table at ihelfrich.github.io/eo14405-contagion/verify.html maps every numerical claim to a primary-source URL (OGE-278 filings, SEC EDGAR, FEC, Federal Register, congressional STOCK Act PTRs).
>
> If the committee staff would find a briefing memo or testimony useful, I am available pro bono.
>
> Best,
> Ian
> ianthelfrich@gmail.com · ianhelfrich.com

### Email draft: press or research contact

Subject: `Open research: EO 14405 contagion + political-economy`

> Hi [name],
>
> I wanted to send you something I've been working on: ihelfrich.github.io/eo14405-contagion.
>
> Short version: EO 14405 reduces stablecoin run risk on every standard contagion metric. It does so by moving the loss-absorption mechanism from commercial bank shareholders to the Federal Reserve's balance sheet at a rate the Fed has not specified and that the order does not bind. The chair who will set the rate, Kevin Warsh, has disclosed >\$100M in directly affected positions and a divestiture deadline of August 11, 2026. The conflict-of-interest network has 153 documented nodes and is structurally redundant: removing any small set of named officials does not fragment it.
>
> Twelve OSINT dossiers source-cite the political-economy findings. Six independent validation streams cross-check the OGE filings, congressional disclosures, WLFI SEC Form D/A, Cantor-Tether reporting, and SNA methodology. The verification table at ihelfrich.github.io/eo14405-contagion/verify.html maps every claim to a primary-source URL.
>
> Happy to walk through it. No paywall, no attribution required.
>
> Best,
> Ian

---

## Image assets ready for use

Each of these is 1200x627 (LinkedIn preview-card aspect), heritage palette, mobile-readable in three seconds:

- [`figures/li_mechanism.png`](figures/li_mechanism.png), the loss-absorption mechanism (pre-EO vs post-EO arrows)
- [`figures/li_scorecard.png`](figures/li_scorecard.png), four contagion metrics, before / after, percent reduction
- [`figures/li_spine.png`](figures/li_spine.png), the five-person spine connecting Trump cluster, Fed cluster, stablecoin-issuer cluster
- [`figures/sensitivity_lolr.png`](figures/sensitivity_lolr.png), net welfare as a function of the Fed LOLR rate, with break-even and historical anchors
- [`figures/linkedin_hero.png`](figures/linkedin_hero.png), original four-metric bar chart, slightly busier than scorecard
- [`figures/analysis_helfrich.png`](figures/analysis_helfrich.png), dense nine-panel publication figure; use when speaking to an empirically inclined audience

Direct CDN-stable URLs for embedding:
```
https://ihelfrich.github.io/eo14405-contagion/figures/li_mechanism.png
https://ihelfrich.github.io/eo14405-contagion/figures/li_scorecard.png
https://ihelfrich.github.io/eo14405-contagion/figures/li_spine.png
https://ihelfrich.github.io/eo14405-contagion/figures/sensitivity_lolr.png
```

---

## What I will not do

I will not pay for amplification. I will not gate any of this behind a Substack or a newsletter. I will not accept advertising on any page of this artifact.

If a journalist or a Fed staffer or a committee aide quotes from this work without attribution, that is fine. The point is the framework, not the byline.

If a journalist or a Fed staffer or a committee aide finds an error, please [file an issue](https://github.com/ihelfrich/eo14405-contagion/issues) or email me directly. I will fix or acknowledge in a public erratum on the landing page.

---

*Dr. Ian Helfrich, Ph.D. Economics, Georgia Tech 2024 · Independent researcher · No financial interest in any entity discussed.*
