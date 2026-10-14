# Studio 초대 검토 review

Review this local page with `better-interface`. Read `app/PRODUCT.md`, inspect `app/index.html`, `app/styles.css` and `app/app.js`, then inspect the rendered page using Playwright CLI. This is a review request: do not edit application files.

Serve the `app/` directory locally, for example with `python3 -m http.server 8765 --bind 127.0.0.1 --directory app` (choose another free port if needed). Open that localhost URL in a fresh named Playwright CLI session. Keep this case independent from the other cases.

Review the full invitation page across all six domains. Test validation, pending repeat activation, success, dialog open/Escape/close, 320px reflow and reduced motion. Keep the existing Korean voice, system font and warm neutral bordered layout; report any concrete issue you can substantiate.

Use up to three minutes for this bounded page. Report actual findings with source locations and relevant runtime observations, then a scoped verdict. State which checks could not be completed. Do not infer a failure merely from a preferred style, and do not infer a pass from source alone when the claim depends on browser behavior. No source changes or external services are needed.
