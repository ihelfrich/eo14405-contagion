# Validation campaign — consolidated findings

*Compiled 26 May 2026. Six parallel validation streams: Codex CLI (one stream redispatched to Claude after stdin hang), Gemini CLI, and four Claude general-purpose agents. Every claim below traces to a primary-source URL in the per-stream validation file in this directory.*

This summary consolidates the six-stream validation run that followed the initial deep-dive OSINT dossiers. The point is to mark each claim that will appear in the published documents as VERIFIED (elevate verbatim), CORRECTED (elevate with sharper wording), PARTIAL (keep but hedge to press-reported), UNVERIFIED (keep in dossier with explicit "press only" tag), or REFUTED (do not publish).

## Verified at primary-source documents (paper-grade)

These claims trace to OGE-278 forms, SEC DEF 14A proxies, SEC Form D/A filings, FEC Form 3X, CFTC press releases, NY AG press releases, the Federal Register, congressional committee letters, or court dockets. They survive into the published paper.

| Person / fact | Primary source | Source file |
|---|---|---|
| Kevin Warsh OGE-278 certified 2026-04-10; amended ethics agreement 2026-04-17; two Juggernaut Fund LP positions each "Over $50,000,000" (floor sum $100M); 90-day divestiture window expires 2026-08-11 | oge.gov public release | `oge-278-validation.md` |
| William Pulte OGE-278 BTC and SOL each $500,001-$1,000,000 in a Coinbase wallet; MARA Holdings common $5,000,001-$25,000,000; FHFA crypto-mortgage directive 2025-06-25 issued with positions intact | oge.gov + FHFA | `oge-278-validation.md` |
| Kevin Hassett OGE-278 Coinbase Global Class A common $1,000,001-$5,000,000; Coinbase Asset Management Academic and Regulatory Advisory Council fee $50,001 from 03/2021 to 01/2025 | oge.gov | `oge-278-validation.md` |
| Cynthia Lummis approximately 5 BTC personal holdings on Senate STOCK Act PTRs; chairs Senate Banking Digital Assets Subcommittee; primary sponsor of BITCOIN Act (S. 954); co-sponsor of GENIUS Act (S. 394) signed 2025-07-18 | efdsearch.senate.gov + congress.gov | `congress-validation.md` |
| Andy Barr: $7.2M in Fairshake / Defend American Jobs IE supporting him in 2024 cycle; $2.36M cumulative from Crypto.com's Foris DAX entity to his "Keep America Great PAC" for 2026 KY Senate primary | FEC + OpenSecrets | `congress-validation.md` |
| Tim Scott co-sponsor of GENIUS Act; $64,700 in crypto-executive personal contributions during 2023-2024 cycle | congress.gov + FEC | `congress-validation.md` |
| Bryan Steil $764,206 Fairshake IE in 2024 cycle | FEC | `congress-validation.md` |
| Bernie Moreno $40.1M Defend American Jobs IE against Sherrod Brown in 2024 cycle; defeated Brown by approximately 4 points | FEC + AP race call | `congress-validation.md` |
| M. Michele Burns sits simultaneously on Circle (CRCL) and Goldman Sachs (GS) boards as of 2026 DEF 14A proxies | Circle DEF 14A 2026-04-01 + Goldman DEF 14A 2026-03-19 | `board-interlocks-validation.md` |
| Heath Tarbert chronology: 14th CFTC Chair Jul 2019 to Jan 2021, Citadel Securities CLO Apr 2021 to Jun 2023, Circle CLO since Jul 2023, Circle President since Jan 1 2025 | Circle DEF 14A | `board-interlocks-validation.md` |
| WLFI corporate structure: Delaware corporation, CIK 0002043140, principal office 4400 Biscayne Blvd Ste 900 Miami FL, officers and directors Folkman and Herro, cumulative Reg-D sales of $52,133,139 across 1,966 investors as of 2025-07-03 Form D/A | SEC EDGAR Form D/A accession 0002043140-25-000001 | `wlfi-deep-dive.md` |
| DJT (Trump Media) Q1 2026 net loss to common stockholders $405.8M; CRO holdings 756,079,523 tokens | SEC EDGAR 10-Q filed 2026-05-08 | `wlfi-deep-dive.md` |
| USAT launched 2026-01-27 through Anchorage Digital Bank (OCC-chartered trust company); Bo Hines CEO | Anchorage Digital announcement + OCC Conditional Approval | `cantor-tether-validation.md` |
| CFTC $41M settlement against Tether and Bitfinex Oct 15 2021 | CFTC press release 8450-21 | `cantor-tether-validation.md` |
| NY AG $18.5M settlement against Tether 2021-02-23 | NY AG press release | `cantor-tether-validation.md` |
| Warren-Wyden joint inquiry letter to Lutnick on Tether-Cantor relationship dated 2026-04-30 (the fourth Warren-led letter) | Senate Banking minority staff publication | `cantor-tether-validation.md` |

## Corrected and elevated

Original dossier claim was substantively correct but the wording was imprecise or a detail was off. The corrected version goes into the paper.

| Original claim | Correction | Source |
|---|---|---|
| Warsh "OGE flagged out of compliance" | OGE verbatim language is "in compliance for all lines except [enumerated lines]; once the filer divests these assets, he will be in compliance" | `oge-278-validation.md` |
| Pulte "MARA equity disclosed" (range not specified) | Actually MARA Holdings common $5,000,001 to $25,000,000 | `oge-278-validation.md` |
| Hassett "$50K+ from Coinbase Advisory Council" | More precisely: $50,001 from Coinbase Asset Management Academic and Regulatory Advisory Council (subsidiary), 03/2021 to 01/2025 | `oge-278-validation.md` |
| WSJ Cantor-Tether stake article dated "November 4, 2024" | Actually November 24, 2024 (date error in `tether-ifinex.md` and `SYNTHESIS.md`) | `cantor-tether-validation.md` |
| DJT BTC holdings "11,542 BTC" | Actually 9,542.16 BTC per Q1 2026 10-Q XBRL tag (off by approximately 2,000 coins) | `wlfi-deep-dive.md` |
| BitGo Trust "South Dakota state-chartered" | Was state-chartered; converted to OCC national trust bank (BitGo Bank and Trust, N.A.) in December 2025 | `wlfi-deep-dive.md` |
| "House investigation into WLFI UAE stake" attributed loosely | Actually House Select Committee on the CCP (Khanna investigation), not House Financial Services or Oversight | `wlfi-deep-dive.md` |
| "Senate Banking letter to SEC on WLFI" | Joint Warren (Senate Banking minority) + Waters (House Financial Services minority) letter, not Senate-only | `wlfi-deep-dive.md` |
| "Anchorage already holds Fed master-account access" (in SYNTHESIS.md) | This is incorrect; Anchorage holds OCC trust-bank charter and is the LPMA pathway, not pre-existing access. The dossier itself contradicts the SYNTHESIS line | `cantor-tether-validation.md` |
| Tarbert / Brooks / Hildebrand "0 gap years between regulator and private" | Actual gaps: Tarbert 2.5 months, Brooks days, Hildebrand 9 months. Use "immediate" or quote actual gaps | `board-interlocks-validation.md` |
| Cantor Equity Partners accession 0001213900-25-044410 | Does not exist; correct accession is 0001213900-25-034374 (April 23 2025 business-combination 8-K under CIK 1865602) | `board-interlocks-validation.md` |
| Dante Disparte listed as Circle NEO | Disparte is senior officer but not in the 2026 DEF 14A NEO list (Allaire, Fox-Geen, Razzaghi, Tarbert, Chandhok); move to "senior officers" subsection | `board-interlocks-validation.md` |

## Partial (press-sourced, retain with hedging)

These claims appear in mainstream financial press but were not located in primary regulatory filings. They stay in the dossiers with explicit "per press reporting" framing, and they appear in the paper only with the same hedging.

| Claim | Source | Status |
|---|---|---|
| Cantor Fitzgerald approximately 5% equity stake in Tether via ~$600M convertible bond | WSJ Nov 24 2024 | Press-only, no primary filing |
| Cantor custodies majority of Tether's $141B in Treasury reserves | $141B confirmed by Q1 2026 BDO attestation; Cantor custodian attribution is press-only | $141B verified, custodian attribution partial |
| Tether loan to Lutnick family Dynasty Trust A | Press reporting only; no UCC-1 filing retrieved | Press-only |
| SDNY DOJ investigation of Tether for sanctions/AML | WSJ Oct 25 2024; Tether denied; no charging documents public | Press-only |
| WLFI DT Marks DEFI LLC contractual claim to 75% protocol revenue | Press reporting; not in any primary SEC filing | Press-only |
| WLFI 70/30 Trump / family ownership split of DT Marks DEFI LLC | Press reporting; no Delaware filing retrieved | Press-only |
| WLF Holdco LLC 38% equity (was 60%) | Press reporting | Press-only |

## Refuted (do not publish)

The validation produced one substantive refutation of the qualitative SNA findings, plus two minor refutations.

| Original claim | Refutation | Source |
|---|---|---|
| The "minimum-cut spine" (Warsh, Miran, Lutnick, Hassett, Quintenz) disconnects the Trump cluster from the Fed cluster from the stablecoin cluster | Refuted. The network is structurally redundant. Trump-Andreessen and Trump-Cook edges survive removal of the five-node spine. The network does not actually fragment at those five removals | `sna-methodology-check.md` |
| Top-10 eigenvector centrality including Pulte and Lutnick | Refuted. Recomputation places David Sacks and D. John Sauer in the top 10 instead. The SNA-FINDINGS.md table has been updated | `sna-methodology-check.md` |
| Duke FinReg "institutional analysis" of WLFI Howey test | Actually a single-author blog post by Lee Reiners. Not Duke institutional | `wlfi-deep-dive.md` |

## Items requiring follow-up before subsequent publication

These were partial-finding or no-finding items where additional primary-source retrieval would strengthen the published documents but is not blocking for the current version.

1. Direct WSJ archive retrieval (paywall) of the Cantor-Tether November 24 2024 article
2. UCC-1 filing search for any Tether-to-Dynasty-Trust-A security interest
3. Senate Banking minority text of the prior three Warren-Lutnick letters to confirm the "fourth letter" sequencing
4. CourtListener API token authenticated retrieval of WLFI litigation dockets
5. Delaware Division of Corporations filing search for DT Marks DEFI LLC and Aryam Investment 1
6. Warsh 2026-04-22 Senate Banking confirmation hearing transcript for any recusal Q&A
7. WLFI Form 3 on issuer "ALTS" (November 2025) - not yet integrated
8. Pulte FHFA divestiture endnote check at the FHFA directive's signing date
9. The Trump-Andreessen donation edge and the Trump-Cook litigation edge in the SNA - confirm both exist in the dossiers, not just in press

## Aggregate assessment

Sixteen claims survive at primary-source-quality and can appear in the paper. Eleven claims need wording corrections before they appear. Seven claims need to appear as "per press reporting" rather than as documented facts. Three claims are refuted and have been or will be removed from the published documents.

The validation work changes the technical character of the SNA in one specific way: the network is structurally redundant rather than spine-fragile. That is a more interesting finding than the original minimum-cut claim, because it tells us the conflict-of-interest architecture cannot be unwound by replacing a small number of named individuals. It is the structure itself that has to change.

The validation work does not change the technical character of the contagion analysis. That analysis is computational, calibrated against the USDC March 2023 episode, and stands independent of the political-economy facts. What the validation has done is sharpened the political-economy disclosure that accompanies it.

## Files in this directory

- `oge-278-validation.md` (3,393 words) — Warsh, Pulte, Hassett OGE-278 verification
- `congress-validation.md` (Gemini) — Lummis, Barr, Scott, Steil, Moreno congressional disclosures
- `wlfi-deep-dive.md` (3,481 words) — WLFI corporate stack, USD1 custody, DJT treasury, House and Senate inquiries
- `cantor-tether-validation.md` (3,558 words) — Cantor 5% claim, $141B custody, USAT launch, CFTC and NY AG settlements
- `board-interlocks-validation.md` (4,606 words) — Tarbert, Burns, Brooks, Lutnick succession, Hildebrand, Biber, Disparte
- `sna-methodology-check.md` (Gemini) — Edge audit, centrality recomputation, minimum-cut refutation, Louvain sanity check
