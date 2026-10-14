# 내보내기 미리보기 review

Review this local page with `better-colors`. Read `app/PRODUCT.md`, inspect `app/index.html`, `app/styles.css` and `app/app.js`, then inspect the rendered page using Playwright CLI. Inspect and improve the color correctness and measured contrast of this bounded page. Implement the findings within this role in app/index.html, app/styles.css and app/app.js as needed. Keep the existing product purpose, system font, Korean/English content intent and vanilla stack. Do not change PRODUCT.md or unrelated behavior.

Serve the `app/` directory locally, for example with `python3 -m http.server 8765 --bind 127.0.0.1 --directory app` (choose another free port if needed). Open that localhost URL in a fresh named Playwright CLI session. Keep this case independent from the other cases.

Inspect light and dark appearances using the theme switch, including the preview caption, file-name input and PDF action. Measure opacity-composited text against its actual surface and identify required boundaries separately from decorative separators.

Use up to three minutes for this bounded page. Report the observed problems, the actual changes and relevant before/after runtime observations, then a scoped verdict. State which checks could not be completed. Do not infer a failure merely from a preferred style, and do not infer a pass from source alone when the claim depends on browser behavior. Source changes are authorized only in this case’s three application source files. Re-run the affected interactions and measurements after your changes. No external services are needed.
