"""
build_site.py — render markdown sources to a deployable static site
under site/, with the Helfrich heritage palette + typography.

Pipeline:
  1. Copy docs/style.css to site/style.css
  2. Convert each top-level markdown source to site/<slug>.html via pandoc
  3. Render each dossier to site/dossiers/<slug>.html
  4. Copy figures/ into site/figures/
  5. Build site/index.html (landing page)
  6. Build site/_redirects-equivalent meta tags

Run:
    python tools/build_site.py
"""
from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
SITE = HERE / "site"

# Mapping: source path -> (output filename, page title, meta description)
PAGES = [
    ("blog-research-note.md", "index.html",
     "Notes on Executive Order 14405",
     "Master account access and stablecoin run dynamics. A long-form research note by Dr. Ian Helfrich."),
    ("paper.md", "paper.html",
     "Stablecoin Run Risk Under Direct Federal Reserve Access",
     "Formal working paper: spectral and optimal-transport analysis of EO 14405."),
    ("linkedin-post.md", "short.html",
     "Notes on EO 14405 — Short version",
     "700-word LinkedIn-format summary of the EO 14405 contagion analysis."),
    ("verify.md", "verify.html",
     "Claim-by-claim verification — EO 14405",
     "Every numeric and factual claim mapped to its primary-source URL."),
    ("outreach.md", "outreach.html",
     "Outreach kit — EO 14405",
     "Pull quotes, share copy, tag list, and email templates for FRB, Senate Banking, and press."),
    ("dossiers/SYNTHESIS.md", "dossiers/synthesis.html",
     "Political-economy synthesis — EO 14405",
     "The synthesis of twelve OSINT dossiers on the principals behind EO 14405."),
]

# Individual dossier files
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


def pandoc_html(src: Path, out: Path, title: str, description: str,
                rel_css: str = "style.css") -> None:
    """
    Convert a markdown file to an HTML5 page with the heritage CSS,
    KaTeX math (via auto-render so it catches ALL delimiter patterns
    including \\tag{N} and \\Big inside $$...$$ blocks that pandoc's
    own --mathjax mode mishandles), and a complete <head> with
    semantic metadata.
    """
    out.parent.mkdir(parents=True, exist_ok=True)
    head_extra = HERE / ".build_head_extra.html"

    # KaTeX auto-render handles $$, $, \(, \[ delimiters uniformly.
    # The onload handler renders all math in document.body once both
    # katex.min.js and auto-render.min.js are loaded.
    katex_block = '''
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

    head_extra.write_text(
        f'<meta name="description" content="{description}">\n'
        f'<meta name="author" content="Ian Helfrich">\n'
        f'<meta property="og:title" content="{title}">\n'
        f'<meta property="og:description" content="{description}">\n'
        f'<meta property="og:type" content="article">\n'
        f'<meta property="og:image" content="https://ihelfrich.github.io/eo14405-contagion/figures/li_mechanism.png">\n'
        f'<meta property="og:image:width" content="1200">\n'
        f'<meta property="og:image:height" content="627">\n'
        f'<meta property="og:url" content="https://ihelfrich.github.io/eo14405-contagion/{out.name}">\n'
        f'<meta name="twitter:image" content="https://ihelfrich.github.io/eo14405-contagion/figures/li_mechanism.png">\n'
        f'<meta name="twitter:site" content="@ianhelfrich">\n'
        f'<meta name="twitter:card" content="summary_large_image">\n'
        f'<link rel="preconnect" href="https://rsms.me/">\n'
        f'<link rel="stylesheet" href="https://rsms.me/inter/inter.css">\n'
        f'<link rel="stylesheet" '
        f'href="https://fonts.googleapis.com/css2?'
        f'family=Source+Serif+4:opsz,wght@8..60,400;8..60,600;8..60,700&'
        f'family=JetBrains+Mono:wght@400;500&display=swap">\n'
        f'<link rel="stylesheet" href="{rel_css}">\n'
        + katex_block + "\n",
        encoding="utf-8",
    )
    subprocess.run([
        "pandoc",
        "--standalone",
        "--from", "markdown+tex_math_dollars+tex_math_double_backslash+pipe_tables+fenced_code_blocks+footnotes+yaml_metadata_block+raw_tex",
        "--to", "html5",
        # --mathjax tells pandoc to wrap inline math as `\(...\)` and
        # display math as `\[...\]`. The KaTeX auto-render script we
        # load in head_extra picks up BOTH those delimiters and renders
        # client-side. We pass an explicit (unused) MathJax URL so
        # pandoc does not also inject its own MathJax script tag (KaTeX
        # handles the rendering).
        "--mathjax=about:blank",
        "--metadata", f"title={title}",
        "--include-in-header", str(head_extra),
        "--wrap=preserve",
        "-o", str(out),
        str(src),
    ], check=True, cwd=HERE)
    head_extra.unlink(missing_ok=True)


def render_index() -> None:
    """Build the landing page index linking all parts of the work."""
    landing = SITE / "landing.html"
    # The actual landing is at index.html (which is the blog research
    # note). This file is a sister navigation page.
    html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Helfrich — Research notes</title>
<meta name="description" content="Research notes by Dr. Ian Helfrich.">
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
    <img src="figures/analysis_helfrich.png" alt="Nine-panel contagion analysis figure">
    <figcaption>EO 14405 contagion analysis under four analytical frameworks. Full caption and methodology in the paper.</figcaption>
  </figure>

  <a class="card" href="paper.html">
    <div class="tag">Academic working paper</div>
    <h2>Stablecoin Run Risk Under Direct Federal Reserve Access</h2>
    <p class="desc">Formal version with five propositions, proofs, full math, and Section 9 extensions (continuous Fed reaction function, cross-jurisdiction transmission, per-issuer reserve composition, MMF substitution, operational rails residual). ~7,000 words.</p>
  </a>

  <a class="card" href="short.html">
    <div class="tag">Short version · LinkedIn</div>
    <h2>The argument in 700 words</h2>
    <p class="desc">For readers with limited attention budget. Single thesis, one figure, link to depth.</p>
  </a>

  <a class="card" href="dossiers/synthesis.html">
    <div class="tag">Political-economy synthesis</div>
    <h2>The principals behind EO 14405</h2>
    <p class="desc">Synthesis of six OSINT dossiers documenting the financial and personnel networks among the actors whose interests the order affects. Source-cited from SEC EDGAR, FEC filings, Federal Register, court dockets, and the Federal Reserve.</p>
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


def main() -> None:
    print(f"Building site at {SITE}")
    if SITE.exists():
        shutil.rmtree(SITE)
    SITE.mkdir(parents=True)

    # CSS
    shutil.copy(HERE / "docs" / "style.css", SITE / "style.css")
    print(f"  copied style.css")

    # Figures
    figs_dst = SITE / "figures"
    figs_dst.mkdir(exist_ok=True)
    for f in (HERE / "figures").glob("*"):
        if f.is_file() and f.suffix in {".png", ".pdf", ".svg", ".geojson", ".json"}:
            shutil.copy(f, figs_dst / f.name)
    print(f"  copied figures")

    # Top-level pages
    for src, out, title, desc in PAGES:
        src_p = HERE / src
        out_p = SITE / out
        rel = "../style.css" if "/" in out else "style.css"
        if not src_p.exists():
            print(f"  [skip] {src}")
            continue
        pandoc_html(src_p, out_p, title, desc, rel_css=rel)
        print(f"  {src} -> {out}")

    # Dossiers
    for src, title in DOSSIERS:
        src_p = HERE / src
        out_p = SITE / "dossiers" / (Path(src).stem + ".html")
        if not src_p.exists():
            print(f"  [skip] {src}")
            continue
        pandoc_html(src_p, out_p, title, "OSINT dossier on EO 14405 principals.",
                    rel_css="../style.css")
        print(f"  {src} -> {out_p.relative_to(SITE)}")

    # Landing page (sister to index.html which IS the blog research note)
    render_index()
    print("  built landing.html")

    print(f"\nSite at: {SITE}")
    print("Deploy via .github/workflows/deploy-pages.yml on push to main.")


if __name__ == "__main__":
    main()
