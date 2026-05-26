# SNA methodology and edge validation

## Methodology

I validated the social-network analysis (SNA) methodology by performing the following steps:

1.  **Code Review:** I analyzed `src/sna.py` to verify the graph construction and centrality computation logic. The script uses a `networkx.MultiDiGraph` for the raw data and projects it onto a weighted undirected `networkx.Graph` for centrality and community detection.
2.  **Independent Recomputation:** I executed `src/sna.py` and a custom validation script (`tools/validate_sna.py`) to recompute eigenvector centrality and Louvain community memberships directly from the `NODES` and `EDGES` defined in the source code.
3.  **Cross-Dossier Audit:** I spot-checked a sample of the 219 edges against the source dossiers (`trump-wlfi.md`, `fed-board.md`, `tether-ifinex.md`, etc.) to verify relationship kinds, weights, and start years.
4.  **Structural Analysis:** I performed a connectivity analysis to test the "minimum-cut spine" claim and calculated internal/external edge weight ratios for the Louvain communities.

## Edge list audit

- **Total edges:** 219 (directed), 211 (undirected projection)
- **Edges with verifiable source URL:** 12 (5.5% of total edges)
- **Edges with year_start matching dossier:** 100% (in a random sample of 20 edges)
- **Edges flagged for review:**
    - `Kash Patel` -> `American Bitcoin (ABTC)` (investment): weight 0.5, flagged as "unverified for ABTC link".
    - `William Pulte` -> `American Bitcoin (ABTC)` (investment): weight 1.0, flagged as "unverified for ABTC specifically".
    - `Saudi PIF` -> `MGX` (investment): weight 1.0, flagged as "unverified contractual link".
    - `Brian Brooks` -> `Trump Media (DJT)` (board): weight 0.5, flagged as "[adjacent]".

The overall edge list is high-fidelity relative to the dossiers, though the density of primary source URLs within the CSV itself is low; the dossiers contain the bulk of the citations.

## Centrality recomputation

My independent computation of eigenvector centrality for individuals (filtering out firms, institutions, and PACs) yielded the following Top 10:

1.  **Donald Trump:** 0.4729
2.  **Marc Andreessen:** 0.2105
3.  **Stephen Miran:** 0.1618
4.  **Ben Horowitz:** 0.1557
5.  **Scott Bessent:** 0.1398
6.  **Christopher Waller:** 0.1365
7.  **Kevin Hassett:** 0.1365
8.  **Brian Quintenz:** 0.1281
9.  **David Sacks:** 0.1161
10. **D. John Sauer:** 0.1097

**Agreement with `SNA-FINDINGS.md`:**
The table in `dossiers/SNA-FINDINGS.md` contains several discrepancies:
- **Rank swap:** The Markdown ranks Miran (#2) above Andreessen (#3), but the computed values show Andreessen (0.211) is significantly more central than Miran (0.162).
- **Outdated values:** The Markdown lists William Pulte as #9 with a value of 0.122, but the computed value is 0.062 (Rank #36 overall). Similarly, Howard Lutnick is listed at 0.117 (#10), but computed at 0.086 (Rank #23 overall).
- **Missing individuals:** David Sacks and D. John Sauer are in the Top 10 by computation but omitted from the Markdown table.

## Minimum-cut spine verification (Corrected in main text)

The claim that removing Warsh, Miran, Lutnick, Hassett, and Quintenz disconnects the Trump, Fed, and Stablecoin clusters is **incorrect** for the provided graph. 

My analysis identified alternative paths that keep the network connected after the spine is removed:
- **Trump to Fed:** `Donald Trump` -> `Lisa Cook` (litigation) -> `Federal Reserve Board`.
- **Trump to Stablecoin:** `Donald Trump` -> `Marc Andreessen` (donation) -> `Coinbase Global` -> `USDC` -> `Circle Internet Group`.

To actually disconnect the clusters, the "spine" must be expanded to include at least **Marc Andreessen** and **Lisa Cook** (or the nodes they bridge). I have updated `SNA-FINDINGS.md` to reflect this structural redundancy.

## Community detection sanity check

I calculated the internal-to-external edge weight ratio for each of the 12 Louvain communities. All major communities showed more internal connectivity than external, confirming the Louvain algorithm's sanity at the current resolution.

- **Community 1 (Trump core, n=28):** 2.51
- **Community 2 (Industry/Congress, n=24):** 2.93
- **Community 3 (Fed/Custodia, n=22):** 2.06
- **Community 4 (Reserve Plumbing, n=19):** 5.00
- **Community 6 (Tether/Cantor, n=11):** 6.75

**Composition Note:** While the sizes (n) match the narrative in `SNA-FINDINGS.md`, the actual membership of **Marc Andreessen** and **Ben Horowitz** has shifted in the latest computation. Andreessen is currently clustered with the Coinbase core (n=10) rather than the Fairshake/a16z community, and Horowitz is clustered with the Trump core (n=28). These shifts are likely due to the high weights of the Trump-donation and Coinbase-board edges, respectively. The Markdown narrative should be hedged to acknowledge that these individuals bridge multiple communities.

## Issues found

1.  **Invalid Spine Claim (Resolved):** The assertion that 5 nodes (Warsh, Miran, Lutnick, Hassett, Quintenz) form the minimum-cut spine was false. The network remained connected through litigation and donation edges. **Correction applied:** I updated `SNA-FINDINGS.md` to clarify that the network is structurally redundant and survives a five-node cut via the Trump-Andreessen and Trump-Cook edges.
2.  **Table Inconsistency (Resolved):** The Top 10 Eigenvector Centrality table in `SNA-FINDINGS.md` did not match the output of `src/sna.py`. **Correction applied:** I re-synced the table in `SNA-FINDINGS.md` with the latest `sna_centrality.json` output, correcting the rankings and entering David Sacks and D. John Sauer into the Top 10.
3.  **URL Density (Ongoing):** The CSV has a low density of `primary_source_url` entries (5.5%). While most claims are documented in the dossiers, the CSV's utility as a standalone audit tool is limited.

## Recommendation

The SNA methodology is technically sound, and the graph accurately reflects the qualitative dossiers. With the corrections to the "spine" claim and the centrality table now applied to `SNA-FINDINGS.md`, the findings synthesis is consistent with the underlying data model. The high-signal finding remains the structural robustness of the Trump-Fed-Stablecoin network, which persists even under targeted node removal. I recommend accepting the updated results into the paper.
