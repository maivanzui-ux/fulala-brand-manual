# Fulala Brand Manual

Brand guidelines and the base design system for Fulala, in Czech and English (CZ/EN switch in the sidebar).

Chapters: Introduction, Logo, Colours, Typography, Illustrations, Design system.

## Structure

- `index.html` – the built manual (a single static page, this is what Vercel serves)
- `files/` – the download files (`logo`, `symbol`, `illustrations`, `colours`); the PDFs in its root are the original brand sources
- `src/` – sources the page is built from
  - `template.html` – page layout, Logo/Colours/Typography/Illustrations chapters, styles and scripts
  - `ds.html`, `ds.css`, `ds.js` – the Design system chapter
  - `en.py` – English translations, keyed by the exact Czech text
  - `*.svg.part` – logo and illustrations extracted from the brand PDFs
  - `assets.py` – generates the download files in `files/` (CMYK PDF/EPS, illustration SVG/PNG, Adobe swatches, ZIPs); `build.py` runs it
  - `build.py` – assembles everything into `index.html`

## Download file names

Every downloadable file follows one pattern (English, lowercase, hyphens):

- single files: `fulala-<subject>-<variant>[-cmyk].<ext>`, e.g. `fulala-logo-white-on-cinnabar.svg`, `fulala-tiger-black-cmyk.pdf`
- variants: `cinnabar`, `black`, `white`, `white-on-cinnabar`; `-cmyk` marks print files (PDF, EPS)
- packages: `fulala-<subject>-digital.zip` (SVG + PNG, RGB) and `fulala-<subject>-print.zip` (PDF + EPS, CMYK)
- folders in `files/`: `logo`, `symbol`, `illustrations`, `colours`

Illustrations are listed tigers first (tiger head, tiger with dumpling, tiger with menu), then the other motifs; new illustrations follow the same order in the manual, the menus and the packages.

Exceptions: favicon files keep the names browsers expect (`favicon.ico`, `apple-touch-icon.png`, `icon-512.png` …) inside `fulala-symbol-favicon.zip`; the original brand PDFs in the root of `files/` keep their source names. Add new files through `src/assets.py` so they get the same names.

## Editing

1. Edit the files in `src/`. When you change or add Czech text, add the matching English entry to `src/en.py`.
2. Rebuild: `python3 src/build.py`
3. Open `index.html` in a browser to check, then commit and push. Vercel deploys every push to `main`.

Sections marked **Návrh / Draft** are proposed rules that still need approval.
