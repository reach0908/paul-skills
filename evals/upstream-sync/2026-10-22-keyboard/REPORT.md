# State-machine and variant keyboard follow-up

The user requested completion of the two deferred updates after resolving keyboard verification. Both updates are now applied locally. The final browser matrix passes 8/8 cases, and the four negative controls demonstrate failing shell exits. No commit, PR, release, global installation or new promotion was performed.

## Pinned scope and preservation

This completes the proposal from the [original sweep](../2026-10-22/REPORT.md). That directory, including its failed browser result and deferred decisions, remains unchanged.

- Source: `https://github.com/jakubkrehel/skills`.
- Import and previous reviewed revision: `d574cc8a576dc24256ad38268b8d03d86724a1b3`.
- Reviewed target: `4c66b1fa86e9ab70187b43d7da9b6fdb29f2ef63`, using the cached checkout fetched in the original sweep. This follow-up did not query remote HEAD again.
- Local Git base: `e5438096106564ded2ddaede61d8061f9f7b9380`, plus the earlier uncommitted wizard, chief-of-staff and source-reconciliation work.
- The original compare helper confirmed no local drift in either deferred skill before applying the saved proposal. The patch also passed `git apply --check`.
- Immutable import paths/revisions, every other source and skill record, invocation policy, licenses, browser routing, and variant task-state/overlay requirements are preserved. `ask-matt` was read; the roles and routing did not change, so its map needed no edit.

The [resolution record](resolution.json) preserves both complete before/after skill records. Each former defer is explicitly resolved as adapt, with this report replacing its active report link. The original historical decision remains in that record and the original sweep. Both reviewed revisions advance only after verified completion.

| Skill | Final whole-tree digest |
| --- | --- |
| state-machine | `sha256:d5e7bcba09e9835b06b9a4f931434d84df2e1cbc996e8b6c5f3dc9c1d5012947` |
| variant | `sha256:1d194b8d2af8ac0abf3e820b8c1e55d03a8a37da08dd68d1ad1c75794baf463b` |

## Diagnosis and correction

The original checker still failed on the 390px state-machine case: after Tab reached SELECT with a visible focus outline, ArrowDown followed by Enter left `choice-0` selected. [Original rerun](original-result.json).

Removing the fixture styling, groups and all event handlers left a plain select with Alpha and Bravo. The same keys still left Alpha selected. [Minimal script](minimal.js), [result](minimal-result.json).

Three hypotheses were tested: headless-specific native-menu handling, incorrect menu-opening keys, and delayed processing. The same browser version was tested headed and headless. Space/ArrowDown/Enter, two ArrowDown presses/Enter, Alt+ArrowDown/ArrowDown/Enter, and a 500ms delay also left Alpha selected. The key events were trusted and not default-prevented. Typing `b` selected Bravo and emitted trusted input and change events in both modes. [Probe script](probes.js), [headless results](headless-probes.json), [headed results](headed-probes.json).

This isolates the earlier failure to the installed native-select automation behavior rather than the proposed styles or fixture event handler. It does not identify the exact Chrome/OS implementation cause or prove native popup arrow navigation works. The correction is to stop treating a native select like the custom list: the list retains its arrow shortcuts, while the select owns its native keyboard handling and updates the shared URL on change.

The new checker enters with real Tab and uses actual native type-ahead keys, Enter and Escape. It asserts the trusted change event, selected value and URL, without `selectOption`, programmatic focus or value assignment in its keyboard proof. The reference instructions now explicitly preserve native select handling and require real keyboard evidence.

## Applied behavior and evidence

The grouped list sits beside the component when the available container fits it. At narrower widths, a native select with the same groups sits above it. Both controls stay mounted; CSS chooses visibility and the URL keeps the active selection across resize. The updated human docs describe this behavior. [Candidate patch](candidate.patch), [frozen sources](candidate/), [environment and source hashes](environment.json).

The fixture generator extracts the reference HTML/CSS and supplies synthetic labels, a task input and a small authored interaction adapter. State-machine has 30 choices in three groups; variant has three choices on one axis. The fixtures establish reference and adapter behavior, not an independent agent's implementation quality.

| Skill | Viewport | Result | Unique choices traversed |
| --- | --- | --- | --- |
| state-machine | 1280 × 800 | pass | 30 |
| state-machine | 390 × 844 | pass | 30 |
| state-machine | 320 × 450 | pass | 30 |
| state-machine | 640 × 400 | pass | 30 |
| variant | 1280 × 800 | pass | 3 |
| variant | 390 × 844 | pass | 3 |
| variant | 320 × 450 | pass | 3 |
| variant | 640 × 400 | pass | 3 |

Each cell checks expected counts/groups, initial focus, Tab and Shift+Tab order, visible focus, keyboard selection, product input/save access, shortcut suppression during input, H hide/restore, all four global arrows, modified-key suppression, traversal of every choice, active state/ARIA agreement, preserved input and feedback, resize preservation, horizontal bounds and URL restoration. Wide cases also check pointer selection and long-list scrolling. Every measured document width fits its viewport. [Final structured observations](browser-final.json), [screenshots and fixture pages](browser-fixtures/), [console record](console-errors.txt).

Preflight: Playwright CLI 0.1.22 available; owned sessions survived between commands; the local server at `http://127.0.0.1:8973` served the expected fixture; authentication was not required. Chrome was `152.0.7977.82` on macOS `27.0.1`. The final headless run completed at `2026-10-21T18:17:09.463Z` (`2026-10-22 03:17:09 KST`). Sessions were `paul-keyboard-20261022` and `paul-keyboard-headed-20261022`; both and the temporary server were closed after evidence collection.

## Checker controls and repository checks

[run_browser.py](run_browser.py) checks both CLI exit and structured status, retains partial failures and returns exit 1 on a failed scenario even when the CLI itself returns 0. It also requires all eight cases. Four independent mutations each fail exactly one 390px state-machine case, while the other seven complete:

| Mutation | Required detected failure | Runner exit |
| --- | --- | --- |
| Remove one option | wrong option count | 1 |
| Remove select from Tab order | not naturally keyboard reachable | 1 |
| Block selection keys | native keyboard change missing | 1 |
| Force 1500px stage width | horizontal page overflow | 1 |

The initial key-block mutation also blocked Tab, so it correctly failed earlier at forward focus order. That did not isolate selection, and is retained in [the initial result](blocked-keys-initial.json). The mutation was narrowed to preserve Tab and Shift, then the intended selection failure was observed. [Final controls](negative-controls.json). A subsequent clean run with the final checker passed 8/8.

- `npm run check:local`: passed, including `npm run check`, helper tests, grader controls and PM evidence checks. [Log](check-local.log).
- `claude plugin validate . --strict`: passed with the existing `ICON_MISSING` directory warning. [Log](plugin-validation.log).
- All seven comparison helpers reran against the original pinned targets. All 63 direct-origin mappings are reconciled, with zero pending decisions and zero local drift. The six existing absent repository-wide review baselines still yield aggregate UNKNOWN/exit 2; those are distinct from the completed skill mappings. [Summary](reconciliation-summary.json), [raw helper outputs](after/).

## Reproduce and limits

From the repository root, generate the fixture into `/private/tmp/paul-keyboard-20261022/browser` using `make_browser_fixture.py <output> .`, serve it on local port 8973, and open an owned Chrome session with `playwright-cli -s=<session> open http://127.0.0.1:8973/state-machine.html --browser=chrome`. Run `python3 evals/upstream-sync/2026-10-22-keyboard/run_browser.py --session <session> --output <result.json>`. Add `--mutation missing-option`, `no-tab`, `blocked-keys` or `overflow` to obtain the corresponding expected nonzero result. Close the owned session and server afterward.

These are desktop viewport checks of extracted reference markup with a synthetic component. They do not establish physical-iPhone behavior, browser zoom, screen-reader operation, the native popup's arrow navigation, independent skill-quality parity, human preference or model superiority. The original failed observations stay failed under their original method. No unresolved item remains for applying these two reviewed source updates locally.
