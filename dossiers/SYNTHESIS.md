# The political economy of EO 14405: a synthesis

*Companion to the working paper. Last updated 26 May 2026.*

This file synthesizes the six individual dossiers (`trump-wlfi.md`,
`sacks-a16z-quintenz.md`, `circle-coinbase.md`, `tether-ifinex.md`,
`custodia-wyoming-spdi.md`, `fairshake-campaign-finance.md`) into a single
political-economy narrative. The point is not to prove a conspiracy. It
is to map the financial and personnel networks among the people and
firms whose interests the executive order materially affects, so that
readers can independently evaluate whether the order's substantive
provisions track those interests.

## Reader's frame

The author's claim is narrow. EO 14405 is a regulatory action with
identifiable beneficiaries. Several of those beneficiaries have direct
financial relationships with the executive branch that signed the order
and with the legislative branch that prepared the political conditions
for it. Whether that constitutes corruption is a normative question this
note does not answer. Whether the relationships exist as a matter of
public record is a factual question this note documents.

If you disagree with the policy frame, the factual scaffolding below
should still be useful, because every claim in it carries a source you
can verify. Where I have inferred a connection rather than observed it
in primary documents, I have marked it. Where I have not been able to
confirm a widely-reported claim against a primary source, I have flagged
it as [secondary].

## The conflict structure in one sentence

A sitting US president signed an executive order whose principal
operational provisions materially benefit a stablecoin issuer in which
his immediate family holds a contractual claim to 75 percent of protocol
revenue, while his Commerce Secretary's investment bank holds a 5
percent equity stake in the world's largest stablecoin issuer that is
the second-largest direct beneficiary of the same order.

The dossiers document each clause of that sentence in primary sources.

## Layer 1: the Trump-family revenue channel

The most direct of the documented relationships is between World Liberty
Financial (WLFI) and the Trump family. Per SEC Form D/A filings (CIK
0002043140, accession 0002043140-25-000001, filed 3 July 2025):

- WLFI is a Delaware corporation; principal office 4400 Biscayne Blvd
  Ste 900, Miami FL.
- Officers and directors of record: Zachary Folkman, Chase Herro.
- Cumulative Reg-D sales: \$52,133,139 across 1,966 investors as of the
  filing date.

The Trump family channel is documented in WLFI's separate disclosures
(see `dossiers/trump-wlfi.md` for the chain of citations):

- **DT Marks DEFI LLC** holds a contractual claim to **75 percent of WLF
  protocol revenue**, plus a fluctuating equity stake (currently
  approximately 38 percent, down from an earlier 60 percent) in WLF
  Holdco LLC.
- DT Marks DEFI LLC is reportedly 70 percent owned by Donald Trump and
  30 percent by other family members.
- USD1, WLFI's dollar-backed stablecoin, launched in 2025. Its custodian
  is BitGo Trust (South Dakota state-chartered, master-account-eligible
  under EO 14405 Section 4).

The order's Section 4(b) and 4(c) directly affect USD1's regulatory
trajectory. Direct master-account access for USD1's BitGo Trust
custodian would lower the operational frictions and reserve-management
costs that determine WLFI's protocol revenue. The Trump family's
contractual revenue claim flows through that channel.

A parallel exposure: **DJT (Trump Media and Technology Group, NASDAQ:DJT,
CIK 0001849635)** disclosed in its Q1 2026 10-Q filed 8 May 2026 a
treasury position of **11,542 BTC plus 756 million CRO tokens** built
mid-2025 from \$2.3 billion in stock and note proceeds. The 10-Q reports
a \$405.9 million Q1 2026 net loss almost entirely from crypto markdowns.
This is a second conflict surface that EO 14405 does not directly affect
but that situates the Trump-family financial position relative to the
broader crypto-asset class.

No SEC, CFTC, or NY DFS enforcement action against WLFI or USD1 as of
this compilation. The Senate Banking Committee has sent a letter to the
SEC on file; the House has opened an investigation into an alleged \$500
million UAE 49 percent stake purchase; Duke FinReg has published an
analysis arguing WLFI's token issuance satisfies the *Howey* securities
test.

## Layer 2: Howard Lutnick, Cantor Fitzgerald, and Tether

The second-largest documented conflict in this dossier set involves the
US Secretary of Commerce, Howard Lutnick, and the world's largest
stablecoin, Tether (USDT).

Per the Wall Street Journal (24 November 2024) and subsequent disclosures:

- **Cantor Fitzgerald** (Lutnick's investment bank prior to his Cabinet
  confirmation) acquired an approximately 5 percent equity stake in
  Tether via a roughly \$600 million convertible bond.
- Cantor custodies the majority of Tether's reported \$141 billion in
  U.S. Treasury reserves.
- The Lutnick family Cantor acquisition (through Dynasty Trust A) was
  reportedly financed in part by a Tether loan, though specific terms
  are not public.

In January 2026, Cantor/Tether launched **USAT**, a GENIUS-Act-compliant
US sibling to USDT. Bo Hines is named CEO. USAT operates through
Anchorage Digital Bank, an OCC-chartered trust company whose OCC trust-bank charter is the regulatory pathway to Fed master-account eligibility under EO 14405 Section 4. This is the operational pathway through
which the offshore-USDT economic engine can acquire US Fed payment rails
without iFinex itself submitting to US consolidated supervision.

Tether's regulatory history complicates the picture. The CFTC settled a
\$41 million case against Tether and Bitfinex on 15 October 2021 for
misleading reserve attestations; the New York Attorney General
separately settled an \$18.5 million case on 23 February 2021. Tether
was barred from operating in NY State. A Wall Street Journal report (25
October 2024) described a Manhattan U.S. Attorney's office investigation
into Tether for sanctions and AML violations; Tether denied the
existence of the investigation, and no charging documents are public.

Senators Warren and Wyden opened a fourth formal congressional inquiry
into the Cantor-Tether relationship on 30 April 2026. The full text of
that inquiry is on file with the Senate Banking minority staff.

## Layer 3: David Sacks, the ethics waiver, and a16z

David Sacks served as the White House AI and Crypto Czar from January
2025 to March 2026, as a Special Government Employee (SGE).

Per Office of Government Ethics disclosures (see `dossiers/
sacks-a16z-quintenz.md`):

- Sacks divested an estimated \$200 million in crypto holdings including
  positions in Bitcoin, Ether, Solana, Bitwise 10, Coinbase, Robinhood,
  Multicoin LP, and Blockchain Capital LP.
- He received a **broad ethics waiver on 5 March 2025**, the scope of
  which has not been made public.
- His OGE-278 was never publicly released.
- Senators Elizabeth Warren and Melanie Stansbury opened a formal
  investigation into the waiver.

The a16z (Andreessen Horowitz) firm placed alumni throughout the
administration:

- **Brian Quintenz**, formerly CFTC Commissioner 2017-2021, then a16z
  Global Head of Policy 2022-2025, was nominated CFTC Chair. He
  disclosed \$3.4 million in crypto-linked assets at his confirmation
  hearing, including stakes in three a16z funds (CNK Fund III, Seed 1,
  IV) plus Kalshi equity and options. His nomination was withdrawn in
  September 2025 after the Winklevoss twins pressured the nomination
  over a Gemini complaint.
- **Scott Kupor**, formerly a16z managing partner, was confirmed Director
  of the Office of Personnel Management.
- **Marc Andreessen** sits on the President's Council of Advisors on
  Science and Technology (PCAST). Press reporting (Politico, January
  2025) suggested Andreessen spent approximately half his time at
  Mar-a-Lago in late 2024.
- a16z committed approximately **\$47 million** to the Fairshake PAC across
  the 2024 and 2026 election cycles.

a16z's Crypto Fund IV closed at \$4.5 billion in 2022; Crypto Fund V
closed at \$2.2 billion in May 2026. Marc Andreessen and Ben Horowitz
each personally gave \$2.5 million to Trump's Make America Great Again
super PAC in the 2024 cycle.

## Layer 4: the regulator-to-regulated revolving door

The most direct revolving door from regulator to regulated entity in
this set is **Heath Tarbert**, the 14th CFTC Chairman (2019-2021), now
President of Circle Internet Group (CRCL, NYSE). Circle is the issuer of
USDC, the second-largest stablecoin by market cap and the largest
US-domiciled one. The CFTC under Trump 2.0 has jurisdiction over much of
the digital-asset spot market under the proposed FIT21 / CLARITY
framework.

Secondary revolving-door instances documented in the dossiers:

- **Brian Brooks**, former Acting OCC Comptroller (2020), then Coinbase
  Chief Legal Officer (2021), now active in policy advocacy on master-
  account access.
- **Paul Atkins**, current SEC Chair, founded Patomak Global Partners,
  a consulting firm with crypto clients. His personal crypto holdings
  were disclosed in his nomination filings.
- **Brian Quintenz** (above; CFTC->a16z->CFTC nominee, withdrawn).

The pattern is consistent: senior regulators with crypto-industry
relationships, often built immediately after their public service ends,
later return to roles where they shape the same policy area they once
regulated.

## Layer 5: the campaign-finance machine

Per Federal Election Commission filings for Fairshake PAC (FEC ID
C00835959) and its affiliates Defend American Jobs (C00836221) and
Protect Progress (C00848440):

- Total funds raised by Fairshake in the 2023-2024 cycle: **\$260.07
  million**.
- Total spent: **\$195.83 million**.
- Top three donors accounted for approximately **84 percent of funding**:
  Coinbase (approximately \$75 million), Ripple (approximately \$50
  million), and Andreessen Horowitz partners (approximately \$44 million).
- Individual donors included Brian Armstrong (Coinbase), Brad
  Garlinghouse (Ripple), Tyler and Cameron Winklevoss (Gemini), Jesse
  Powell (Kraken), and Jeremy Allaire (Circle).

Race-by-race outcomes (53 wins of 58 targeted races):

- **OH-Senate**: Approximately \$40 million spent against Sherrod Brown
  (the sitting chair of the Senate Banking Committee, the relevant
  committee for stablecoin legislation). Bernie Moreno, a crypto-
  friendly Republican car dealer and founder of Champ Titles, defeated
  Brown by about 4 percentage points.
- **CA-Senate primary**: Approximately \$10 million spent against Katie
  Porter. Adam Schiff advanced; Porter lost the primary.
- **MT-Senate**: Substantial spend against Jon Tester. Tim Sheehy
  defeated him.
- **NY-16 House**: Approximately \$2.08 million against Jamaal Bowman,
  as junior partner to AIPAC's approximately \$14.5 million.

Coinbase's separate corporate lobbying spend disclosed under the Lobbying
Disclosure Act was approximately \$3.88 million federally through Q1-Q3
2024 (OpenSecrets). The Stand With Crypto Alliance, a 501(c)(4) founded
14 August 2023 by Coinbase's Faryar Shirzad, claims 443,000 verified
advocates and 2 million self-reported members.

## Layer 6: the legal substrate that the EO is operationalizing

The litigation history that produced EO 14405 is documented in
`dossiers/custodia-wyoming-spdi.md`:

- **Custodia Bank** (Wyoming SPDI, founded 2019 by Caitlin Long, formerly
  Avanti) applied for a Federal Reserve master account on 5 October 2020.
- The Federal Reserve Bank of Kansas City and the Board of Governors
  jointly denied the application on 27 January 2023.
- The U.S. District Court for the District of Wyoming upheld the denial
  in March 2024.
- The 10th Circuit affirmed by 2-1 on 31 October 2025, with Judge
  Tymkovich dissenting on Major Questions doctrine grounds.
- The 10th Circuit denied en banc review 7-3 on 13 March 2026.
- A Supreme Court certiorari petition is not docketed as of this
  compilation date.

The Federal Reserve Account Access Guidelines (87 FR 51099, 19 August
2022) codify a three-tier framework that places non-insured, non-
federally-supervised SPDIs in Tier 3 (highest scrutiny). Custodia's
denial is the canonical Tier 3 outcome.

The **Kraken Financial Limited Purpose Master Account** approval (KC Fed,
4 March 2026) is the institutional precedent EO 14405 is generalizing.
The terms are restrictive: one-year initial term, Fedwire access only,
NO interest on reserves, NO discount window access, Tier 3 review.
Kraken got the rails, not the IORB-earning master account that Custodia
sought.

The earlier **TNB USA narrow-bank** dismissal (S.D.N.Y., 25 March 2020,
Carter J.) remains the conceptual bookend: the Fed can block eligible-
but-novel applicants on policy grounds orthogonal to statutory eligibility.

## What the synthesis means for the working paper

The financial-contagion analysis in the paper documents that EO 14405
reduces stablecoin run risk along every standard metric, while
relocating the absorption mechanism onto the Federal Reserve's balance
sheet. This is a technical finding about network topology. It does not
depend on the political-economy facts in this dossier.

But the technical finding has policy implications, and the policy
implications are evaluated by political actors. The dossier documents
that several of those actors have direct financial relationships with
the policy beneficiaries. Three implications follow.

First, **the welfare conclusion in Section 6 of the paper is sensitive to
the implicit subsidy rate the Fed adopts when extending emergency
liquidity to non-bank master-account holders**. That rate will be set by
the Federal Reserve, whose chair was confirmed by a Senate where the
crypto industry materially affected several seats. The political
economy of the rate-setting decision should be visible to readers
evaluating the welfare conclusion.

Second, **the Fed's 120-day Section 4(b) report will be drafted under a
chair appointed by the same administration that signed the order**. The
appointment and the order are not independent. A report that concluded
the regional Reserve Banks lacked independent master-account authority
would constitute a direct repudiation of an order the chair's appointing
administration just signed. The institutional incentive runs in one
direction.

Third, **the conflict-of-interest pattern documented here is novel to a
financial regulatory action at this scale**. It is appropriate that a
working paper analyzing the financial-contagion implications of the
order disclose what is publicly known about those interests. Readers
should evaluate the technical findings in light of the institutional
context in which the policy will be implemented.

## Reader exercises

1. **Independent verification of the WLFI revenue claim.** Search SEC
   EDGAR for CIK 0002043140 and read the Form D/A. Note the listed
   officers and directors and the cumulative Reg-D sales. Compare to the
   reported Trump-family revenue channel via DT Marks DEFI LLC. Is the
   contractual claim documented in the EDGAR filings, or does it appear
   only in WLFI's separate disclosures? What does the gap imply?

2. **Cantor-Tether equity check.** Locate the November 2024 Wall Street
   Journal coverage of Cantor's Tether equity stake. Cross-reference
   against Cantor Fitzgerald's public disclosures (Cantor is a private
   broker-dealer, so direct SEC filings are limited; use the Treasury
   FRY-7 and FOCUS reports where applicable). Does the 5 percent figure
   appear in any primary document, or only in press reporting?

3. **Fairshake spending verification.** Pull Fairshake PAC's FEC Form 3X
   for 2024 directly from fec.gov (committee ID C00835959). Confirm or
   correct the \$260.07 million / \$195.83 million figures. Identify the
   top 10 disclosed donors and compare to the names in this dossier.

4. **Custodia certiorari watch.** Search the Supreme Court docket at
   supremecourt.gov for any cert petition filed in *Custodia Bank v.
   Federal Reserve Board* since March 13, 2026. If filed, note the
   docket number and the amicus filings.

5. **Kraken Financial master-account terms.** Locate the Federal Reserve
   Bank of Kansas City's 4 March 2026 announcement and any subsequent
   disclosures about Kraken Financial's account terms. Verify the
   "no IOR, no discount window" claim against primary FRBKC sources.

The author has done his due diligence but he is not infallible. The
exercises above are designed to give the reader concrete entry points
to either confirm or correct the factual scaffolding before evaluating
the technical contagion analysis that the paper builds on top of it.

---

## Source files

- `dossiers/trump-wlfi.md` (2,308 words)
- `dossiers/sacks-a16z-quintenz.md` (2,384 words)
- `dossiers/circle-coinbase.md` (2,816 words)
- `dossiers/tether-ifinex.md` (2,671 words)
- `dossiers/custodia-wyoming-spdi.md` (3,094 words)
- `dossiers/fairshake-campaign-finance.md` (3,078 words)

Each dossier has its own sources list. This synthesis is a navigational
aid, not a substitute for reading them.
