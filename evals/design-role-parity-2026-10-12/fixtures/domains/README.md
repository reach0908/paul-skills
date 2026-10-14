# Domain review fixtures

Twenty-one independent local cases, three each for the seven domain review roles. `cases.json` lists each role, task file, fixture directory and timeout. Each application has its own HTML, CSS, JavaScript and product context. Serve only a selected `app/` directory on loopback. Reload resets state.

Keep each execution in a fresh fixture copy and named Playwright CLI session. Read the task and product context, inspect source, operate the page, and report evidence. Executor copies contain no evaluator rubric. Run all three cases per role in manifest order, with fresh page state for each case. Record any shared agent context across those cases. The caller owns trial arms, repeated runs and comparison.

These are bounded review exercises, not comprehensive accessibility certification or full reference-branch coverage. Desktop resizing, text enlargement, browser zoom, touch emulation and assistive-technology testing are distinct observations. Preserve that distinction in reports.
