# Circle + Coinbase: the US public-market stablecoin axis

*Compiled 2026-05-26 for the EO 14405 contagion working paper. Source-cited; uncertainty flagged inline.*

## Executive summary

Circle Internet Group (NYSE: CRCL, CIK 1876042) and Coinbase Global (NASDAQ: COIN, CIK 1679788) are the two US-listed entities with the most direct upside from Executive Order 14405's instruction that the Federal Reserve evaluate non-bank access to master accounts and payment services. USDC, the second-largest stablecoin (roughly \$70B in circulation as of February 2026, ~\$78B by April 2026), is issued by Circle, with its reserves predominantly held in the BlackRock-managed Circle Reserve Fund and in bank deposits custodied at BNY Mellon. Coinbase, through the dissolved Centre Consortium and the restructured August 2023 commercial agreement, shares the interest income generated on USDC reserves and runs the largest distribution channel for USDC by trading and wallet volume. Both companies have unusually direct conflicts with US financial-stability policy: Circle's President is Heath Tarbert, the former 14th CFTC Chair; Coinbase's CEO Brian Armstrong has sold roughly \$550M of stock in the year leading into January 2026 under a 10b5-1 plan adopted Aug 15, 2024; Coinbase founded and continues to fund Stand With Crypto and Fairshake, the largest crypto super-PAC of the 2024 cycle. The SEC's June 2023 enforcement action against Coinbase was dismissed with prejudice in February 2025.

## Circle Internet Financial (CRCL)

### Corporate structure

EDGAR CIK 0001876042. Current legal name **Circle Internet Group, Inc.**, a Delaware corporation (SIC: Finance Services). Prior names on EDGAR: Circle Internet Financial Ltd (2023-12 to 2024-04), Circle Internet Finance Public Ltd Co (2021-12 to 2022-12), CIrcle Acquisition Public Ltd Co (2021-08 to 2021-10). The 2021-2022 entities are the abandoned Concord Acquisition SPAC route; the current Delaware corporation re-filed S-1 in 2025 for a conventional IPO. (Source: `forensic-econ edgar info --cik 1876042`.)

IPO: priced on NYSE under ticker CRCL the week of **June 5, 2025** (not June 2024 as originally listed in some secondary sources; the IPO calendar slipped twelve months). The Form S-1 was first filed in DRS form in 2023, amended four times in early 2025, and a fresh S-1 was filed August 12, 2025 after the initial offering. (Source: EDGAR filings list, accessions 0001193125-25-084832 through 0001193125-25-178989.)

Most recent annual report: 10-K for FY2025 filed 2026-03-09 (accession 0001876042-26-000062). First post-IPO 10-Q was for the period ended 2025-06-30 (accession 0001628280-25-039781).

### S-1 highlights, reserve composition and custody

The S-1 discloses that Circle earns "nearly all" of its revenue from interest income on USDC reserves. Reserves are held in two forms:

1. **The Circle Reserve Fund**, a SEC-registered 2a-7 government money-market fund managed by **BlackRock**. The S-1 reports that approximately **87% of USDC reserves are concentrated in this single money-market-fund structure**, creating a third-party manager / custodian concentration risk that Circle acknowledges as a risk factor. (Source: Stocktitan summary of CRCL S-1; Kavout analysis of Circle revenue mix.)
2. **Cash deposits at banks**, with **BNY Mellon as primary custodian** (announced March 2022). The S-1 also lists Cross River Bank and Customers Bank as banking partners in the historical period. (Source: Circle press release "Circle Selects BNY Mellon to Custody USDC Reserves", March 2022; cointelegraph; decrypt.)

Auditor history (relevant for attestation credibility):
- **Grant Thornton LLP**: independent auditor and monthly attestation provider from 2015 through 2022. (Source: Circle blog "USDC Reserve Attestation Report from Grant Thornton LLP, March 2021".)
- **Deloitte & Touche LLP**: independent auditor since fiscal year 2022. (Source: Blockworks, "Circle Taps Deloitte as New Auditor.")
- Note: secondary sources occasionally claim "BDO" succeeded Grant Thornton. This appears to be a confusion with Tether's auditor switch. **[uncertain, Deloitte is more strongly attested in sources reviewed]**.

### USDC circulating supply trajectory

| Date | Circulating supply (USD) | Source |
|---|---|---|
| Jan 2023 | ~\$44B | Coinmetrics, Chainalysis |
| Mar 2023 (post-SVB low) | ~\$33B | Chainalysis SVB-depeg analysis |
| Early 2024 | ~\$33B | eco.com support, citing Q1 2026 retro |
| End 2024 | ~\$42B | eco.com |
| Feb 2025 | \$54.95B (Feb 4) / \$56.28B (Feb 28) | secondary aggregator |
| June 2025 (IPO) | ~\$61B | S-1 cover page (Stocktitan) |
| Feb 2026 | ~\$70B | secondary aggregator |
| Apr 2026 | ~\$78B | eco.com |

The trough is the March 2023 depeg episode. Circulating supply lost roughly a quarter of its float in the four weeks following the SVB disclosure and did not recover to pre-SVB levels until well into 2024. (Source: Federal Reserve FEDS Notes, "In the Shadow of Bank Runs: Lessons from the Silicon Valley Bank Failure and Its Impact on Stablecoins", 2025-12-17.)

### Reserve composition over time (qualitative)

| Period | Cash at banks | Treasury MMF / direct T-bills | Notes |
|---|---|---|---|
| Pre-2022 | Mixed cash + commercial paper | None | Commercial paper exposure attested by Grant Thornton |
| 2022 (post-Mar) | Bank deposits at BNY/SVB/SilverGate/Signature/Customers/Cross River | Circle Reserve Fund launched | First clean separation into 2a-7 fund |
| Mar 10, 2023 | \$3.3B at SVB (8% of reserves) | Bulk in Reserve Fund | Disclosed Friday night, depeg overnight |
| Mid-2023 onward | BNY Mellon as primary custodian | ~87% in Circle Reserve Fund | Bank concentration reduced |
| 2024–2026 | BNY Mellon dominant | BlackRock-managed Reserve Fund dominant | S-1 disclosure |

### Key personnel and holdings

- **Jeremy Allaire**, CEO, co-founder. Form 3 filed at IPO; subsequent Form 4s in the May 2025 cleanup. The full holdings table would require parsing the individual Form 4 XML, which is feasible from the accession list above but not done in this dossier. **[uncertain on precise share count; recommend dedicated Form 4 parse]**
- **Heath Tarbert**, joined Circle as **Chief Legal Officer and Head of Corporate Affairs in June 2023**; elevated to **President** by 2025. Former **14th Chairman of the CFTC (2019–2021)**; previously Assistant Secretary of the Treasury for International Markets and Development; acting Under Secretary of the Treasury for International Affairs. Tarbert is publicly quoted endorsing the GENIUS Act and CFTC Acting Chair Pham's tokenized-collateral pilot. (Sources: Tarbert LinkedIn; Wikipedia; Circle leadership page; CFTC press release 9146-25.) This is the single most direct revolving-door connection between US derivatives regulation and the dominant US-public stablecoin issuer.
- **Dante Disparte**, Chief Strategy Officer / Head of Global Policy. Previously Head of Policy and Communications for the Diem (formerly Libra) Association. **[Diem affiliation widely reported but not re-verified in this pass]**.

### Recent regulatory / legal exposure

No active SEC enforcement action against Circle disclosed in the 10-K reviewed. CourtListener query returned a 401 (`forensic-econ osint court` needs `COURTLISTENER_TOKEN`); recommend re-running with auth. **[uncertain, pending CourtListener re-run]**.

## Coinbase Global (COIN)

### Recent filings

CIK 1679788. Annual filers since IPO (April 2021 direct listing):

| Form | Filing date | Period |
|---|---|---|
| 10-K | 2026-02-12 | FY2025 |
| 10-K | 2025-02-13 | FY2024 |
| 10-K | 2024-02-15 | FY2023 |
| 10-K | 2023-02-21 | FY2022 |
| 10-K | 2022-02-25 | FY2021 |

(Source: `forensic-econ edgar list --cik 1679788 --form 10-K --limit 5`.)

### USDC revenue share

Under the **August 2023 restructured commercial agreement** (which dissolved Centre and gave Coinbase a minority equity stake in Circle), Circle and Coinbase **equally share interest income generated on USDC reserves, weighted by distribution and usage** (i.e., USDC held on Coinbase's platform generates revenue that flows largely to Coinbase; USDC held elsewhere generates revenue that flows largely to Circle, with a base equal-share component). (Sources: CoinDesk 2023-08-21; Fortune Crypto 2023-08-21; Decrypt 2023-08-21.)

Coinbase 10-K and 10-Q filings break out a "stablecoin revenue" line item, which is materially driven by USDC reserve interest. Precise FY2024 and FY2023 figures could not be extracted in this pass because the SEC EDGAR HTML returned 403 to the WebFetch tool. **[uncertain on exact dollar figures, recommend pulling via `forensic-econ edgar facts --cik 1679788` to get XBRL-tagged values, or via direct EDGAR fetch with proper UA header]**.

### CEO Form 4 trading pattern

Brian Armstrong adopted a Rule **10b5-1 plan on August 15, 2024**, and has executed pre-arranged sales steadily since. Documented transactions (compiled from Stocktitan and Investing.com summaries of individual Form 4 filings; each maps to an accession listed under `forensic-econ edgar list --cik 1679788 --form 4`):

| Date | Shares / proceeds | Price range |
|---|---|---|
| 2024-11-18 | ~\$293.9M sold | \$289.13–\$326.58 |
| 2024-11-25 | 25,000 shares (~\$7.68M) | \$305.33–\$309.18 |
| 2025-06-25/26 | 449,155 Class A converted-and-sold (~\$163M gross) | \$358.00–\$369.25 |
| 2025-08-12 | 25,000 Class A | \$324.33–\$329.52 |
| 2025-09-04 | 12,643 + 6,474 + 5,883 shares | \$301.43 / \$302.57 / \$303.39 |
| 2025-11-03 | ~\$8.4M total | \$335.12–\$340.15 |

Aggregate sales over the year ending January 2026 are reported at roughly **\$550M, more than 1.5M shares**. (Sources: coinpaprika.com "Coinbase CEO Armstrong Sells \$550M Stock Over Past Year"; coinpedia.org corroborates.) The current Form 4 activity in May 2026 (accessions 0001679788-26-000055 through -000060) reflects continued execution under the 10b5-1 plan.

### SEC v. Coinbase resolution

Filed June 6, 2023 in the Southern District of New York. On **February 21, 2025**, Coinbase announced an agreement-in-principle with SEC Staff to **jointly stipulate to dismissal with prejudice**, formalised by the Commission on **February 27, 2025** (CoinDesk: "Coinbase Case Dropped by U.S. SEC as Agency Reverses Crypto Stance"). The reversal followed Gary Gensler's departure and Acting Chair Mark Uyeda's overhaul of Enforcement Division leadership. (Sources: Coinbase Form 8-K filed Feb 2025, accession 0001193125-25-031346; CoinDesk; Manatt client alert; University of Chicago Business Law Review commentary on equitable estoppel.)

### Stand With Crypto and Fairshake

- **Stand With Crypto** founded by Coinbase in **August 2023** (not October 2023; the Coinbase blog "Crypto is Here to Stay" predates Oct). It registered a PAC in May 2024 to channel ~450,000 member contributions toward 2024 federal candidates. (Source: Coinbase blog; cointelegraph 2024-05.)
- **Fairshake** super-PAC: founded March 2023; Coinbase made **at least six separate contributions**; total Fairshake raise from inception through December 2024 was **\$260M** across 75 contributions. Coinbase's documented \$25M donation on June 3, 2024 came days after Biden's veto of the SAB 121-overturning resolution. A further \$25M Coinbase pledge was reported October 31, 2024. (Sources: Wikipedia "Fairshake"; Fortune Crypto 2024-06-03; Bloomberg 2024-10-31; cointelegraph "Crypto-backed group gathers \$141M funding to influence US elections.")

## Centre Consortium chronology

- **Sept 2018**: Founded as a joint venture between Circle and Coinbase to govern USDC issuance, reserves, and protocol changes.
- **2018–2022**: Operated as the formal governance body; Coinbase and Circle each had equal seats and shared in attestation responsibilities.
- **Mar 10–13, 2023**: Centre's standardised reserve disclosures forced Circle to publicly confirm \$3.3B SVB exposure on the night of March 10. USDC depegged to ~\$0.87 by 2 AM Mar 11. FDIC's Mar 12 announcement that all SVB depositors would be made whole restored the peg by Mar 13. (Source: CoinDesk 2023-03-11; CNBC 2023-03-11; Federal Reserve FEDS Notes 2025-12.)
- **Aug 21, 2023**: Circle and Coinbase **dissolved Centre**. Stated rationale: "regulatory clarity makes the consortium structure no longer necessary." Coinbase acquired a minority equity stake in Circle (widely reported at ~\$210M valuation contribution against an undisclosed share count; **[uncertain on exact percentage equity]**). Aurpay's "\$908M" figure for the total deal appears to be a derived/speculative number, not a direct Circle disclosure. (Sources: CoinDesk 2023-08-21; Fortune Crypto 2023-08-21; Decrypt 2023-08-21.)

## Custody bank relationships

### Pre-March 2023

USDC reserves were spread across **Silicon Valley Bank, Silvergate, Signature Bank, Customers Bank, Cross River Bank, and BNY Mellon**. The \$3.3B SVB exposure represented 8% of approximately \$40B in reserves at the time. Silvergate's voluntary wind-down (announced March 8, 2023) and Signature's takeover (March 12) further compressed Circle's banking optionality during the same week.

### Post-SVB shift

After FDIC made depositors whole, Circle moved aggressively to **consolidate custody at BNY Mellon** and shift reserve composition toward the BlackRock-managed Circle Reserve Fund (2a-7 government MMF). Cross River Bank was retained as a settlement and minting partner; **[uncertain on Customers Bank status as of 2026]**.

### Current state (2026)

- Primary custodian for cash and Treasuries: **BNY Mellon**
- Money-market fund manager: **BlackRock** (Circle Reserve Fund, ~87% of reserves per S-1)
- Settlement/minting bank: **Cross River Bank** (historical; status as of 2026 unverified)
- Independent auditor and monthly attestation: **Deloitte & Touche LLP** (since FY2022)

## EO 14405 direct benefit

EO 14405 (signed week of May 19, 2026, titled per coverage as "Integrating financial technology innovation into regulatory frameworks") directs the Federal Reserve, **within 120 days**, to evaluate its legal authority to grant non-bank financial firms direct access to Reserve Bank master accounts and payment services. The language is **"requested" not "directed"** for the Fed Board specifically, in deference to Fed independence. (Sources: CoinDesk 2026-05-19; American Banker; The Block.)

Direct benefits to Circle and Coinbase if implemented:

1. **Circle**: a Fed master account would allow USDC to hold reserves directly at the Fed rather than at BNY Mellon, eliminating one layer of bank-deposit counterparty risk. This would functionally make USDC a synthetic CBDC sitting on Circle's balance sheet but fully reserved at the Fed. The same change would also let Circle internalise the spread that BNY Mellon currently earns on the float, materially increasing Circle's net interest margin on reserves.
2. **Coinbase**: direct settlement access via a Coinbase Fed account would let USDC redemptions clear without going through a correspondent bank, eliminating the SVB-style "stuck deposits" failure mode that triggered the March 2023 depeg. Coinbase's revenue share on USDC reserve interest would also benefit pro-rata from Circle's margin expansion.

The contagion concern for the working paper: a Fed master account converts what is currently a private-sector run risk (USDC redemption pressure flowing through commercial banks) into a direct Fed balance-sheet exposure. The Fed becomes the implicit lender-of-last-resort for the stablecoin sector without statutory authority to set capital, liquidity, or activity restrictions on the issuers, the asymmetry the working paper's Eisenberg-Noe and global-game modules are designed to formalise.

## Sources

- EDGAR filings via `forensic-econ`: CIK 1876042 (Circle), CIK 1679788 (Coinbase).
- Federal Reserve FEDS Notes, "In the Shadow of Bank Runs: Lessons from the Silicon Valley Bank Failure and Its Impact on Stablecoins", 2025-12-17. https://www.federalreserve.gov/econres/notes/feds-notes/in-the-shadow-of-bank-run-lessons-from-the-silicon-valley-bank-failure-and-its-impact-on-stablecoins-20251217.html
- CoinDesk, "Circle Confirms \$3.3B of USDC's Cash Reserves Stuck at Failed Silicon Valley Bank", 2023-03-11.
- CNBC, "Stablecoin USDC breaks dollar peg after firm reveals it has \$3.3 billion in SVB exposure", 2023-03-11.
- Circle press release, "Circle Selects BNY Mellon to Custody USDC Reserves", March 2022.
- Stocktitan, summary of CRCL S-1 (10M shares, \$61B USDC circulating).
- Kavout, "What's Fueling Circle's Revenue Surge and Record Margins."
- Blockworks, "Circle Taps Deloitte as New Auditor."
- CoinDesk, "Coinbase Gets a Stake in Stablecoin Operator Circle and USDC Adds 6 New Blockchains", 2023-08-21.
- Fortune Crypto, "Coinbase takes equity stake in Circle as USDC-focused Centre Consortium shutters", 2023-08-21.
- CoinDesk, "Coinbase Case Dropped by U.S. SEC as Agency Reverses Crypto Stance", 2025-02-27.
- Coinbase Form 8-K, accession 0001193125-25-031346.
- Stocktitan, multiple Form 4 summaries for COIN insider trading.
- Coinpaprika, "Coinbase CEO Armstrong Sells \$550M Stock Over Past Year."
- Coinbase blog, "Crypto is Here to Stay" (Stand With Crypto founding).
- Wikipedia, "Fairshake" PAC entry.
- Fortune Crypto, "Coinbase donates \$25 million to super PAC Fairshake days after Biden vetoes crypto custody bill", 2024-06-03.
- Bloomberg, "Coinbase Pledges Further \$25 Million of Funding for Fairshake PAC", 2024-10-31.
- Heath Tarbert: LinkedIn; Wikipedia; Circle leadership page; The Block "Former CFTC head joins Circle as chief legal officer"; CFTC press release 9146-25.
- CoinDesk, "Trump orders government, Fed to review crypto firms' access to payment rails", 2026-05-19.
- American Banker, "Trump issues EO to revisit Fed master accounts for fintechs."
- The Block, "Trump orders Fed to review giving crypto firms access to master accounts."

## Uncertainty

1. Exact FY2024 / FY2023 dollar values for Coinbase's stablecoin revenue line, SEC EDGAR HTML 403'd. Recommend rerun via `forensic-econ edgar facts --cik 1679788` for XBRL-tagged values, or direct fetch with proper UA.
2. Allaire and Tarbert share counts and option holdings, Form 4 XML not parsed in this pass. The full Form 4 accession list is captured above; targeted parse is straightforward.
3. CourtListener queries failed with 401 (missing `COURTLISTENER_TOKEN`). The SEC v. Coinbase docket history and any Circle-related civil cases should be re-pulled with auth.
4. Auditor succession claim "Grant Thornton then BDO" in the task brief: not corroborated. Deloitte is the attested successor since FY2022. The BDO confusion may be with Tether's auditor history.
5. Exact percentage equity Coinbase holds in Circle post-August 2023 deal, secondary reports vary; primary source would be Circle's S-1 cap table footnotes.
6. Customers Bank and Cross River Bank present-day status as USDC banking partners, confirmed as historical, status as of May 2026 not directly verified.
7. The "\$908M" Coinbase-Circle deal value circulating in some secondary outlets appears to be a derived figure; treat as unverified.
