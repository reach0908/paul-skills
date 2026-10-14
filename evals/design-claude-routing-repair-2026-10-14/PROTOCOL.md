# Claude routing repair protocol

Frozen before the first model run on 2026-10-14. The prior 0.4.0 report and its 33/34 outcome remain historical evidence.

## Hypothesis and package

The automatic description needs to name UI change-review requests as a reason to load better-interface before file inspection. Its body routes those requests to an explicit interface-review command. interface-review stays user-only. General screen audits and the other design entry points must remain reachable.

The candidate is a frozen copy of all 44 promoted skills and the unchanged 0.4.0 manifest, identified by bundle-manifest.json, not a release. Load it with the session-only --plugin-dir flag. Verify the exact runtime path and injected bodies; never infer the source from the displayed version alone. Baseline cases use the actual global 0.4.0 installation with no override. Global settings and installed plugin bodies remain unchanged.

[Claude's loading reference](https://code.claude.com/docs/en/plugins/loading#name-conflicts) documents the session override. [Plugin creation](https://code.claude.com/docs/en/plugins/create#load-a-plugin-for-one-session) documents its nonpersistent scope. Runtime evidence must independently confirm that it took effect.

## Fixed sample

cases.json fixes 46 fresh processes: 43 candidate and 3 concurrent baseline comparisons.

- Reuse all 34 original prompts unchanged: 17 explicit, 12 natural owner requests, 5 user-only boundaries.
- Add eight candidate routing checks: real Git working change, staged, branch, PR, exact range, unspecified target, directly invoked better-interface on a change, and a current-screen audit without the previous negative diff cue.
- Add one explicit interface-review working case on a real local Git fixture, continuing through better-interface and its six owners.
- Run the old release on the exact former failure, Git working and staged prompts too. These three pairs are descriptive evidence, not a statistical superiority study.

All directories use neutral case_NNN names and fresh session UUIDs. No expected skill name, grader or report is placed in a trial directory. Empty fixtures remain empty. Git fixtures contain only tracked before.html as src/Panel.html, an initial commit and its uncommitted after.html revision. They contain no private product material, remote or custom instructions.

## Host and bounds

Inherit the user's model and effort; record resolved values. Start a new Claude process for every case. Disable hooks per process and external MCP servers. Use only Skill, Read, Glob and Grep for entry/preparation trials. The one actual handoff case additionally permits specified read-only Git commands through Bash. No product writes, browser or external-service work. No permission bypass flag.

Two processes maximum; 360 seconds per process; $0.80 host list-cost threshold per ordinary case and $2.00 for the actual handoff. Stop dispatching at $22 total list estimate, accepting that in-flight calls may exceed the threshold. Stop and inspect after two consecutive environment failures. Preserve all attempts; no answer-based rerolls. A plugin-source infrastructure failure is recorded separately before any rerun.

## Acceptance

Every candidate case must complete, expose exactly 12 automatic design entries and 17 direct commands, load the correct package, preserve input files and have no denied or failed tools.

- Explicit entry: full host-injected target body equals the frozen source. A tool call is not required for native slash expansion.
- Natural entry: successful Skill invocation and exact host-injected owner body. A name in a response is insufficient.
- User-only boundaries: no unauthorized call, file read, search or body disclosure for any of the five user-only skills.
- Change routing: better-interface loads before any file discovery; the answer names /paul-skills:interface-review and preserves working, staged, branch, pr number or exact range. With no target, leave it unspecified. No domain calls, file inspection or verdict. Direct better-interface invocation may inject the body without a Skill call.
- Authorized handoff: explicit interface-review body, successful better-interface and all six domain calls with exact bodies, real before/after evidence and a classified accessible-name regression. No repeated invitation to invoke interface-review. Runtime claims must remain unverified.
- Current audit: better-interface loads; no redirect to the change-review command and no user-only skill is opened.

Collector controls and manual reading of routing/handoff answers supplement structural checks. Record incomplete and failed cases. Invocation evidence does not establish full design-output parity, browser QA, release installation or performance superiority.
