# Research Aside development evidence

This is a development smoke for the native Aside CLI route on 2026-10-09, Asia/Seoul. It verifies discovery, same-session continuation, and recovery of the owned investigation's status and final assistant answer. It is not a controlled trial of the whole skill or a model comparison.

## Observable results

- The installed CLI was `1.26.916.1741`. Its guide advertised an update; the investigation then retrieved the original [macOS arm64 CLI manifest](https://releases.aside.com/cli/AsideCLI-darwin-arm64-latest.json), which reported `1.26.1008.1938`. The manifest was read again locally and is retained in `official-cli-manifest.json`.
- The argument-safe helper started `exec` with a self-contained brief and `ultrabrowse`. The initial sandbox could not reach the local daemon. The same task succeeded through the host's normal permission escalation.
- The current helper resumed that known session with a targeted follow-up. Both discovery and follow-up returned exit 0 and inspectable answers.
- After reading `aside guide repl` and `aside skills show aside`, the caller used `aside.sessions.get(id)` and `aside.sessions.messages(id, {limit: 4, order: 'desc'})` only for the owned investigation. Status was idle and the final answer was present. A later ten-message read captured the follow-up answer; the original answer was retained from the initial run's stdout. Both are in `aside-responses.json` with their capture methods.
- The official versioned macOS arm64 archive was downloaded to a temporary folder and its code signature verified through macOS. TeamIdentifier `8CPD4K4TBB` matched the installed CLI. Latest `1.26.1008.1938` passed eight version/help/guide commands, including `exec`, `session resume`, and REPL help. The installation was not replaced. Captured output and the measured archive hash are in `latest-cli-help.json`.
- `npm run check` passed all 29 tests. Nine launcher tests cover literal prompt transport, missing/broken CLI, execution failure, configured defaults, resumption, running follow-ups, and invalid briefs. `claude plugin validate . --strict` also passed.

## Features selected

| Research need | Selected capability | Evidence boundary |
| --- | --- | --- |
| Discovery | `exec --effort ultrabrowse` | Live smoke on installed CLI |
| Direct original-source audit | REPL snapshots and screenshots | Installed guide and [developer help](https://docs.aside.com/help/developers); this smoke tested REPL session reads |
| Continue a known investigation | `session resume` | Live follow-up using the saved helper |
| Redirect or queue running work | `session steer` and `session queue` | Installed guide and argument-transport fixtures; live mutation not exercised |
| Recover status and final answer | Built-in Aside REPL session reader | Actual reads of the owned investigation |
| Latest-version check | Original release metadata GET | Retrieved official manifest; no installer run |

## Limits

The latest executable was used only for version/help/guide inspection, not a live browser investigation. Public developer help is unversioned and still shows `--session`; both inspected CLI releases document `session resume`. Latest command syntax and guides were verified, while live browser/API behavior was exercised through the installed CLI. The skill consults runtime help and site API documentation before using a feature. The raw initial audit predates the latest-package inspection; its remaining-gap claims should be read with this later evidence.

This evidence does not establish full-skill compliance, absence of nested executor dispatch, wayfinder integration behavior, or model performance. The initial discovery preceded the follow-up helper additions; the preserved helper is the exact body used for the follow-up. Model/cost/token/duration telemetry is recorded as null. The raw assistant answers remain data, including their source claims; the caller's narrower conclusions are recorded above. The owned session ID is redacted.

The separate local source `research-with-aside` was supplied by the user for adaptation. Its used files were read and content-hashed in `skill-sources.json`; no Git commit or license was invented. Local adaptation is authorized, and redistribution status remains unestablished. Original source bodies and unrelated personal files are not copied into these artifacts.

## Post-update review

After the user authorized installation of CLI `1.26.1008.1938`, a [separate post-update review](post-update/README.md) exercised the current helper and live session APIs on that installed version. This earlier record remains the historical pre-update smoke.
