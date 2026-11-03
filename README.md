# Fulala Brand Manual

Brand guidelines and the base design system for Fulala, in Czech and English (CZ/EN switch in the sidebar).

Chapters: Introduction, Logo, Colours, Typography, Illustrations, Design system.

## Structure

- `index.html` – the built manual (a single static page, this is what Vercel serves)
- `files/` – original brand asset PDFs offered under "Ke stažení / Downloads"
- `src/` – sources the page is built from
  - `template.html` – page layout, Logo/Colours/Typography/Illustrations chapters, styles and scripts
  - `ds.html`, `ds.css`, `ds.js` – the Design system chapter
  - `en.py` – English translations, keyed by the exact Czech text
  - `*.svg.part` – logo and illustrations extracted from the brand PDFs
  - `build.py` – assembles everything into `index.html`

## Editing

1. Edit the files in `src/`. When you change or add Czech text, add the matching English entry to `src/en.py`.
2. Rebuild: `python3 src/build.py`
3. Open `index.html` in a browser to check, then commit and push. Vercel deploys every push to `main`.

Sections marked **Návrh / Draft** are proposed rules that still need approval.
