"""
build_site.py - render markdown sources to a deployable static site
under site/, with the Helfrich heritage palette + typography.

Pipeline:
  1. Copy docs/style.css + docs/favicon.svg to site/
  2. Strip the leading '# Title' from each markdown source (the title
     is set via Pandoc metadata, so the body should not carry a second
     h1). Pass the cleaned body to pandoc.
  3. Convert each top-level markdown source to site/<slug>.html via pandoc
     with a heavy head_extra: KaTeX, OG card, canonical URL, JSON-LD
     ScholarlyArticle / Article schema, favicon.
  4. Long pages get a Pandoc-generated table of contents in a sticky
     sidebar; short pages render edge-to-edge.
  5. Post-process the HTML to inject:
       - reading-time badge under the masthead
       - heading anchor links (CSS-driven hover #)
  6. Copy figures/ into site/figures/
  7. Build site/landing.html (sister nav page) + site/404.html.
  8. Emit sitemap.xml + robots.txt.

Run:
    python tools/build_site.py
"""
from __future__ import annotations

import re
import shutil
import subprocess
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
SITE = HERE / "site"
SITE_URL = "https://ihelfrich.github.io/eo14405-contagion"

# Pages with a TOC sidebar (long-form documents only)
TOC_PAGES = {"index.html", "paper.html"}

# (source, output, title, description, is_scholarly)
PAGES = [
    ("blog-research-note.md", "index.html",
     "Notes on Executive Order 14405",
     "Master account access and stablecoin run dynamics. A long-form research note by Dr. Ian Helfrich.",
     False),
    ("paper.md", "paper.html",
     "Stablecoin Run Risk Under Direct Federal Reserve Access",
     "Formal working paper: spectral and optimal-transport analysis of EO 14405.",
     True),
    ("linkedin-post.md", "short.html",
     "Notes on EO 14405: Short version",
     "1,800-word LinkedIn-format summary of the EO 14405 contagion analysis with the four inline figures.",
     False),
    ("verify.md", "verify.html",
     "Claim-by-claim verification: EO 14405",
     "Every numeric and factual claim mapped to its primary-source URL.",
     False),
    ("outreach.md", "outreach.html",
     "Outreach kit: EO 14405",
     "Pull quotes, share copy, tag list, and email templates for FRB, Senate Banking, and press.",
     False),
    ("dossiers/SYNTHESIS.md", "dossiers/synthesis.html",
     "Political-economy synthesis: EO 14405",
     "The synthesis of twelve OSINT dossiers on the principals behind EO 14405.",
     False),
]

DOSSIERS = [
    ("dossiers/trump-wlfi.md",              "Trump family + World Liberty Financial + USD1"),
    ("dossiers/sacks-a16z-quintenz.md",     "David Sacks + a16z + Brian Quintenz"),
    ("dossiers/circle-coinbase.md",         "Circle (CRCL) + Coinbase (COIN)"),
    ("dossiers/tether-ifinex.md",           "Tether + iFinex + Cantor Fitzgerald"),
    ("dossiers/custodia-wyoming-spdi.md",   "Custodia + Wyoming SPDIs"),
    ("dossiers/fairshake-campaign-finance.md", "Fairshake PAC + Stand With Crypto"),
    ("dossiers/fed-board.md",               "Federal Reserve Board + Reserve Bank presidents"),
    ("dossiers/trump-extended-family.md",   "Trump extended family financial exposure"),
    ("dossiers/trump-admin-financial-roster.md", "Trump 2.0 administration financial-policy roster"),
    ("dossiers/congress-finance-committees.md",  "Senate Banking + House Financial Services 119th Congress"),
    ("dossiers/stablecoin-board-interlocks.md",  "Stablecoin ecosystem board interlocks + regulator alumni"),
    ("dossiers/SNA-FINDINGS.md",            "Social Network Analysis: findings from the 153-node conflict graph"),
]

PUBLISHED = "2026-05-22"   # FR publication date
TODAY = date.today().isoformat()


# ---------------------------------------------------------------------- #
# Markdown preprocessing
# ---------------------------------------------------------------------- #

H1_LEADING = re.compile(r"\A\s*#\s+[^\n]+\n+(?:#{2}\s+[^\n]+\n+)?", re.MULTILINE)
# Match a leading "# Title" line and optionally a following "## Subtitle" line.

def strip_leading_h1(text: str) -> str:
    """Remove the document's first H1 (and optional following H2 subtitle) so
    Pandoc doesn't double up the H1 generated from the title metadata."""
    return H1_LEADING.sub("", text, count=1)


def count_words(markdown: str) -> int:
    """Rough word count from markdown source. Strips code fences and
    image/link syntax so the estimate isn't inflated by URLs."""
    no_code = re.sub(r"```[\s\S]*?```", " ", markdown)
    no_inline_code = re.sub(r"`[^`]*`", " ", no_code)
    no_links = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", no_inline_code)
    no_images = re.sub(r"!\[[^\]]*\]\([^)]+\)", " ", no_links)
    return len(re.findall(r"\b\w+\b", no_images))


def reading_time_min(markdown: str) -> int:
    """Conservative adult reading speed for prose with formulas: 220 wpm."""
    return max(1, round(count_words(markdown) / 220))


# ---------------------------------------------------------------------- #
# JSON-LD schema
# ---------------------------------------------------------------------- #

def jsonld(title: str, description: str, page_url: str, is_scholarly: bool) -> str:
    import json
    schema_type = "ScholarlyArticle" if is_scholarly else "Article"
    obj = {
        "@context": "https://schema.org",
        "@type": schema_type,
        "headline": title,
        "description": description,
        "image": f"{SITE_URL}/figures/li_mechanism.png",
        "author": {
            "@type": "Person",
            "name": "Dr. Ian Helfrich",
            "url": "https://ianhelfrich.com",
            "sameAs": ["https://github.com/ihelfrich"],
            "jobTitle": "Independent researcher",
            "alumniOf": {
                "@type": "EducationalOrganization",
                "name": "Georgia Institute of Technology",
            },
        },
        "datePublished": PUBLISHED,
        "dateModified": TODAY,
        "mainEntityOfPage": page_url,
        "isAccessibleForFree": True,
        "license": "https://creativecommons.org/licenses/by/4.0/",
        "inLanguage": "en",
    }
    return ('<script type="application/ld+json">\n'
            + json.dumps(obj, indent=2)
            + "\n</script>")


# ---------------------------------------------------------------------- #
# KaTeX block (unchanged, reused)
# ---------------------------------------------------------------------- #

KATEX_BLOCK = '''
<link rel="stylesheet"
      href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css"
      integrity="sha384-n8MVd4RsNIU0tAv4ct0nTaAbDJwPJzDEaqSD1odI+WdtXRGWt2kTvGFasHpSy3SV"
      crossorigin="anonymous">
<script defer
        src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"
        integrity="sha384-XjKyOOlGwcjNTAIQHIpgOno0Hl1YQqzUOEleOLALmuqehneUG+vnGctmUb0ZY0l8"
        crossorigin="anonymous"></script>
<script defer
        src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/contrib/auto-render.min.js"
        integrity="sha384-+VBxd3r6XgURycqtZ117nYw44OOcIax56Z4dCRWbxyPt0Koah1uHoK0o4+/RRE05"
        crossorigin="anonymous"
        onload="renderMathInElement(document.body, {
          delimiters: [
            {left: '$$', right: '$$', display: true},
            {left: '\\\\[', right: '\\\\]', display: true},
            {left: '\\\\(', right: '\\\\)', display: false},
            {left: '$', right: '$', display: false}
          ],
          throwOnError: false,
          strict: 'ignore'
        });"></script>
'''.strip()


# ---------------------------------------------------------------------- #
# HTML post-processing (anchor links, reading-time, TOC wrap)
# ---------------------------------------------------------------------- #

HEADING_RE = re.compile(
    r'<(h[2-5])\s+id="([^"]+)"([^>]*)>(.+?)</\1>', re.DOTALL
)

def inject_heading_anchors(html: str) -> str:
    """Add a hover-revealed # link before each h2-h5 with an id."""
    def repl(m: re.Match) -> str:
        tag, hid, rest, body = m.group(1), m.group(2), m.group(3), m.group(4)
        anchor = f'<a class="heading-anchor" href="#{hid}" aria-label="Link to this section">#</a>'
        return f'<{tag} id="{hid}"{rest}>{anchor}{body}</{tag}>'
    return HEADING_RE.sub(repl, html)


def inject_reading_time(html: str, minutes: int) -> str:
    """Place a reading-time badge directly after the title h1."""
    badge = f'<p class="reading-time">~{minutes} min read · updated {TODAY}</p>'
    return re.sub(
        r'(</h1>)',
        r'\1\n' + badge,
        html,
        count=1,
    )


def wrap_with_toc_layout(html: str) -> str:
    """If pandoc emitted <nav id="TOC">, wrap <nav>+<article> in .has-toc."""
    nav_match = re.search(r'(<nav[^>]*id="TOC"[^>]*>[\s\S]+?</nav>)', html)
    if not nav_match:
        return html
    nav_html = nav_match.group(1)
    # Remove the nav from its original location and re-insert wrapped with article
    html_no_nav = html.replace(nav_html, "", 1)
    # Find the <article> and wrap both
    html_no_nav = re.sub(
        r'(<body[^>]*>)',
        r'\1\n<div class="has-toc">\n' + nav_html + '\n',
        html_no_nav,
        count=1,
    )
    html_no_nav = re.sub(
        r'(</article>)',
        r'\1\n</div>',
        html_no_nav,
        count=1,
    )
    return html_no_nav


# ---------------------------------------------------------------------- #
# Pandoc invocation
# ---------------------------------------------------------------------- #

def pandoc_html(src: Path, out: Path, title: str, description: str,
                is_scholarly: bool = False,
                rel_css: str = "style.css",
                rel_favicon: str = "favicon.svg") -> None:
    """Convert markdown to HTML with the full head_extra and post-processing."""
    out.parent.mkdir(parents=True, exist_ok=True)

    # 1. Read + preprocess the markdown source
    raw_md = src.read_text(encoding="utf-8")
    minutes = reading_time_min(raw_md)
    cleaned_md = strip_leading_h1(raw_md)
    cleaned_src = HERE / ".build_cleaned.md"
    cleaned_src.write_text(cleaned_md, encoding="utf-8")

    # 2. Build head_extra
    page_url = f"{SITE_URL}/{out.relative_to(SITE).as_posix()}"
    head_extra = HERE / ".build_head_extra.html"

    schema = jsonld(title, description, page_url, is_scholarly)

    head_extra.write_text(
        f'<meta name="description" content="{description}">\n'
        f'<meta name="author" content="Ian Helfrich">\n'
        f'<link rel="canonical" href="{page_url}">\n'
        f'<link rel="icon" href="{rel_favicon}" type="image/svg+xml">\n'
        f'<link rel="alternate icon" href="{rel_favicon}">\n'
        f'<meta property="og:title" content="{title}">\n'
        f'<meta property="og:description" content="{description}">\n'
        f'<meta property="og:type" content="article">\n'
        f'<meta property="og:url" content="{page_url}">\n'
        f'<meta property="og:site_name" content="Helfrich Research">\n'
        f'<meta property="og:image" content="{SITE_URL}/figures/li_mechanism.png">\n'
        f'<meta property="og:image:width" content="1200">\n'
        f'<meta property="og:image:height" content="627">\n'
        f'<meta property="og:image:alt" content="EO 14405 loss-absorption mechanism diagram">\n'
        f'<meta property="article:published_time" content="{PUBLISHED}">\n'
        f'<meta property="article:modified_time" content="{TODAY}">\n'
        f'<meta property="article:author" content="Ian Helfrich">\n'
        f'<meta name="twitter:card" content="summary_large_image">\n'
        f'<meta name="twitter:image" content="{SITE_URL}/figures/li_mechanism.png">\n'
        f'<meta name="twitter:site" content="@ianhelfrich">\n'
        f'<link rel="preconnect" href="https://rsms.me/">\n'
        f'<link rel="stylesheet" href="https://rsms.me/inter/inter.css">\n'
        f'<link rel="stylesheet" '
        f'href="https://fonts.googleapis.com/css2?'
        f'family=Source+Serif+4:opsz,wght@8..60,400;8..60,600;8..60,700&'
        f'family=JetBrains+Mono:wght@400;500&display=swap">\n'
        f'<link rel="stylesheet" href="{rel_css}">\n'
        f'{schema}\n'
        + KATEX_BLOCK + "\n",
        encoding="utf-8",
    )

    # 3. Pandoc call. Add --toc for long pages.
    cmd = [
        "pandoc",
        "--standalone",
        "--from", "markdown+tex_math_dollars+tex_math_double_backslash+pipe_tables"
                  "+fenced_code_blocks+footnotes+yaml_metadata_block+raw_tex",
        "--to", "html5",
        "--mathjax=about:blank",
        "--metadata", f"title={title}",
        "--include-in-header", str(head_extra),
        "--wrap=preserve",
    ]
    if out.name in TOC_PAGES:
        cmd += ["--toc", "--toc-depth=3"]
    cmd += ["-o", str(out), str(cleaned_src)]

    subprocess.run(cmd, check=True, cwd=HERE)

    cleaned_src.unlink(missing_ok=True)
    head_extra.unlink(missing_ok=True)

    # 4. Post-process: inject heading anchors, reading-time, TOC wrap
    html = out.read_text(encoding="utf-8")
    html = inject_heading_anchors(html)
    html = inject_reading_time(html, minutes)
    if out.name in TOC_PAGES:
        html = wrap_with_toc_layout(html)
    out.write_text(html, encoding="utf-8")


# ---------------------------------------------------------------------- #
# Landing, 404, sitemap, robots
# ---------------------------------------------------------------------- #

def render_landing() -> None:
    """Build the sister navigation page at site/landing.html."""
    landing = SITE / "landing.html"
    html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Helfrich: Research notes</title>
<meta name="description" content="Research notes by Dr. Ian Helfrich.">
<link rel="canonical" href="https://ihelfrich.github.io/eo14405-contagion/landing.html">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<meta property="og:title" content="Helfrich: Research notes">
<meta property="og:description" content="Research notes by Dr. Ian Helfrich on EO 14405 and stablecoin contagion.">
<meta property="og:type" content="website">
<meta property="og:url" content="https://ihelfrich.github.io/eo14405-contagion/landing.html">
<meta property="og:image" content="https://ihelfrich.github.io/eo14405-contagion/figures/li_mechanism.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="627">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="https://ihelfrich.github.io/eo14405-contagion/figures/li_mechanism.png">
<link rel="preconnect" href="https://rsms.me/">
<link rel="stylesheet" href="https://rsms.me/inter/inter.css">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Source+Serif+4:opsz,wght@8..60,400;8..60,600;8..60,700&family=JetBrains+Mono:wght@400;500&display=swap">
<link rel="stylesheet" href="style.css">
<style>
  .landing { max-width: 760px; margin: 0 auto; padding: 60px 28px 80px; }
  .masthead { border-bottom: 3px double var(--carolina-navy); padding-bottom: 16px; margin-bottom: 28px; }
  .masthead .eyebrow { font-family: var(--sans); font-size: 11px; color: var(--carolina-blue); font-weight: 700; letter-spacing: 0.18em; text-transform: uppercase; }
  .masthead h1 { font-size: 36px; margin: 8px 0 6px; color: var(--carolina-navy); }
  .masthead .sub { font-family: var(--sans); color: var(--slate); font-size: 14px; }
  .card { background: white; border: 1px solid var(--mist); border-left: 4px solid var(--carolina-blue); border-radius: 6px; padding: 20px 22px; margin: 14px 0; display: block; text-decoration: none; color: inherit; transition: border-color 0.15s, box-shadow 0.15s, transform 0.15s; }
  .card:hover { border-left-color: var(--old-gold); box-shadow: 0 2px 14px rgba(19,41,75,0.10); transform: translateY(-1px); }
  .card .tag { font-family: var(--sans); font-size: 11px; color: var(--carolina-blue); font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; }
  .card h2 { font-size: 22px; margin: 6px 0 8px; color: var(--carolina-navy); border: none; padding: 0; }
  .card .desc { color: var(--slate); font-size: 14.5px; margin: 0; }
  .figure-tile { margin: 24px 0; padding: 0; border: 1px solid var(--mist); background: var(--parchment); border-left: 4px solid var(--old-gold); }
  .figure-tile img { display: block; width: 100%; height: auto; }
  .figure-tile figcaption { font-family: var(--sans); font-size: 13px; color: var(--slate); padding: 10px 14px; background: white; border-top: 1px solid var(--mist); }
  .hero { background: linear-gradient(135deg, var(--carolina-navy) 0%, var(--carolina-blue) 100%); color: white; padding: 32px 28px; border-radius: 8px; margin-bottom: 24px; }
  .hero .eyebrow { color: rgba(255,255,255,0.85); }
  .hero h2 { color: white; font-size: 28px; margin: 8px 0 12px; border: none; padding: 0; }
  .hero p { color: rgba(255,255,255,0.92); font-size: 15.5px; margin: 0 0 14px; }
  .hero a.cta { display: inline-block; background: var(--old-gold); color: var(--carolina-navy); padding: 10px 18px; border-radius: 4px; font-weight: 700; font-family: var(--sans); text-decoration: none; }
  .hero a.cta:hover { background: white; color: var(--carolina-navy); }
  .meta-foot { margin-top: 56px; padding-top: 18px; border-top: 1px solid var(--mist); font-family: var(--sans); font-size: 12.5px; color: var(--slate); }
</style>
</head>
<body>
<div class="landing">
  <header class="masthead">
    <div class="eyebrow">Helfrich · Research notes</div>
    <h1>Notes on Executive Order 14405</h1>
    <div class="sub">Master account access and stablecoin run dynamics · 26 May 2026</div>
  </header>

  <div class="hero">
    <div class="eyebrow">Read first</div>
    <h2>The research note</h2>
    <p>Long-form, interactive, Socratic. About 5,700 words with nine reader exercises, two steelman boxes, and a glossary. Treats the reader as a colleague rather than a customer.</p>
    <a class="cta" href="index.html">Read the research note →</a>
  </div>

  <figure class="figure-tile">
    <img src="figures/li_mechanism.png" alt="EO 14405 loss-absorption mechanism diagram">
    <figcaption>The loss-absorption mechanism does not vanish under EO 14405. It changes its mailing address.</figcaption>
  </figure>

  <a class="card" href="paper.html">
    <div class="tag">Academic working paper</div>
    <h2>Stablecoin Run Risk Under Direct Federal Reserve Access</h2>
    <p class="desc">Formal version with five propositions, proofs, full math, and Section 9 extensions (continuous Fed reaction function, cross-jurisdiction transmission, per-issuer reserve composition, MMF substitution, operational rails residual). ~7,000 words.</p>
  </a>

  <a class="card" href="short.html">
    <div class="tag">Short version · LinkedIn</div>
    <h2>The argument in 1,800 words</h2>
    <p class="desc">For readers with a limited attention budget. Hook in the first three lines, four inline figures, structural-not-character disclaimer, the 133-basis-point break-even, and the ask.</p>
  </a>

  <a class="card" href="dossiers/synthesis.html">
    <div class="tag">Political-economy synthesis</div>
    <h2>The principals behind EO 14405</h2>
    <p class="desc">Synthesis of twelve OSINT dossiers documenting the financial and personnel networks among the actors whose interests the order affects. Source-cited from SEC EDGAR, FEC filings, Federal Register, court dockets, and the Federal Reserve.</p>
  </a>

  <a class="card" href="dossiers/SNA-FINDINGS.html" style="border-left-color:var(--indiana-crimson);">
    <div class="tag" style="color:var(--indiana-crimson);">Social Network Analysis</div>
    <h2>The 153-node conflict-of-interest graph</h2>
    <p class="desc">Eigenvector centrality, Louvain communities, and the structural-redundancy finding that no small set of named officials disconnects the spine linking the Trump administration, the Federal Reserve, and the stablecoin issuers. Includes two publication figures and a reviewer-auditable edge CSV.</p>
  </a>

  <a class="card" href="verify.html" style="border-left-color:var(--old-gold);">
    <div class="tag" style="color:var(--old-gold);">Verification table</div>
    <h2>Every claim, mapped to its primary source</h2>
    <p class="desc">For journalists, Fed staff, and committee aides who want to audit in thirty seconds. PRIMARY / SECONDARY / PRESS / MODEL source classes, OGE-278 + SEC EDGAR + FEC + Federal Register URLs, explicit notes on what is press-sourced and what is not.</p>
  </a>

  <a class="card" href="outreach.html" style="border-left-color:var(--bse-teal);">
    <div class="tag" style="color:var(--bse-teal);">Outreach kit</div>
    <h2>Pull quotes, share copy, email templates</h2>
    <p class="desc">For readers who want to amplify or contact policymakers. Pull quotes, tag list, hashtag strategy, share-copy variants for X/Bluesky/Mastodon, and three email-draft templates (FRB staff, Senate Banking, press). Reuse without attribution.</p>
  </a>

  <figure class="figure-tile" style="border-left-color:var(--indiana-crimson);">
    <img src="figures/sensitivity_lolr.png" alt="Net welfare under EO 14405 as a function of the Fed lender-of-last-resort rate, showing break-even at 133 basis points">
    <figcaption>Net welfare sensitivity to the one variable the order does not specify. The Federal Reserve Board sets it.</figcaption>
  </figure>

  <h2 style="margin-top:36px;font-size:20px;color:var(--carolina-navy);border-bottom:1.5px solid var(--old-gold);padding-bottom:8px;">Individual OSINT dossiers (44,000+ words, source-cited)</h2>
  <ul style="list-style:none;padding:0;">
    <li style="padding:8px 0;border-bottom:1px solid var(--mist);"><a href="dossiers/trump-wlfi.html" style="color:var(--carolina-blue);">Trump family + World Liberty Financial + USD1</a></li>
    <li style="padding:8px 0;border-bottom:1px solid var(--mist);"><a href="dossiers/trump-extended-family.html" style="color:var(--carolina-blue);">Trump extended family financial exposure (Kushner, Boulos, others)</a></li>
    <li style="padding:8px 0;border-bottom:1px solid var(--mist);"><a href="dossiers/trump-admin-financial-roster.html" style="color:var(--carolina-blue);">Trump 2.0 administration financial-policy roster (Bessent, Pulte, Hassett, more)</a></li>
    <li style="padding:8px 0;border-bottom:1px solid var(--mist);"><a href="dossiers/sacks-a16z-quintenz.html" style="color:var(--carolina-blue);">David Sacks + a16z + Brian Quintenz crypto-policy nexus</a></li>
    <li style="padding:8px 0;border-bottom:1px solid var(--mist);"><a href="dossiers/fed-board.html" style="color:var(--carolina-blue);">Federal Reserve Board + 12 Reserve Bank presidents</a></li>
    <li style="padding:8px 0;border-bottom:1px solid var(--mist);"><a href="dossiers/congress-finance-committees.html" style="color:var(--carolina-blue);">Senate Banking + House Financial Services 119th Congress</a></li>
    <li style="padding:8px 0;border-bottom:1px solid var(--mist);"><a href="dossiers/stablecoin-board-interlocks.html" style="color:var(--carolina-blue);">Stablecoin ecosystem board interlocks + regulator alumni</a></li>
    <li style="padding:8px 0;border-bottom:1px solid var(--mist);"><a href="dossiers/circle-coinbase.html" style="color:var(--carolina-blue);">Circle (CRCL) + Coinbase (COIN) + Centre Consortium</a></li>
    <li style="padding:8px 0;border-bottom:1px solid var(--mist);"><a href="dossiers/tether-ifinex.html" style="color:var(--carolina-blue);">Tether + iFinex + Cantor Fitzgerald nexus</a></li>
    <li style="padding:8px 0;border-bottom:1px solid var(--mist);"><a href="dossiers/custodia-wyoming-spdi.html" style="color:var(--carolina-blue);">Custodia + Wyoming SPDIs + the EO 14405 legal substrate</a></li>
    <li style="padding:8px 0;border-bottom:1px solid var(--mist);"><a href="dossiers/fairshake-campaign-finance.html" style="color:var(--carolina-blue);">Crypto campaign finance: Fairshake, Stand With Crypto, and the 2024 cycle</a></li>
    <li style="padding:8px 0;border-bottom:1px solid var(--mist);"><a href="dossiers/synthesis.html" style="color:var(--carolina-blue);">Political-economy synthesis (the original 6-dossier overview)</a></li>
  </ul>

  <div class="meta-foot">
    <strong>Source repository:</strong> <a href="https://github.com/ihelfrich/eo14405-contagion">github.com/ihelfrich/eo14405-contagion</a><br>
    <strong>Author:</strong> Dr. Ian Helfrich, Ph.D. Economics, Georgia Tech 2024 · Independent researcher<br>
    <strong>License:</strong> Research note CC BY 4.0 · Code MIT · Data linked to primary sources<br>
    <strong>Disclosures:</strong> No financial interest in any entity discussed.<br>
    <strong>Style guide:</strong> Heritage palette (UNC Chapel Hill, Georgia Tech, BGSE, Indiana University) at <a href="https://github.com/ihelfrich/eo14405-contagion/blob/main/docs/style-guide.md">docs/style-guide.md</a>.
  </div>
</div>
</body>
</html>
"""
    landing.write_text(html, encoding="utf-8")


def render_404() -> None:
    out = SITE / "404.html"
    html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>404: Page not found · Helfrich Research</title>
<meta name="description" content="The page you are looking for does not exist on the Helfrich research site.">
<link rel="icon" href="/eo14405-contagion/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://rsms.me/">
<link rel="stylesheet" href="https://rsms.me/inter/inter.css">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Source+Serif+4:opsz,wght@8..60,400;8..60,600;8..60,700&display=swap">
<link rel="stylesheet" href="/eo14405-contagion/style.css">
<style>
  body { background: var(--parchment); }
  .nf { max-width: 640px; margin: 14vh auto 0; padding: 0 28px; text-align: center; font-family: var(--serif); }
  .nf .code { font-family: var(--sans); font-size: 14px; color: var(--carolina-blue); letter-spacing: 0.2em; text-transform: uppercase; }
  .nf h1 { font-size: 44px; color: var(--carolina-navy); margin: 12px 0 14px; border: none; padding: 0; }
  .nf p { color: var(--slate); font-size: 16px; line-height: 1.55; }
  .nf .cta { display: inline-block; margin-top: 22px; background: var(--carolina-navy); color: white; padding: 11px 20px; border-radius: 4px; font-family: var(--sans); font-weight: 700; text-decoration: none; }
  .nf .cta:hover { background: var(--old-gold); color: var(--carolina-navy); }
</style>
</head>
<body>
<div class="nf">
  <div class="code">404</div>
  <h1>That page is not here.</h1>
  <p>The URL you followed does not exist on the Helfrich research site. If you came from a link in the EO 14405 paper or one of the dossiers, please <a href="https://github.com/ihelfrich/eo14405-contagion/issues">file an issue</a> so I can fix the broken reference.</p>
  <a class="cta" href="/eo14405-contagion/">Go to the research note</a>
</div>
</body>
</html>
"""
    out.write_text(html, encoding="utf-8")


def render_sitemap_and_robots(pages: list[Path]) -> None:
    sitemap = ['<?xml version="1.0" encoding="UTF-8"?>']
    sitemap.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    for p in pages:
        rel = p.relative_to(SITE).as_posix()
        if rel == "index.html":
            rel = ""
        loc = f"{SITE_URL}/{rel}".rstrip("/") if rel else f"{SITE_URL}/"
        sitemap.append("  <url>")
        sitemap.append(f"    <loc>{loc}</loc>")
        sitemap.append(f"    <lastmod>{TODAY}</lastmod>")
        sitemap.append("    <changefreq>weekly</changefreq>")
        # Higher priority for index, paper, short, verify
        prio = "1.0" if rel in ("", "paper.html", "short.html") else "0.7"
        sitemap.append(f"    <priority>{prio}</priority>")
        sitemap.append("  </url>")
    sitemap.append("</urlset>\n")
    (SITE / "sitemap.xml").write_text("\n".join(sitemap), encoding="utf-8")

    robots = (
        "User-agent: *\n"
        "Allow: /\n"
        f"Sitemap: {SITE_URL}/sitemap.xml\n"
    )
    (SITE / "robots.txt").write_text(robots, encoding="utf-8")


# ---------------------------------------------------------------------- #
# Main
# ---------------------------------------------------------------------- #

def main() -> None:
    print(f"Building site at {SITE}")
    if SITE.exists():
        shutil.rmtree(SITE)
    SITE.mkdir(parents=True)

    # CSS + favicon
    shutil.copy(HERE / "docs" / "style.css", SITE / "style.css")
    shutil.copy(HERE / "docs" / "favicon.svg", SITE / "favicon.svg")
    print("  copied style.css + favicon.svg")

    # Figures
    figs_dst = SITE / "figures"
    figs_dst.mkdir(exist_ok=True)
    for f in (HERE / "figures").glob("*"):
        if f.is_file() and f.suffix in {".png", ".pdf", ".svg", ".geojson", ".json"}:
            shutil.copy(f, figs_dst / f.name)
    print("  copied figures")

    rendered_pages: list[Path] = []

    # Top-level pages
    for src, out, title, desc, is_sch in PAGES:
        src_p = HERE / src
        out_p = SITE / out
        rel_css = "../style.css" if "/" in out else "style.css"
        rel_favicon = "../favicon.svg" if "/" in out else "favicon.svg"
        if not src_p.exists():
            print(f"  [skip] {src}")
            continue
        pandoc_html(src_p, out_p, title, desc,
                    is_scholarly=is_sch,
                    rel_css=rel_css, rel_favicon=rel_favicon)
        rendered_pages.append(out_p)
        print(f"  {src} -> {out}")

    # Dossiers
    for src, title in DOSSIERS:
        src_p = HERE / src
        out_p = SITE / "dossiers" / (Path(src).stem + ".html")
        if not src_p.exists():
            print(f"  [skip] {src}")
            continue
        pandoc_html(src_p, out_p, title,
                    "OSINT dossier on EO 14405 principals.",
                    is_scholarly=False,
                    rel_css="../style.css", rel_favicon="../favicon.svg")
        rendered_pages.append(out_p)
        print(f"  {src} -> {out_p.relative_to(SITE)}")

    # Landing, 404, sitemap, robots
    render_landing()
    print("  built landing.html")
    render_404()
    print("  built 404.html")
    render_sitemap_and_robots(rendered_pages)
    print(f"  built sitemap.xml + robots.txt ({len(rendered_pages)} URLs)")

    print(f"\nSite at: {SITE}")
    print("Deploy via .github/workflows/deploy-pages.yml on push to main.")


if __name__ == "__main__":
    main()
