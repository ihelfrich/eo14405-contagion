# Social network analysis of the EO 14405 conflict perimeter

*Compiled 26 May 2026 from the eleven dossiers in this folder. The underlying
graph is in `src/sna.py`; the edge list is in `data/sna_edges.csv`; centrality
tables in `figures/sna_centrality.json`; the publication figures in
`figures/sna_full.png` and `figures/sna_nexus.png`.*

## What we are doing

The eleven dossiers in this folder each map one corner of the political
economy surrounding Executive Order 14405. Trump and WLFI sit in one
(`trump-wlfi.md`). The Fed Board and the Reserve Bank presidents sit in
another (`fed-board.md`). The cabinet financial roster sits in a third
(`trump-admin-financial-roster.md`). The 119th Congress finance committees
sit in a fourth (`congress-finance-committees.md`). The stablecoin board
interlocks and BlackRock-Circle plumbing sit in a fifth
(`stablecoin-board-interlocks.md`). The Trump extended family, Caitlin
Long's Custodia litigation, the Sacks/a16z/Quintenz nexus, Circle and
Coinbase as issuers, Tether and Cantor, and the Fairshake campaign-finance
machine each get their own file.

Reading these in isolation produces a sequence of conflict-of-interest
narratives. Reading them as a graph produces something else: a structural
view of which individuals connect which networks, where the cut points
are, and which clusters the executive order is operationally serving.
This dossier is the read-out. It is meant as a navigational aid for
reviewers who want to test whether the qualitative findings in the
individual dossiers are robust to a quantitative restatement.

The graph was built by hand. I read each dossier, extracted every
documented relationship I could trace to a specific filing or report, and
encoded it as a directed edge with a kind, a weight, an approximate
year, and a source URL where one existed. The 153 nodes and 219 directed
edges that result are the smallest version of the graph that still
preserves the structural features the dossiers describe. Relationships
flagged as `[unverified]` or `[uncertain]` in the source dossiers were
omitted unless their omission would create a misleading gap; in that
case they are encoded with `[unverified]` in the notes field and a weight
of 0.5. The edge list in `data/sna_edges.csv` is what a reviewer should
audit. (see `src/sna.py` for the source code.)

## Structure of the graph

153 nodes. 219 directed edges, collapsing to 211 undirected edges after
multi-edges are summed. Network density on the undirected projection is
0.018, which is sparse in the standard sense but high for a hand-encoded
network with this much heterogeneity in node kind. The largest connected
component contains 152 of the 153 nodes; the singleton is an aliased name
that exists only to anchor a donation edge. Diameter on the largest
component is 9. Average shortest path length is 4.23. (Stats are computed
in `src/sna.py::compute_centrality` and saved to
`figures/sna_centrality.json`.)

Edges break down by kind as follows. Employment and policy-authority
edges dominate, because most of the people in the graph are connected to
firms or institutions through a job. Ownership and family edges are
fewer in number but heavier in weight (2.0 versus 1.0), because those
are the channels the dossiers identify as load-bearing for the conflict
analysis: Trump's claim through DT Marks DEFI LLC to 75 percent of
WLFI protocol revenue (see `trump-wlfi.md`), Cantor's 5 percent equity
stake in Tether (see `tether-ifinex.md`), Kushner's sole ownership of
Affinity Partners (see `trump-extended-family.md`), and the kinship ties
that organize the Trump family financial network.

Louvain community detection on the weighted undirected projection
returns 12 communities at the modularity-maximizing resolution. The
six largest are the ones the figure colors. Together they account for
117 of the 153 nodes. The six smaller communities are mostly two-node
or three-node pendants: Patomak Global Partners with Paul Atkins and the
SEC, for example, or the Paxos cluster sitting almost alone with State
Street.

## The six communities

**Community 1 (n = 28, Carolina Navy): Trump-WLFI + administration core.**
The largest community contains the Trump family (Donald, Don Jr., Eric,
Barron, Ivanka, Tiffany), the WLFI corporate stack (World Liberty
Financial, USD1, DT Marks DEFI LLC, BitGo Trust, the named officers
Zachary Folkman and Chase Herro), the Trump Media treasury position,
the American Bitcoin mining venture, and most of the cabinet-level
financial-policy roster: Bessent, Hassett, Pulte, Bondi, Patel, Greer,
Sauer, Rubio, Faulkender, Vought. The community structure here matches
the analytic finding in `trump-wlfi.md` that the Trump family revenue
channel is operationally one network with the administration personnel
who staff its regulatory perimeter.

**Community 2 (n = 24, Old Gold): Fairshake / a16z / industry-Congress.**
The second community is the Fairshake-led campaign-finance machine and
the legislators and venture-capital partners it funded. Marc Andreessen,
Ben Horowitz, the Andreessen Horowitz firm itself, Chris Dixon, the
Fairshake PAC and its affiliates Defend American Jobs, Protect Progress,
and Keep America Great PAC, the Stand With Crypto Alliance, plus the
elected officials in either chamber whose 2024 campaigns received
material PAC support: Bernie Moreno, Bryan Steil, Andy Barr, Ruben
Gallego. Brian Quintenz (the withdrawn CFTC Chair nominee) and Scott
Kupor sit in this community because their a16z employment edges
dominate. (see `fairshake-campaign-finance.md`,
`sacks-a16z-quintenz.md`, `congress-finance-committees.md`.)

**Community 3 (n = 22, Indiana Crimson): Fed Board + Custodia + skeptics.**
The Federal Reserve Board node itself, the Reserve Bank presidents who
are not directly connected to the Trump-WLFI core (Waller, Bowman,
Cook, Jefferson, Barr, Williams, Hammack, Kashkari, Collins, Musalem,
Goolsbee, Logan, Daly, Paulson), the Custodia Bank litigation pair
(Caitlin Long and Custodia), David Sacks, Druckenmiller (Warsh's
consulting principal), and the EO 14405 node itself. The Custodia
denial and the Kraken approval are both inside this community: the
regulators that decided both cases sit together, alongside the
analytical framework (Waller's "skinny master account") that the order
ratifies. (see `fed-board.md`, `custodia-wyoming-spdi.md`.)

**Community 4 (n = 19, Carolina Blue): BlackRock-Circle-BNY-Goldman.**
The custodial and reserve-management spine: BlackRock, Larry Fink,
Philipp Hildebrand, Robert Mitchnick, the BUIDL tokenized fund, the
Circle Reserve Fund, Circle Internet Group, USDC, Heath Tarbert, Jeremy
Allaire, Dante Disparte, M. Michele Burns (Circle director also on the
Goldman Sachs board), Craig Broderick (ex-Goldman CRO now Circle Risk
Committee chair), Rajeev Date (ex-CFPB now Circle Lead Independent
Director), Beth Hammack (Cleveland Fed President with a 31-year Goldman
career), BNY Mellon, Goldman Sachs, Securitize. This community is the
operational layer that holds the dollar tokens, manages their reserves,
and routes the redemptions. (see `stablecoin-board-interlocks.md`.)

**Community 5 (n = 13, BSE Teal): custodian nexus (Anchorage, BitGo, Brooks).**
The OCC-chartered trust company perimeter. Anchorage Digital, BitGo,
BitGo Trust, Diogo Monica, Nathan McCauley, Katie Biber, Brian Brooks,
Haun Ventures, Katie Haun, Chris Lehane, Paradigm, Frederick Ehrsam.
The community is where the regulator-to-private revolving door has been
busiest: Brooks went from OCC Acting Comptroller in 2021 to BitGo
director in 2025, with stops at Coinbase, Binance.US, and Bitfury along
the way. Biber went from Anchorage General Counsel to Paradigm Chief
Legal Officer while keeping her seat on Anchorage's board. (see
`stablecoin-board-interlocks.md`, `circle-coinbase.md`.)

**Community 6 (n = 11, Violet): Tether-Cantor-Lutnick.**
Tether, iFinex, Bitfinex, Paolo Ardoino, Giancarlo Devasini, Howard
Lutnick, Brandon Lutnick, Cantor Fitzgerald, USAT, Bo Hines, Twenty
One Capital. This is the offshore-USDT economic engine and its
U.S.-cabinet-level conduit. The community is small because Tether's
own corporate stack is shallow (a handful of named officers); the
heavy edges are the Cantor 5 percent stake, the custody of \$141 billion
in Tether's reported Treasury reserves, the USAT launch through
Anchorage in January 2026, and the SPAC business combination with
SoftBank that took the stack public. (see `tether-ifinex.md`.)

## Top 10 individuals by eigenvector centrality

Eigenvector centrality on the undirected weighted projection. The
ranking is mechanical, but the conflict assessment is mine after
cross-reading the centrality value against the qualitative dossier
content.

| Rank | Individual | Eig. cent. | Dossier conflict assessment |
|---|---|---:|---|
| 1 | Donald Trump | 0.473 | Holds the kinship and ownership edges that fan out across the entire graph. The graph centrality matches the political-economy claim in `trump-wlfi.md`: the signing principal is also the contractual beneficiary. |
| 2 | Stephen Miran | 0.162 | Triple-counted: ex-Hudson Bay Capital, ex-CEA Chair, current Fed Governor (see `trump-admin-financial-roster.md` and `fed-board.md`). The "Mar-a-Lago Accord" framework is the intellectual scaffold the EO sits on. |
| 3 | Marc Andreessen | 0.211 | Coinbase board director since December 2020, a16z co-founder, \$2.5M MAGA PAC personal donor in 2024 (see `sacks-a16z-quintenz.md`). The single node that connects industry capital, the issuer roster, and the political donor base. |
| 4 | Ben Horowitz | 0.156 | a16z co-founder, \$2.5M personal MAGA PAC donation 2024 (see `sacks-a16z-quintenz.md`). Co-anchor of the second community. |
| 5 | Scott Bessent | 0.140 | Treasury Secretary; ex-Key Square Group founder; disclosed \$250K to \$500K IBIT position at nomination with a March 2025 divestment pledge (see `trump-admin-financial-roster.md`). Sets the GENIUS Act implementing posture. |
| 6 | Christopher Waller | 0.137 | Fed Governor; intellectual author of the "skinny master account" framework EO 14405 ratifies (see `fed-board.md`). Policy conflict rather than financial conflict, but the policy conflict is exact. |
| 7 | Kevin Hassett | 0.137 | NEC Director; chairs the White House Digital Assets Working Group while holding \$1M to \$5M Coinbase common stock per June 2025 OGE filing (see `trump-admin-financial-roster.md`). |
| 8 | Brian Quintenz | 0.128 | ex-CFTC Commissioner, ex-a16z Global Head of Policy, withdrawn CFTC Chair nominee (see `sacks-a16z-quintenz.md`). Withdrawal under Winklevoss pressure illustrates the limits of the network's coordination. |
| 9 | William Pulte | 0.122 | FHFA Director; \$500K-\$1M each in Bitcoin and Solana not divested while issuing the June 25, 2025 FHFA directive ordering Fannie and Freddie to "study" crypto as mortgage reserves (see `trump-admin-financial-roster.md`). |
| 10 | Howard Lutnick | 0.117 | Commerce Secretary; family retains operational control of Cantor Fitzgerald via Brandon Lutnick; Cantor holds ~5% Tether equity and custodies the majority of Tether's ~\$141B Treasury reserves (see `tether-ifinex.md`). |

The pattern is internally consistent. The top ten are the people the
dossiers also flag as the highest-risk conflict surface, in roughly the
order the dossiers rank them. Eigenvector centrality does not tell us
anything new about who is conflicted, but it confirms that the qualitative
ranking can be derived from network position alone.

## Top 5 board interlock nodes

By the count of distinct corporate boards held simultaneously within the
ecosystem or one degree away.

1. **Marc Andreessen.** Coinbase (director since December 2020), Meta,
   Samsara, and the Andreessen Horowitz partnership itself. PCAST member
   per January 2025 press reporting. (see `sacks-a16z-quintenz.md`,
   `stablecoin-board-interlocks.md`.)

2. **M. Michele Burns.** Circle audit committee director since 2013,
   Goldman Sachs Group director, Anheuser-Busch InBev director, Etsy
   director. This is the load-bearing Circle-to-Goldman interlock:
   Burns sits on the issuer that Goldman is underwriting and on the
   investment bank doing the underwriting. (see
   `stablecoin-board-interlocks.md`.)

3. **Brian Brooks.** Now sits on BitGo (September 2025) and Strategy Inc.
   (MSTR), plus a CEO seat at Meridian Capital Group. As OCC Acting
   Comptroller he personally approved the Anchorage Digital trust
   charter in January 2021; he is now on the board of a competing trust
   company. (see `stablecoin-board-interlocks.md`.)

4. **Katie Biber.** Anchorage Digital director, Protocol Labs director,
   Rumble (NASDAQ:RUM) director, plus Paradigm Chief Legal Officer.
   Earlier in her career she was counsel to the Romney 2008 and 2012
   presidential campaigns. Sits at the intersection of crypto legal
   strategy, OCC-chartered banking, and Republican election-law
   expertise. (see `stablecoin-board-interlocks.md`.)

5. **Brandon Lutnick.** Chairman of Cantor Fitzgerald, Cantor Fitzgerald
   L.P., and Cantor Equity Partners, plus the BGC Group board. With his
   father (Howard) serving as Commerce Secretary, Brandon is the
   operational locus for the Cantor-Tether-USAT plumbing. (see
   `tether-ifinex.md`, `stablecoin-board-interlocks.md`.)

## Top 5 regulator-to-regulated revolving-door nodes

Sorted by the speed and consequence of the move.

1. **Brian Brooks (OCC Acting Comptroller → BitGo, Coinbase, Binance.US,
   Bitfury).** Approved the Anchorage Digital trust charter on January
   13, 2021 as OCC Acting Comptroller. Joined Binance.US as CEO on May
   1, 2021, fewer than four months later. Subsequent tour through
   Coinbase Chief Legal Officer, Bitfury CEO, Meridian Capital Group
   CEO, BitGo director, and Strategy Inc. (MSTR) director. (see
   `stablecoin-board-interlocks.md`.)

2. **Heath Tarbert (CFTC Chair → Citadel Securities → Circle).** Fourteenth
   CFTC Chairman, July 2019 to January 2021. Chief Legal Officer of
   Citadel Securities from April 2021. Chief Legal Officer of Circle
   from July 2023; President of Circle since January 2025. Zero gap
   between regulator role and Citadel; under four years to the President
   chair at the issuer his former regulator now reviews. (see
   `stablecoin-board-interlocks.md`.)

3. **Brian Quintenz (CFTC Commissioner 2017-2021 → a16z 2022-2025 → CFTC
   Chair nominee 2025).** Closed the loop by being nominated to chair
   the agency he had previously served as Commissioner, with the a16z
   tour in the middle. Nomination withdrawn September 2025 under
   Winklevoss-Gemini pressure, which is itself a structural feature of
   the network: the customers of one a16z portfolio firm (Coinbase
   competitors) opposed the placement of an a16z principal in the
   regulator chair. (see `sacks-a16z-quintenz.md`.)

4. **Philipp Hildebrand (Swiss National Bank Chair, BIS director, FSB
   Vice Chair → BlackRock Vice Chairman).** The central-banker-to-asset-
   manager move at the most senior level, with zero gap between the
   2012 SNB exit and the BlackRock appointment. Hildebrand carries the
   Basel and FSB relationships into BlackRock's tokenization
   conversations. (see `stablecoin-board-interlocks.md`.)

5. **Faryar Shirzad (NSC International Economic Affairs 2003-2006 → Goldman
   Sachs Office of Government Affairs ~15 years → Coinbase Chief Policy
   Officer).** Longer interval than the others, but the structural role
   is the same. Founded the Stand With Crypto Alliance in August 2023
   while at Coinbase, claiming 443,000 verified advocates as a 501(c)(4)
   advocacy arm. (see `stablecoin-board-interlocks.md`,
   `fairshake-campaign-finance.md`.)

## The Trump-Fed-Stablecoin spine

The induced subgraph in `figures/sna_nexus.png` plots the connecting
tissue. The minimal cut between Trump, the Fed Board, and the stablecoin
issuers contains roughly five named individuals. They are the people who
would have to be removed from the graph for the three subnetworks to
fall apart.

1. **Kevin Warsh.** Connects the Federal Reserve Board (as Chair from
   May 13, 2026) to the documented crypto-investor class (twenty-plus
   blockchain and digital-asset equity stakes per the April 2026 OGE
   filing, plus the undisclosed Duquesne holdings the OGE ethics officer
   flagged as out of compliance). The single highest-leverage edge in
   the graph between the Fed and the asset class the Fed regulates.
   (see `fed-board.md`.)

2. **Stephen Miran.** Connects Hudson Bay Capital (a multi-strategy
   hedge fund actively trading FTX bankruptcy claims) to the cabinet
   (as CEA Chair March 2025 to nomination) to the Federal Reserve (as
   Governor from September 2025). His November 7, 2025 Fed speech
   calling stablecoins "an established and fast-growing part of the
   financial landscape" was delivered while sitting as a voting Fed
   governor. The "Mar-a-Lago Accord" framework he wrote at Hudson Bay
   is the intellectual scaffold under EO 14405. (see
   `trump-admin-financial-roster.md`, `fed-board.md`.)

3. **Howard Lutnick.** Connects the cabinet (as Commerce Secretary) to
   Cantor Fitzgerald (via Brandon Lutnick) to Tether (via the 5 percent
   equity stake and reserve custody) to USAT (the GENIUS-compliant US
   sibling launched January 2026 through Anchorage). The Lutnick edge
   is the cleanest single explanation for why the second-largest
   beneficiary of EO 14405 is the offshore-USDT system and not a
   U.S.-domiciled issuer. (see `tether-ifinex.md`.)

4. **Kevin Hassett.** Connects the cabinet (as NEC Director) to Coinbase
   (as a Coinbase Global Advisory Council member receiving \$50,001
   before his appointment, then holding \$1M to \$5M in COIN common
   stock per the June 2025 OGE filing he did not divest) to the
   inter-agency policy file (as the chair of the White House Digital
   Assets Working Group). The July 2025 Working Group report on
   stablecoin and banking-related recommendations is the operational
   EO implementation document. (see `trump-admin-financial-roster.md`.)

5. **Brian Quintenz.** Connects a16z (as ex-Global Head of Policy) to
   the CFTC (as ex-Commissioner and Chair nominee). Even after the
   withdrawal, Quintenz remains the structural representation of the
   a16z-to-regulator route. The withdrawal itself is also informative:
   the Winklevoss objection demonstrates that the network has internal
   factions and is not a single coordinated actor. (see
   `sacks-a16z-quintenz.md`.)

If a reviewer wants the shortest possible answer to "who connects the
three subnetworks?", it is Warsh, Miran, Lutnick, Hassett, and Quintenz.
A wider answer adds Bessent (Treasury-WLFI), Pulte (FHFA-crypto-mortgage),
and Tarbert (CFTC-Circle).

## Reader exercises

Every numerical claim in this dossier traces to a specific filing or
report. To verify, here is where to look in the open record.

1. **Trump-family revenue claim.** Open SEC EDGAR, search CIK 0002043140
   for World Liberty Financial, read the Form D/A filed July 3, 2025.
   The officers of record (Folkman, Herro) and the Reg-D sales figure
   (\$52.1 million across 1,966 investors) are there. The 75 percent
   protocol-revenue claim through DT Marks DEFI LLC is in WLFI's
   separate disclosures, not the EDGAR filings; the gap between the
   two records is itself worth noting. (Companion: `trump-wlfi.md`.)

2. **Cantor 5 percent Tether stake.** The Wall Street Journal of
   November 4, 2024 is the canonical source. Cantor Fitzgerald is a
   private broker-dealer, so no SEC proxy or annual report on this
   directly. The Cantor Equity Partners SPAC business-combination
   filing of April 2025 (SEC accession 0001213900-25-044410) discloses
   Tether and iFinex as principal counterparties. (Companion:
   `tether-ifinex.md`, `stablecoin-board-interlocks.md`.)

3. **Fairshake total spend.** Pull FEC committee filings for committee
   ID C00835959 (Fairshake), C00836221 (Defend American Jobs), C00848440
   (Protect Progress). OpenSecrets aggregates these. The reported \$260.07
   million raised and \$195.83 million spent in the 2023-2024 cycle are
   directly verifiable. The top-three-donor figure (approximately 84
   percent of funding from Coinbase, Ripple, and a16z partners) requires
   adding the Schedule A receipts. (Companion: `fairshake-campaign-finance.md`.)

4. **Warsh OGE disclosure.** The April 2026 Warsh OGE-278 was publicly
   reported by CBS News and CoinDesk; the underlying PDF was not made
   public in full. Senator Warren's letter to Stanley Druckenmiller
   requesting release of the Duquesne confidentiality agreement is on
   the Senate Banking minority website. The CoinDesk April 14, 2026
   story names the twenty-plus crypto-venture stakes. (Companion:
   `fed-board.md`.)

5. **Kraken master account decision.** The Kansas City Fed approval of
   March 4, 2026 was announced through Banking Dive coverage; the Waters
   letter to Schmid is on the House Financial Services Democrats site
   as a PDF (link in `fed-board.md`). The Federal Reserve Account Access
   Guidelines (87 FR 51099, August 19, 2022) are the regulatory
   framework Schmid acted under. (Companion: `custodia-wyoming-spdi.md`,
   `fed-board.md`.)

6. **Hassett Coinbase position.** The June 2025 OGE financial disclosure
   for senior White House officials is referenced in Crypto Times
   reporting and is the canonical source for the \$1M to \$5M COIN figure.
   The pre-NEC \$50,001 from Coinbase Global Advisory Council service
   should appear in the same filing. (Companion:
   `trump-admin-financial-roster.md`.)

7. **Pulte FHFA crypto directive.** The June 25, 2025 directive itself
   is on the FHFA website. The crypto.news and American Prospect
   reporting names the \$500K-\$1M each Bitcoin and Solana positions plus
   the MARA Holdings equity. (Companion:
   `trump-admin-financial-roster.md`.)

8. **Affinity Partners Form ADV.** The March 22, 2026 amendment is
   available via SEC IAPD search for A Fin Management LLC. The \$6.16
   billion AUM and the LP composition (Saudi PIF, Qatar Investment
   Authority, Lunate) are in the filing. The Wyden letter of September
   24, 2024 has the most detail on the fee structure. (Companion:
   `trump-extended-family.md`.)

9. **Senate Banking 2024 IE spending.** Pull FEC committee filings
   C00836221 (Defend American Jobs) for the Ohio Senate IE expenditures
   against Sherrod Brown (\$40.1 million). The Coindesk September 26,
   2024 piece aggregates these. (Companion:
   `fairshake-campaign-finance.md`, `congress-finance-committees.md`.)

10. **Circle DEF 14A and S-1.** Both filings are on SEC EDGAR under CIK
    1876042. The 2026 DEF 14A (accession 0001876042-26-000112) is the
    source for the Tarbert, Burns, Broderick, Date board configuration.
    The S-1 is the source for the Circle Reserve Fund structure and the
    BlackRock-managed reserve disclosure. (Companion:
    `stablecoin-board-interlocks.md`.)

## What the graph adds to the dossiers

The dossiers, read separately, document the conflict-of-interest
perimeter as a sequence of vignettes. The graph adds three things:

First, it tests internal consistency. The top ten by eigenvector
centrality recovers the same set of individuals the dossiers flagged
as the highest-risk conflict surface. If the qualitative ranking and
the network ranking diverged sharply, the dossier-by-dossier methodology
would be suspect. They do not diverge; the agreement is a sanity check.

Second, it identifies the minimum cut. The Trump-Fed-Stablecoin spine
contains roughly five named individuals (Warsh, Miran, Lutnick, Hassett,
Quintenz, plus secondary nodes Bessent, Pulte, Tarbert). These are the
people whose removal would most fragment the network. A reviewer who
wants to understand the load-bearing structure of EO 14405 can read
those eight dossier entries and skip the rest without losing the spine.

Third, it makes the community structure visible. Louvain returns six
substantive communities that map cleanly onto the six conflict layers
the dossiers describe: Trump-WLFI core, Fairshake / industry-Congress,
Fed Board + Custodia + skeptics, BlackRock-Circle reserves, the
custodian nexus around Anchorage and BitGo, and the offshore Tether-
Cantor-Lutnick stack. The community structure is not the same as the
conflict structure (the same individual can sit at a structural cut
point without being personally conflicted), but the overlap is large
enough to be informative.

The graph is also incomplete. Spousal and immediate-family employment
for most of the Fed governors and Reserve Bank presidents is not
publicly documented (see `fed-board.md` Uncertainty section). Full
OGE-278 disclosures for cabinet appointees other than Warsh and Hassett
are not fully on the public record. The three undisclosed Affinity
Partners beneficial owners would, if disclosed, likely add edges to the
Kushner-Gulf cluster. Senate eFD and House Clerk PDFs were not pulled
for every named member of Congress (see `congress-finance-committees.md`
Uncertainty section). What the graph encodes is the documented network
as of May 26, 2026; the graph is a lower bound on the connectivity, not
an upper bound.

If the open record were ever fully released, the graph would densify
in three predictable places. The first is the spousal-employment column
for the Fed governors and Reserve Bank presidents, which is currently
empty for most of them. The second is the OGE-278 specifics for the
Trump 2.0 cabinet beyond the small set we have on Bessent, Hassett, and
Pulte. The third is the Affinity Partners LP roster, which the Wyden
letter of September 2024 documents as six foreign beneficial owners of
which three are unnamed in the public record. Adding any of those would
not change the topology in this dossier, but it would shift the
centrality numbers and could in principle reorganize the community
boundaries.

---

*Compiled May 26, 2026 by Helfrich Research in support of the EO 14405
contagion working paper. Encoded relationships and sources are in
`src/sna.py` and `data/sna_edges.csv`. Source code for centrality
computation and figure rendering is in `src/sna.py` and
`src/sna_visualize.py`. Reviewers are encouraged to audit the edge list
directly and to flag any documented relationship the graph is missing.*
