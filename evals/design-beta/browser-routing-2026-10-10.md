# Browser routing clarification

The user clarified the tool policy after the harness benchmark: Aside for research and ordinary agent browsing, Playwright for development verification, and Playwright by default for work not otherwise specified. An explicit tool choice takes priority. The analysis or QA agent owns interpretation and verdicts separately from browser operation. Static analysis uses source and analyzers unless runtime evidence is needed.

## Changes

- `design-browser` owns the routing policy, with a conditional Aside procedure and a controlled tool-comparison procedure. Playwright remains the default for unclassified browser work.
- The 13 adapted design skills pass purpose and expected observations to that policy. `explain-interface` no longer independently recommends Chrome DevTools MCP. `break` keeps its one-look budget with the selected driver.
- `wireframe` and `user-flow` pass the expected behavior and honor an explicit tool override when using a fallback.
- Promoted `prototype` and its human docs carry the same policy without depending on a beta skill. Its role and placement in `ask-matt` are unchanged; the router was read and required no new route.
- The source registry retains immutable import/review revisions and records this local policy decision with updated tree digests. No upstream reconciliation was advanced.

## Evidence and limits

The maintainer read installed `aside --help` and `playwright-cli --help`. Aside advertises account selection, exec, repl and guides; Playwright CLI advertises named sessions, snapshots, interaction, run-code and capture commands. This is interface availability evidence, not browser task success or performance evidence.

The previous [design review](results-2026-10-09.json) and [planning exercise](../design-planning/results-2026-10-10.json) keep their original hashes and Playwright observations. They do not validate this later routing revision. This update changes instructions; no new product mutation, tool installation, account change or promotion is involved.

Tool efficiency and result quality remain unmeasured. The new comparison procedure requires the same task, initial state, access, acceptance criteria and work budget, repeated runs, recorded failures/interventions, and review of the resulting artifacts. It separates setup from execution cost and leaves unavailable token/cost data unknown. The existing three-arm skill experiment continues to hold the browser driver fixed.

## Validation

An independent agent received only the skill and seven realistic requests. It selected: source research with Aside, general reference reading with Aside, static analysis without a browser, development QA with Playwright, unclassified browsing with Playwright, an explicit Aside override, and a controlled experiment without declaring a winner. Each answer kept the responsible agent's verdict separate from browser observations. The local report is `.scratch/design-browser-routing-20261010/independent-routes.md`.

The agent found one heading ambiguity: Playwright session syntax could appear to govern the Aside branch. The maintainer nested that heading under Playwright execution and named the session explicitly. This was an instruction-level exercise, not browser execution or an efficiency comparison.

`npm run check` passed with 36 tests and consistent provenance/invocation records; `claude plugin validate . --strict`, the design-browser skill validator and `git diff --check` passed. Local Markdown references resolve. Original import/review revisions remain unchanged. These checks establish package consistency and bounded routing behavior, not product QA, tool superiority or promotion readiness.
