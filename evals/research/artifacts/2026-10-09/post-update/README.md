# Research review after the Aside CLI update

The integrated research workflow passed a live development smoke on installed CLI `1.26.1008.1938` on 2026-10-09, Asia/Seoul. The current helper performed discovery, resumed the same owned investigation, and returned inspectable evidence. The caller independently checked the official release manifest through a REPL snapshot and retrieved the investigation's idle state, absent suspension, and final assistant answer through the documented Aside session API.

This record follows the earlier development evidence in the parent directory. That earlier record used the previous installed CLI and remains unchanged. This review does not establish independent full-skill compliance or model performance.

## Scope and evidence

The review checked the installed command syntax, helper behavior, source-audit instructions, result retrieval, and research consumers. Local evidence includes the ten successful help/version/guide commands in `installed-cli-help.json`, the exact current helper in `executed-helper.py`, final Aside answers in `aside-responses.json`, and the session read in `session-reader.json`. Each stage's exit status and the current skill digest are recorded in `result.json`.

The two public questions were bounded to the official CLI manifest and developer help. The filled prompts are retained in `discovery-brief.txt` and `followup-brief.txt`. Model, cost, token, and full-run duration telemetry were unavailable and remain null.

## Findings and fixes

| Question | Finding | Evidence and limit |
| --- | --- | --- |
| Does the installed version match current official metadata? | Both return `1.26.1008.1938` | Installed `--version` and the original [CLI manifest](https://releases.aside.com/cli/AsideCLI-darwin-arm64-latest.json), independently read through a browser snapshot in `source-audit.txt`. The endpoint is mutable and reports no release date. |
| Do the selected commands match this release? | `exec --effort ultrabrowse`, `session resume`, `steer`, `queue`, and REPL remain documented | Captured installed help and guides. Discovery and resume were exercised live; steer and queue have fixture coverage. |
| Does continuation retain the intended session? | The helper resumed the original investigation and returned its follow-up answer | Tracked CLI stdout and the specific owned-session reader. An acknowledgment alone was not treated as completion. |
| Can invalid follow-up input accidentally start a new investigation? | The previous helper treated an empty ID as no follow-up and started `exec` | Reproduced with the process fixture before the fix. The helper now rejects empty, surrounding-whitespace, or dash-prefixed IDs before any CLI call. |
| Can an effort setting be silently ignored on resume? | Explicit `ultrabrowse` previously passed validation but was not sent to the session command | Reproduced before the fix. Explicit effort is now rejected for follow-ups, retaining the session settings. |
| Do direct audits follow the installed REPL guide? | The instructions now inventory and reuse matching tabs before opening a new one | The current installed guide and direct manifest audit. Transcript reads expand through documented options rather than assuming a pagination API. |
| Are the consumers compatible? | `wayfinder` supplies one executor and the output path; `ask-matt` describes the same route | Static review of the current consumer instructions. No wayfinder runtime trial was conducted. |

## Claim ledger

| Claim | Original source | Evidence class | Date/version | Confidence and reason | Missing check |
| --- | --- | --- | --- | --- | --- |
| Latest advertised macOS arm64 CLI matches the installed version | [Aside CLI manifest](https://releases.aside.com/cli/AsideCLI-darwin-arm64-latest.json) and local `aside --version` | Retrieved original metadata plus executable observation | `1.26.1008.1938`, checked 2026-10-09 | High, independent snapshot agrees with the agent retrieval and installed version | Future release availability needs a fresh read |
| Public developer help and installed continuation syntax differ | [Aside developer help](https://docs.aside.com/help/developers) and local `aside session resume --help` | Source-owner documentation plus executable observation | No public page version/date found; local CLI `1.26.1008.1938` | High for the observed difference: the page uses `--session`, while current help uses `session resume` | The legacy form was not exercised at runtime; a help-only probe cannot prove alias support |
| Current `session resume` works for this investigation | Same-session helper execution and `session-reader.json` | Local runtime observation | Installed CLI `1.26.1008.1938`, 2026-10-09 | High for the bounded case: exit 0, final follow-up answer present, idle state and no suspension | Other hosts, accounts, interruptions, and failure states remain untested |

The raw Aside follow-up says that continuation was not executed. That statement describes the browser agent's own actions: the caller separately executed the real helper resumption and verified it. Public documentation drift does not by itself establish removal or deprecation of the old form.

## Validation and limitations

`npm run check` passed all 31 tests, including 11 helper integration tests. `claude plugin validate . --strict` and `git diff --check` passed. The two new regression tests failed before the helper fix and passed afterward. Research docs and the existing Changeset include the adjustments.

The live case establishes native discovery, same-session continuation, direct manifest snapshots, and owned-session result retrieval on the installed version. The developer page body was available through Aside's web reader; its browser snapshot exposed only the title. The session ID is redacted. Live steer/queue behavior, independent full-skill execution, nested dispatch prevention, and wayfinder integration still require separate trials. No model comparison or reliability rate is claimed.
