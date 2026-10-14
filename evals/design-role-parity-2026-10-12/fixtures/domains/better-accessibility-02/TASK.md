# 초대 요청 관리 review

Review this local page with `better-accessibility`. Read `app/PRODUCT.md`, inspect `app/index.html`, `app/styles.css` and `app/app.js`, then inspect the rendered page using Playwright CLI. Inspect and improve the accessibility and keyboard operation of this bounded page. Implement the findings within this role in app/index.html, app/styles.css and app/app.js as needed. Keep the existing product purpose, system font, Korean/English content intent and vanilla stack. Do not change PRODUCT.md or unrelated behavior.

Serve the `app/` directory locally, for example with `python3 -m http.server 8765 --bind 127.0.0.1 --directory app` (choose another free port if needed). Open that localhost URL in a fresh named Playwright CLI session. Keep this case independent from the other cases.

Send the local invite twice while it is pending and inspect the completed effects, name and focus. Try an invalid email and correct it. Archive the first request by keyboard, continue with the next request, then open and close the policy dialog using the keyboard.

Use up to three minutes for this bounded page. Report the observed problems, the actual changes and relevant before/after runtime observations, then a scoped verdict. State which checks could not be completed. Do not infer a failure merely from a preferred style, and do not infer a pass from source alone when the claim depends on browser behavior. Source changes are authorized only in this case’s three application source files. Re-run the affected interactions and measurements after your changes. No external services are needed.
