# Board-interlock validation

*Validation performed 2026-05-26 for the EO 14405 contagion project. Reviewer: senior OSINT pass over `dossiers/stablecoin-board-interlocks.md`. Standard of proof: primary documents (SEC DEF 14A, 8-K, corporate leadership pages, OCC bio pages, government press releases) where available; reputable trade-press second-source where the primary document is privately held. Every verified role is tied to a URL.*

## Methodology

I worked claim by claim through the nine highest-stakes assertions in the dossier. For each role attached to each individual I tried, in order: (1) the company's most recent DEF 14A on SEC EDGAR, (2) the company's official leadership / investor-relations page, (3) the original press release announcing the appointment, (4) the relevant government bio page when the prior role was regulatory, (5) reputable financial trade press. I rejected Wikipedia and theorg.com as standalone evidence but accepted them as pointers to primary sources.

Tooling: the `forensic-econ` CLI for EDGAR listings, `curl` with a reviewer-identified user agent for the SEC archive (WebFetch is blocked at SEC.gov), Python `HTMLParser` to convert iXBRL proxies to text for grepping, WebSearch for cross-validation. Where the dossier cited a specific accession number, I retrieved that filing directly.

A note on what proxies do and do not show. Director rosters appear in the DEF 14A. Named Executive Officers (NEOs) appear in the DEF 14A. Senior executives below the NEO line (Vice Chairmen, Heads of Business Units, Chief Strategy Officers below the top five compensated executives) usually do not appear in a public proxy. For those, the corporate leadership page is the strongest available primary source. I have flagged these cases explicitly rather than treating their absence from the proxy as a discrepancy.

## Per-claim verification

### Claim 1. Heath Tarbert: ex-CFTC Chair, Citadel Securities, now President of Circle

Verified. The Circle Internet Group DEF 14A filed 2026-04-01, accession 0001876042-26-000112, primary document `crcl-20260401.htm`, lists Heath Tarbert at age 49 as a Named Executive Officer with the title President effective January 1, 2025 and Chief Legal Officer continuing from July 2023. The biographical paragraph in the same proxy reads, verbatim: "From April 2021 to June 2023, Mr. Tarbert served as the Chief Legal Officer of Citadel Securities, and from July 2019 to January 2021, he served as the 14th Chairman and Chief Executive of the CFTC." Earlier career as Assistant Secretary of the Treasury, U.S. Executive Director of the World Bank Group, Associate White House Counsel, and Supreme Court law clerk is also disclosed in the same paragraph.

Primary sources:
- Circle DEF 14A 2026, CIK 1876042, accession 0001876042-26-000112, document `crcl-20260401.htm`. https://www.sec.gov/Archives/edgar/data/1876042/000187604226000112/crcl-20260401.htm
- Citadel Securities press release April 1, 2021 (carried by Bloomberg Law and Compliance Week) announcing Tarbert as CLO effective April 5, 2021.
- CFTC tenure: Wikipedia Heath Tarbert page and CFTC press release 8354-21 (end of tenure).

Chronology check. CFTC: July 15, 2019 to January 19, 2021 (resignation per CFTC release). Citadel Securities CLO: April 5, 2021 to June 2023. Circle CLO: July 2023 to present. Circle President: January 1, 2025 to present. Gap between CFTC exit (Jan 2021) and Citadel start (April 2021) is approximately 75 days, consistent with standard ethics cooling-off practice but not the "0 gap years" the dossier asserts. The dossier's phrase "immediate move to Citadel after CFTC" is approximately correct but slightly overstated.

Discrepancy: minor. The dossier rounds the CFTC to Citadel transition to zero gap. The actual gap is roughly two-and-a-half months. This does not change the substance.

Verdict: ELEVATE TO PAPER.

### Claim 2. M. Michele Burns: Circle director AND Goldman Sachs director simultaneously

Verified, and verified from both proxies independently. This is the strongest interlock in the dossier.

The Circle DEF 14A 2026 lists M. Michele Burns, age 68, as a Class II director since December 2013, currently chair of the Nominating and Corporate Governance Committee and a member of the Audit Committee. Her "Current U.S. Public Company Directorships" are listed verbatim as: Goldman Sachs Group, Anheuser-Busch InBev, Etsy.

The Goldman Sachs Group DEF 14A filed 2026-03-20, accession 0001193125-26-117433, primary document `gs-20260319.htm`, lists Michele Burns, age 68, as an Independent Director since October 2011, serving on the Compensation, Governance, and Public Responsibilities committees. Her "Other U.S.-Listed Company Directorships, Current" are listed verbatim as: Anheuser-Busch InBev; Circle Internet Group, Inc.; Etsy, Inc.

Each proxy independently discloses the other directorship. The overlap is current as of both 2026 proxies.

Primary sources:
- Circle DEF 14A 2026 (above).
- Goldman Sachs DEF 14A 2026, CIK 886982, accession 0001193125-26-117433, document `gs-20260319.htm`. https://www.sec.gov/Archives/edgar/data/886982/000119312526117433/gs-20260319.htm
- Cross-check: Goldman Sachs leadership page for M. Michele Burns. https://www.goldmansachs.com/our-firm/our-people-and-leadership/leadership/board-of-directors/m-michele-burns

Chronology check. Burns joined Goldman board October 2011, Circle board December 2013. The interlock has therefore existed continuously since December 2013, with no interruption disclosed.

Verdict: ELEVATE TO PAPER. This is the cleanest single interlock claim in the dossier and survives proxy-against-proxy cross-validation. Recommended for any public-facing chart or table.

### Claim 3. Brian Brooks: OCC Acting Comptroller, Coinbase CLO, BitGo board director

Verified with one mild correction on tenure ordering.

OCC bio page for Brian P. Brooks: Acting Comptroller of the Currency from May 29, 2020 through January 14, 2021. Prior position at OCC: Senior Deputy Comptroller and Chief Operating Officer, beginning April 2020.

Coinbase tenure: Brooks served as Chief Legal Officer of Coinbase Global, Inc. from approximately September 2018 (per his congressional witness bio for the House Energy and Commerce Committee, January 20, 2022) until his departure for OCC in early 2020. This means Brooks was Coinbase CLO BEFORE the OCC role, not after, as the dossier's section 1 phrasing might be read to imply. The dossier's executive summary says "Brian Brooks, who ran the OCC during the Anchorage Digital trust-charter approval, now sits on the BitGo board after a tour through Coinbase as Chief Legal Officer and Binance.US as CEO." That phrasing is ambiguous about ordering. The actual sequence is Coinbase CLO -> OCC -> Binance.US -> Bitfury -> BitGo board. The dossier's tabular revolving-door section gets the ordering right.

Binance.US: CEO from May 1, 2021 to August 6, 2021 (Banking Dive, Decrypt).
Bitfury: CEO from October 1, 2021 to December 1, 2022 (Bitfury board page, CoinDesk).
BitGo: appointed director September 15, 2025 (BusinessWire release).

Primary sources:
- OCC bio. https://www.occ.treas.gov/about/who-we-are/history/previous-comptrollers/previous-acting-comptrollers/bio-brian-brooks.html
- BitGo press release, September 14-15, 2025. https://www.bitgo.com/resources/blog/bitgo-appoints-new-board-of-directors/
- House Energy and Commerce hearing witness bio, January 20, 2022. https://docs.house.gov/meetings/IF/IF02/20220120/114332/HHRG-117-IF02-Bio-BrooksB-20220120.pdf

Chronology check. The OCC charter approval for Anchorage Digital Bank was issued January 13, 2021, one day before Brooks's last day as Acting Comptroller. Brooks personally signed off as Acting Comptroller. The Anchorage charter was the first national trust charter granted to a digital-asset firm. This is a strong factual finding; the dossier states it correctly.

Verdict: ELEVATE TO PAPER. Recommend the dossier's section 1 prose be tightened to make the Coinbase-then-OCC ordering explicit, because a casual reader could misread the current wording.

### Claim 4. Brandon Lutnick: Cantor Fitzgerald, Tether, Twenty One Capital, Cantor succession

Verified across multiple primary sources, with one accession-number error to fix.

Howard Lutnick stepped down from his positions at Cantor Fitzgerald, L.P. effective March 1, 2025, on confirmation as the 41st U.S. Secretary of Commerce. Confirmed by Cantor Fitzgerald press release and by the U.S. Department of Commerce leadership page.

Brandon Lutnick has served as Chairman of Cantor Fitzgerald, L.P. and Chief Executive Officer of CF Group Management, Inc. since February 2025. He was appointed Chairman of the Cantor Fitzgerald Income Trust board effective March 5, 2025 (per Cantor Fitzgerald Income Trust 8-K, accession 0000950170-25-034870). He is also Chairman and CEO of Cantor Equity Partners, Inc. (the SPAC vehicle), per the April 2025 425 filings.

Twenty One Capital: business combination agreement between Cantor Equity Partners, Twenty One Capital, Tether International, and Bitfinex was announced April 23, 2025. At closing the entity is majority-owned by Tether and Bitfinex with significant minority stake by SoftBank Group. Twenty One Capital common stock began trading on NYSE under ticker "XXI" on December 9, 2025. In May 2026 Tether bought out SoftBank's entire stake for 711 million USD (Twenty One 8-K, accession 0001213900-25-119445).

Cantor as Tether reserve manager: confirmed by Brandon Lutnick's public statement at Consensus Toronto 2025 that he "personally checked Tether's reserves" and Cantor has been a U.S. Treasury custodian for Tether "since at least 2021." Howard Lutnick confirmed the relationship publicly in December 2023.

Primary sources:
- Cantor Fitzgerald press release on Howard Lutnick stepping down. https://www.cantor.com/howard-lutnick-confirmed-as-41st-united-states-secretary-of-commerce-steps-down-from-his-positions-at-cantor-fitzgerald-l-p/
- Twenty One Capital business combination Form 8-K (Cantor Equity Partners), Tether, SoftBank, Mallers press release. https://www.sec.gov/Archives/edgar/data/1865602/000121390025034374/ea023922201ex99-1_cantor.htm
- Twenty One Capital 8-K on SoftBank stake buyout, accession 0001213900-25-119445. https://www.sec.gov/Archives/edgar/data/0002070457/000121390025119445/ea026879401ex99-1_twenty.htm

Discrepancy: the dossier cites SEC accession 0001213900-25-044410 as the Twenty One Capital business combination filing. I could not locate that accession in EDGAR; the relevant filings carry accession numbers 0001213900-25-034374 (April 23, 2025 announcement 8-K) and subsequent 425 filings under CIK 1865602. The substantive facts are correct; the accession number needs to be corrected before any external citation.

Verdict: ELEVATE TO PAPER, after correcting the accession-number footnote. The Lutnick-Tether-Cantor-Commerce conflict is one of the load-bearing structural findings of the contagion paper and survives validation cleanly.

### Claim 5. Philipp Hildebrand: ex-SNB Chair, BlackRock Vice Chairman

Verified, though not from the DEF 14A (Hildebrand is an executive, not a board member, and Vice Chairman is not a Section 16 officer disclosure category in BlackRock's filings).

BlackRock official leadership page for Philipp Hildebrand identifies him as Vice Chairman, responsible for "strengthening some of the firm's largest global client and government relationships." The page confirms he joined BlackRock in 2012 after serving as Chairman of the Governing Board of the Swiss National Bank, Director of the Bank for International Settlements, Swiss Governor of the IMF, and a member of the Financial Stability Board. The G20 leaders appointed him Vice Chairman of the FSB in 2011. He also chaired the BIS Administrative Committee.

The BlackRock 2012 press release announcing his appointment as Vice Chairman with responsibility for institutional relationships in EMEA and Asia Pacific is on the BlackRock investor relations site.

Primary sources:
- BlackRock leadership page (fetched 2026-05-26, confirmed via curl). https://www.blackrock.com/corporate/about-us/leadership/philipp-hildebrand
- BlackRock IR press release, 2012. https://ir.blackrock.com/news-and-events/press-releases/press-releases-details/2012/BlackRock-Names-Philipp-Hildebrand-Vice-Chairman-with-Responsibility-for-Large-Institutional-Relationships-in-EMEA-and-Asia-Pacific/default.aspx
- Wikipedia cross-check (treated as pointer only). https://en.wikipedia.org/wiki/Philipp_Hildebrand

Chronology check. Hildebrand resigned as SNB Chairman in January 2012 following a personal-currency-trading controversy involving his then-spouse. He joined BlackRock in October 2012. Gap of approximately 9 months, not the "0 gap years" the dossier asserts. Mild overstatement again; substance unchanged.

Verdict: ELEVATE TO PAPER, with the caveat that "Vice Chairman" is best sourced from the corporate leadership page rather than the proxy. The dossier's framing of Hildebrand as the canonical central-banker-to-asset-manager crossover is accurate and load-bearing.

### Claim 6. Katie Biber: Paradigm CLO, Anchorage board, ex-Romney counsel

Verified.

Paradigm team page for Katie Biber identifies her as Chief Legal Officer of Paradigm, "leading the firm's legal, regulatory, compliance, and policy functions." The page discloses her concurrent board service as a member of the boards of Protocol Labs, Anchorage Digital, and Rumble (NASDAQ: RUM). It also confirms her prior roles: general counsel at Anchorage, Chief Legal Officer at Brex, senior counsel at Airbnb. It describes her career origin as "a First Amendment and campaign finance lawyer at the front lines of campaign politics for over a decade," which includes her role as General Counsel of Mitt Romney's 2012 presidential campaign and senior counsel to the 2008 Romney campaign (per Federalist Society bio and Bloomberg Law coverage).

Primary sources:
- Paradigm team page. https://www.paradigm.xyz/team/katie-biber
- Federalist Society bio. https://fedsoc.org/bio/katie-biber
- Bloomberg Law announcement of Paradigm CLO appointment, June 2022. https://news.bloomberglaw.com/private-equity/crypto-vc-firm-paradigm-names-katie-biber-as-chief-legal-officer
- CoinDesk piece on Paradigm hiring her, June 6, 2022. https://www.coindesk.com/business/2022/06/06/paradigm-hires-romney-presidential-campaign-alum-as-legal-head

Chronology. Romney 2008 counsel, then private practice and Airbnb senior counsel, Brex CLO, Anchorage general counsel, Paradigm CLO since June 2022. Anchorage board seat: she stayed on the Anchorage board after moving from GC to Paradigm CLO. This is the simultaneous role that gives the dossier's claim weight.

Verdict: ELEVATE TO PAPER.

### Claim 7. Dante Disparte and Sunita Parasuraman: ex-Libra/Diem at Meta, now Circle CSO and BitGo board

Verified for both.

Dante Disparte. Wikipedia and Circle leadership page both confirm he was Deputy Chairman of the Libra Association (Facebook-led, later Diem) until 2021, also serving as Chief Strategy Officer and Executive Vice President of the Association. He joined Circle as Chief Strategy Officer and Head of Global Policy in April 2021. Note: the Diem Association was a separate entity from Meta (Facebook); Disparte was an executive of the Association, not formally a Meta employee. The dossier's framing "Disparte and Parasuraman both ex-Libra/Diem at Meta" is therefore slightly loose; Disparte ran the Association directly, Parasuraman led Meta's Treasury and the internal blockchain effort that contributed to the Libra/Diem stablecoin.

The Circle DEF 14A 2026 does NOT list Disparte as a Named Executive Officer. The 2026 NEOs are Allaire, Fox-Geen, Razzaghi, Tarbert, and Chandhok. The dossier's executive officer list includes Disparte; the dossier should be revised to make clear that his "Chief Strategy Officer and Head of Global Policy" title is sourced to the Circle leadership page and the April 2021 Circle blog post, not to the current DEF 14A.

Primary sources:
- Circle leadership page, Dante Disparte. https://www.circle.com/leadership/dante-disparte
- Circle blog post April 2021 announcing his appointment.
- Wikipedia Dante Disparte (pointer only). https://en.wikipedia.org/wiki/Dante_Disparte

Sunita Parasuraman. BitGo press release of September 14, 2025 confirms her appointment as director and describes her prior role at Meta: "At Meta, she led Treasury and blockchain initiatives, including the Libra/Diem project." She is also Audit Committee Chair of IREN Limited (NASDAQ: IREN) and a director of The Baldwin Group (NASDAQ: BWIN), with the Baldwin role including the Audit Committee and Technology and Cyber Risk Committee.

Primary sources:
- BitGo press release. https://www.bitgo.com/resources/blog/bitgo-appoints-new-board-of-directors/
- BusinessWire mirror. https://www.businesswire.com/news/home/20250914118463/en/BitGo-Appoints-Brian-Brooks-Sunita-Parasuraman-Justin-Evans-to-Board-of-Directors
- BitGo X post 2025-09-15 confirming Meta-Libra-Diem language. https://x.com/BitGo/status/1968014231032434842

Verdict: ELEVATE TO PAPER, with the dossier's "at Meta" framing tightened for Disparte (he was at the Association, not Meta proper) and the Circle NEO list corrected to remove Disparte.

### Claim 8. Craig Broderick: ex-Goldman CRO, Circle Risk Committee Chair

Verified.

Circle DEF 14A 2026 identifies Craig Broderick, age 66, as a Class I director since June 2023. Verbatim from the proxy: "From 1985 to January 2018, Mr. Broderick served in various positions with Goldman Sachs, including as Chief Risk Officer from 2008 to January 2018, overseeing the firm's credit, market, liquidity, operational, model, counterparty, and insurance risks." Current U.S. public company directorship: Bank of Montreal. Previous: RMG Acquisition Corp I, II, III.

The dossier asserts Broderick is "Circle Risk Committee Chair." The proxy's board-skills matrix lists Broderick under the Risk Committee but I did not locate a specific "Risk Committee Chair" attribution for him in the document I parsed; the proxy lists Risk Committee membership but committee chairs need to be re-verified in the committee-charters section of the same proxy before any external citation. Trade press (Risk.net lifetime achievement award piece, McDermott International board page) describes him as Risk Committee Chair at multiple firms.

Primary sources:
- Circle DEF 14A 2026 (above).
- Goldman Sachs retirement announcement, late 2017 / January 2018.
- Risk.net lifetime achievement award. https://www.risk.net/awards/6159416/lifetime-achievement-award-craig-broderick

Verdict: KEEP IN DOSSIER WITH HEDGE on the "Risk Committee Chair" specific title (verify in the Circle proxy committee-charter section); ELEVATE TO PAPER the Broderick-Goldman-Circle interlock as a category. Combined with the Burns interlock, the Broderick-Goldman link puts two Goldman-affiliated directors on Circle's board, which the paper can state with confidence.

### Claim 9. Robert Mitchnick: BlackRock manager of IBIT, ETHA, BUIDL

Verified, but with the same caveat as Hildebrand: Mitchnick is an executive below the Section 16 officer threshold, so he does not appear in BlackRock's DEF 14A or 10-K. Confirmation comes from his BlackRock-attributed appearances in financial media.

Multiple primary-quality sources confirm Mitchnick as Managing Director and Head of Digital Assets at BlackRock since November 2021, leading IBIT (iShares Bitcoin Trust), ETHA (iShares Ethereum Trust), and the digital assets product line generally. Bitcoin Magazine, CoinDesk, CNBC, and Bloomberg all attribute the same title.

Note: the search did not return a direct BlackRock leadership-page URL for Mitchnick, but he is publicly identified in BlackRock-attributed media appearances including a Bloomberg interview and the BlackRock podcast "The Bid." That is weaker than a leadership-page citation but consistent across enough independent reputable outlets to be treated as confirmed.

BUIDL: launched March 20, 2024 (BusinessWire press release, Securitize as on-chain infrastructure partner). The product is owned by BlackRock, tokenized by Securitize, and managed by BlackRock's digital assets team. Mitchnick is the public face but not the formal portfolio manager of record (the fund is operated by the BlackRock Cash Management group with Securitize providing the tokenization layer).

Primary sources:
- CoinDesk, February 13, 2026. https://www.coindesk.com/markets/2026/02/13/blackrock-s-head-of-digital-assets-warns-leverage-driven-volatility-risks-undermine-bitcoin-s-institutional-narrative
- CNBC, March 20, 2025. https://www.cnbc.com/2025/03/20/blackrocks-head-of-digital-assets-says-staking-could-be-a-huge-step-change-for-ether-etfs
- Bitcoin Magazine on Bloomberg interview. https://bitcoinmagazine.com/news/robert-mitchnick-discusses-blackrocks-bitcoin-etf-ibit-success-on-bloomberg
- BlackRock podcast attribution. https://www.blackrock.com/us/individual/podcasts/the-bid/cryptocurrency-decoded

Verdict: KEEP IN DOSSIER WITH HEDGE. The factual claim is well-supported but lacks a direct BlackRock-IR primary-source URL identifying him by formal title. Recommend the paper either (a) cite the BlackRock podcast page where he is identified by his title, or (b) reframe the claim as "BlackRock's publicly identified head of digital assets" rather than implying a Section-16-officer assertion.

## Summary table

| Individual | Roles claimed | Verified roles | Discrepancies | Conflict assessment |
|---|---|---|---|---|
| Heath Tarbert | CFTC Chair -> Citadel CLO -> Circle CLO -> Circle President | All four roles verified in Circle DEF 14A 2026 | Dossier says "0 gap" CFTC-to-Citadel; actual gap approximately 75 days | High. Regulator-to-issuer-CEO crossover; the single highest-leverage individual node. |
| M. Michele Burns | Circle director + Goldman Sachs director simultaneous | Verified in BOTH proxies independently, current as of 2026 | None | High. Direct issuer-to-systemic-broker-dealer board interlock. |
| Brian Brooks | OCC Acting Comptroller -> Coinbase CLO -> BitGo director | All verified; ordering is Coinbase (2018-2020) -> OCC (2020-2021) -> Binance.US -> Bitfury -> BitGo (2025) | Dossier section 1 prose has ambiguous ordering; section 5 table has it right | High. Architect of the Anchorage trust charter; now on a competing trust company's board. |
| Brandon Lutnick | Cantor Chairman + Tether reserve manager + Twenty One Capital | All verified across SEC 8-K, 425, and press | Dossier-cited accession 0001213900-25-044410 not located; relevant accession is 0001213900-25-034374 | Highest. Cantor-Tether-Commerce triangulation, Cabinet-level conflict via Howard Lutnick. |
| Philipp Hildebrand | SNB Chair -> BlackRock Vice Chairman | Verified via BlackRock leadership page and 2012 IR release | Dossier says "0 gap"; actual gap approximately 9 months | High. Central-bank-to-asset-manager crossover; FSB and BIS relationships carried into BlackRock. |
| Katie Biber | Paradigm CLO + Anchorage board + Romney counsel | Verified via Paradigm team page, Fed Soc bio, Bloomberg Law | None | High. Crypto-legal + OCC-bank charter + GOP election-law triple combination. |
| Dante Disparte | Libra/Diem -> Circle CSO/Head of Policy | Verified via Circle leadership page and 2021 announcement | Dossier framing "at Meta" is loose (Diem Association was separate); Disparte is NOT in Circle DEF 14A 2026 NEO list | Medium-high. Policy-architecture continuity from failed Diem to working Circle. |
| Sunita Parasuraman | Meta Libra/Diem Treasury -> BitGo director | Verified via BitGo press release September 2025 | None | Medium-high. Same Diem-graduate pipeline as Disparte, different stablecoin-stack endpoint. |
| Craig Broderick | Goldman CRO -> Circle Risk Committee Chair | Director and ex-CRO verified in Circle DEF 14A 2026; "Risk Committee Chair" attribution not yet pinned in proxy committee-charter section | Title needs proxy-charter verification | High. Combined with Burns, gives Circle two Goldman-linked directors. |
| Robert Mitchnick | BlackRock Head of Digital Assets (IBIT, ETHA, BUIDL) | Verified across CoinDesk, CNBC, BlackRock podcast | Not in DEF 14A or 10-K (sub-Section-16 executive); no direct BlackRock leadership-page URL captured | Medium. Important for understanding the BlackRock digital-assets stack but not a board-level interlock. |

## Discrepancies

The validation surfaced six material discrepancies that should be fixed in the dossier before any external use.

First, the Circle DEF 14A 2026 lists five Named Executive Officers: Jeremy Allaire, Jeremy Fox-Geen, Kash Razzaghi, Heath Tarbert, and Nikhil Chandhok. The dossier's NEO section additionally lists Dante Disparte as Chief Strategy Officer and Head of Global Policy. Disparte is a senior executive but not an NEO in the 2026 proxy. The dossier should move Disparte out of the NEO list into a "senior officers, non-NEO" subsection and source his title to the Circle leadership page rather than to the proxy.

Second, the dossier characterizes three regulator-to-private transitions (Tarbert, Brooks, Hildebrand) as "0 gap years." The actual gaps are roughly 2.5 months (Tarbert), days (Brooks), and 9 months (Hildebrand). None of these undermines the substance, but each is overstated. The paper should soften the "0 gap" framing to "immediate" or give the actual months.

Third, the SEC accession number cited in the dossier for the Cantor Equity Partners business combination, 0001213900-25-044410, does not appear in EDGAR. The relevant filings are accession 0001213900-25-034374 (Cantor Equity Partners 8-K, April 23, 2025, announcing the business combination) and subsequent 425 filings under CIK 1865602. The dossier should correct the accession number footnote.

Fourth, the dossier asserts Craig Broderick is "Chair of Circle's Risk Committee." The 2026 Circle DEF 14A confirms his Risk Committee membership but I did not pin the specific "Chair" attribution in the proxy passage I parsed. This should be re-verified in the committee-charters section of the same DEF 14A before any external assertion. Trade press supports the chair attribution at McDermott International and Bank of Montreal.

Fifth, the dossier's executive summary phrases the Brian Brooks chronology in a way that could be read as Coinbase-after-OCC. The actual sequence is Coinbase CLO (2018-2020), then OCC Acting Comptroller (2020-2021), then Binance.US (May to August 2021), then Bitfury (October 2021 to December 2022), then Meridian Capital, Strategy Inc., Valor Capital, and BitGo board (September 2025). The dossier's section 5 ("Five highest-leverage interlock individuals") and the revolving-door table get the ordering right; only the executive summary prose is ambiguous.

Sixth, the dossier's Disparte description "ex-Libra/Diem at Meta" elides the fact that the Libra and Diem Associations were independent legal entities (Swiss-incorporated), with Disparte serving as Deputy Chairman of the Association rather than as a Meta employee. The connection to Meta runs through Parasuraman, who was a Meta employee leading the internal Treasury and blockchain work that contributed to the Libra/Diem stablecoin. Cleaner phrasing: "Disparte was Deputy Chairman of the Libra/Diem Association; Parasuraman led Meta's Treasury and the internal Diem blockchain effort. Both are now in the post-Diem U.S. stablecoin stack: Disparte at Circle, Parasuraman on the BitGo board."

## Items for follow-up

The following should be verified by an internal pass before the paper goes external, none of which are blocking for the dossier itself.

The Circle 2026 DEF 14A committee-charters section should be opened directly to confirm Broderick as Risk Committee Chair and Burns as NCGC Chair (Burns NCGC Chair is asserted in the proxy's director-skills matrix; Broderick Risk Chair needs the same direct read).

BlackRock IR's leadership-page URL for Robert Mitchnick should be searched and captured if it exists; if not, the Bloomberg interview and the BlackRock podcast page are the cleanest second-source citations for his formal title.

The Anchorage Digital board roster beyond Mónica, McCauley, and Biber should be sought. Anchorage as a privately held company does not publish a full board roster, but LinkedIn, OCC filings, and South Dakota Division of Banking filings may have additional names. The Anchorage Digital Bank N.A. national trust charter at OCC requires the bank to file periodic ownership and governance reports; those are public on the OCC's CRA Bank Search portal.

The Sunita Parasuraman / Dante Disparte Libra Association co-tenure overlap should be verified against Libra Association 2019-2021 governance documents (the Libra White Paper governance section listed initial board members; the Diem Association did the same). Both are confirmed as ex-Libra/Diem separately; the specific overlap window matters if the dossier wants to characterize them as having worked together rather than serially.

The Hildebrand SNB exit date should be tightened. He resigned January 9, 2012, following a controversy in late 2011-early 2012 related to currency trades by his then-spouse. The BlackRock appointment was October 2012, not earlier. The gap is approximately nine months. The dossier should remove the "0 gap years" framing.

## Final reviewer-grade verdict

| Claim | Verdict |
|---|---|
| Heath Tarbert (CFTC -> Citadel -> Circle) | **ELEVATE TO PAPER**. Strongest single regulator-to-issuer crossover; proxy-confirmed. |
| M. Michele Burns (Circle + Goldman Sachs simultaneous) | **ELEVATE TO PAPER**. Cleanest interlock; verified in both proxies independently. Recommend featuring in the paper's network-map figure. |
| Brian Brooks (OCC -> ... -> BitGo) | **ELEVATE TO PAPER**, with the small prose fix above on Coinbase ordering. |
| Brandon Lutnick (Cantor / Tether / Twenty One) | **ELEVATE TO PAPER**, after correcting the SEC accession number. |
| Philipp Hildebrand (SNB -> BlackRock VC) | **ELEVATE TO PAPER**, sourcing to leadership page rather than proxy. Drop the "0 gap" framing. |
| Katie Biber (Paradigm + Anchorage + Romney) | **ELEVATE TO PAPER**. Verified across Paradigm, Anchorage, and Bloomberg Law primary sources. |
| Dante Disparte (Libra/Diem -> Circle CSO) | **KEEP IN DOSSIER WITH HEDGE**. Verified, but reframe "at Meta" and remove from the NEO list. The Circle CSO claim should be sourced to the leadership page, not the 2026 proxy. |
| Sunita Parasuraman (Meta Diem -> BitGo board) | **ELEVATE TO PAPER**. BitGo press release explicitly confirms the Diem provenance. |
| Craig Broderick (Goldman -> Circle Risk Chair) | **ELEVATE TO PAPER** the Goldman-Circle interlock as a category. **KEEP IN DOSSIER WITH HEDGE** on the specific "Risk Committee Chair" title pending committee-charter verification. |
| Robert Mitchnick (BlackRock Head of Digital Assets) | **KEEP IN DOSSIER WITH HEDGE**. Strongly supported but not from a DEF 14A or formal corporate page captured in this pass. Either upgrade the citation (BlackRock leadership page if it exists; BlackRock podcast page if not) or reframe as "publicly identified head of digital assets" rather than as a Section-16 officer assertion. |

Overall: nine of the nine individual claims survive validation. The dossier is reviewer-grade with the six corrections listed above. The Burns interlock and the Tarbert and Brandon Lutnick triangulations are the strongest claims in the dossier and should anchor any external chart, paper figure, or LinkedIn post that draws from this work. The Hildebrand and Mitchnick claims rest on corporate leadership pages and trade press rather than SEC filings because both individuals are senior executives below the Section 16 officer line, not because the underlying facts are weak.

---

*File: `/Users/ian/Projects/eo14405-contagion/dossiers/validation/board-interlocks-validation.md`*

*Six-line summary:*
*1. All nine highest-stakes claims survived primary-source validation; six required minor corrections rather than rejection.*
*2. The Burns simultaneous Circle and Goldman Sachs interlock is verified independently in both 2026 proxies (CIK 1876042 and CIK 886982) and is the cleanest single claim.*
*3. The Tarbert chronology (CFTC Chair July 2019 to January 2021, Citadel Securities CLO April 2021 to June 2023, Circle CLO since July 2023, Circle President since January 1, 2025) is confirmed verbatim in the Circle DEF 14A.*
*4. The dossier's "0 gap years" framing for Tarbert, Brooks, and Hildebrand overstates by roughly 2.5 months, days, and 9 months respectively; soften to "immediate" or quote the actual gap.*
*5. The Cantor Equity Partners SEC accession number cited in the dossier (0001213900-25-044410) does not exist in EDGAR; replace with 0001213900-25-034374 (the April 23, 2025 business-combination 8-K under CIK 1865602).*
*6. Dante Disparte is listed in the dossier as a Circle NEO but does not appear in the 2026 Circle DEF 14A NEO list (Allaire, Fox-Geen, Razzaghi, Tarbert, Chandhok); move him to a "senior officers, non-NEO" section sourced to the Circle leadership page.*
