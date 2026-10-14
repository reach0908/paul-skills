# Korean and mixed-script text

Use the actual Korean face and fallback stack when measuring. Latin `ch` widths and uppercase tracking recipes do not define Hangul line length or spacing. Keep project typography tokens unless rendered evidence shows a problem.

Compare Korean-only titles, Korean with product names, numbers and long URLs. Inspect the shortest supported width and text enlargement. Check for clipped glyphs, broken word groups, a missing full-text path and inconsistent line height after font fallback.

Choose word-breaking behavior for the content. `word-break: keep-all` can keep Korean word groups together but a long unbroken value still needs overflow handling. Test an appropriate `overflow-wrap` fallback on URLs and identifiers. Avoid applying aggressive breaking to all prose just to repair one exceptional value.

Keep the correct `lang` on the document and language changes. Let the browser shape text; avoid manual line breaks tied to one viewport. Confirm that real Korean fallback glyphs remain readable while the preferred font loads.

Report the actual string, viewport, loaded font and observed break. A Latin recipe mismatch alone is not a Korean typography finding.
