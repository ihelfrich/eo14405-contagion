"""
sna.py -- Social network analysis of the EO 14405 conflict-of-interest perimeter.

Hand-encoded from the eleven dossiers in ``dossiers/``. Each Edge carries a
``primary_source_url`` pointing to the documenting filing or report. The graph
is a ``networkx.MultiDiGraph``; centrality measures are computed on the
underlying undirected projection.

Outputs
-------
- ``figures/sna_centrality.json``   ranked centrality tables
- ``data/sna_edges.csv``            edge list reviewers can audit

Conventions
-----------
- Node kind: ``person``, ``firm``, ``institution``, ``pac``.
- Edge kind: ``employment``, ``family``, ``board``, ``donation``,
  ``investment``, ``custody``, ``regulator``, ``revolving_door``, ``kinship``,
  ``ownership``, ``policy_authority``, ``litigation``.
- Priority of a node: ``high``, ``medium``, ``low`` (drives node sizing tiebreaker
  in the visualization and informs the conflict-tier assessment in the
  accompanying SNA-FINDINGS.md write-up).
- Weight on an edge: 1.0 default; 2.0 for relationships the dossiers explicitly
  flag as the load-bearing channel (e.g., DT Marks DEFI's 75% revenue claim,
  the Cantor-Tether 5% equity stake).
"""

from __future__ import annotations

import csv
import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Iterable

import networkx as nx

# --------------------------------------------------------------------------
# Paths
# --------------------------------------------------------------------------

HERE = Path(__file__).resolve().parent.parent
DATA_DIR = HERE / "data"
FIG_DIR = HERE / "figures"
DATA_DIR.mkdir(parents=True, exist_ok=True)
FIG_DIR.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------------------------------
# Data classes
# --------------------------------------------------------------------------


@dataclass
class Node:
    name: str
    kind: str  # person | firm | institution | pac
    role: str = ""
    organization: str = ""
    priority: str = "medium"  # high | medium | low
    notes: str = ""


@dataclass
class Edge:
    source: str
    target: str
    kind: str
    weight: float = 1.0
    year_start: int | None = None
    notes: str = ""
    primary_source_url: str = ""


# --------------------------------------------------------------------------
# Nodes
# --------------------------------------------------------------------------

NODES: list[Node] = [
    # ----- Trump family and WLFI -----
    Node("Donald Trump", "person", "President of the United States", "White House",
         "high", "Signed EO 14405; ~70% of DT Marks DEFI LLC"),
    Node("Donald Trump Jr.", "person", "Co-founder American Bitcoin", "Trump Org",
         "high", "Eric Trump's American Bitcoin co-founder; DT Marks DEFI beneficiary"),
    Node("Eric Trump", "person", "Co-founder American Bitcoin", "Trump Org",
         "high", "American Bitcoin / WLFI promoter"),
    Node("Barron Trump", "person", "WLFI promoter", "Trump family",
         "medium", "Promoted WLFI launch"),
    Node("Jared Kushner", "person", "Founder, Affinity Partners", "Affinity Partners",
         "high", "$6.16B AUM, ~99% non-US-investor money"),
    Node("Ivanka Trump", "person", "Affinity Partners partner", "Affinity Partners",
         "medium", "Sazan Island Albania participant"),
    Node("Massad Boulos", "person", "Senior Advisor on Arab/ME Affairs; Africa", "State Department",
         "medium", "Trump in-law in two regional policy portfolios"),
    Node("Michael Boulos", "person", "Trump in-law", "SCOA Nigeria/Fadoul Group",
         "low", "Tiffany Trump's spouse"),
    Node("Tiffany Trump", "person", "Trump family", "Trump family", "low", ""),
    Node("Lara Trump", "person", "Fox News host", "Fox News", "low", "Eric Trump's spouse"),
    Node("Kimberly Guilfoyle", "person", "US Ambassador to Greece", "State Department",
         "low", "Confirmed September 2025"),

    # WLFI firms
    Node("World Liberty Financial", "firm", "Stablecoin issuer (USD1)", "WLFI",
         "high", "CIK 0002043140; 75% revenue to DT Marks DEFI"),
    Node("USD1", "firm", "Trump-family stablecoin", "WLFI", "high", "Launched 2025"),
    Node("DT Marks DEFI LLC", "firm", "Trump-family revenue vehicle", "Trump family",
         "high", "Holds 75% of WLF protocol revenue"),
    Node("Trump Media (DJT)", "firm", "Truth Social / TruthFi", "Trump Media",
         "high", "11,542 BTC + 756M CRO treasury; CIK 0001849635"),
    Node("American Bitcoin (ABTC)", "firm", "Bitcoin miner", "Trump family",
         "medium", "Eric Trump + Don Jr; merged with Gryphon Digital Mining"),
    Node("Affinity Partners", "firm", "Private equity fund", "Kushner",
         "high", "$6.16B AUM as of Mar 2026 ADV"),
    Node("BitGo Trust", "firm", "USD1 custodian, SD-chartered", "BitGo",
         "high", "Master-account-eligible under EO 14405"),
    Node("Zachary Folkman", "person", "WLFI officer", "WLFI", "medium", ""),
    Node("Chase Herro", "person", "WLFI officer", "WLFI", "medium", ""),

    # Foreign LPs / counterparties
    Node("Saudi PIF", "institution", "Sovereign wealth fund", "Saudi Arabia",
         "high", "$2B Affinity commitment; 1.25% fee"),
    Node("Qatar Investment Authority", "institution", "Sovereign wealth fund", "Qatar",
         "medium", "~$1.5B Affinity 2024 commitment"),
    Node("Lunate", "firm", "Abu Dhabi asset manager", "UAE",
         "medium", "Co-invested with QIA in Affinity"),
    Node("MGX", "firm", "UAE state-backed crypto investor", "UAE",
         "high", "$2B USD1 settlement to Binance May 2025"),

    # ----- Trump 2.0 administration -----
    Node("Scott Bessent", "person", "Treasury Secretary", "Treasury",
         "high", "ex-Key Square; IBIT $250K-$500K"),
    Node("Howard Lutnick", "person", "Commerce Secretary", "Commerce",
         "high", "ex-Cantor Fitzgerald CEO; family retains control"),
    Node("Brandon Lutnick", "person", "Chairman, Cantor Fitzgerald", "Cantor Fitzgerald",
         "high", "Howard Lutnick's son; chairs Cantor stack from Feb 2025"),
    Node("Kevin Hassett", "person", "NEC Director", "White House",
         "high", "$1M-$5M COIN; chairs Digital Assets Working Group"),
    Node("Stephen Miran", "person", "ex-CEA Chair; Fed Governor", "Federal Reserve",
         "high", "ex-Hudson Bay Capital; Mar-a-Lago Accord author"),
    Node("William Pulte", "person", "FHFA Director", "FHFA",
         "high", "$500K-$1M each BTC + SOL + MARA equity, not divested"),
    Node("Russell Vought", "person", "OMB Director", "OMB", "medium",
         "Project 2025 lead architect"),
    Node("Mike Faulkender", "person", "ex-Deputy Treasury; ex-Acting IRS Comm.",
         "Treasury", "medium", "ex-AFPI Chief Economist"),
    Node("Pamela Bondi", "person", "ex-Attorney General", "DOJ",
         "medium", "ex-Ballard Partners; fired April 2026"),
    Node("Kash Patel", "person", "FBI Director", "FBI", "medium",
         "ex-Trump Media board; GBTC + CORZ holdings"),
    Node("Jamieson Greer", "person", "USTR", "USTR", "low",
         "ex-King & Spalding (Cleveland-Cliffs, BASF)"),
    Node("D. John Sauer", "person", "Solicitor General", "DOJ", "low",
         "ex-Trump personal counsel"),
    Node("Marco Rubio", "person", "Secretary of State", "State Department", "low",
         "Board of Peace / Gaza stablecoin"),
    Node("David Sacks", "person", "ex-AI/Crypto Czar (SGE)", "White House",
         "high", "Jan 2025 - Mar 2026; broad ethics waiver"),
    Node("Paul Atkins", "person", "SEC Chair", "SEC", "high",
         "ex-Patomak Global Partners"),
    Node("Brian Quintenz", "person", "ex-CFTC Comm.; withdrawn CFTC Chair nominee",
         "a16z/CFTC", "high", "ex-a16z Global Head of Policy"),
    Node("Scott Kupor", "person", "OPM Director", "OPM", "medium",
         "ex-a16z Managing Partner"),
    Node("Heath Tarbert", "person", "President, Circle; CLO Circle", "Circle",
         "high", "ex-14th CFTC Chair; ex-Citadel Securities CLO"),
    Node("Brian Brooks", "person", "BitGo director; MSTR director", "BitGo/MSTR",
         "high", "ex-OCC Acting Comptroller"),

    # ----- Fed Board + Reserve Bank presidents -----
    Node("Kevin Warsh", "person", "Fed Chair (May 2026)", "Federal Reserve",
         "high", "$100M+ disclosed; 20+ crypto-venture stakes"),
    Node("Christopher Waller", "person", "Fed Governor", "Federal Reserve",
         "high", "Author 'skinny master account' framework"),
    Node("Michelle Bowman", "person", "Vice Chair for Supervision (Fed)",
         "Federal Reserve", "high", "Kraken master account 'pilot'"),
    Node("Lisa Cook", "person", "Fed Governor", "Federal Reserve", "low",
         "Trump v. Cook removal litigation"),
    Node("Philip Jefferson", "person", "Vice Chair (Fed)", "Federal Reserve", "low", ""),
    Node("Michael Barr", "person", "Fed Governor; ex-VC Supervision",
         "Federal Reserve", "low", "Stepped down Feb 2025"),
    Node("Jeffrey Schmid", "person", "KC Fed President", "Federal Reserve",
         "high", "Approved Kraken Financial master account Mar 2026"),
    Node("John Williams", "person", "NY Fed President", "Federal Reserve", "medium", ""),
    Node("Beth Hammack", "person", "Cleveland Fed President", "Federal Reserve",
         "medium", "31-year Goldman Sachs veteran"),
    Node("Neel Kashkari", "person", "Minneapolis Fed President", "Federal Reserve",
         "low", "Stablecoins 'buzzword salad'"),
    Node("Susan Collins", "person", "Boston Fed President", "Federal Reserve", "low", ""),
    Node("Alberto Musalem", "person", "St Louis Fed President", "Federal Reserve",
         "medium", "ex-Tudor Investment Corp"),
    Node("Austan Goolsbee", "person", "Chicago Fed President", "Federal Reserve", "low", ""),
    Node("Lorie Logan", "person", "Dallas Fed President", "Federal Reserve", "low",
         "ex-NY Fed SOMA Manager"),
    Node("Mary Daly", "person", "SF Fed President", "Federal Reserve", "low", ""),
    Node("Tom Barkin", "person", "Richmond Fed President", "Federal Reserve",
         "low", "ex-McKinsey"),
    Node("Anna Paulson", "person", "Philadelphia Fed President", "Federal Reserve", "low", ""),
    Node("Stanley Druckenmiller", "person", "Founder, Duquesne Family Office",
         "Duquesne Family Office", "medium", "Warsh consulting principal"),

    # Federal Reserve institutions
    Node("Federal Reserve Board", "institution", "Central bank Board of Governors",
         "Federal Reserve", "high", ""),
    Node("Kansas City Fed", "institution", "Reserve Bank", "Federal Reserve",
         "high", "Approved Kraken master account"),

    # ----- Congress -----
    Node("Tim Scott", "person", "Senate Banking Chair (R-SC)", "US Senate",
         "high", "GENIUS Act co-sponsor"),
    Node("Cynthia Lummis", "person", "Chair, Senate Subcom. on Digital Assets (R-WY)",
         "US Senate", "high", "Personal BTC >$100K; BITCOIN Act sponsor"),
    Node("Bill Hagerty", "person", "Senator (R-TN)", "US Senate", "high",
         "Lead Senate sponsor of GENIUS Act"),
    Node("Mike Crapo", "person", "Senator (R-ID)", "US Senate", "medium", ""),
    Node("Bernie Moreno", "person", "Senator (R-OH)", "US Senate", "high",
         "$40.1M Defend American Jobs IE support; ex-Champ Titles"),
    Node("Ruben Gallego", "person", "Senator (D-AZ)", "US Senate", "high",
         "$10M Protect Progress IE support"),
    Node("Andy Barr", "person", "Representative (R-KY)", "US House", "high",
         "~$7M Fairshake 2026 primary support; $2.3M Foris DAX"),
    Node("Elizabeth Warren", "person", "Senate Banking Ranking Member (D-MA)",
         "US Senate", "high", "Lead Senate antagonist"),
    Node("Jack Reed", "person", "Senator (D-RI)", "US Senate", "low", ""),
    Node("Sherrod Brown", "person", "ex-Senate Banking Chair (D-OH)", "US Senate (former)",
         "medium", "Defeated by Moreno after $40M IE spend"),
    Node("French Hill", "person", "House Fin. Services Chair (R-AR)", "US House",
         "high", "ex-Delta Trust & Banking founder, Regions Bank"),
    Node("Bryan Steil", "person", "Chair, House Digital Assets Subcom. (R-WI)",
         "US House", "high", "$764,206 Fairshake IE support"),
    Node("Maxine Waters", "person", "House Fin. Services Ranking Member (D-CA)",
         "US House", "high", "Lead House antagonist; 'UNSTABLE Act' framing"),
    Node("Bill Huizenga", "person", "House Fin. Services Vice Chair (R-MI)",
         "US House", "medium", ""),
    Node("Frank Lucas", "person", "Representative (R-OK)", "US House", "low", ""),
    Node("Stephen Lynch", "person", "Representative (D-MA)", "US House", "medium",
         "Lead sponsor Stop TRUMP in Crypto Act"),
    Node("Senate Banking Committee", "institution", "Senate committee", "US Senate",
         "high", ""),
    Node("House Financial Services Committee", "institution", "House committee",
         "US House", "high", ""),

    # ----- PACs -----
    Node("Fairshake PAC", "pac", "Crypto super PAC", "Crypto industry",
         "high", "FEC C00835959; $260M 2024 cycle"),
    Node("Defend American Jobs", "pac", "Republican-facing Fairshake affiliate",
         "Crypto industry", "high", "FEC C00836221"),
    Node("Protect Progress", "pac", "Democratic-facing Fairshake affiliate",
         "Crypto industry", "high", "FEC C00848440"),
    Node("Stand With Crypto Alliance", "pac", "501(c)(4)", "Coinbase",
         "medium", "Founded by Faryar Shirzad Aug 2023"),
    Node("Keep America Great PAC", "pac", "Aligned dark-money PAC",
         "Crypto industry", "medium", "$2.3M from Foris DAX (Crypto.com)"),

    # ----- Issuers / custodians / VCs / banks -----
    Node("Circle Internet Group", "firm", "USDC issuer (NYSE:CRCL)", "Circle",
         "high", "CIK 1876042"),
    Node("USDC", "firm", "Circle stablecoin", "Circle", "high", ""),
    Node("Jeremy Allaire", "person", "Chairman/CEO Circle", "Circle", "high", "Co-founder"),
    Node("Dante Disparte", "person", "Chief Strategy Officer Circle", "Circle",
         "medium", "ex-Diem/Libra"),
    Node("M. Michele Burns", "person", "Circle audit committee director", "Circle",
         "high", "Also Goldman Sachs board director"),
    Node("Craig Broderick", "person", "Circle Risk Committee Chair", "Circle",
         "medium", "ex-Goldman Sachs CRO"),
    Node("Rajeev Date", "person", "Circle Lead Independent Director", "Circle",
         "medium", "ex-CFPB Deputy Director"),
    Node("Coinbase Global", "firm", "Exchange (NASDAQ:COIN)", "Coinbase",
         "high", "CIK 1679788"),
    Node("Brian Armstrong", "person", "CEO Coinbase", "Coinbase", "high", ""),
    Node("Marc Andreessen", "person", "Coinbase director; a16z GP", "a16z/Coinbase",
         "high", "$2.5M MAGA PAC 2024 cycle; PCAST member"),
    Node("Ben Horowitz", "person", "a16z GP", "a16z", "high",
         "$2.5M MAGA PAC 2024 cycle"),
    Node("Frederick Ehrsam", "person", "Coinbase co-founder; Paradigm GP",
         "Coinbase/Paradigm", "high", ""),
    Node("Paul Grewal", "person", "Coinbase CLO", "Coinbase", "medium",
         "ex-US Magistrate Judge"),
    Node("Faryar Shirzad", "person", "Coinbase Chief Policy Officer", "Coinbase",
         "high", "ex-Goldman, ex-NSC"),
    Node("Paul Clement", "person", "Coinbase director", "Coinbase",
         "medium", "43rd US Solicitor General"),
    Node("Chris Lehane", "person", "Coinbase director; OpenAI VP", "Coinbase/OpenAI",
         "medium", "ex-Haun Ventures, ex-Airbnb"),
    Node("Andreessen Horowitz (a16z)", "firm", "VC firm", "a16z",
         "high", "$47M Fairshake; Crypto Fund IV $4.5B"),
    Node("Paradigm", "firm", "Crypto VC", "Paradigm", "medium", "Spun out of a16z networks"),
    Node("Haun Ventures", "firm", "Crypto VC", "Haun Ventures", "medium",
         "Founded by Katie Haun 2022"),
    Node("Katie Haun", "person", "Founder, Haun Ventures", "Haun Ventures",
         "medium", "ex-Coinbase GC, ex-prosecutor"),
    Node("Chris Dixon", "person", "a16z crypto practice head", "a16z", "high", ""),
    Node("Katie Biber", "person", "Paradigm CLO; Anchorage director", "Paradigm/Anchorage",
         "high", "ex-Romney 2008/2012 counsel"),

    # Tether stack
    Node("Tether (USDT)", "firm", "Largest stablecoin issuer", "iFinex",
         "high", "$141B Treasury reserves"),
    Node("iFinex", "firm", "Parent of Tether/Bitfinex", "iFinex", "high", ""),
    Node("Bitfinex", "firm", "Crypto exchange (offshore)", "iFinex", "medium", ""),
    Node("Paolo Ardoino", "person", "CEO Tether", "Tether", "high",
         "~20% Tether equity"),
    Node("Giancarlo Devasini", "person", "Chairman Tether", "Tether", "high",
         "~47% equity; Forbes >$22B net worth"),
    Node("Cantor Fitzgerald", "firm", "Investment bank", "Cantor", "high",
         "~5% Tether equity via $600M convertible bond"),
    Node("USAT", "firm", "Cantor/Tether GENIUS-compliant US stablecoin",
         "Cantor/Tether", "high", "Launched Jan 2026"),
    Node("Bo Hines", "person", "CEO USAT", "USAT/Cantor", "medium", ""),
    Node("Twenty One Capital", "firm", "Tether-Bitfinex-SoftBank SPAC vehicle",
         "Cantor SPAC", "medium", "via Cantor Equity Partners"),

    # Custodians and banks
    Node("BitGo", "firm", "Crypto custodian", "BitGo", "high",
         "Pre-IPO Sept 2025; SD-chartered trust"),
    Node("Anchorage Digital", "firm", "OCC-chartered digital-asset bank",
         "Anchorage", "high", "OCC trust charter Jan 2021"),
    Node("Diogo Monica", "person", "Anchorage Executive Chairman; Haun GP",
         "Anchorage/Haun", "high", ""),
    Node("Nathan McCauley", "person", "Anchorage co-founder/CEO", "Anchorage",
         "medium", ""),
    Node("Paxos Trust", "firm", "Stablecoin issuer (PYUSD, USDP)", "Paxos",
         "medium", ""),
    Node("Charles Cascarilla", "person", "CEO Paxos", "Paxos", "medium", ""),
    Node("Kraken Financial", "firm", "Crypto firm; Fed master account holder",
         "Kraken", "high", "First crypto Fed master account (Mar 2026)"),
    Node("Jesse Powell", "person", "Founder Kraken", "Kraken", "medium",
         "Fairshake donor"),
    Node("Custodia Bank", "firm", "Wyoming SPDI; denied Fed master account",
         "Custodia", "high", "Founded 2019 by Caitlin Long"),
    Node("Caitlin Long", "person", "Founder/CEO Custodia", "Custodia", "high", ""),

    # BlackRock + custody banks
    Node("BlackRock", "firm", "Asset manager (NYSE:BLK)", "BlackRock", "high",
         "Manages ~90% of USDC non-bank reserves; IBIT $46.5B"),
    Node("Larry Fink", "person", "Chairman/CEO BlackRock", "BlackRock", "high", ""),
    Node("Philipp Hildebrand", "person", "Vice Chairman BlackRock",
         "BlackRock", "high", "ex-SNB Chair, ex-FSB Vice Chair"),
    Node("Robert Mitchnick", "person", "Head Digital Assets BlackRock",
         "BlackRock", "medium", "Runs IBIT, ETHA, BUIDL"),
    Node("Circle Reserve Fund", "firm", "BlackRock-managed USDC reserve fund",
         "BlackRock/Circle", "high", "2a-7 govt MMF; BNY custody"),
    Node("BUIDL", "firm", "BlackRock tokenized MMF", "BlackRock/Securitize",
         "medium", "Tokenized by Securitize"),
    Node("Securitize", "firm", "Tokenization platform", "Securitize", "medium",
         "SPAC merger Oct 2025"),
    Node("BNY Mellon", "firm", "Custodian (NYSE:BK)", "BNY Mellon", "high",
         "Primary USDC fiat-reserve custodian"),
    Node("State Street", "firm", "Custodian (NYSE:STT)", "State Street",
         "medium", "PYUSD custodian"),
    Node("Goldman Sachs", "firm", "Investment bank", "Goldman Sachs", "medium",
         "Lead underwriter Circle IPO; Anchorage investor"),

    # Donors / industry execs
    Node("Coinbase", "firm", "alias for Coinbase Global", "Coinbase", "medium",
         "$75M Fairshake; FEC complaint pending"),
    Node("Ripple", "firm", "XRP issuer", "Ripple", "medium",
         "~$50M Fairshake"),
    Node("Brad Garlinghouse", "person", "CEO Ripple", "Ripple", "medium",
         "Fairshake donor"),
    Node("Tyler Winklevoss", "person", "Co-founder Gemini", "Gemini", "medium",
         "Fairshake donor; pressured Quintenz withdrawal"),
    Node("Cameron Winklevoss", "person", "Co-founder Gemini", "Gemini", "medium", ""),
    Node("Crypto.com (Foris DAX)", "firm", "Crypto exchange", "Crypto.com", "medium",
         "$2.3M to Keep America Great PAC"),
]

# --------------------------------------------------------------------------
# Edges
# --------------------------------------------------------------------------

EDGES: list[Edge] = []

E = EDGES.append


def add(source, target, kind, weight=1.0, year_start=None, notes="", url=""):
    E(Edge(source, target, kind, weight, year_start, notes, url))


# ------ Trump family / WLFI core ------
add("Donald Trump", "DT Marks DEFI LLC", "ownership", 2.0, 2024,
    "~70% beneficial ownership per press reporting",
    "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0002043140")
add("Donald Trump Jr.", "DT Marks DEFI LLC", "ownership", 1.0, 2024,
    "Trump family beneficial owner")
add("Eric Trump", "DT Marks DEFI LLC", "ownership", 1.0, 2024, "Trump family")
add("Barron Trump", "DT Marks DEFI LLC", "ownership", 1.0, 2024, "Trump family")
add("DT Marks DEFI LLC", "World Liberty Financial", "ownership", 2.0, 2024,
    "75% of WLF protocol revenue; ~38% of WLF Holdco LLC")
add("World Liberty Financial", "USD1", "ownership", 2.0, 2025,
    "USD1 is WLFI's dollar-backed stablecoin")
add("USD1", "BitGo Trust", "custody", 2.0, 2025,
    "BitGo Trust custodies USD1 reserves")
add("Zachary Folkman", "World Liberty Financial", "employment", 1.0, 2024,
    "Officer of record per SEC Form D/A")
add("Chase Herro", "World Liberty Financial", "employment", 1.0, 2024,
    "Officer of record per SEC Form D/A")
add("Donald Trump Jr.", "American Bitcoin (ABTC)", "employment", 1.0, 2025,
    "Co-founder")
add("Eric Trump", "American Bitcoin (ABTC)", "employment", 1.0, 2025,
    "Co-founder")
add("Donald Trump", "Trump Media (DJT)", "ownership", 2.0, 2024,
    "Trump family principal beneficiary; 11,542 BTC + 756M CRO treasury")
add("Kash Patel", "Trump Media (DJT)", "board", 1.0, 2022,
    "Board director from April 2022; ~$800K stock compensation",
    "https://en.wikipedia.org/wiki/Kash_Patel")
add("USD1", "MGX", "custody", 1.0, 2025,
    "$2B USD1 settlement to Binance (May 2025)")

# Kushner / Affinity / Gulf
add("Jared Kushner", "Affinity Partners", "ownership", 2.0, 2021,
    "Sole owner via A Fin Management LLC")
add("Ivanka Trump", "Affinity Partners", "employment", 1.0, 2021,
    "Partner; Sazan Island Albania negotiations participant")
add("Saudi PIF", "Affinity Partners", "investment", 2.0, 2021,
    "$2B commitment; 1.25% management fee",
    "https://www.finance.senate.gov/chairmans-news/wyden-investigation-of-kushner-firm-continues-new-letter-outlines-affinity-partners-fee-structure-lack-of-return-to-investors-questionable-deals-with-foreign-governments")
add("Qatar Investment Authority", "Affinity Partners", "investment", 1.0, 2024,
    "~$1.5B commitment with Lunate")
add("Lunate", "Affinity Partners", "investment", 1.0, 2024,
    "Abu Dhabi-linked co-investor")
add("Saudi PIF", "MGX", "investment", 1.0, 2024,
    "Same Gulf principal class invests in MGX [structural, unverified contractual link]")

# Family ties / kinship
add("Donald Trump", "Donald Trump Jr.", "kinship", 1.0, None, "father-son")
add("Donald Trump", "Eric Trump", "kinship", 1.0, None, "father-son")
add("Donald Trump", "Ivanka Trump", "kinship", 1.0, None, "father-daughter")
add("Donald Trump", "Tiffany Trump", "kinship", 1.0, None, "father-daughter")
add("Donald Trump", "Barron Trump", "kinship", 1.0, None, "father-son")
add("Ivanka Trump", "Jared Kushner", "family", 1.0, 2009, "spouses")
add("Tiffany Trump", "Michael Boulos", "family", 1.0, 2022, "spouses")
add("Michael Boulos", "Massad Boulos", "kinship", 1.0, None, "father-son")
add("Eric Trump", "Lara Trump", "family", 1.0, 2014, "spouses")

# Trump admin staff ties
add("Donald Trump", "Scott Bessent", "employment", 1.0, 2025,
    "Treasury Secretary appointment")
add("Donald Trump", "Howard Lutnick", "employment", 1.0, 2025,
    "Commerce Secretary appointment")
add("Donald Trump", "Kevin Hassett", "employment", 1.0, 2025,
    "NEC Director appointment")
add("Donald Trump", "William Pulte", "employment", 1.0, 2025, "FHFA Director")
add("Donald Trump", "Russell Vought", "employment", 1.0, 2025, "OMB Director")
add("Donald Trump", "Pamela Bondi", "employment", 1.0, 2025, "Attorney General")
add("Donald Trump", "Kash Patel", "employment", 1.0, 2025, "FBI Director")
add("Donald Trump", "Jamieson Greer", "employment", 1.0, 2025, "USTR")
add("Donald Trump", "D. John Sauer", "employment", 1.0, 2025, "Solicitor General")
add("Donald Trump", "Marco Rubio", "employment", 1.0, 2025, "Secretary of State")
add("Donald Trump", "David Sacks", "employment", 1.0, 2025,
    "AI/Crypto Czar (SGE); broad ethics waiver Mar 5 2025")
add("Donald Trump", "Mike Faulkender", "employment", 1.0, 2025,
    "Deputy Treasury + Acting IRS Commissioner")
add("Donald Trump", "Stephen Miran", "employment", 1.0, 2025,
    "CEA Chair then Fed Governor")
add("Donald Trump", "Paul Atkins", "employment", 1.0, 2025, "SEC Chair")
add("Donald Trump", "Massad Boulos", "employment", 1.0, 2025,
    "Senior Advisor Arab/ME Affairs and Africa")
add("Donald Trump", "Kimberly Guilfoyle", "employment", 1.0, 2025,
    "Ambassador to Greece")

# Cabinet revolving doors
add("Scott Bessent", "Treasury", "policy_authority", 2.0, 2025,
    "FSOC chair; OFAC; primary-dealer relationships")
add("Howard Lutnick", "Cantor Fitzgerald", "employment", 2.0, 1996,
    "Former Chairman/CEO; family retains control via Brandon")
add("Brandon Lutnick", "Cantor Fitzgerald", "employment", 2.0, 2025,
    "Chairman from Feb 2025")
add("Brandon Lutnick", "Twenty One Capital", "employment", 1.0, 2025,
    "Chairman and CEO of Cantor Equity Partners SPAC vehicle")
add("Howard Lutnick", "Brandon Lutnick", "kinship", 1.0, None, "father-son")
add("Cantor Fitzgerald", "Tether (USDT)", "investment", 2.0, 2024,
    "~5% Tether equity via ~$600M convertible bond",
    "https://www.wsj.com/finance/cantor-fitzgerald-tether-stake")
add("Cantor Fitzgerald", "Tether (USDT)", "custody", 2.0, 2024,
    "Custodies majority of Tether's ~$141B Treasury reserves")
add("Cantor Fitzgerald", "USAT", "ownership", 2.0, 2026,
    "Cantor/Tether GENIUS-compliant US stablecoin launched Jan 2026")
add("Bo Hines", "USAT", "employment", 1.0, 2026, "CEO of USAT")
add("Tether (USDT)", "USAT", "ownership", 2.0, 2026, "Tether US sibling")
add("USAT", "Anchorage Digital", "custody", 1.0, 2026,
    "USAT operates through Anchorage Digital Bank")
add("Cantor Fitzgerald", "Twenty One Capital", "ownership", 1.0, 2025,
    "Cantor SPAC vehicle for Tether-Bitfinex-SoftBank")
add("Tether (USDT)", "Twenty One Capital", "ownership", 1.0, 2025,
    "Majority owner of SPAC vehicle per Cantor Equity Partners 425 filing")
add("Bitfinex", "Twenty One Capital", "ownership", 1.0, 2025, "Co-owner")

# Hassett
add("Kevin Hassett", "Coinbase Global", "investment", 2.0, 2024,
    "$1M-$5M COIN common stock per June 2025 OGE filing")
add("Kevin Hassett", "Coinbase Global", "employment", 1.0, 2022,
    "Coinbase Global Advisory Council (pre-NEC); received $50,001",
    "https://cryptotimes.io/news/")
add("Kevin Hassett", "White House Digital Assets Working Group", "policy_authority", 2.0, 2025,
    "Chairs Working Group while holding $1M-$5M COIN")

# Add the Working Group node implicitly missing -- create it
NODES.append(Node("White House Digital Assets Working Group", "institution",
                  "Inter-agency Working Group", "White House", "high",
                  "Chaired by Hassett; chartered by EO 14178"))

# Pulte / FHFA / crypto-mortgage
add("William Pulte", "FHFA", "policy_authority", 2.0, 2025,
    "FHFA Director; issued crypto-mortgage directive June 25 2025")
NODES.append(Node("FHFA", "institution", "Housing finance regulator", "FHFA",
                  "high", "Fannie + Freddie GSE supervisor"))
add("William Pulte", "American Bitcoin (ABTC)", "investment", 1.0, 2025,
    "MARA Holdings equity; structurally adjacent miner exposure [unverified for ABTC specifically]")

# Bessent
add("Scott Bessent", "Treasury", "employment", 2.0, 2025, "Treasury Secretary")
NODES.append(Node("Treasury", "institution", "US Department of the Treasury",
                  "Treasury", "high", ""))
add("Scott Bessent", "Donald Trump", "employment", 1.0, 2025, "Cabinet appointment")

# Miran
add("Stephen Miran", "Federal Reserve Board", "employment", 2.0, 2025,
    "Fed Governor since Sept 2025 replacing Kugler",
    "https://www.federalreserve.gov/aboutthefed/bios/board/miran.htm")

# Patel
add("Kash Patel", "FBI", "policy_authority", 2.0, 2025, "FBI Director")
NODES.append(Node("FBI", "institution", "Federal Bureau of Investigation",
                  "DOJ", "medium", ""))
add("Kash Patel", "American Bitcoin (ABTC)", "investment", 0.5, 2025,
    "Core Scientific $50K-$100K + GBTC $50K-$100K [unverified for ABTC link]")

# Sacks / a16z
add("David Sacks", "Andreessen Horowitz (a16z)", "investment", 1.0, 2024,
    "Held a16z fund LP positions; divested at SGE")
add("Brian Quintenz", "Andreessen Horowitz (a16z)", "employment", 2.0, 2022,
    "Global Head of Policy 2022-2025")
add("Brian Quintenz", "Andreessen Horowitz (a16z)", "investment", 1.0, 2024,
    "Stakes in CNK Fund III, Seed 1, IV per confirmation hearing")
add("Brian Quintenz", "Donald Trump", "employment", 1.0, 2025,
    "CFTC Chair nominee; nomination withdrawn September 2025")
add("Scott Kupor", "Andreessen Horowitz (a16z)", "employment", 1.0, 2010,
    "ex-Managing Partner")
add("Tyler Winklevoss", "Brian Quintenz", "litigation", 1.0, 2025,
    "Pressured nomination over Gemini complaint")
add("Marc Andreessen", "Andreessen Horowitz (a16z)", "employment", 2.0, 2009,
    "Co-founder and GP")
add("Ben Horowitz", "Andreessen Horowitz (a16z)", "employment", 2.0, 2009,
    "Co-founder and GP")
add("Chris Dixon", "Andreessen Horowitz (a16z)", "employment", 1.0, 2018,
    "Crypto practice head")
add("Marc Andreessen", "Coinbase Global", "board", 2.0, 2020,
    "Director since December 2020")
add("Marc Andreessen", "Donald Trump", "donation", 2.0, 2024,
    "$2.5M to MAGA super PAC")
add("Ben Horowitz", "Donald Trump", "donation", 2.0, 2024,
    "$2.5M to MAGA super PAC")
add("Andreessen Horowitz (a16z)", "Fairshake PAC", "donation", 2.0, 2024,
    "~$44M to Fairshake (2024 + 2026 cycles ~$47M total)")
add("Andreessen Horowitz (a16z)", "Anchorage Digital", "investment", 1.0, 2021,
    "Major investor alongside Goldman, KKR, Visa, GIC")

# Tarbert revolving door
add("Heath Tarbert", "Circle Internet Group", "employment", 2.0, 2023,
    "CLO 2023; President since Jan 2025")
add("Heath Tarbert", "Circle Internet Group", "revolving_door", 2.0, 2025,
    "ex-CFTC Chair (2019-2021); ex-Citadel Securities CLO 2021-2023")

# Brooks revolving door
add("Brian Brooks", "Anchorage Digital", "regulator", 2.0, 2021,
    "As OCC Acting Comptroller approved Anchorage trust charter Jan 2021")
add("Brian Brooks", "Coinbase Global", "employment", 1.0, 2018,
    "ex-Chief Legal Officer 2018-2020")
add("Brian Brooks", "BitGo", "board", 2.0, 2025,
    "Director from September 2025",
    "https://bitgo.com/press")
add("Brian Brooks", "Trump Media (DJT)", "board", 0.5, 2025,
    "Strategy Inc (MSTR) director [adjacent]")

# Shirzad
add("Faryar Shirzad", "Coinbase Global", "employment", 2.0, 2021,
    "Chief Policy Officer")
add("Faryar Shirzad", "Goldman Sachs", "employment", 1.0, 2003,
    "Goldman Global co-head OGA ~15 years")
add("Faryar Shirzad", "Stand With Crypto Alliance", "employment", 1.0, 2023,
    "Founded Aug 2023 while at Coinbase")
add("Stand With Crypto Alliance", "Coinbase Global", "employment", 1.0, 2023,
    "Founded by Coinbase Chief Policy Officer")

# Circle board interlocks
add("Jeremy Allaire", "Circle Internet Group", "employment", 2.0, 2013,
    "Co-founder, Chairman, CEO")
add("Dante Disparte", "Circle Internet Group", "employment", 1.0, 2021,
    "Chief Strategy Officer; ex-Diem/Libra EVP")
add("M. Michele Burns", "Circle Internet Group", "board", 1.0, 2013, "Director")
add("M. Michele Burns", "Goldman Sachs", "board", 2.0, 2017,
    "Goldman Sachs Group board director")
add("Craig Broderick", "Circle Internet Group", "board", 1.0, 2023,
    "Risk Committee Chair")
add("Craig Broderick", "Goldman Sachs", "employment", 1.0, 1985,
    "Goldman 1985-2018; CRO 2008-2018")
add("Rajeev Date", "Circle Internet Group", "board", 1.0, 2013,
    "Lead Independent Director")
add("Circle Internet Group", "USDC", "ownership", 2.0, 2018, "USDC issuer")
add("USDC", "BNY Mellon", "custody", 2.0, 2022,
    "Primary fiat-reserve custodian")
add("Circle Internet Group", "BlackRock", "custody", 2.0, 2025,
    "BlackRock manages ~90% of non-bank USDC reserves under Mar 2025 MoU")
add("BlackRock", "Circle Reserve Fund", "ownership", 2.0, 2025,
    "Manages Circle Reserve Fund (2a-7 govt MMF)")
add("Circle Reserve Fund", "BNY Mellon", "custody", 1.0, 2025,
    "Custodied within BNY infrastructure")

# Coinbase board / executives
add("Brian Armstrong", "Coinbase Global", "employment", 2.0, 2012,
    "Founder, Chairman/CEO")
add("Frederick Ehrsam", "Coinbase Global", "board", 2.0, 2013, "Co-founder, director")
add("Frederick Ehrsam", "Paradigm", "employment", 1.0, 2018, "Co-founder, GP")
add("Paul Grewal", "Coinbase Global", "employment", 1.0, 2020, "CLO")
add("Paul Clement", "Coinbase Global", "board", 1.0, 2024, "Director")
add("Chris Lehane", "Coinbase Global", "board", 1.0, 2024, "Director")
add("Chris Lehane", "Haun Ventures", "employment", 1.0, 2022,
    "ex-Chief Strategy Officer 2022-2024")
add("Coinbase Global", "Fairshake PAC", "donation", 2.0, 2024,
    "~$75M to Fairshake in 2024 cycle")
add("Coinbase", "Fairshake PAC", "donation", 1.0, 2024, "alias")
add("Brian Armstrong", "Fairshake PAC", "donation", 1.0, 2024,
    "Personal $1M+ contribution")
add("Coinbase Global", "USDC", "investment", 2.0, 2018,
    "Revenue share via former Centre Consortium and ongoing Coinbase Reserve Programs")

# Haun / Anchorage
add("Katie Haun", "Haun Ventures", "employment", 2.0, 2022,
    "Founder; ex-Coinbase GC")
add("Diogo Monica", "Anchorage Digital", "employment", 2.0, 2017,
    "Co-founder, Executive Chairman from Mar 2024")
add("Diogo Monica", "Haun Ventures", "employment", 1.0, 2024,
    "General Partner")
add("Nathan McCauley", "Anchorage Digital", "employment", 2.0, 2017,
    "Co-founder, CEO")
add("Katie Biber", "Anchorage Digital", "board", 2.0, 2022,
    "Director; ex-General Counsel")
add("Katie Biber", "Paradigm", "employment", 1.0, 2022,
    "Chief Legal Officer")

# Paxos
add("Charles Cascarilla", "Paxos Trust", "employment", 2.0, 2012, "Co-founder, CEO")
add("Paxos Trust", "State Street", "custody", 1.0, 2023,
    "PYUSD reserve custodian (Paxos issuance, State Street custody)")

# BitGo
add("BitGo", "BitGo Trust", "ownership", 2.0, 2018, "BitGo Trust SD-chartered")

# Kraken
add("Jesse Powell", "Kraken Financial", "employment", 2.0, 2011,
    "Founder Kraken")
add("Jesse Powell", "Fairshake PAC", "donation", 1.0, 2024, "Donor")
add("Kansas City Fed", "Kraken Financial", "regulator", 2.0, 2026,
    "Approved limited-purpose master account March 4, 2026",
    "https://democrats-financialservices.house.gov/uploadedfiles/fed_kraken_master_account.pdf")
add("Jeffrey Schmid", "Kansas City Fed", "employment", 2.0, 2023,
    "President since August 2023")
add("Jeffrey Schmid", "Kraken Financial", "policy_authority", 2.0, 2026,
    "Signed off on Kraken master account")

# Custodia
add("Caitlin Long", "Custodia Bank", "employment", 2.0, 2019,
    "Founder/CEO")
add("Federal Reserve Board", "Custodia Bank", "regulator", 2.0, 2023,
    "Denied master-account application Jan 27 2023",
    "https://custodiabank.com")

# Fed governors
add("Kevin Warsh", "Federal Reserve Board", "employment", 2.0, 2026,
    "Confirmed Chair May 13 2026 54-45")
add("Kevin Warsh", "Stanley Druckenmiller", "employment", 2.0, 2011,
    "Duquesne Family Office partner/advisor 2011-2026; $10.2M consulting fees")
add("Stanley Druckenmiller", "Kevin Warsh", "investment", 1.0, 2011,
    "Confidentiality agreements; OGE ethics officer flagged out of compliance",
    "https://www.banking.senate.gov/newsroom/minority/warren-presses-druckenmiller-to-release-kevin-warsh-from-confidentiality-agreements-on-undisclosed-100-million")
add("Christopher Waller", "Federal Reserve Board", "employment", 2.0, 2020,
    "Fed Governor since Dec 2020")
add("Michelle Bowman", "Federal Reserve Board", "employment", 2.0, 2018,
    "Governor 2018; Vice Chair for Supervision June 2025")
add("Lisa Cook", "Federal Reserve Board", "employment", 1.0, 2022, "Governor")
add("Donald Trump", "Lisa Cook", "litigation", 1.0, 2025,
    "Trump v. Cook removal attempt August 25 2025",
    "https://www.scotusblog.com/2026/01/trump-v-cook-an-explainer/")
add("Philip Jefferson", "Federal Reserve Board", "employment", 1.0, 2022, "Vice Chair")
add("Michael Barr", "Federal Reserve Board", "employment", 1.0, 2022,
    "Stepped down as VC Supervision Feb 28 2025")
add("John Williams", "Federal Reserve Board", "employment", 1.0, 2018,
    "NY Fed President; permanent FOMC voter, FOMC Vice Chair")
add("Beth Hammack", "Federal Reserve Board", "employment", 1.0, 2024,
    "Cleveland Fed President from Aug 2024")
add("Beth Hammack", "Goldman Sachs", "employment", 2.0, 1993,
    "Goldman 1993-2024; co-head global finance")
add("Neel Kashkari", "Federal Reserve Board", "employment", 1.0, 2016,
    "Minneapolis Fed President")
add("Neel Kashkari", "Goldman Sachs", "employment", 1.0, 2002,
    "Goldman Sachs IT-security IB 2002-2006")
add("Susan Collins", "Federal Reserve Board", "employment", 1.0, 2022,
    "Boston Fed President")
add("Alberto Musalem", "Federal Reserve Board", "employment", 1.0, 2024,
    "St Louis Fed President")
add("Austan Goolsbee", "Federal Reserve Board", "employment", 1.0, 2023,
    "Chicago Fed President")
add("Lorie Logan", "Federal Reserve Board", "employment", 1.0, 2022,
    "Dallas Fed President; ex-NY Fed SOMA Manager 2019-2022")
add("Mary Daly", "Federal Reserve Board", "employment", 1.0, 2018,
    "SF Fed President")
add("Tom Barkin", "Federal Reserve Board", "employment", 1.0, 2018,
    "Richmond Fed President")
add("Anna Paulson", "Federal Reserve Board", "employment", 1.0, 2025,
    "Philadelphia Fed President from July 2025")
add("Kansas City Fed", "Federal Reserve Board", "employment", 1.0, 1913,
    "Regional Reserve Bank")

# Stephen Miran -> Hudson Bay / Kushner sovereign tie-in
NODES.append(Node("Hudson Bay Capital", "firm", "Hedge fund", "Hudson Bay",
                  "medium", "FTX claims trader; Miran's prior employer"))
add("Stephen Miran", "Hudson Bay Capital", "employment", 2.0, 2024,
    "Senior Strategist Feb 2024 to Fed nomination")

# Bondi / Ballard
NODES.append(Node("Ballard Partners", "firm", "Lobbying / FARA firm",
                  "Ballard Partners", "medium",
                  "Bondi's pre-AG lobbying employer; Qatar FARA client"))
add("Pamela Bondi", "Ballard Partners", "employment", 2.0, 2019,
    "Registered lobbyist and FARA 2019-Jan 2025")
add("Ballard Partners", "Qatar Investment Authority", "employment", 0.5, 2022,
    "Ballard registered for State of Qatar (anti-trafficking work for 2022 FIFA World Cup)")

# Greer / King & Spalding
NODES.append(Node("King & Spalding", "firm", "Law firm", "King & Spalding",
                  "low", "Greer's pre-USTR partner firm"))
add("Jamieson Greer", "King & Spalding", "employment", 2.0, 2020,
    "Partner 2020-2025 (trade remedies, CFIUS)")

# Sauer / Trump personal counsel
add("D. John Sauer", "Donald Trump", "employment", 1.0, 2023,
    "Counsel in Trump v. United States 2024")

# Atkins / Patomak
NODES.append(Node("Patomak Global Partners", "firm", "Consulting firm",
                  "Patomak Global Partners", "medium",
                  "Founded by Atkins; crypto clients"))
add("Paul Atkins", "Patomak Global Partners", "employment", 2.0, 2009,
    "Founder")
add("Paul Atkins", "SEC", "policy_authority", 2.0, 2025, "SEC Chair")
NODES.append(Node("SEC", "institution", "Securities and Exchange Commission",
                  "SEC", "high", ""))

# Congress / PACs
add("Bernie Moreno", "Senate Banking Committee", "employment", 1.0, 2025,
    "Senator on Banking Committee")
add("Defend American Jobs", "Bernie Moreno", "donation", 2.0, 2024,
    "$40.1M in IE support against Brown",
    "https://www.coindesk.com/policy/2024/09/26/crypto-pacs-dominate-ohio-senate-race-spending-40m-on-sherrod-browns-foe")
add("Defend American Jobs", "Sherrod Brown", "donation", -2.0, 2024,
    "Negative IE: $40.1M against Brown")
add("Sherrod Brown", "Senate Banking Committee", "employment", 1.0, 2007,
    "Banking Chair until Jan 2025")
add("Fairshake PAC", "Defend American Jobs", "donation", 2.0, 2023,
    "Affiliated PAC")
add("Fairshake PAC", "Protect Progress", "donation", 2.0, 2023,
    "Affiliated PAC")
add("Protect Progress", "Ruben Gallego", "donation", 2.0, 2024,
    "~$10M IE support")
add("Ruben Gallego", "Senate Banking Committee", "employment", 1.0, 2025,
    "Top Dem on Digital Assets Subcommittee")
add("Marc Andreessen", "Ruben Gallego", "donation", 1.0, 2024,
    "High-dollar fundraiser August 2024")
add("Fairshake PAC", "Bryan Steil", "donation", 2.0, 2024,
    "$764,206 IE supporting Steil")
add("Bryan Steil", "House Financial Services Committee", "employment", 1.0, 2019,
    "Chair, Digital Assets, Fin Tech, AI Subcommittee")
add("Fairshake PAC", "Andy Barr", "donation", 2.0, 2026,
    "~$7M for KY-Senate primary")
add("Keep America Great PAC", "Andy Barr", "donation", 2.0, 2026,
    "Aligned PAC supporting Barr")
add("Crypto.com (Foris DAX)", "Keep America Great PAC", "donation", 2.0, 2026,
    "$2.3M to Keep America Great PAC")
add("Andy Barr", "House Financial Services Committee", "employment", 1.0, 2013,
    "Committee member")
add("Tim Scott", "Senate Banking Committee", "employment", 2.0, 2025,
    "Chair from Jan 2025")
add("Cynthia Lummis", "Senate Banking Committee", "employment", 2.0, 2025,
    "Chair, Digital Assets Subcommittee")
add("Cynthia Lummis", "American Bitcoin (ABTC)", "investment", 1.0, 2022,
    "Personal BTC holdings reported >$100K [structural BTC exposure]")
add("Bill Hagerty", "Senate Banking Committee", "employment", 2.0, 2021,
    "Lead Senate sponsor GENIUS Act")
add("Mike Crapo", "Senate Banking Committee", "employment", 1.0, 1999,
    "Ranking member-class senator")
add("Elizabeth Warren", "Senate Banking Committee", "employment", 2.0, 2013,
    "Ranking Member")
add("Jack Reed", "Senate Banking Committee", "employment", 1.0, 1997, "Member")
add("French Hill", "House Financial Services Committee", "employment", 2.0, 2025,
    "Chair from Jan 2025")
add("Maxine Waters", "House Financial Services Committee", "employment", 2.0, 2003,
    "Ranking Member")
add("Bill Huizenga", "House Financial Services Committee", "employment", 1.0, 2011,
    "Vice Chair")
add("Frank Lucas", "House Financial Services Committee", "employment", 1.0, 2025,
    "Digital Assets and Capital Markets Subcommittees")
add("Stephen Lynch", "House Financial Services Committee", "employment", 1.0, 2001,
    "Lead sponsor Stop TRUMP in Crypto Act")

# Industry donors
add("Brad Garlinghouse", "Ripple", "employment", 2.0, 2017, "CEO Ripple")
add("Ripple", "Fairshake PAC", "donation", 2.0, 2024, "~$50M Fairshake 2024")
add("Brad Garlinghouse", "Fairshake PAC", "donation", 1.0, 2024, "Donor")
add("Tyler Winklevoss", "Fairshake PAC", "donation", 1.0, 2024, "Donor")
add("Cameron Winklevoss", "Fairshake PAC", "donation", 1.0, 2024, "Donor")
add("Jeremy Allaire", "Fairshake PAC", "donation", 1.0, 2024, "Donor")

# Tether internals
add("Paolo Ardoino", "Tether (USDT)", "employment", 2.0, 2023, "CEO")
add("Paolo Ardoino", "Bitfinex", "employment", 1.0, 2014, "CTO")
add("Giancarlo Devasini", "Tether (USDT)", "employment", 2.0, 2014, "Chairman; ~47% equity")
add("iFinex", "Tether (USDT)", "ownership", 2.0, 2014, "Parent")
add("iFinex", "Bitfinex", "ownership", 2.0, 2012, "Parent")

# BlackRock board interlocks
add("Larry Fink", "BlackRock", "employment", 2.0, 1988,
    "Founder, Chairman, CEO")
add("Philipp Hildebrand", "BlackRock", "employment", 2.0, 2012, "Vice Chairman")
add("Robert Mitchnick", "BlackRock", "employment", 1.0, 2018,
    "Head of Digital Assets")
add("BlackRock", "BUIDL", "ownership", 2.0, 2024, "BlackRock tokenized MMF")
add("BUIDL", "Securitize", "custody", 1.0, 2024, "On-chain plumbing")
add("BUIDL", "USDC", "custody", 1.0, 2024, "Redeemable in USDC")

# Goldman / Coinbase exec ties
add("Goldman Sachs", "Anchorage Digital", "investment", 1.0, 2021,
    "Anchorage investor alongside a16z/KKR/Visa/GIC")
add("Goldman Sachs", "Circle Internet Group", "investment", 1.0, 2024,
    "Lead underwriter Circle IPO")

# Cross-link the Trump-Fed-Stablecoin spine
add("EO 14405", "Federal Reserve Board", "policy_authority", 2.0, 2026,
    "Order directs Fed to ease master-account scope")
NODES.append(Node("EO 14405", "institution",
                  "Executive Order on Fed master-account access",
                  "White House", "high",
                  "Signed May 22 2026 (also referenced as the May/March 2026 directive)"))
add("Donald Trump", "EO 14405", "policy_authority", 2.0, 2026,
    "Signed the order")
add("EO 14405", "USD1", "policy_authority", 2.0, 2026,
    "Affects USD1's regulatory trajectory (Section 4)")
add("EO 14405", "USAT", "policy_authority", 2.0, 2026,
    "Affects USAT via Anchorage Fed payment-rail access")
add("EO 14405", "Kraken Financial", "policy_authority", 1.0, 2026,
    "Kraken master account is the operational precedent")
add("EO 14405", "Custodia Bank", "policy_authority", 1.0, 2026,
    "Custodia denial is the legal substrate")

# Lummis -> EO indirect via her policy authority
add("Cynthia Lummis", "EO 14405", "policy_authority", 1.0, 2026,
    "BITCOIN Act codifies adjacent Strategic Bitcoin Reserve")
add("Stephen Miran", "EO 14405", "policy_authority", 1.0, 2026,
    "Mar-a-Lago Accord intellectual scaffold")
add("Christopher Waller", "EO 14405", "policy_authority", 2.0, 2026,
    "'Skinny master account' framework Oct 2025 ratified by EO")

# Trump 2.0 ethics waiver layer
add("David Sacks", "EO 14405", "policy_authority", 1.0, 2026,
    "Czar role Jan 2025 - Mar 2026 covered the order's drafting period")

# Senate Banking aggregate edge
add("Senate Banking Committee", "EO 14405", "policy_authority", 1.0, 2026,
    "Committee jurisdiction over implementing GENIUS Act, market structure")
add("House Financial Services Committee", "EO 14405", "policy_authority", 1.0, 2026,
    "Committee jurisdiction")


# --------------------------------------------------------------------------
# Graph construction and centrality
# --------------------------------------------------------------------------


def build_graph() -> nx.MultiDiGraph:
    """Construct the multigraph; reject edges referring to undeclared nodes."""
    G = nx.MultiDiGraph()
    declared = {n.name for n in NODES}
    for n in NODES:
        G.add_node(n.name, **{k: v for k, v in asdict(n).items() if k != "name"})
    missing = set()
    for e in EDGES:
        if e.source not in declared:
            missing.add(e.source)
            continue
        if e.target not in declared:
            missing.add(e.target)
            continue
        G.add_edge(e.source, e.target,
                   kind=e.kind, weight=e.weight,
                   year_start=e.year_start, notes=e.notes,
                   primary_source_url=e.primary_source_url)
    if missing:
        raise ValueError(f"Edges reference undeclared nodes: {sorted(missing)}")
    return G


def compute_centrality(G: nx.MultiDiGraph) -> dict:
    """
    Compute eigenvector, betweenness, Katz centrality on the undirected
    projection; degree on the directed graph; clustering on the simple
    undirected projection; Louvain communities on the undirected projection.
    """
    UG = nx.Graph()
    for u, v, data in G.edges(data=True):
        w = float(data.get("weight", 1.0))
        if UG.has_edge(u, v):
            UG[u][v]["weight"] += w
        else:
            UG.add_edge(u, v, weight=w)
    for n in G.nodes:
        if n not in UG:
            UG.add_node(n)

    n_nodes = UG.number_of_nodes()

    eig = nx.eigenvector_centrality_numpy(UG, weight="weight")
    btw = nx.betweenness_centrality(UG, weight="weight", normalized=True)
    try:
        katz = nx.katz_centrality_numpy(UG, alpha=0.05, beta=1.0, weight="weight")
    except Exception:
        katz = nx.katz_centrality(UG, alpha=0.05, beta=1.0, weight="weight",
                                  max_iter=2000, tol=1e-6)
    deg = dict(G.degree())
    indeg = dict(G.in_degree())
    outdeg = dict(G.out_degree())
    cluster = nx.clustering(UG, weight="weight")

    seed = 14405
    communities = nx.community.louvain_communities(UG, seed=seed, weight="weight")
    comm_id = {}
    for i, comm in enumerate(communities):
        for node in comm:
            comm_id[node] = i

    # Graph-level descriptive stats
    if nx.is_connected(UG):
        diameter = nx.diameter(UG)
        avg_path = nx.average_shortest_path_length(UG)
    else:
        # Largest connected component
        largest = max(nx.connected_components(UG), key=len)
        H = UG.subgraph(largest)
        diameter = nx.diameter(H)
        avg_path = nx.average_shortest_path_length(H)

    density = nx.density(UG)

    out = {
        "graph_stats": {
            "n_nodes": n_nodes,
            "n_edges_directed": G.number_of_edges(),
            "n_edges_undirected": UG.number_of_edges(),
            "density_undirected": density,
            "diameter_largest_cc": diameter,
            "avg_shortest_path_largest_cc": avg_path,
            "n_communities": len(communities),
        },
        "communities": [
            {"id": i, "size": len(comm),
             "members": sorted(comm)}
            for i, comm in enumerate(communities)
        ],
        "eigenvector": _sorted(eig),
        "betweenness": _sorted(btw),
        "katz": _sorted(katz),
        "degree_total": _sorted(deg),
        "in_degree": _sorted(indeg),
        "out_degree": _sorted(outdeg),
        "clustering": _sorted(cluster),
        "node_community": comm_id,
    }
    return out


def _sorted(d):
    return [{"node": k, "value": float(v)}
            for k, v in sorted(d.items(), key=lambda kv: -kv[1])]


def write_edges_csv(path: Path = DATA_DIR / "sna_edges.csv") -> Path:
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["source", "target", "kind", "weight",
                    "year_start", "notes", "primary_source_url"])
        for e in EDGES:
            w.writerow([e.source, e.target, e.kind, e.weight,
                        e.year_start if e.year_start is not None else "",
                        e.notes, e.primary_source_url])
    return path


def write_centrality_json(out: dict,
                          path: Path = FIG_DIR / "sna_centrality.json") -> Path:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, default=str)
    return path


def main():
    G = build_graph()
    out = compute_centrality(G)
    edges_path = write_edges_csv()
    cent_path = write_centrality_json(out)
    stats = out["graph_stats"]
    print(f"Nodes: {stats['n_nodes']}")
    print(f"Edges (directed): {stats['n_edges_directed']}")
    print(f"Edges (undirected): {stats['n_edges_undirected']}")
    print(f"Density: {stats['density_undirected']:.4f}")
    print(f"Diameter (largest CC): {stats['diameter_largest_cc']}")
    print(f"Avg shortest path (largest CC): "
          f"{stats['avg_shortest_path_largest_cc']:.3f}")
    print(f"Communities (Louvain): {stats['n_communities']}")
    print("Top 10 eigenvector centrality:")
    for row in out["eigenvector"][:10]:
        print(f"  {row['value']:.4f}  {row['node']}")
    print(f"Wrote {edges_path}")
    print(f"Wrote {cent_path}")
    return G, out


if __name__ == "__main__":
    main()
