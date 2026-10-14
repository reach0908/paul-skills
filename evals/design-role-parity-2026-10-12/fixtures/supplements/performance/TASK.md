# Local browser performance observation

Use Playwright CLI to measure this local page's Render labels interaction at 1280 by 900. Do not modify the page. Start each of three samples from a fresh navigation with zero labels, then activate the actual button once. Keep browser conditions identical across samples and record tool/browser versions, workload, viewport, capture method and raw observations.

Return the page's `labels:handler-to-dom` User Timing measure and observe main-thread long tasks during the interaction if the installed browser supports that API. Report unsupported collection honestly. Confirm that 120 labels and the completion status exist after each sample. Explain what each metric measures and does not measure. The evaluation owner will judge performance; do not assign a product QA pass or turn the elapsed CLI command time into an application metric. Include commands, failures and raw structured results. Close only your own browser session.

This is fictional local data, with no network service or account operation. No optimization is requested.
