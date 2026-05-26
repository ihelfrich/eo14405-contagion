# WLFI / USD1 deep-dive validation

Validator: senior OSINT pass for Dr. Ian Helfrich
Compiled: 2026-05-26
Scope: every load-bearing factual claim in `dossiers/trump-wlfi.md` and the WLFI sections of `dossiers/SYNTHESIS.md` and `dossiers/SNA-FINDINGS.md`, traced to a primary document where one exists.

## Methodology

For each claim I attempted, in order, to:

1. Pull the underlying SEC filing through `~/go/bin/forensic-econ edgar` (CIK 0002043140 for World Liberty Financial, Inc., CIK 0001849635 for Trump Media & Technology Group Corp.). Where possible I went straight to the XBRL-tagged values inside the filing's iXBRL document rather than to press paraphrases.
2. Where the claim concerns a congressional letter or committee action, retrieve the PDF directly from `banking.senate.gov` or the committee's own document store and convert with `pdftotext`.
3. Where the claim concerns an academic blog post, fetch the published URL.
4. Where no primary source is available (press-only reporting), note that explicitly and downgrade the claim's confidence accordingly.
5. For corporate-registry questions about BitGo's charter, I checked both BitGo's own corporate page and the OCC's announcement of charter conversion.

The CourtListener federal-docket pass failed because the local `forensic-econ` client lacks an API token. I substituted a press-confirmed docket location instead and flagged the case-number gap.

## Per-claim verification

### Corporate structure (Form D/A claims)

Primary source: SEC Form D/A, World Liberty Financial, Inc., accession `0002043140-25-000001`, filed July 3, 2025. Retrieved locally to `/tmp/wlfi_formd_2025/2025-07-03_D-A_xslFormDX01_primary_doc.xml`.

| Claim | Status | Notes |
|---|---|---|
| Delaware corporation, year of incorporation 2024 | CONFIRMED | Item 1: "Corporation" box checked, jurisdiction "DELAWARE", "Within Last Five Years" with year "2024" |
| CIK 0002043140 | CONFIRMED | EDGAR metadata via `forensic-econ edgar info` |
| Principal office 4400 Biscayne Boulevard, Suite 900, Miami, FL 33137 | CONFIRMED | Item 2 address fields confirm 4400 Biscayne Boulevard, Suite 900, Miami, Florida, ZIP 33137, phone 212-672-4700 |
| Officers and directors of record: Zachary Folkman and Chase Herro only | CONFIRMED | Item 3 lists only these two related persons, each with all three boxes (Executive Officer, Director, Promoter) checked |
| Folkman address in Dorado, Puerto Rico | CONFIRMED | "425 Carr 693 PMB 285, Dorado, PUERTO RICO, 00646" |
| Herro address in Dorado, Puerto Rico | CONTRADICTED | Herro's Item 3 address is "407 Ayre St. PMB #1358, Wilmington, DELAWARE, 19805", not Dorado. The dossier paragraph "Zachary Folkman ... listed address in Dorado, Puerto Rico) and Chase Herro (same combined roles)" reads as if both are in Dorado, which the filing does not support. Roles are identical; addresses are not. |
| Cumulative Reg-D sales of \$52,133,139 as of July 3, 2025 | CONFIRMED | Item 13 shows Total Offering Amount \$52,133,139, Total Amount Sold \$52,133,139, Total Remaining \$0 |
| 1,966 investors | CONFIRMED | Item 14 reports 1,966 total investors |
| Clarification note about a separate concurrent Regulation S offering | CONFIRMED | Item 13 clarification reads "The TAS excludes amounts offered and sold to non-US persons in a separate concurrent, offering consistent with Regulation S." |
| Above the operating corp sits WLF Holdco LLC, above that DT Marks DEFI LLC | NOT IN FORM D | The Form D names only the issuer. The Holdco / DT Marks chain is sourced to press (CNBC October 2024, Reuters March 2025) and to the April 2, 2025 Warren-Waters letter, which describes DT Marks DEFI LLC as "an entity affiliated with Donald J. Trump and certain of his family members." Acceptable as press-confirmed but not from a primary SEC filing. |

There is also a Form 3 on file, accession `0001104659-25-111655`, filed November 13, 2025, reporting beneficial ownership for issuer ticker **ALTS** with World Liberty Financial, Inc. listed as the reporting person, address 407 ARYE STREET, SUITE 1358, Wilmington, DE 19804, and event date August 12, 2025. The Form 3 is not about WLFI's own securities; it is WLFI reporting a 1,000,000-share position in a separate Alts-ticker issuer as Director plus Other. This is worth noting in the dossier and is currently not mentioned anywhere.

### Trump family revenue channel

| Claim | Status | Notes |
|---|---|---|
| DT Marks DEFI LLC holds a contractual right to 75% of WLF protocol revenues | PRESS-CONFIRMED, NO PRIMARY DOC | CNBC October 17, 2024 reported the 75% figure based on company gold-paper / token-sale terms. The Warren-Waters letter of April 2, 2025 paraphrases Reuters that "the Trump family has a claim on 75% of net revenues from token sales and 60% from World Liberty operations once the core business gets going". No SEC filing or contract directly establishes the 75%. Acceptable for the dossier; for the paper this should remain hedged as "according to company-published materials and reporting." |
| DT Marks DEFI LLC is 70% Donald Trump / 30% other family members | PRESS-CONFIRMED, NO PRIMARY DOC | Same source chain. The Warren-Waters letter cites only "affiliated with Donald J. Trump and certain of his family members" without percentages. The 70/30 split appears in secondary reporting and on Wikipedia; I could not find a primary disclosure. |
| WLF Holdco LLC equity stake "currently 38%, was 60%" | PRESS-CONFIRMED, NO PRIMARY DOC | The Block (2025) reported a roughly 20-point reduction to about 40%; Cryptonews and subsequent reporting put the current figure near 38%. There is no SEC primary filing where DT Marks DEFI LLC is named as an equity holder of WLF Holdco LLC. |

### USD1 stablecoin

| Claim | Status | Notes |
|---|---|---|
| Custodian is BitGo Trust | CONFIRMED via WLF marketing materials and BitGo press, but with a stale-status caveat below |
| BitGo Trust is South Dakota state-chartered | PARTIALLY CONFIRMED, NOW STALE | BitGo Trust Company, Inc. was originally a South Dakota state-chartered trust company. In December 2025 the OCC granted full unconditional approval to convert it to BitGo Bank & Trust, N.A., a federally chartered national trust bank (OCC NR 2025-125c; BitGo press of December 12, 2025). The dossier description "South Dakota state-chartered" is correct for the period in which USD1 launched but is no longer the current charter. The paper should say "originally South Dakota state-chartered; converted to OCC-chartered national trust bank effective December 2025" because that conversion changes the regulatory channel through which EO 14405 reaches USD1. |
| Launched 2025 | CONFIRMED | March 2025 launch on Ethereum and BNB Chain is press-consistent; New York Times "Trump's Crypto Venture Introduces New Digital Currency" (David Yaffe-Bellany, March 25, 2025) anchors the date. |
| Reserves managed by BlackRock; cash plus short-duration Treasuries | NOT IN PRIMARY SOURCE | This composition appears on the company website and in eco.com and CoinMarketCap explainers. No published independent attestation report (analogous to Circle's USDC monthly attestation by Deloitte) was located in this validation pass. Mark as "company-disclosed, not independently attested" in the dossier. |
| Circulating supply roughly \$2B late 2025, above \$4B by April 2026 | PRESS-CONFIRMED | CoinMarketCap profile and other tracker sites agree on the magnitude. Acceptable as a press claim. |

### House investigation

| Claim | Status | Notes |
|---|---|---|
| House investigation into an alleged \$500M, 49% UAE stake purchase | CONFIRMED with refinement | The House inquiry was opened by the **House Select Committee on the Chinese Communist Party**, ranking member Rep. Ro Khanna (D-CA), in a letter dated February 4, 2026. The dossier refers to it generically as a "House investigation" which is correct; for any paper-grade citation the committee name needs to be specified, because "House investigation" by default reads as House Financial Services or House Oversight, neither of which opened this probe. |
| WSJ original report on the deal | CONFIRMED | WSJ reported the deal in early February 2026 (the WSJ article itself is paywalled; CNN, The Block, Ledger Insights, and the House letter all reference and quote it). The deal: Aryam Investment 1 vehicle, \$500 million for 49% of WLFI, signed roughly four days before January 2025 inauguration, \$250M at signing and \$250M by mid-July 2025, with approximately \$187M of the first tranche flowing to Trump-family entities and approximately \$31M to Witkoff-family entities. Signed by Eric Trump. Closing terms remain confidential; the SEC Form D does not reflect this transaction. |

### DJT (Trump Media) crypto treasury

Primary source: Trump Media & Technology Group Corp. Q1 2026 10-Q, accession `0001140361-26-020229`, filed May 8, 2026 for the period ended March 31, 2026. Retrieved to `/tmp/djt_10q_q1_2026/2026-05-08_10-Q_ef20070602_10q.htm`.

| Claim | Status | Notes |
|---|---|---|
| 10-Q filed May 8, 2026 | CONFIRMED | EDGAR filing date matches |
| 11,542 BTC as of March 31, 2026 | CONTRADICTED | The XBRL-tagged value under `djt:DigitalAssetNumberOfUnits` for the Bitcoin row of the Note 4 Digital Assets table is **9,542.16 BTC**, identical to the December 31, 2025 figure (no net BTC purchases or sales in Q1 2026). The dossier figure of 11,542 BTC is off by roughly 2,000 BTC and is wrong. The 9,542.16 figure is the consolidated holdings. The filing also separately reports 4,260.73 BTC pledged as collateral to convertible notes and a covered-call position over 4,000 BTC with 2,000 BTC posted as collateral; none of those sum to 11,542. This appears to be a transposition or a confusion with an earlier reporting period. |
| 756,079,523 CRO (Cronos) as of March 31, 2026 | CONFIRMED | XBRL value 756,079,523.00, of which 615,984,303.6 is subject to contractual sale restriction. |
| Q1 2026 net loss of \$405.9M from crypto markdowns | CONFIRMED with mild refinement | XBRL-tagged `us-gaap:NetIncomeLossAvailableToCommonStockholdersBasic` is $(405,813.5) thousand for Q1 2026, which rounds to \$405.8M. The dossier's "\$405.9 million" is within rounding. Note that consolidated `us-gaap:NetIncomeLoss` (parent + noncontrolling) is $(387,849.8) thousand or \$387.8M; "net loss" can be quoted either way, so the dossier should specify "net loss available to common stockholders" for precision. |
| Net loss is "almost entirely unrealized losses on crypto" | DIRECTIONALLY CONFIRMED | The 10-Q's MD&A discussion of digital asset fair-value changes is the dominant driver of the loss; the exact share is computable from the filing's fair-value tables. The dossier's framing is acceptable but the precise number would require a one-line addition from the Note 4 fair-value reconciliation. |

### Senate Banking letter to SEC

Primary source: PDF retrieved from `https://www.banking.senate.gov/imo/media/doc/wlf_sec_letter.pdf` to `/tmp/senate_wlf_letter.pdf`, converted with `pdftotext` to `/tmp/senate_wlf_letter.txt`.

| Claim | Status | Notes |
|---|---|---|
| A Senate Banking letter to SEC regarding WLFI exists | CONFIRMED | Letter dated April 2, 2025, addressed to Hon. Mark T. Uyeda, Acting SEC Chairman |
| Letter author | REFINEMENT | The letter is jointly signed by **Sen. Elizabeth Warren** (Ranking Member, Senate Banking, Housing, and Urban Affairs) and **Rep. Maxine Waters** (Ranking Member, House Financial Services). The dossier's "Senate Banking Committee letter" is technically correct but undersells the joint Senate-House-minority character. |
| Substantive content | CONFIRMED | The letter explicitly requests preservation of all SEC records on WLF from October 15, 2024 forward, names President Trump, Donald Trump Jr., Eric Trump, Barron Trump, and DT Marks DEFI LLC as related persons of interest, and ties the inquiry to the SEC's reported pause of its case against Justin Sun in February 2025. |

### Duke FinReg analysis arguing WLFI satisfies Howey

| Claim | Status | Notes |
|---|---|---|
| Duke FinReg Blog post arguing WLFI is an unregistered security exists | CONFIRMED | URL `https://sites.duke.edu/thefinregblog/2026/05/08/is-wlfi-an-unregistered-security/` resolves, post title is "Is $WLFI an Unregistered Security?", author Lee Reiners, date May 8, 2026. The post applies Howey: investment of money in a common enterprise with expectation of profits from the essential managerial efforts of WLF (token freeze power, supply allocation, ecosystem development). |
| Characterization in the dossier as "Duke FinReg analysis" | CONFIRMED with refinement | This is a single-author blog post by Lee Reiners on the FinReg Blog hosted at Duke Law, not a peer-reviewed law-journal article. The dossier should describe it as "a Duke FinReg Blog post by Lee Reiners" rather than "Duke FinReg analysis" to avoid implying institutional weight beyond what a faculty blog carries. |

### Justin Sun litigation (mentioned in dossier under "Regulatory and enforcement timeline")

| Claim | Status | Notes |
|---|---|---|
| Sun filed suit against WLF in April 2026 alleging fraud, breach of contract, \$75M frozen tokens | CONFIRMED via press, refined | Filed April 21-22, 2026 in the U.S. District Court for the Northern District of California (San Francisco). The dispute concerns roughly 4 billion frozen WLFI tokens (Sun puts the value near \$320M; the \$75M figure in the dossier appears to reflect the investment principal Sun publicly committed, not the asserted current value). The dossier's "\$75 million" is incomplete. |
| WLF countersued for defamation | CONFIRMED | Filed by WLF on May 4, 2026 in the Eleventh Judicial Circuit Court for Miami-Dade County, Florida (state court, not federal). The dossier currently does not specify state vs. federal venue; for precision the paper should. |
| CourtListener docket numbers | NOT FOUND IN PRIMARY SOURCES | `forensic-econ osint court` returned 401 (no API token in environment). The N.D. Cal. case caption and Miami-Dade case caption are available via press; the docket numbers would be retrievable through PACER or with a CourtListener key. Mark as a follow-up. |

## Discrepancies found

In order of how much they would matter for a paper:

1. **DJT BTC holdings: 9,542.16 BTC, not 11,542 BTC.** This is the largest factual error in the WLFI dossier. The 10-Q is unambiguous in its XBRL tagging. The dossier's number is either a typo or a confusion with a different reporting period. Fix this before any external publication that cites the dossier.

2. **BitGo Trust charter status.** South Dakota state-charter is now historical. The OCC granted national-trust-bank approval in December 2025, and the entity now operates as BitGo Bank & Trust, N.A. This actually strengthens the EO 14405 conflict argument (an OCC-chartered national trust bank has clearer master-account standing than a state-chartered trust) but the dossier as written is stale.

3. **House investigation attribution.** The probe came from the House Select Committee on the CCP via Ranking Member Khanna, not from a standard oversight committee. This needs to be named.

4. **Senate Banking letter signatories.** Jointly Warren (Senate Banking minority) and Waters (House Financial Services minority). The dossier currently reads as Senate-only.

5. **Chase Herro address.** Listed in Wilmington, DE on the July 2025 Form D/A, not Dorado, PR. The dossier groups Folkman and Herro under one Puerto Rico address.

6. **Duke FinReg framing.** A blog post by Lee Reiners, not an institutional Duke analysis. Cite by author.

7. **Sun litigation venue and dollar figure.** California Northern District for Sun v. WLF; Miami-Dade Circuit for the WLF defamation countersuit; Sun's asserted damages are not \$75M but rather the value of approximately 4 billion frozen WLFI tokens, with the \$75M figure being the original investment principal.

8. **DT Marks DEFI LLC ownership chain.** None of the 75% revenue claim, the 70/30 Trump/family split, or the 60% → 38% Holdco equity step-down is in any primary SEC filing. All three rest on Reuters / CNBC / The Block reporting plus company-published materials. This is acceptable for a dossier but the paper text should phrase them as "according to company gold paper and Reuters reporting" rather than as if they were SEC disclosures.

## Items requiring follow-up

- **PACER / CourtListener docket numbers** for Sun v. World Liberty Financial (N.D. Cal., April 2026) and World Liberty Financial v. Sun (Eleventh Judicial Circuit, Miami-Dade, May 2026). Either acquire a CourtListener API token for the local `forensic-econ` client or pull through PACER directly.

- **Reg-S concurrent offering size.** The July 2025 Form D/A explicitly excludes non-US sales under a separate Regulation S concurrent offering. Reuters reported aggregate token sales above \$500M as of early 2025; the residual (above the \$52.13M US-person Reg-D figure) is the Reg-S tranche, but that tranche has no public filing on EDGAR because Regulation S sales are not subject to Form D. Tracking the size requires either company disclosure or, more practically, on-chain analysis of wallet flows.

- **USD1 reserve attestation.** No published independent attestation report was located. Either the engagement exists and is not publicly posted, or there is none. For any Howey or run-risk argument the existence of an attestation matters; the paper should not assume one exists.

- **Aryam Investment 1 entity registration.** The UAE deal flows through a vehicle named in WSJ reporting; OpenCorporates and an UAE-jurisdiction search would help establish beneficial ownership. Not done in this pass.

- **DT Marks DEFI LLC Delaware filing.** Available through the Delaware Division of Corporations entity search. Would establish formation date, registered agent, and any amendments. Not done in this pass.

- **WLFI ALTS Form 3 (November 2025)**, worth a separate look at what ALTS is and why WLFI is reporting a 1,000,000-share Director-plus-Other beneficial-ownership position in it. This filing is on the WLFI EDGAR page but is not mentioned in the dossier.

## Aggregate confidence assessment

Per top-level claim block, with action recommended for the paper draft:

| Claim block | Confidence after this pass | Action |
|---|---|---|
| WLFI corporate structure (CIK, Delaware, Miami address, Folkman and Herro as officers, \$52.13M, 1,966 investors, Reg-S exclusion) | HIGH (primary-source confirmed) | **ELEVATE TO PAPER** with the corrected Herro Wilmington-DE address. |
| Trump family revenue channel (75% protocol revenue via DT Marks DEFI LLC; 70/30 internal split; 60% → 38% Holdco equity) | MEDIUM (press-confirmed, no SEC filing) | **KEEP IN DOSSIER WITH HEDGE** "according to Reuters and CNBC reporting and company-published materials, not on the face of any SEC filing." |
| USD1 custodian, charter, launch date | MEDIUM-HIGH but stale on charter | **ELEVATE TO PAPER** with the BitGo charter update (South Dakota state-chartered through December 2025; OCC-chartered national trust bank thereafter). |
| USD1 reserve composition (BlackRock-managed, T-bill plus cash) | LOW-MEDIUM (company-disclosed, no third-party attestation found) | **KEEP IN DOSSIER WITH HEDGE** "company-disclosed reserve composition; no independent attestation publicly available as of May 26, 2026." |
| House investigation into \$500M UAE 49% stake | HIGH | **ELEVATE TO PAPER** naming the House Select Committee on the CCP and ranking member Khanna, with WSJ reporting as the trigger and the Aryam Investment 1 vehicle. |
| DJT Q1 2026 10-Q figures | MIXED | **ELEVATE TO PAPER** with the corrected BTC figure of 9,542.16 (not 11,542). Keep the CRO and net-loss figures. Clarify "net loss available to common stockholders" for the \$405.8M figure. |
| Senate Banking letter to SEC | HIGH | **ELEVATE TO PAPER** as the Warren-Waters joint letter of April 2, 2025 to Acting SEC Chair Uyeda. |
| Duke FinReg "analysis" | MEDIUM (it's a blog post by Lee Reiners, not an institutional position) | **KEEP IN DOSSIER WITH HEDGE** as "blog post by Lee Reiners, Duke FinReg Blog, May 8, 2026, arguing WLFI satisfies Howey." Do not characterize as the institutional position of Duke Law. |

The core of the dossier survives the deep-dive intact. The corporate-structure spine and the congressional-letter strand are both anchored in primary documents that match the dossier to the dollar and to the investor count. The places the dossier overreaches are exactly where one would expect: the private-LLC ownership chain, where SEC filings simply do not disclose what reporters have reconstructed, and one numerical typo in the DJT BTC count that needs to be corrected.

For a paper-grade citation pass I would (a) fix BTC, (b) fix the BitGo charter, (c) name the House committee, (d) name both Senate and House signatories on the April 2025 letter, (e) hedge the LLC-chain percentages as press-sourced, (f) add the Sun litigation venue, and (g) note that the November 2025 Form 3 (ALTS issuer) deserves its own footnote in the corporate-structure paragraph.

---

File: `/Users/ian/Projects/eo14405-contagion/dossiers/validation/wlfi-deep-dive.md`

Six-line summary:
1. Form D/A primary data (Miami office, \$52.13M, 1,966 investors, Folkman and Herro as the only related persons, Reg-S exclusion clause) all match the dossier exactly; Herro's address is Wilmington DE, not Dorado PR as the dossier groups it.
2. DJT Q1 2026 10-Q reports 9,542.16 BTC, not 11,542 BTC: the dossier figure is wrong by roughly two thousand coins. CRO and net loss survive verification.
3. The April 2, 2025 Senate Banking letter is real and on file; it is jointly signed by Sen. Warren and Rep. Waters to Acting SEC Chair Uyeda, not Senate-Banking-only.
4. The House investigation into the alleged \$500M UAE 49% stake exists; it was opened by the House Select Committee on the CCP (ranking member Khanna), not by a Financial Services or Oversight committee.
5. BitGo Trust Company's South Dakota state charter is now historical; the OCC approved conversion to BitGo Bank & Trust, N.A. in December 2025.
6. The Duke FinReg "analysis" is a blog post by Lee Reiners; the 75% protocol-revenue and DT Marks DEFI LLC ownership claims are press-only, not in any SEC filing, and the dossier should hedge them accordingly.
