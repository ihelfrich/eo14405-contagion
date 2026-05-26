# Helfrich research-note style guide

The visual and editorial system used across this project (and intended as
a portable identity system for subsequent work).

## Palette

### Primary (heritage and identity)

| Token         | Hex       | Source                       | Role |
|---------------|-----------|------------------------------|------|
| Carolina Blue | `#4B9CD3` | UNC Chapel Hill primary      | Dominant brand color |
| Carolina Navy | `#13294B` | UNC institutional navy       | Body ink, headings, structure |
| Old Gold      | `#B3A369` | Georgia Tech Old Gold        | Heritage accent, emphasis, rules |

### Accent (secondary, used at lower density)

| Token            | Hex       | Source                              | Role |
|------------------|-----------|-------------------------------------|------|
| BSE Teal         | `#2C7873` | Barcelona Graduate School aesthetic | Comparison data, alternative framing |
| Indiana Crimson  | `#990000` | Indiana University crimson          | Warnings, dissent. <5% of any document |

### Neutrals

| Token     | Hex       | Role |
|-----------|-----------|------|
| Parchment | `#FAF8F3` | Warm cream background |
| Slate     | `#4E5667` | Secondary text, axis labels |
| Mist      | `#E8E2D5` | Borders, dividers |

## Color theory rationale

- **Carolina Blue + Carolina Navy** is a single-hue light/dark pair: same
  family, different depth. The eye reads them as one identity, not two
  competing colors.
- **Blue + Old Gold** is a classical heraldic pair (used by Yale, Notre
  Dame, half of European royalty); reads serious and traditional without
  being academic-dusty. The muted "Old" Gold avoids the
  cheerleader-yellow problem.
- **BSE Teal** sits geometrically between Carolina Blue and a green;
  it is the third color that gives the palette range without leaving the
  harmonious blue-green family. Carries quiet Mediterranean intellectual
  association.
- **Indiana Crimson** is the only red, and the only fully-saturated
  color, so it draws the eye when used. It is the stop sign of the
  palette.
- **Parchment over white** signals scholarship over startup, reads
  warmer, and reduces eye fatigue on long reads.

## WCAG contrast (against Parchment background)

| Token            | Ratio | Use |
|------------------|-------|-----|
| Carolina Navy    | 13:1  | AAA body text safe |
| Slate            | 6.3:1 | AA  body text safe |
| Indiana Crimson  | 9:1   | AA  accent body safe |
| Carolina Blue    | 3.4:1 | Display text >=18px only |
| BSE Teal         | 4.7:1 | AA large text safe |
| Old Gold         | 2.8:1 | Accent / icon only |

## Typography

| Role         | Family             | Source              |
|--------------|--------------------|---------------------|
| Body, headings | Source Serif 4   | Adobe Fonts (free, open license) |
| UI, metadata, sidebars, captions | Inter | rsms.me/inter |
| Monospace    | JetBrains Mono     | jetbrains.com/lp/mono |

Rationale: avoids both the Times-New-Roman academic-dusty trap and the
Helvetica startup-generic trap. Source Serif 4 has optical sizing and
generous proportions for sustained reading. Inter is the most
carefully-spaced contemporary sans. JetBrains Mono renders code
cleanly without the cluttered ligatures of Fira Code.

For the *Pictures of Inference* book and any Helfrich publication, use
this stack. Do not deviate to local-system fonts; type identity is part
of brand identity.

## Layout

Body width 65ch (the Bringhurst measure, ~10-12 words per line).
Line height 1.55. Paragraph spacing generous (1.2em). Heading hierarchy
ranges from H1 (32px Carolina Navy) to H4 (15px small-caps Inter Slate).

## Component system

### Body links
Carolina Blue underline, transitions to Old Gold on hover. No
unnecessary ornament.

### "Verify this yourself" sidebars
Pale Carolina Blue background (5 percent tint), Old Gold left border
3px, Inter sans for the metadata label, Source Serif body.

### "Try the calibration" exercise boxes
Parchment background, BSE Teal top and bottom rules, formula in
JetBrains Mono. Hint and solution offered in indented, smaller text.

### Steelman boxes
Dashed BSE Teal border, italic body, explicit "STEELMAN OF THE
OPPOSING POSITION" label in Inter small caps.

### Disclosed-assumption boxes
Solid Old Gold left border, parchment fill, the assumption stated
clearly, then alternatives listed in two-column Inter.

### "How I could be wrong" sections
Subtle Indiana Crimson 1px left margin rule, italic body. The crimson
appears here and only here. It is the stop sign.

### Footnotes and citations
Numbered, Carolina Navy superscript. Click jumps to bottom-of-document
with full citation in Inter.

Inline citations: author-year format (Eisenberg and Noe 2001). Full
bibliography in Chicago author-date.

### Code blocks
JetBrains Mono, parchment background, Old Gold left border 2px. No
syntax highlighting in dark-mode-on-light-page; instead, use a muted
syntax theme that respects the surrounding palette.

## Editorial conventions

### Title style

Do not use the "X does not do Y. It does Z" construction. The format
manufactures a faux reveal where the structure provides the rhetorical
work rather than the content. The right title declares the subject.

Acceptable patterns:

- "Notes on [Subject]"
- "[Subject Phrase] and [Object Phrase]: [Methodological Qualifier]"
- "[Pure Substantive Title]" with subtitle naming the method

Unacceptable patterns:

- "[Thing] doesn't [verb]. It [other verb]."
- "Why [X] is actually [Y]"
- "The hidden [thing] behind [other thing]"
- Any rhetorical question used to manufacture mystery

### Voice

Declarative. Precise. Confident where the evidence supports it. Hedge
where it does not. Never sell the reader a conclusion through tonal
manipulation. The reader is a colleague, not a customer.

Avoid:

- "It is worth noting that"
- "Crucially" / "Importantly" / "Notably" as sentence starters
- Parallel triplets used for rhythmic emphasis
- Significance-puffery phrases ("a testament to", "marks a pivotal
  moment")
- "The real question is" / "at its core" / "fundamentally"
- Rule-of-three padding
- Em dashes (use parentheses, commas, colons, or new sentences)

### No em dashes

Period. This is a hard constraint. Em dashes are the most common AI
tell because they smooth over what should be a deliberate sentence
boundary. Use other punctuation.
