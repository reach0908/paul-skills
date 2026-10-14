# 문서 관리 review

Review this local page with `better-writing`. Read `app/PRODUCT.md`, inspect `app/index.html`, `app/styles.css` and `app/app.js`, then inspect the rendered page using Playwright CLI. Inspect and improve the interface copy and action wording of this bounded page. Implement the findings within this role in app/index.html, app/styles.css and app/app.js as needed. Keep the existing product purpose, system font, Korean/English content intent and vanilla stack. Do not change PRODUCT.md or unrelated behavior.

Serve the `app/` directory locally, for example with `python3 -m http.server 8765 --bind 127.0.0.1 --directory app` (choose another free port if needed). Open that localhost URL in a fresh named Playwright CLI session. Keep this case independent from the other cases.

Review search with a query that has no results, clear it in the input, and inspect the document-deletion dialog before completing the local simulated deletion. Check confirmation consequences and success wording against the product policy.

Use up to three minutes for this bounded page. Report the observed problems, the actual changes and relevant before/after runtime observations, then a scoped verdict. State which checks could not be completed. Do not infer a failure merely from a preferred style, and do not infer a pass from source alone when the claim depends on browser behavior. Source changes are authorized only in this case’s three application source files. Re-run the affected interactions and measurements after your changes. No external services are needed.
