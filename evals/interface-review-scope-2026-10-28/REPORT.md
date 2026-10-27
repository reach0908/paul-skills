# interface-review domain scope, 2026-10-28

Status: development evidence for a local change to two promoted skills, `interface-review` and `better-interface`. It rests on machine graders and two blind checklist passes by fresh agent sessions; no human review yet. n is 3 per arm per case on synthetic fixtures. That supports observations on three tasks, not a general quality claim. The protocol and checklist were committed before the first run ([PROTOCOL.md](PROTOCOL.md), [review.json](review.json)); one dated amendment fixed two grader regexes before the branch run. The branch arm ran twice: r1 on the first skill text, and r2 after code review closed gaps in the surface map. r2 is the shipped text, and r1 stays recorded.

## Change under test

| Arm | Skills | Stage digests (`stage.py`) |
| --- | --- | --- |
| main | origin/main `794b572` (v0.5.0): every change review loads all six `better-*` owners | [outputs/main/stage.json](outputs/main/stage.json) |
| branch r1 | `d032162`: `interface-review` classifies changed lines with [surface-map.md](../../skills/design/interface-review/surface-map.md) and hands `better-interface` a domain map; no UI surface means no owner and a short result | [outputs/branch/stage.json](outputs/branch/stage.json) |
| branch r2 (shipped) | `5c0e655`: r1 plus the review fixes. The map now counts hooks and selectors whose returned state flips a render condition, translation key references, shown formatters, text-switching conditions and excluded binaries that render. The no-UI exit reads the stated intent first. 'Surface and motion' is renamed 'Polish and motion'. The audit procedure lets the map grow | [outputs/branch-r2/stage.json](outputs/branch-r2/stage.json) |

The staged plugins differ in `interface-review` (SKILL.md, new surface-map.md), `better-interface` (SKILL.md, audit-procedure.md, review-format.md) and one router line in `ask-matt`. No run loaded `ask-matt`.

## Settings

Executor `claude-opus-5-5` in every run (each trace's `modelUsage`), Claude Code 2.1.312 (the aggregates' `claudeVersion`), `CLAUDE_CODE_EFFORT_LEVEL=medium` in the runner environment (requested; the trace does not show the applied effort). `claude plugin eval <stage> --eval-dir evals/irscope --ablation none --scaffold --keep-temp --no-publish --trust-plugin --allow-tools 'Bash(git:*)' --model claude-opus-5-5 --runs 3 -j 3 --max-cost-usd 12`. No LLM graders, so judge cost is $0. Costs are the runner's list-price figures (`costBasis: list`), not an invoice. Tokens come from each trace's `result` event. Main ran first, r1 about 20 minutes later and r2 about an hour after that, each in its own runner invocation.

Every run but one hit 1 to 3 Bash permission denials: 12 in main, 12 in r1 and 13 in r2. They were compound shell commands outside the `Bash(git:*)` grant, such as `for` loops, `export` prefixes and `python3` contrast scripts. The agents retried with plain `git` calls or worked the contrast out by hand, and some noted the denial. No run ended early. The denials are listed per run in each trace's `result.permission_denials`.

## Results

Means over 3 runs per cell. Owners are read from the traces' `Skill` tool calls and their results, not from the reports. Every listed load succeeded, and no run read a `better-*/SKILL.md` through `Read` instead.

| Case | Arm | Domain owners loaded (per run) | Graders | Cost (mean / total) | Wall time | Input / output / cache read / cache write / thinking tokens |
| --- | --- | --- | --- | --- | --- | --- |
| S-01 data-only category merge | main | all six, plus `better-interface` (3/3) | 0/3 all pass | $0.76 / $2.29 | 111s | 29 / 6,856 / 586,439 / 63,418 / 918 |
| S-01 data-only category merge | branch r1 | none, no `better-interface` (3/3) | 3/3 | $0.33 / $1.00 | 56s | 13 / 3,387 / 169,901 / 28,876 / 646 |
| S-01 data-only category merge | branch r2 | none, no `better-interface` (3/3) | 3/3 | $0.34 / $1.02 | 59s | 14 / 3,497 / 194,242 / 29,069 / 739 |
| S-02 perf-only home page | main | all six, plus `better-interface` (3/3) | 0/3 | $0.68 / $2.03 | 90s | 22 / 5,749 / 394,024 / 60,495 / 959 |
| S-02 perf-only home page | branch r1 | none, no `better-interface` (3/3) | 3/3 | $0.28 / $0.85 | 44s | 9 / 2,589 / 103,774 / 26,198 / 384 |
| S-02 perf-only home page | branch r2 | none, no `better-interface` (3/3) | 2/3 | $0.30 / $0.90 | 51s | 10 / 2,925 / 126,033 / 27,117 / 530 |
| S-03 color + layout | main | all six, plus `better-interface` (3/3) | 3/3 after amendment (0/3 as run) | $0.90 / $2.70 | 141s | 28 / 10,404 / 547,918 / 72,710 / 3,469 |
| S-03 color + layout | branch r1 | accessibility, layout, colors, plus `better-interface` (3/3) | 3/3 | $0.73 / $2.18 | 126s | 25 / 9,756 / 468,314 / 54,782 / 2,896 |
| S-03 color + layout | branch r2 | accessibility, layout, colors, plus `better-interface` (3/3) | 3/3 | $0.75 / $2.24 | 146s | 25 / 10,477 / 451,013 / 55,828 / 3,241 |

Arm totals: main $7.02 (runner wall 374s), r1 $4.03 (234s), r2 $4.17 (268s). Per-run data: [outputs/main/record.json](outputs/main/record.json), [outputs/branch/record.json](outputs/branch/record.json), [outputs/branch-r2/record.json](outputs/branch-r2/record.json). Raw traces: `outputs/<arm>/<case>/run<n>/trace.jsonl`. Runner verdicts: `outputs/<arm>/aggregate-result.json` and `runner.log`.

### Graders that failed

- **main, S-01 and S-02 (6/6 runs).** These are the intended red: six owners loaded (`S1-no-domain-owner-skill`), no "no UI surface" statement, and a `Clear` row in coverage. Perf run 1 marked all six domains `Clear` for a diff with no rendered change. Every main S-01 run marked accessibility, layout and writing `Clear`.
- **main, S-03 (3/3 as run).** `S3-reflow-finding` used `\b320\b`, which cannot match `320px`. All three reports state the 320px overflow, and the amended pattern passes them ([outputs/main/regrade.json](outputs/main/regrade.json)).
- **main, S-02 run 0.** `RO-no-checkout-mutation` matched `rebase-apply` in the read-only mid-operation check. It is a grader false positive; the amended pattern passes it.
- **r1.** None failed.
- **r2, S-02 run 1.** `S1-no-ui-surface-stated` failed. The run loaded no owner and reached the right conclusion, and it checked that the loading and error transitions are unchanged (the new hook rule). But it wrote every skip reason only in Korean ("검토 안 함: 바뀐 UI가 없음") instead of the specified `Not reviewed: no UI surface in the change scope`. This is a real wording failure against the skill's report format, not a grader defect.

### Findings on the real UI diff (S-03)

Two fresh sessions graded the S-03 reports blind to arm, with IDs shuffled and the mapping revealed afterwards:

- main against r1: [outputs/blind](outputs/blind/), [verbatim report](outputs/blind/grader-report.md).
- main against r2: [outputs/blind-r2](outputs/blind-r2/), [verbatim report](outputs/blind-r2/grader-report.md).

The main column is from the first grade; the second grade regraded the same main messages with the same result on F1 to F3, V and X.

| Item | main | branch r1 | branch r2 |
| --- | --- | --- | --- |
| F1 accent contrast 2.54:1, HIGH | 3/3 (one token row each) | 3/3 (one token row, or two rows split per consumer in 2 runs) | 3/3 (split per consumer in 1 run) |
| F2 toolbar grid overflow at 320px and in the 720px column, HIGH | 3/3 | 3/3 | 3/3 |
| F3 raw `12px` gap | 3/3 as its own LOW row | 3/3; 2 as their own LOW row, 1 folded into F2's reason | 3/3 as its own LOW row |
| Block verdict | 3/3 | 3/3 | 3/3 |
| Finding wrongly attributed to the change | 0 | 0 | 0 |
| Other `Introduced`/`Regression` findings | none | none | none |
| Pre-existing findings | chip state by color only (HIGH) 2/3; `role="status"` (LOW) 1/3 | chip state by color only (HIGH) 3/3 | chip state by color only (HIGH) 2/3; unlabelled filter group (LOW, unverifiable) 1/3; one run states none |
| Factual slips | 1 (an ungraded text-vs-accent ratio off by about 0.1) | 1 run: says translated labels would be "clipped" (they would wrap); mislabelled Before/After cells | 2 runs, minor: an incomplete account of how the change affects the chip's state cue; chips described as "in the same row" |

The protocol's rule counts a finding as kept when it appears in at least as many runs as main, at the same severity.

- **r2 (shipped).** Keeps F1, F2 and F3 by that rule, 3/3 each.
- **r1.** Keeps F1 and F2. F3 is **not fully kept**: its own LOW row appears in 2/3 runs against main's 3/3, and the third run mentions it only inside F2's reason, at F2's HIGH severity. The checklist's F3 ("any severity, optional") is looser than the protocol's rule, and the protocol governs. With n=3 the r1 fold and the r2 recovery cannot be told apart from run-to-run variation.

No other change-attributed finding appears in any arm. Writing, typography and UI were never loaded on the branch. Main produced no finding in those domains on this diff. It marked writing `Not reviewed` and typography and UI `Clear` in 3/3.

### Skipped-domain coverage

No branch run marked a skipped domain `Clear`.

- **No-UI runs, r1 (6/6).** Every row says `Not reviewed: no UI surface in the change scope`; one run wrote the reason in Korean.
- **No-UI runs, r2.** 5/6 give the English string. One gives only the Korean translation; it is the grader failure above.
- **S-03, r1.** Run 2 writes `Not reviewed: no copy`, `no type` and `no surface or motion in the change scope` in the Result cell. Runs 0 and 1 put the same reason in the evidence cell and leave the Result cell as a dash placeholder.
- **S-03, r2.** Runs 0 and 1 write the reason in the Result cell (`no copy`, `no type`, `no polish or motion`; run 1 partly in Korean). Run 2 again puts it in the evidence cell.

So the reason sits outside the Result cell in 3 of 6 branch S-03 runs. That is a formatting slip against the specified table, not a `Clear`, and r2's mistakes-table row did not remove it.

### Reading

- **No-UI diffs.** In both revisions the branch loads no owner and no `better-interface` in 12/12 runs. It states why per domain and points correctness concerns (an unbounded prefetch cache, whether the API filters hidden categories) at code review. Mean cost is 45% (S-01) and 44% (S-02) of main's for r2, and 43% and 42% for r1, in about half the wall time. One r2 run of 6 broke the exact wording.
- **UI diff.** Both revisions load the three owners the changed lines reach. r2 keeps all three findings at main's severity in 3/3 runs, at 83% of main's mean cost (r1: 81%, with the F3 fold).
- **Mixed result.** The cost and owner-loading result is consistent across 18 branch runs. The finding result is equivalent for r2 on this one diff and slightly weaker for r1. The report-format compliance of the skipped-domain rows is imperfect in both revisions.
- The cost gap tracks the skipped bodies. Cache writes per run fall by about 35k tokens on the no-UI cases and 18k on S-03.

## Quality floor

Under the [quality floor](../design-beta/quality-floor.md), against Jakub's original `interface-review` and `better-interface` at the pinned `d574cc8`: **not compared**. No paired run against the originals was made. The requirement to load all six owners before marking a domain without evidence was added by this fork's [domain-entry repair](../design-domain-entry-repair-v4-2026-10-14/PROTOCOL.md) (candidate 8). The originals' outcomes on these three cases are unmeasured.

## Limits

- Three synthetic tasks, one model, one host, n=3 per arm and revision. Two of the three test the cheapest branch (no UI at all). The surface map's middle rows (markup, copy, type, polish and motion, unclassified) are exercised only through color and box-and-flow lines here. The rules r2 added (hooks, i18n keys, formatters, binaries, stated intent) have no case of their own; r2's runs only show they did not disturb these three.
- The fixtures are deliberately clean. A diff that mixes a perf change with one rendered line, a Tailwind `className` edit, or a changed shared primitive was not run. The map says those load, but that is untested.
- The two private sessions that motivated this were not replayed; the fixtures imitate their shape.
- The arms ran sequentially, not interleaved. Prompt-cache state or service load could differ between the two windows. Wall times include runner overhead under `-j 3`.
- The blind graders are AI sessions on the same model as the executor; their F3 and pre-existing judgments need human confirmation. The checklist was written by the author of the change.
- Current-screen audits are unchanged in source and were not re-run here. The native suite's `better-interface-settings-audit` and `interface-review-staged` cases were not re-run either.
- Codex was not run.
- Spend: $15.22 list price for main, r1 and r2, within the $40 ceiling. The blind grading sessions ran on the session's subscription, with no separate figure reported.
