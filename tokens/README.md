# Fulala design tokens

`fulala.tokens.json` is the single source of truth (W3C Design Tokens format).
It mirrors the Figma file FULALA 2.0, page Design System:

| JSON group | Figma | CSS |
|---|---|---|
| `color.white` … `color.honey-bronze` | collection **Fulala** (`color/*`) | `--fulala-color-cinnabar` |
| `color.bg/text/border/action/feedback.*` | collection **Semantic** (aliases) | `--fulala-color-bg-page` |
| `space.*`, `radius.*`, `border-width.*` | collection **Dimensions** | `--fulala-space-4`, `--fulala-radius-pill` |
| `typography.*` | text styles `Web/*`, `UI/*` | `--fulala-typography-h2` + `.fulala-h2` |
| `shadow.pop` | effect style `Shadow/Pop` | `--fulala-shadow-pop` |

Headings: Grandstander (Display Bold, headings SemiBold). Body and UI: DM Sans.

After editing the JSON run `python3 tokens/build_tokens.py` to regenerate `fulala-tokens.css`,
and update the matching variable in Figma (each Figma variable has its CSS name as code syntax).
