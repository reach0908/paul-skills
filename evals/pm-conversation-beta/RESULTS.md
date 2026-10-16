# PM conversation and prototype walkthrough beta results

2026-10-14. Development evidence for five optional candidates. Not a promotion decision or measured skill/model superiority.

## Implemented behavior

- office-hours preserves the startup/builder conversation, response posture, adaptive follow-up, related decisions/landscape, premise revision, distinct approaches and actual user choice, compact canonical record, bounded review and specific closing. Host/runtime and intentional behavioral changes are documented in SOURCE-REVIEW.md.
- prototype-user-test implements a moderator and fresh AI participant workflow: separate author and neutral task packets, actual UI attempts, freeze before interview, same-participant neutral follow-up, then observed-versus-intended comparison. It is original authoring for design evaluation, not a general product review.
- problem-discovery routes requested idea development without restarting an answered interview. product-brief adds benchmark-to-decision synthesis, scoped impact and cross-artifact readiness. experiment-design separates AI walkthroughs from human usability and other evidence.
- ask-matt and its docs include optional beta routes, preserving 0.4.1 design review invocation. The promoted plugin array/root skill catalog are unchanged; all five candidates remain in-progress.

## Actual cases and limits

| Case | Observed outcome | What this does not establish |
| --- | --- | --- |
| Builder conversation, four user/assistant turns (office v1) | Offered adjacent uses, changed direction after a user rejected the game, compared three approaches, waited for a choice, and retained the user's choice against its own recommendation | Initial sound-recorder prompt overlaps the upstream example. This is mechanism evidence, not novel-idea quality or upstream parity. Record used an available installed brief dependency; the updated brief is tested separately |
| Selected personal-project record (office v2) | Retained approved scope and unknowns, but still summarized the saved record rather than showing its whole body | The initial pointer repair was insufficient; kept as failed presentation evidence |
| Same-input fresh record recheck (office v3) | The response includes the entire final saved decision record verbatim. Existing approvals and deferred sync survived. No new interview or implementation | One bounded artifact-presentation recheck, not repeatable overall superiority |
| Goal changes from personal to startup | In the same continued conversation, rejected waitlist interest as validated demand, preserved the existing local choice and asked for a concrete commitment behavior | Mode-shift response only; all six diagnostic routes and subsequent business decisions were not exercised |
| PM handoff from conflicting synthetic artifacts | Preserved D1-D4, treated superseded public-feed proposal as history, left two unselected return policies unresolved, did not approve the draft's copy-deletion rule, identified impossible integration-test ordering, and allowed common design to start | Static document readiness only. No browser, iOS implementation or actual user study. All five raw inputs stayed unchanged |
| Prototype walkthrough v1, one fresh participant, two tasks and interview | Save and target introduction were found without UI coaching. Returning from saved detail opened recommendations; the participant independently tried a recovery. All 63 original evidence files retained their hashes after interview | Tool permission/daemon reconnection needed moderator infrastructure help. First failure preserved. The final recovery capture was 2.387s past the retry deadline; final observation was 8m20s after retry start. Task 2 is bounded partial completion, not within-limit success |
| Prototype walkthrough v2 with preflight | Preflight isolated infrastructure from the UI attempt. One newly fresh participant completed the combined task in 124.615 seconds and five UI actions within 3 minutes/eight actions, including an unassisted extra-tab recovery. Same-context post-task interview and frozen hashes were preserved | One AI, one viewport/combined task; no search or persistence observation. Moderator list_agents incidentally returned unrelated task status summaries, which were not opened/used and were not passed to the participant. Packet/budget differ from v1; no paired efficiency claim |

These are actual in-session agent executions using fresh fork_turns=none contexts where stated, with inherited host settings and no model overrides. The moderator/participant are separate contexts; post-task interview deliberately reuses the participant. Exact model build, effort, token/cost and comparable duration telemetry were not exposed and remain null. Reported UI clock intervals include tool/model/infrastructure overhead, not human task time or application performance.

No expected answer or grading rubric was supplied to evaluators. A complete collaboration tool-event transcript was unavailable; actual dispatch packets, saved observations, captures and responses are retained. The moderator necessarily received author intent as task input, while its fresh participant did not. All products and task text are synthetic. Private field sessions are not copied into these artifacts.

## Observed repairs

1. office-hours v1 produced a file and summary; a first pointer repair (v2) still did not display the complete saved record. v3 explicitly reads and reproduces the final saved body. A new-context same-input run passed byte-for-byte inclusion of its own saved record. Original outputs and both prior skill snapshots remain separate.
2. The first prototype pass spent its attempt budget on sandbox/daemon transport and overran a strict deadline during recovery. v2 preflights the browser route before participant dispatch, communicates working transport without UI hints, separates UI/interview bounds, and explicitly labels late evidence. The first attempt and its strict time-guard failure remain visible. A fresh moderator/participant execution exercised the revised preflight and separate bounds without UI coaching. The participant remained blind to intent; a moderator status-summary exposure is separately disclosed.

The source template/sections are pinned with MIT notice and file hashes. Local source revisions are preserved; changes to the prompts get new local digests rather than pretending to advance upstream review. Full gstack helper/runtime parity and independent record-review behavior remain untested.

## Artifact map and verification

- trials.json names actual tasks, outputs, skill versions and evidence boundaries.
- artifacts/office-builder, office-record-recheck, office-record-recheck-v3 and handoff preserve responses, records and source-integrity checks.
- artifacts/coordinator preserves exact neutral dispatches, frozen raw browser observations, screenshots, interview and intent comparison, including original failures and cleanup.
- artifacts/prototype-recheck preserves the preflight pass's actual evidence and report.
- fixtures/ contains only synthetic input; the runnable shelf is in fixtures/shelf/.
- integrity.json and verify.py check stored bytes and actual skill trees. Run `PYTHONDONTWRITEBYTECODE=1 python3 evals/pm-conversation-beta/verify.py`. A corrupted-copy negative control must fail. These checks do not grade the observations.

Checks on Node 22.19.0 and temporary npm 10.9.4: npm run check passed (61 skill records, 44 promoted paths, 38 deterministic tests); claude plugin validate . --strict passed; quick_validate passed for all five candidates. scripts/link-skills.sh linked 57 eligible skills into each of two disposable trial harness paths, without daily global relinking. Artifact integrity passed for the recorded files and five current skill trees; a corrupted-copy negative control was rejected with an artifact digest mismatch. The first manifest-generation attempt mistakenly included its prior manifest; that self-reference was removed and both controls rerun successfully. Raw browser stdout is preserved verbatim, including incidental whitespace.

The latest 0.4.1 design-routing main was merged into the isolated PM branch; unrelated work in the original checkout was preserved. These checks establish package, metadata and named artifact properties only.

## Next user trial

Use the installed office-hours on a genuinely open idea, or provide prototype-user-test a runnable URL and the author's intended outcome. The moderator keeps the expected route private and asks fresh participants to attempt neutral goals. Inspect whether useful follow-ups, author-intent separation, actual behavior, interview evidence and current-decision handoff survive. User acceptance and explicit promotion remain pending.

Natural selection and successful operation on every installed host, multiple simultaneous participants/shared backend isolation, real human interviews, paid services, production effects, statistical usability or source-quality superiority are not established by these cases. Individual beta installation and any fresh-host discovery check are separate receipts, not release or promotion evidence.
