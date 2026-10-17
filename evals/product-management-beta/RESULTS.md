# PM beta results, 2026-10-14

Three implemented candidates were exercised with five no-skill/candidate pairs, then one fresh same-input candidate recheck after a bounded repair: 11 actual in-session agent runs. Tasks use a synthetic Pocket Cards product. This is observable smoke evidence, not a measured quality gain, customer outcome, human acceptance or promotion decision.

The base is c6bd4d24ed4df1f4f3fdcf52f7b635f7f432b70e. Workers used fresh fork_turns=none sessions with inherited parent settings and no overrides. The host does not expose exact model/effort/version or token/cost/duration telemetry through these tools, so these fields are null. The no-skill and candidate arms share task bytes and input hashes, permissions and output requirement. Only the candidate receives a workflow. No expected answer or evaluator rubric was dispatched. Raw outputs, edits and exact loaded skill trees are retained in [trials.json](trials.json); a full worker tool-event transcript was unavailable.

## Observations

| Case | No-skill baseline | Candidate | Evidence |
| --- | --- | --- | --- |
| Sufficient personal-tool problem | Proceeds without another interview, retains offline/self-report limits | Same progression, with linked evidence and explicit hypothesis/later scope | [Baseline](artifacts/discovery-ready-baseline/result.md), [candidate](artifacts/discovery-ready-candidate/result.md) |
| One-part prototype feedback | Changes D5 only and preserves D1-D4 plus unselected AI proposal. Handoff does not unpack mock/report conflict or historical rules; no before/after ledger | Adds changed-before/after reason and revision; preserves rules; links canonical input, observed memory-only mock, unsupported completion report and superseded v1 | [Baseline](artifacts/brief-update-baseline/result.md), [candidate](artifacts/brief-update-candidate/result.md), [edited canonical brief](artifacts/brief-update-candidate/product/brief-v2.md) |
| First demand test | Proposes repeat-use observation with sample/time/resource bounds and readiness check | Proposes manual repeat-use test, distinguishes interest/PASS from demand and marks numbers as proposals. Handoff ambiguity identified below | [Baseline](artifacts/experiment-plan-baseline/result.md), [candidate before repair](artifacts/experiment-plan-candidate/result.md) |
| Incomplete AI result at stop limit | Seven valid pairs fail the predeclared minimum of ten; inconclusive, stop, continue template-based card work | Same bounded decision with planned/executed/observed state and missing raw/provider/user evidence explicit; no added product requirements | [Baseline](artifacts/experiment-result-baseline/result.md), [candidate](artifacts/experiment-result-candidate/result.md) |
| 320px clipping and Tab focus | Design review plus browser observation roles; no unseen PASS | Same design route, no product experiment or browser execution invented | [Baseline](artifacts/design-boundary-baseline/result.md), [candidate](artifacts/design-boundary-candidate/result.md) |

Both arms often performed well. These cases do not justify a claim that the new skills outperform a capable no-skill agent. The clearest observed addition was explicit current-authority/state/change reasoning in the product-brief handoff. Longer outputs are not inherently better.

## Bounded repair and recheck

The first experiment-plan candidate handoff listed source-preservation/private-access rules next to the fixed screen without clearly labelling them as manual-test operating choices. Those rules were introduced by the proposed test, not supplied as user-approved product policy. A downstream builder could read them as product requirements.

The repair adds one distinction to experiment-design: keep test-only operating choices and AI-proposed policy changes separate from user-approved product rules in the handoff. Static clarity review also makes prototype/design-browser dependency calls explicit and separate. Source revisions and original file hashes stay unchanged; the reviewed current skill-tree digest is updated only for this adaptation.

A fresh worker received the exact same task and evidence, the repaired workflow and no prior output/diagnosis/rubric. Its [raw output](artifacts/experiment-plan-repair/result.md), under “다음 역할에 전달할 입력”, preserves the supplied fixed screen and explicitly labels sample size, timing, manual help and no-notification conditions as test proposals rather than product policy. The targeted ambiguity was absent in this run. Other plan details changed between runs; this is one targeted recheck, not repeatable superiority evidence. Original and repaired workflow snapshots remain separate in trials.json.

## Checks

- npm run check: package/catalog/provenance/invocation consistency, with 42 total skill records and the same 27 promoted paths, plus 31 deterministic tests.
- claude plugin validate . --strict: passed. Manifests and root promoted catalog were not changed.
- skill-creator quick_validate: all three candidates passed.
- git diff --check and modified prose checks: passed.
- verify.py: artifact/task/source/skill/licence integrity checked separately from behavior. A corrupted-artifact negative control must fail.
- scripts/link-skills.sh with disposable HOME: 38 eligible skills linked into both trial harness directories; daily installs were not altered. Actual agent runs explicitly read workflow files, so host discovery/Skill-tool activation is untested.

These checks establish the named artifact and packaging properties only. The original design-beta files are preserved in their checkout; design inputs were hashed for read-only role comparison.

## Remaining limits and next user validation

Not covered: incomplete discovery questions in business/builder mode; new-brief synthesis on a larger brief; pre-mortem branch; feasibility experiments; real participants, demand, AI provider quality or production effects; automatic routing in fresh installed Claude/Codex hosts; full PM→design→engineering execution; repeated comparative measurements. Human acceptance remains pending.

Next, use one public or locally private product task under the user's control: clarify only its unresolved product context, update the brief after one scoped design correction, then give the current brief and latest design references to technical synthesis. Inspect whether reasons, permissions/persistence/completion and observed-versus-intended state survive each handoff, whether any question repeats and whether AI suggestions remain proposals. For an experiment, agree on stop/result decisions before execution and inspect the resulting update. Keep private source artifacts in their owning project. Record the user's acceptance and failure evidence before requesting any formal promotion. Additional evaluation campaigns and a standalone product-handoff remain follow-up proposals, not blockers to this implementation.
