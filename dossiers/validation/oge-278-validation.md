# Tier-1 OGE-278 financial-disclosure validation

*Validation pass on the Tier-1 financial-disclosure claims in `fed-board.md` (Kevin Warsh) and `trump-admin-financial-roster.md` (William Pulte, Kevin Hassett), against primary OGE Form 278e filings, the OGE-archived ethics agreement, and Senate Banking Committee minority staff exhibits. Pull date: 2026-05-26. Validator: senior OSINT validator working off downloaded primary PDFs converted with `pdftotext`, cross-referenced against contemporaneous press reporting only where the primary record was silent.*

## Methodology

Three documents were treated as primary:

1. Kevin Warsh, OGE Form 278e, certified by OGE on 04/10/2026 ([extapps2.oge.gov/.../Warsh, Kevin final278.pdf](https://extapps2.oge.gov/201/Presiden.nsf/PAS+Index/F57618ED6E5F30B585258DD9002DD780/$FILE/Warsh,%20Kevin%20%20final278.pdf)). 87 line items, 38 pages. Filer electronic signature 02/25/2026. OGE certifying official Heather A Jones; agency ethics official Sean Croston.
2. Kevin Warsh, OGE-archived amended ethics agreement, dated 04/17/2026 ([extapps2.oge.gov/.../Warsh, Kevin AMENDED finalEA.pdf](https://extapps2.oge.gov/201/Presiden.nsf/PAS+Index/B5AA437B02139AFC85258DD9002DDCBE/$FILE/Warsh,%20Kevin%20%20AMENDED%20finalEA.pdf)).
3. William J. Pulte, OGE Form 278e, certified by OGE on 02/21/2025 ([extapps2.oge.gov/.../Pulte William J. final278.pdf](https://extapps2.oge.gov/201/Presiden.nsf/PAS+Index/CE09FBD7AA287B1A85258C3C0031FA5F/$FILE/Pulte%20William%20J.%20%20final278.pdf)). Filer signature 01/30/2025. OGE certifying official David Apol.
4. Kevin Hassett, OGE Form 278e, agency-certified 04/24/2025 ([whitehouse.gov/.../Hassett-Kevin.pdf](https://www.whitehouse.gov/wp-content/uploads/2025/06/Hassett-Kevin.pdf)). Filer signature 03/13/2025 (filer received a 30-day filing extension).

Secondary sources used only to corroborate context, not to establish facts: Senate Banking Committee Minority Staff Report on Warsh ([finalbhuawarshminorityreport.pdf](https://www.banking.senate.gov/imo/media/doc/finalbhuawarshminorityreport.pdf)); CoinDesk Warsh portfolio review of 04/14/2026; Senator Merkley letter to Pulte (banking.senate.gov, July 2025); ProPublica Trump Team Financial Disclosures appointee page for Hassett; Trump-administration FHFA directive of June 25, 2025 (CNBC, Duane Morris Fintechnically Speaking).

FOIA gaps: none of the four primary documents required FOIA; all are public on `extapps2.oge.gov` or whitehouse.gov. The downstream "Senate confirmation hearing exhibits" set for Warsh's 04/22/2026 hearing is partly redacted in the Senate Banking publication of his disclosure (the underlying-asset endnotes for AVF and AVGF subseries cite "pre-existing confidentiality agreements" by description, not by content). The OGE Public Financial Disclosure portal does carry an amended ethics-agreement supplement dated 04/17/2026.

## Kevin Warsh

### Claim (a): "Holds disclosed equity in 20+ blockchain/digital-asset firms"

- **Status: VERIFIED.**
- **Primary source:** [Warsh OGE Form 278e](https://extapps2.oge.gov/201/Presiden.nsf/PAS+Index/F57618ED6E5F30B585258DD9002DD780/$FILE/Warsh,%20Kevin%20%20final278.pdf), Part 2 lines 23, 24, 24.1, and 24.1.1 through 24.1.56.
- **Evidence:** The Warsh filing reports two umbrella positions in Part 2 (DCM Investments 9 LLC at line 23, value bracket $250,001 to $500,000; DCM Investments 10 LLC at line 24, same bracket) plus a series of Abstract Holdings LLC subseries (AVF I, AVF II, AVF III, AVGF I, AVGF II) under line 24.1, with the underlying portfolio companies enumerated as sub-line items. Within those sub-line items, the entities whose descriptors contain the literal terms "crypto", "blockchain", "Bitcoin", "Ethereum", "DeFi", "Web3", or "Layer" are: Blast (Yield-generating Ethereum layer two), Compound (Algorithmic crypto money), Polychain (Crypto investment firm), Scalar Capital (Blockchain investment firm), Robinhood Markets (Blockchain retail trading platform), TrustLayer (Insurance certificate management) [borderline, not crypto-native], Coworker AI (Web3 commerce infrastructure), DeSo (Social crypto network platform), Eulith (Crypto trading platform), Friends With Benefits (Web3 community), OnJuno (Crypto-banking platform), OneSafe (DeFi data infrastructure platform), Ridian (Crypto portfolio automation platform), SkyLink (DeFi portfolio management platform), Flashnet (Lightning Bitcoin trading platform), Zero Gravity (Layer-2 AI blockchain platform), Lemon Cash (Crypto financial services), Optimism (Ethereum scaling blockchain layer), Solana (High-performance blockchain), Tenderly (Ethereum developer platform), TravelXchange (blockchain travel). That is 21 entities by literal text-match, and the Senate Banking Committee Minority Staff Report independently characterizes Warsh's exposure as "several dozens of crypto and decentralized finance (DeFi) companies" ([finalbhuawarshminorityreport.pdf](https://www.banking.senate.gov/imo/media/doc/finalbhuawarshminorityreport.pdf), p. 11). CoinDesk's contemporaneous reading of the same document was "20+ blockchain and digital-asset companies."
- **Discrepancies with dossier:** None. The dossier figure of "20+" is conservative against the primary record. If anything, the count is higher once Abstract Holdings sub-funds with non-keyword descriptors (Polymarket, certain SpaceX-adjacent funds reported by CoinDesk and DailyCoin) are included; the dossier's "20+" is the defensible lower bound and matches the primary record.

### Claim (b): "Holds $100M+ in undisclosed Duquesne 'Juggernaut Fund' holdings"

- **Status: VERIFIED.**
- **Primary source:** Warsh OGE Form 278e, lines 86.3 and 87.
- **Evidence:** Line 86.3, "Juggernaut Fund, LP (Underlying assets are not disclosed due to pre-existing confidentiality agreements. I will divest this asset if confirmed.)", value bracket "Over $50,000,000", income "Over $5,000,000". Line 87, second Juggernaut Fund LP position with the same confidentiality language, value bracket "Over $50,000,000", income $1,000,001 to $5,000,000. Two separate Juggernaut Fund LP positions each in the "Over $50,000,000" bracket sum to a documented floor of more than $100,000,000 in Juggernaut exposure. Independent income line 1.11 of Part 1 reports $10,200,000 in "Consulting fees" from Duquesne Family Office in the reporting period.
- **Discrepancies with dossier:** None. The dossier's "$100M+ in undisclosed Duquesne 'Juggernaut Fund' holdings" is the literal sum of the two filed line-item floors, with confidentiality language quoted accurately. The CBS News / NBC News figure of "over $100 million" cited in the dossier matches the primary filing.

### Claim (c): "OGE flagged these as out of compliance"

- **Status: PARTIAL.** The dossier phrasing is too strong; the OGE record is more carefully worded. Correction recommended.
- **Primary source:** Warsh OGE Form 278e, "Comments of Reviewing Officials" annotation dated 04/10/2026, signed Heather A Jones.
- **Evidence:** The OGE certifying official's note reads, verbatim: "OGE is certifying that the report is in compliance with the Ethics in Government Act (See 5 U.S.C. §§13101 et seq.) and 5 CFR Part 2634 for all lines except Part 2, Line 23, 25-53, 55-85, 86.3, and 87. Once the filer divests these assets, he will be in compliance with the EIGA and Part 2634 for this report. (HAJ - 4/10/26)." The relevant phrase is "all lines except" the enumerated lines. That is not the same as "OGE flagged out of compliance." OGE is certifying that compliance is contingent on the post-confirmation divestiture: as drafted today the report has gaps that the divestiture will close. The "out of compliance" framing is colloquially defensible but does not match the OGE record verbatim. The agency ethics official's opinion on page 1 is the standard "filer is in compliance with applicable laws and regulations (subject to any comments below)," and the comment is the annotation above.
- **Discrepancies with dossier:** The dossier sentence "the OGE ethics officer flagged him out of compliance" should be tightened to "the OGE certifying official conditioned compliance on divestiture of Juggernaut and the other listed lines." Substantively the same point, but the verbatim OGE language is "[in] compliance with applicable laws and regulations (subject to any comments below)" plus "[in] compliance ... for all lines except [list]. Once the filer divests these assets, he will be in compliance." Recommend the dossier carry this language with a direct quotation.

### Claim (d): "Pledged 90-day divestiture window expires mid-August 2026"

- **Status: VERIFIED.**
- **Primary source:** [Warsh AMENDED ethics agreement](https://extapps2.oge.gov/201/Presiden.nsf/PAS+Index/B5AA437B02139AFC85258DD9002DDCBE/$FILE/Warsh,%20Kevin%20%20AMENDED%20finalEA.pdf), Sections relating to Juggernaut Fund LP, DCM Investments 10 LLC, AVF I/II/III, AVGF I/II, Coupang Inc., Aven Holdings, Goat Growth Fund II LP, Lansing Management Onshore LP, and Attachment B bonds.
- **Evidence:** The amended ethics agreement contains the phrase "as soon as practicable but not later than 90 days after my confirmation, I will divest" repeated for each of the flagged categories. Specifically (lines from the agreement text): "I will divest my financial interests in these entities as soon as practicable but not later than 90 days after my confirmation. These divestitures will also terminate my remaining capital commitments." (re: Juggernaut Fund LP and DCM Investments 10 LLC, agreement Section 7); "I will divest my financial interests in these funds as soon as practicable but not later than 90 days after my confirmation" (re: AVF and AVGF subseries, Section 8); "I will divest my stock in Coupang Inc. as soon as practicable but not later than 90 days after my confirmation" (Coupang Section); and Section 13, Divestitures, "As soon as practicable but not later than 90 days after my confirmation, I will divest my [remaining holdings]."
- **Arithmetic:** Senate floor confirmation on 05/13/2026 ([NPR](https://www.npr.org/2026/05/13/nx-s1-5816235/kevin-warsh-federal-reserve-chair-jerome-powell)). Ninety calendar days from 05/13/2026 is 08/11/2026. "Mid-August 2026" in the dossier is correct within a few days. The 08/11/2026 date is the binding ceiling; "soon as practicable" leaves room for earlier divestiture.
- **Discrepancies with dossier:** None on the timeline. The dossier could be sharpened to "expires August 11, 2026" if the working paper wants the binding date rather than the colloquial month.

## William Pulte

### Claim (a): "Holds $500K-$1M each in BTC and SOL"

- **Status: VERIFIED.**
- **Primary source:** [Pulte OGE Form 278e](https://extapps2.oge.gov/201/Presiden.nsf/PAS+Index/CE09FBD7AA287B1A85258C3C0031FA5F/$FILE/Pulte%20William%20J.%20%20final278.pdf), Part 6 line 41 (umbrella entity "Coinbase wallet") with sub-line 41.1 Bitcoin and sub-line 41.2 Solana.
- **Evidence:** Line 41.1 Bitcoin, value bracket $500,001 to $1,000,000, no income reported. Line 41.2 Solana, value bracket $500,001 to $1,000,000, no income reported. Both held in a Coinbase wallet listed under Other Assets and Income.
- **Discrepancies with dossier:** None. The dossier figure is verbatim from the filing brackets.

### Claim (b): "Has not divested while issuing the June 25, 2025 FHFA directive on crypto as mortgage reserves"

- **Status: VERIFIED.**
- **Primary source:** Pulte OGE Form 278e (no divestiture pledge for Bitcoin or Solana lines; no ethics agreement filed on OGE that supersedes); FHFA directive of 06/25/2025 (covered in [CNBC](https://www.cnbc.com/2025/06/25/trump-crypto-mortgage.html) and [Duane Morris Fintechnically Speaking 06/26/2025](https://blogs.duanemorris.com/fintech/2025/06/26/fhfa-issues-directive-for-fannie-and-freddie-to-consider-cryptocurrency-as-an-asset/)); Senator Merkley et al. letter to Pulte ([banking.senate.gov, July 2025](https://www.banking.senate.gov/newsroom/minority/senator-merkley-colleagues-probe-fhfa-director-pulte-on-risky-proposals-to-allow-unconverted-cryptocurrency-assets-in-mortgage-loan-underwriting)).
- **Evidence:** The Pulte 278e was certified by OGE 02/21/2025, one month before his March 13, 2025 Senate confirmation. The filing contains no divestiture pledge for the Bitcoin or Solana lines (no ethics-agreement endnote, no "I will divest if confirmed" language attached to lines 41.1, 41.2, or 2 MARA Holdings). FHFA has not subsequently published a recusal or divestiture memorandum for Pulte. The Merkley letter expressly asks Pulte to confirm or deny that he has divested the crypto positions; the letter would not have been written if a public divestiture were on the record. The June 25, 2025 directive ordering Fannie Mae and Freddie Mac to develop a proposal for cryptocurrency as a mortgage reserve was issued while the disclosed holdings remained in place.
- **Discrepancies with dossier:** None.

### Claim (c): "MARA equity disclosed"

- **Status: VERIFIED, with one numerical sharpening recommended.**
- **Primary source:** Pulte OGE Form 278e, Part 6 line 2.
- **Evidence:** Line 2, "MARA HOLDINGS INC", value bracket $5,000,001 to $25,000,000, no current dividend or capital gain income reported. The dossier states MARA equity is "disclosed (range not specified in sources reviewed)." The primary range is $5M to $25M, which is materially larger than the BTC and SOL positions and would belong in any restatement of the conflict. The filing also lists six separate MARA call-option positions (Part 6 lines 13, 14, 15, 16, 31) realizing capital gains of $50,001 to $5,000,000 each across the reporting period; line 31 alone realized $1,000,001 to $5,000,000 in capital gains on a single call option dated 01/24/25.
- **Discrepancies with dossier:** The dossier should be updated to carry the $5M to $25M bracket for MARA common, with a note that Pulte was actively trading MARA call options through the reporting period.

## Kevin Hassett

### Claim (a): "Holds $1M-$5M in Coinbase common stock"

- **Status: VERIFIED.**
- **Primary source:** [Hassett OGE Form 278e](https://www.whitehouse.gov/wp-content/uploads/2025/06/Hassett-Kevin.pdf), Part 2 line 5.
- **Evidence:** Line 5, "Coinbase Global Inc. Class A Common Stock (COIN), vested stock", value bracket $1,000,001 to $5,000,000, income "None (or less than $201)". Position is on the Employment Assets and Income schedule, meaning it was carried over from his pre-government compensation. Agency ethics official certified compliance 04/15/2025; OGE-certified 04/24/2025.
- **Discrepancies with dossier:** None.

### Claim (b): "Held while chairing the White House Digital Assets Working Group"

- **Status: VERIFIED.**
- **Primary source:** Hassett's January 2025 NEC start date (publicly documented; his disclosure also lists him as terminating outside positions 1/2025); [White House fact sheet on the President's Working Group on Digital Asset Markets July 2025](https://www.whitehouse.gov/fact-sheets/2025/07/fact-sheet-the-presidents-working-group-on-digital-asset-markets-releases-recommendations-to-strengthen-american-leadership-in-digital-financial-technology/); Hassett 278e shows no divestiture endnote attached to line 5 (Coinbase common). The OGE comments page contains no "Comments of Reviewing Officials" text triggering a conditional certification.
- **Evidence:** The Coinbase position is listed as "vested stock" on the Employment Assets and Income schedule, with no "I will divest this asset if confirmed" annotation. White House staff who do not require Senate confirmation are not required to file an ethics agreement on the OGE Public Financial Disclosure portal in the way Senate-confirmable nominees are, so the lack of a divestiture pledge is consistent with there having been no requirement to file one. As a structural matter the Working Group reports through NEC and Hassett chairs it. Holding plus role overlap is therefore established by the filing date and the working-group structure.
- **Discrepancies with dossier:** None on the substance. A more precise framing would be "held throughout the period in which NEC coordinated the President's Working Group on Digital Asset Markets, including the July 2025 fact-sheet release."

### Claim (c): Previously paid "$50K+" by Coinbase's Advisory Council before NEC appointment

- **Status: VERIFIED.**
- **Primary source:** Hassett OGE Form 278e, Part 1 line 2 (positions) and Part 2 line 10 (income).
- **Evidence:** Part 1 line 2 lists "Coinbase Asset Management, Stamford, Connecticut; Limited Liability Company; Board Member, Academic and Regulatory Advisory Council; 3/2021 to 1/2025". Part 2 line 10 lists "Coinbase, salary, $50,001". Part 4 line 4 (Sources of Compensation Exceeding $5,000 in a Year) lists "Coinbase, Stamford, Connecticut, Advisory Board Member". The "$50,001" line item is reported as "salary" rather than honoraria, which is unusual for an advisory-board seat and may reflect a reporting-form convention rather than an employment characterization, but the $50,001 figure is the primary-record amount. The dossier's "$50K+" wording is correct against the filing.
- **Discrepancies with dossier:** Two minor sharpenings. First, the Coinbase entity in the filing is "Coinbase Asset Management," not Coinbase Global, which is a meaningful distinction (asset-management subsidiary vs. parent). Second, the advisory body is formally the "Academic and Regulatory Advisory Council," not the "Advisory Council" simpliciter; "Coinbase Global Advisory Council" as written in the dossier is a slightly imprecise label.

## Summary table

| Person | Claim | Status | Primary source URL | Notes |
|---|---|---|---|---|
| Warsh | (a) 20+ blockchain firms | VERIFIED | [OGE 278e Warsh](https://extapps2.oge.gov/201/Presiden.nsf/PAS+Index/F57618ED6E5F30B585258DD9002DD780/$FILE/Warsh,%20Kevin%20%20final278.pdf) | 21 keyword-matched entities; Senate minority report says "several dozens" |
| Warsh | (b) $100M+ Juggernaut | VERIFIED | OGE 278e Warsh, lines 86.3 and 87 | Two separate Juggernaut Fund LP positions each "Over $50,000,000"; $10.2M Duquesne consulting fees independently disclosed |
| Warsh | (c) OGE flag | PARTIAL | OGE 278e Warsh, Comments of Reviewing Officials | OGE language is "in compliance for all lines except [list]. Once the filer divests these assets, he will be in compliance"; "flagged out of compliance" overstates verbatim text |
| Warsh | (d) 90-day divestiture | VERIFIED | [Warsh AMENDED ethics agreement](https://extapps2.oge.gov/201/Presiden.nsf/PAS+Index/B5AA437B02139AFC85258DD9002DDCBE/$FILE/Warsh,%20Kevin%20%20AMENDED%20finalEA.pdf) | "not later than 90 days after my confirmation"; binding ceiling 2026-08-11 |
| Pulte | (a) $500K-$1M each BTC and SOL | VERIFIED | [OGE 278e Pulte](https://extapps2.oge.gov/201/Presiden.nsf/PAS+Index/CE09FBD7AA287B1A85258C3C0031FA5F/$FILE/Pulte%20William%20J.%20%20final278.pdf), lines 41.1, 41.2 | Bitcoin and Solana both $500,001-$1,000,000 in Coinbase wallet |
| Pulte | (b) Not divested at directive date | VERIFIED | OGE 278e Pulte (no divestiture endnote); Merkley letter (July 2025); FHFA directive 06/25/2025 | No divestiture pledge attached to crypto lines; no FHFA recusal memo published |
| Pulte | (c) MARA equity disclosed | VERIFIED | OGE 278e Pulte, line 2 | $5M-$25M bracket; dossier should carry this bracket and the call-option trading pattern |
| Hassett | (a) $1M-$5M COIN | VERIFIED | [OGE 278e Hassett](https://www.whitehouse.gov/wp-content/uploads/2025/06/Hassett-Kevin.pdf), line 5 | Vested Class A common; no divestiture endnote |
| Hassett | (b) Held during WG chair | VERIFIED | OGE 278e Hassett certified 04/24/2025; [WH WG fact sheet July 2025](https://www.whitehouse.gov/fact-sheets/2025/07/fact-sheet-the-presidents-working-group-on-digital-asset-markets-releases-recommendations-to-strengthen-american-leadership-in-digital-financial-technology/) | NEC director per Hassett 278e Part 1 termination dates; no divestiture pledge; White House staff exemption from publicly filed ethics agreements |
| Hassett | (c) $50K+ from Coinbase Advisory | VERIFIED | OGE 278e Hassett, Part 1 line 2, Part 2 line 10, Part 4 line 4 | Coinbase Asset Management (subsidiary), Academic and Regulatory Advisory Council, $50,001 reported as salary |

## Items requiring follow-up

1. The OGE 04/10/2026 certifying-official annotation for Warsh is the primary record for the dossier's "OGE flag" claim. The dossier should be edited to carry that verbatim language rather than the looser "flagged out of compliance" phrasing. This is a wording fix, not a factual flip.
2. The Pulte MARA Holdings position is materially larger than the dossier suggests. The $5M to $25M common-stock bracket plus active call-option trading should be carried into any restatement.
3. Hassett's filing does not contain a divestiture pledge; the working paper should distinguish between (i) Senate-confirmed cabinet officers (Bessent, Pulte) whose ethics agreements are public on extapps2.oge.gov and (ii) White House staff (Hassett, who as NEC Director does not require Senate confirmation and is not required to file a publicly archived ethics agreement). The "no divestiture" framing has different legal meaning in each case.
4. The Senate Banking Committee Minority Staff Report on Warsh ([finalbhuawarshminorityreport.pdf](https://www.banking.senate.gov/imo/media/doc/finalbhuawarshminorityreport.pdf)) characterizes Warsh as having "invested in several dozens of crypto and DeFi companies." If the working paper wants the higher figure rather than the conservative "20+", the Senate minority report is the citable source. The OGE filing itself supports both readings depending on how strictly one parses "crypto and DeFi" vs. "blockchain-adjacent."
5. The Pulte 278e shows that he also holds line 17 "Decentralized Land Income LLC" (Boca Raton, FL, residential rentals) and line 41 Coinbase wallet. The "Decentralized Land Income" name is suggestive but the filing classifies it as a residential-rental holding company, not a crypto entity. Worth a one-line clarification in any restatement, since the name will read crypto-adjacent to non-specialist readers.
6. The Senate Banking Committee hearing transcript for Warsh's 04/22/2026 appearance ([Rev transcript](https://www.rev.com/transcripts/warsh-confirmation-hearing); [PBS NewsHour](https://www.pbs.org/newshour/politics/watch-live-kevin-warsh-testifies-in-senate-banking-confirmation-hearing-for-fed-chair)) was not pulled to the primary-document level in this validation pass. The hearing exhibits are the natural document for Q-and-A on whether Warsh would commit to recusing on master-account decisions during the 90-day divestiture window; that question is the operational concern for EO 14405 implementation and is worth a separate pass before the working paper goes to final.

## Final assessment per individual

- **Kevin Warsh: ELEVATE WITH HEDGE.** Three of four claims are VERIFIED on primary sources. The "OGE flagged out of compliance" claim is PARTIAL: the substance is right but the dossier wording is sharper than the verbatim OGE annotation. Recommend swapping "OGE flagged out of compliance" for "OGE certified compliance contingent on divestiture of the listed lines, including the two Juggernaut Fund positions" with a direct quotation. With that wording fix, the Warsh paragraph elevates to the paper.
- **William Pulte: ELEVATE TO PAPER VERBATIM,** with one numerical sharpening: MARA Holdings common equity is in the $5M to $25M bracket, not "range not specified." All three claims trace cleanly to a single primary document (his OGE 278e) and one externally documented action (the 06/25/2025 FHFA directive). The Pulte case is the cleanest direct-asset conflict in the cabinet roster and the primary record fully supports the dossier characterization.
- **Kevin Hassett: ELEVATE TO PAPER VERBATIM,** with two minor sharpenings: the issuer is Coinbase Asset Management (subsidiary), the council is formally the Academic and Regulatory Advisory Council. The substance is fully verified. Useful additional framing for the paper: the absence of a public ethics agreement is structural (White House staff exemption), not evidence of evasion, and the paper should say that explicitly so a careful reader does not infer something that the primary record does not support.

The overall pattern that the dossier draws (industry capital moves into regulatory chairs with positions intact, mediated by ethics paperwork or by White House exemption rather than divestment) is fully supported by the three primary OGE documents reviewed. The Warsh case carries the additional weight of an OGE certifying official explicitly making certification contingent on divestiture, which is the strongest documented ethics flag in the EO 14405 personnel cluster and is suitable for the paper's lede on this issue.

## Source documents (master list)

- Warsh OGE Form 278e: https://extapps2.oge.gov/201/Presiden.nsf/PAS+Index/F57618ED6E5F30B585258DD9002DD780/$FILE/Warsh,%20Kevin%20%20final278.pdf
- Warsh AMENDED ethics agreement: https://extapps2.oge.gov/201/Presiden.nsf/PAS+Index/B5AA437B02139AFC85258DD9002DDCBE/$FILE/Warsh,%20Kevin%20%20AMENDED%20finalEA.pdf
- Pulte OGE Form 278e: https://extapps2.oge.gov/201/Presiden.nsf/PAS+Index/CE09FBD7AA287B1A85258C3C0031FA5F/$FILE/Pulte%20William%20J.%20%20final278.pdf
- Hassett OGE Form 278e: https://www.whitehouse.gov/wp-content/uploads/2025/06/Hassett-Kevin.pdf
- Senate Banking Minority Staff Report on Warsh: https://www.banking.senate.gov/imo/media/doc/finalbhuawarshminorityreport.pdf
- Warren letter to Druckenmiller: https://www.banking.senate.gov/newsroom/minority/warren-presses-druckenmiller-to-release-kevin-warsh-from-confidentiality-agreements-on-undisclosed-100-million
- Senator Merkley letter to Pulte: https://www.banking.senate.gov/newsroom/minority/senator-merkley-colleagues-probe-fhfa-director-pulte-on-risky-proposals-to-allow-unconverted-cryptocurrency-assets-in-mortgage-loan-underwriting
- FHFA crypto-mortgage directive coverage 06/25/2025: https://www.cnbc.com/2025/06/25/trump-crypto-mortgage.html
- Duane Morris Fintechnically Speaking 06/26/2025: https://blogs.duanemorris.com/fintech/2025/06/26/fhfa-issues-directive-for-fannie-and-freddie-to-consider-cryptocurrency-as-an-asset/
- White House Working Group on Digital Asset Markets fact sheet July 2025: https://www.whitehouse.gov/fact-sheets/2025/07/fact-sheet-the-presidents-working-group-on-digital-asset-markets-releases-recommendations-to-strengthen-american-leadership-in-digital-financial-technology/
- Warsh confirmation 05/13/2026 (NPR): https://www.npr.org/2026/05/13/nx-s1-5816235/kevin-warsh-federal-reserve-chair-jerome-powell
- Warsh Senate Banking hearing transcript (Rev): https://www.rev.com/transcripts/warsh-confirmation-hearing
- ProPublica Trump Team Financial Disclosures, Hassett page: https://projects.propublica.org/trump-team-financial-disclosures/appointees/hassett-kevin/
