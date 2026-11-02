# KaTeX 0.16.9 (vendored)

Typesets the maths in Setu's text view. Copied unchanged from the npm package
`katex@0.16.9` (MIT licence, see LICENSE): `dist/katex.min.js`,
`dist/katex.min.css`, `dist/contrib/auto-render.min.js` and the 20 `.woff2` fonts.
The fonts are embedded in `katex.min.css` as `data:` URIs, so there is no `fonts/`
folder: one file to copy instead of twenty-one. Each embedded font is byte for byte
the npm package's `.woff2`; the `.woff` and `.ttf` fallbacks are left out, because
every browser Setu supports reads woff2.
The same version the aligner team's viewer loads from a CDN; kept here so the
maths renders without the annotator's browser reaching any outside server.
