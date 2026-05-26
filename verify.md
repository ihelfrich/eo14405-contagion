# Claim-by-claim verification

*Companion to the LinkedIn post and the long-form research note. Every numerical and factual claim in those documents is listed here with the primary-source URL that supports it. If you find a claim that does not appear in this table or that cites a source you cannot verify, please file an issue at [github.com/ihelfrich/eo14405-contagion/issues](https://github.com/ihelfrich/eo14405-contagion/issues) and I will fix it or acknowledge the error.*

**Conventions**

- **PRIMARY** = government filing, court docket, SEC EDGAR, Federal Register, FEC, OGE, or central-bank publication. Highest evidentiary weight.
- **SECONDARY** = peer-reviewed academic paper, central-bank research note, or major-outlet investigative reporting with named sources.
- **PRESS** = single-source press reporting that has not been corroborated by a primary filing. Treated as suggestive, never load-bearing.
- **MODEL** = numerical result from the computational appendix in this repository. Reproducible from `paper.md` Sections 4-5 and the Python/Julia code under `src/`.

---

## 1. Executive Order 14405

| Claim | Source class | URL |
|---|---|---|
| EO 14405 signed 2026-05-19 | PRIMARY | [whitehouse.gov/presidential-actions](https://www.whitehouse.gov/presidential-actions/) |
| Published at 91 FR 30475 (2026-05-22) | PRIMARY | [federalregister.gov 2026-10399](https://www.federalregister.gov/documents/2026/05/22/2026-10399) |
| Section 4 directs the Federal Reserve to evaluate direct master-account access for non-bank fintech firms and stablecoin issuers | PRIMARY | EO 14405 §4, FR doc 2026-10399 |
| 120-day Fed evaluation window; 90-day adjudication clock for individual applications | PRIMARY | EO 14405 §4(a)-(b), FR doc 2026-10399 |

## 2. Contagion model results

All results from `paper.md` Sections 4-5; reproducible via `python src/run_all.py` against the calibration in `data/usdc_march2023_calibration.json`.

| Claim | Source class | URL |
|---|---|---|
| Wasserstein-1 run severity falls from 0.82 to 0.04 bp-mass (-95%) | MODEL | [paper.html §5](paper.html) |
| Eisenberg-Noe contagion-amplification index falls from 1.27 to 1.00 (-21%) | MODEL | [paper.html §5](paper.html) |
| Model-implied run probability falls from 0.90 to 0.18 (-80%) | MODEL | [paper.html §5](paper.html) |
| Perron-Frobenius spectral radius falls from 0.87 to 0.42 (-52%) | MODEL | [paper.html §5](paper.html) |
| Calibration anchored to USDC March 2023 depeg | SECONDARY | [Fed FEDS Notes, 2025-12-17](https://www.federalreserve.gov/econres/notes/feds-notes/) |
| Net welfare break-even at \$133 bp LOLR rate | MODEL | [paper.html §7](paper.html), [figures/sensitivity_lolr.png](figures/sensitivity_lolr.png) |

## 3. SVB and the March 2023 episode

| Claim | Source class | URL |
|---|---|---|
| SVB shareholder loss ~ \$40B between 2023-03-08 and 2023-03-10 | PRIMARY | [SEC EDGAR, SVB Financial Group 8-K filings](https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000719739&type=8-K) |
| FDIC receivership 2023-03-10 | PRIMARY | [FDIC press release PR-16-2023](https://www.fdic.gov/news/press-releases/2023/pr23016.html) |

## 4. Kevin Warsh, Fed Chair

| Claim | Source class | URL |
|---|---|---|
| Confirmed 2026-05-13 | PRIMARY | [Senate roll-call](https://www.senate.gov/legislative/votes_new.htm) |
| OGE-278 filed 2026-04-10; amended ethics agreement 2026-04-17 | PRIMARY | [OGE public records](https://extapps2.oge.gov/201/Presiden.nsf) |
| Two Duquesne Capital "Juggernaut Fund" LP positions each in "Over \$50,000,000" bracket | PRIMARY | OGE-278 Schedule A |
| Verbatim OGE compliance language: *"in compliance for all lines except [enumerated lines]; once the filer divests these assets, he will be in compliance"* | PRIMARY | OGE-278 reviewer endorsement |
| Ethics agreement: *"as soon as practicable but not later than ninety days after my confirmation"* | PRIMARY | OGE-278 attached ethics agreement |
| Divestiture deadline 2026-08-11 (90 days from 2026-05-13) | DERIVED | arithmetic on the two PRIMARY dates above |
| Equity in >20 additional blockchain and digital-asset firms | PRIMARY | OGE-278 Schedule A |

## 5. William Pulte, FHFA Director

| Claim | Source class | URL |
|---|---|---|
| Bitcoin in \$500,001-\$1,000,000 bracket | PRIMARY | [OGE-278, Pulte](https://extapps2.oge.gov/201/Presiden.nsf) |
| Solana in \$500,001-\$1,000,000 bracket | PRIMARY | OGE-278, Pulte |
| MARA Holdings common stock in \$5,000,001-\$25,000,000 bracket | PRIMARY | OGE-278, Pulte |
| FHFA directive 2025-06-25 ordering Fannie/Freddie to consider crypto as eligible mortgage reserves | PRIMARY | [FHFA Director's Order 2025-360](https://www.fhfa.gov/news) |
| No recusal endnote on the directive | PRIMARY | directive text + OGE-278 |

## 6. Kevin Hassett, NEC Director

| Claim | Source class | URL |
|---|---|---|
| Coinbase Class A common stock \$1,000,001-\$5,000,000 bracket | PRIMARY | [OGE-278, Hassett](https://extapps2.oge.gov/201/Presiden.nsf) |
| \$50,001 from Coinbase Asset Management Academic and Regulatory Advisory Council, 2021-03 to 2025-01 | PRIMARY | OGE-278, Hassett, Schedule C |
| Chairs the White House Digital Assets Working Group | PRIMARY | [whitehouse.gov press](https://www.whitehouse.gov/briefings-statements/) |

## 7. Cynthia Lummis, Senate Banking Digital Assets Subcommittee Chair

| Claim | Source class | URL |
|---|---|---|
| Personal holding of approximately 5 BTC | PRIMARY | [Senate STOCK Act PTRs, Lummis](https://efdsearch.senate.gov/search/) |
| Sponsored the BITCOIN Act | PRIMARY | [congress.gov S.4912](https://www.congress.gov/) |
| Co-sponsored the GENIUS Act | PRIMARY | congress.gov, GENIUS Act bill page |

## 8. Andy Barr, House Financial Services

| Claim | Source class | URL |
|---|---|---|
| Fairshake + Defend American Jobs \$7.2M in IE supporting his 2024 reelection | PRIMARY | [FEC, Fairshake C00835959](https://www.fec.gov/data/committee/C00835959/) |
| Crypto.com Foris DAX \$2.36M to "Keep America Great PAC" for 2026 Kentucky Senate primary | PRIMARY | [FEC, Keep America Great PAC](https://www.fec.gov/data/) |
| Concurrent service on House Financial Services Committee | PRIMARY | [financialservices.house.gov membership](https://financialservices.house.gov/about/membership.htm) |

## 9. Bernie Moreno, Ohio Senate seat

| Claim | Source class | URL |
|---|---|---|
| Defeated Sherrod Brown in 2024 Ohio Senate race | PRIMARY | [Ohio SOS certified results](https://www.ohiosos.gov/elections/election-results-and-data/) |
| \$40.1M in Defend American Jobs IE spent against Brown | PRIMARY | [FEC, Defend American Jobs C00836221](https://www.fec.gov/data/committee/C00836221/) |
| Brown was sitting Senate Banking Committee Chair at the time | PRIMARY | banking.senate.gov membership records, 118th Congress |

## 10. Howard Lutnick, Commerce Secretary

| Claim | Source class | URL |
|---|---|---|
| Cantor Fitzgerald acquired ~5% equity stake in Tether via ~\$600M convertible bond | PRESS | [WSJ, 2024-11-24](https://www.wsj.com/) |
| Lutnick-family Cantor acquisition reportedly financed in part by a Tether loan, via Dynasty Trust A | PRESS | WSJ 2024-11-24 |
| Tether reported \$141B in U.S. Treasury reserves, Q1 2026 | PRIMARY | [Tether Q1 2026 BDO attestation](https://tether.to/en/transparency/) |
| Cantor as Tether custodian, not in any primary filing | PRESS-ONLY | WSJ 2024-11-24; no UCC-1, no SEC filing confirms |
| USAT (Tether US-compliant sibling) launched 2026-01-27 through Anchorage Digital Bank | PRIMARY | [Anchorage Digital Bank press](https://www.anchorage.com/insights) |
| Anchorage Digital Bank is OCC-chartered (national trust bank) | PRIMARY | [OCC chartered banks list](https://www.occ.treas.gov/topics/charters-and-licensing/) |

## 11. World Liberty Financial (WLFI), USD1 issuer

| Claim | Source class | URL |
|---|---|---|
| SEC Form D/A, CIK 0002043140 | PRIMARY | [SEC EDGAR, CIK 0002043140](https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0002043140) |
| Delaware corporation, Miami office (4400 Biscayne Blvd Ste 900) | PRIMARY | Form D/A as filed |
| \$52,133,139 cumulative Reg-D sales across 1,966 investors | PRIMARY | Form D/A Item 13 + Item 14 |
| BitGo Trust converted from South Dakota state-chartered trust company to OCC national trust bank (BitGo Bank and Trust, N.A.) in December 2025 | PRIMARY | [OCC corporate decisions, BitGo conversion](https://www.occ.treas.gov/topics/charters-and-licensing/interpretations-and-actions/) |
| BitGo is master-account-eligible under EO 14405 §4 | DERIVED | OCC national-trust-bank charter + EO §4 eligibility language |
| DT Marks DEFI LLC reported 75% protocol-revenue claim on WLFI | PRESS | [Reuters investigation 2025](https://www.reuters.com/), [NYT investigation 2025](https://www.nytimes.com/), not in primary SEC filings |

## 12. DJT (Trump Media & Technology Group)

| Claim | Source class | URL |
|---|---|---|
| 9,542.16 BTC on balance sheet, Q1 2026 | PRIMARY | [SEC EDGAR, DJT 10-Q, filed 2026-05-08](https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001849635&type=10-Q) |
| 756,079,523 CRO tokens on balance sheet, Q1 2026 | PRIMARY | DJT 10-Q Q1 2026 |
| \$405.8M net loss to common stockholders, Q1 2026, almost entirely from crypto markdowns | PRIMARY | DJT 10-Q Q1 2026 |

## 13. Network structure (153-node SNA)

| Claim | Source class | URL |
|---|---|---|
| Marc Andreessen gave \$2.5M personally to Trump-supporting super-PACs in 2024 | PRIMARY | [FEC individual contributions](https://www.fec.gov/data/receipts/individual-contributions/) |
| Ben Horowitz gave \$2.5M personally to Trump-supporting super-PACs in 2024 | PRIMARY | FEC individual contributions |
| Trump v. Cook litigation pending at Supreme Court (re: removal of Fed Governor) | PRIMARY | [supremecourt.gov docket](https://www.supremecourt.gov/) |
| Network is structurally redundant: removing Warsh, Pulte, Hassett, Lutnick, and Quintenz does not fragment the spine | MODEL | [dossiers/SNA-FINDINGS.html](dossiers/SNA-FINDINGS.html), reproducible from `src/sna_build.py` |

## 14. Fairshake PAC + 2024 cycle

| Claim | Source class | URL |
|---|---|---|
| Fairshake (FEC C00835959), Defend American Jobs (C00836221), Protect Progress (C00848440) raised ~\$260M, spent ~\$196M in 2023-2024 | PRIMARY | [FEC committee filings](https://www.fec.gov/data/) |
| Top three donors (Coinbase, Ripple, a16z principals) accounted for ~84% of funding | PRIMARY | FEC Form 3X, Schedule A |
| 53 wins of 58 targeted races | SECONDARY | [OpenSecrets summary](https://www.opensecrets.org/) |

## 15. David Sacks, former White House AI and Crypto Czar

| Claim | Source class | URL |
|---|---|---|
| Estimated ~\$200M crypto divestiture as SGE | SECONDARY | [Senate Warren-Stansbury letter, 2025-03](https://www.warren.senate.gov/) |
| Broad ethics waiver granted 2025-03-05 | PRIMARY | [White House counsel's office waiver disclosure](https://www.whitehouse.gov/) |
| OGE-278 not publicly released as of 2026-05-26 | PRIMARY | [extapps2.oge.gov/201/Presiden.nsf](https://extapps2.oge.gov/201/Presiden.nsf) (negative result) |

---

## What is not in this table

Claims about Trump-family beneficial ownership of WLFI revenue at the 75% level are PRESS-sourced from Reuters and the New York Times. No SEC filing names DT Marks DEFI LLC's interest at that percentage. The press accounts cite "people familiar with the arrangement." Treat as suggestive.

Claims about Cantor Fitzgerald serving as Tether's custodian or holding the bulk of Tether's Treasury reserves are PRESS-sourced from the WSJ 2024-11-24 piece. The Q1 2026 BDO attestation confirms the reserve dollar amount, not the custodian's identity. There is no public UCC-1 or SEC filing that names Cantor as the custodian. Treat as suggestive.

Claims about the FRBNY's internal master-account adjudication process are based on its published [Account Access Guidelines, August 2022](https://www.federalreserve.gov/aboutthefed/boardmeetings/master-account-and-services-database.htm) and the [Master Account and Services Database, updated monthly](https://www.federalreserve.gov/aboutthefed/boardmeetings/master-account-and-services-database.htm). Internal deliberative process is not public; nothing in the analysis depends on it.

---

## Reproducing the model results

```bash
git clone https://github.com/ihelfrich/eo14405-contagion
cd eo14405-contagion
pip install -r requirements.txt
python src/run_all.py
```

Expected output: `figures/*.png`, `data/*.json`, plus stdout convergence diagnostics. Total runtime ~3-5 minutes on a 2024 MacBook. Numerical results in this verification table are byte-stable across reruns once you fix the seeds in `src/seeds.py`.

---

*Dr. Ian Helfrich, Ph.D. Economics, Georgia Tech 2024. Independent researcher. No financial interest in any entity discussed. Last updated 2026-05-26.*
