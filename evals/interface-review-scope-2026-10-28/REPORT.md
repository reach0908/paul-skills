# interface-review domain scope, 2026-10-28

Status: development evidence for a local change to two promoted skills, `interface-review` and `better-interface`. It rests on machine graders and one blind checklist pass by a fresh agent session; no human review yet. n is 3 per arm per case on synthetic fixtures. That supports observations on three tasks, not a general quality claim. The protocol and checklist were committed before the first run ([PROTOCOL.md](PROTOCOL.md), [review.json](review.json)); one dated amendment fixed two grader regexes before the branch run.

## Change under test

| Arm | Skills | Stage digests (`stage.py`) |
| --- | --- | --- |
| main | origin/main `794b572` (v0.5.0): every change review loads all six `better-*` owners | [outputs/main/stage.json](outputs/main/stage.json) |
| branch | `d032162`: `interface-review` classifies changed lines with [surface-map.md](../../skills/design/interface-review/surface-map.md) and hands `better-interface` a domain map; no UI surface means no owner and a short result | [outputs/branch/stage.json](outputs/branch/stage.json) |

The staged plugins differ in `interface-review` (SKILL.md, new surface-map.md), `better-interface` (SKILL.md, audit-procedure.md, review-format.md) and one router line in `ask-matt`. No run loaded `ask-matt`.

## Settings

Executor `claude-opus-5-5` in every run (each trace's `modelUsage`), Claude Code 2.1.311, `CLAUDE_CODE_EFFORT_LEVEL=medium` in the runner environment (requested; the trace does not show the applied effort). `claude plugin eval <stage> --eval-dir evals/irscope --ablation none --scaffold --keep-temp --no-publish --trust-plugin --allow-tools 'Bash(git:*)' --model claude-opus-5-5 --runs 3 -j 3 --max-cost-usd 12`. No LLM graders, so judge cost is $0. Costs are the runner's list-price figures (`costBasis: list`), not an invoice. Tokens come from each trace's `result` event. Main ran first and the branch about 20 minutes later, in separate runner invocations.

## Results

Means over 3 runs per cell. Owners are read from the traces' `Skill` tool calls and their results, not from the reports. Every listed load succeeded, and no run read a `better-*/SKILL.md` through `Read` instead.

| Case | Arm | Domain owners loaded (per run) | Graders | Cost (mean / total) | Wall time | Input / output / cache read / cache write / thinking tokens |
| --- | --- | --- | --- | --- | --- | --- |
| S-01 data-only category merge | main | all six, plus `better-interface` (3/3) | 0/3 all pass | $0.76 / $2.29 | 111s | 29 / 6,856 / 586,439 / 63,418 / 918 |
| S-01 data-only category merge | branch | none, no `better-interface` (3/3) | 3/3 | $0.33 / $1.00 | 56s | 13 / 3,387 / 169,901 / 28,876 / 646 |
| S-02 perf-only home page | main | all six, plus `better-interface` (3/3) | 0/3 | $0.68 / $2.03 | 90s | 22 / 5,749 / 394,024 / 60,495 / 959 |
| S-02 perf-only home page | branch | none, no `better-interface` (3/3) | 3/3 | $0.28 / $0.85 | 44s | 9 / 2,589 / 103,774 / 26,198 / 384 |
| S-03 color + layout | main | all six, plus `better-interface` (3/3) | 3/3 after amendment (0/3 as run) | $0.90 / $2.70 | 141s | 28 / 10,404 / 547,918 / 72,710 / 3,469 |
| S-03 color + layout | branch | accessibility, layout, colors, plus `better-interface` (3/3) | 3/3 | $0.73 / $2.18 | 126s | 25 / 9,756 / 468,314 / 54,782 / 2,896 |

Arm totals: main $7.02 (runner wall 374s), branch $4.03 (234s). Per-run data: [outputs/main/record.json](outputs/main/record.json), [outputs/branch/record.json](outputs/branch/record.json). Raw traces: `outputs/<arm>/<case>/run<n>/trace.jsonl`. Runner verdicts: `outputs/<arm>/aggregate-result.json` and `runner.log`.

### Graders that failed

- **main, S-01 and S-02 (6/6 runs).** These are the intended red: six owners loaded (`S1-no-domain-owner-skill`), no "no UI surface" statement, and a `Clear` row in coverage. Perf run 1 marked all six domains `Clear` for a diff with no rendered change. Every main S-01 run marked accessibility, layout and writing `Clear`.
- **main, S-03 (3/3 as run).** `S3-reflow-finding` used `\b320\b`, which cannot match `320px`. All three reports state the 320px overflow, and the amended pattern passes them ([outputs/main/regrade.json](outputs/main/regrade.json)).
- **main, S-02 run 0.** `RO-no-checkout-mutation` matched `rebase-apply` in the read-only mid-operation check. It is a grader false positive; the amended pattern passes it.
- **branch.** None failed.

### Findings on the real UI diff (S-03)

A fresh session graded the six S-03 reports blind to arm, with IDs shuffled ([outputs/blind](outputs/blind/), [verbatim report](outputs/blind/grader-report.md), mapping revealed afterwards):

| Item | main | branch |
| --- | --- | --- |
| F1 accent contrast 2.54:1, HIGH | 3/3 (one token row each) | 3/3 (one token row, or two rows split per consumer in 2 runs) |
| F2 toolbar grid overflow at 320px and in the 720px column, HIGH | 3/3 | 3/3 |
| F3 raw `12px` gap | 3/3 as its own LOW row | 3/3; 2 as their own LOW row, 1 folded into F2's reason |
| Block verdict | 3/3 | 3/3 |
| Finding wrongly attributed to the change | 0 | 0 |
| Other `Introduced`/`Regression` findings | none | none |
| Pre-existing findings | chip state by color only (HIGH) 2/3; `role="status"` (LOW) 1/3 | chip state by color only (HIGH) 3/3 |
| Factual slips | 1 (an ungraded text-vs-accent ratio off by about 0.1) | 1 run: says translated labels would be "clipped" (they would wrap); mislabelled Before/After cells |

No change-attributed finding that main reported was lost on the branch. F3 lost its own row in one branch run but stayed in the report. Writing, typography and UI were never loaded on the branch. Main produced no finding in those domains on this diff. It marked writing `Not reviewed` and typography and UI `Clear` in 3/3.

### Skipped-domain coverage

- **No-UI branch runs (6/6).** All six rows say `Not reviewed: no UI surface in the change scope`; one run wrote it in Korean.
- **Branch S-03 run 2.** Writes `Not reviewed: no copy`, `no type` and `no surface or motion in the change scope` in the Result cell.
- **Branch S-03 runs 0 and 1.** Put the same reason in the evidence cell and leave the Result cell as a dash placeholder. That is a formatting slip against the specified table, not a `Clear`. No branch run marked a skipped domain `Clear`.

### Reading

- On the two no-UI diffs the branch loads no owner and no `better-interface`, states why per domain, and points correctness concerns (an unbounded prefetch cache, whether the API filters hidden categories) at code review. It does this at 43% (S-01) and 42% (S-02) of main's mean cost, in about half the wall time.
- On the UI diff the branch loads the three owners the changed lines reach and keeps every change-attributed finding, at 81% of main's mean cost.
- The cost gap tracks the skipped bodies. Cache writes per run fall by about 35k tokens on the no-UI cases and 18k on S-03.

## Limits

- Three synthetic tasks, one model, one host, n=3. Two of the three test the cheapest branch (no UI at all). The surface map's middle rows (copy, type, markup, surface and motion, unclassified) are exercised only through color and box-and-flow lines here.
- The fixtures are deliberately clean. A diff that mixes a perf change with one rendered line, a Tailwind `className` edit, or a changed shared primitive was not run. The map says those load, but that is untested.
- The private sessions that motivated this (PR #484, #495) were not replayed; the fixtures imitate their shape.
- The arms ran sequentially, not interleaved. Prompt-cache state or service load could differ between the two windows. Wall times include runner overhead under `-j 3`.
- The blind grader is an AI session on the same model as the executor; its F3 and pre-existing judgments need human confirmation. The checklist was written by the author of the change.
- Current-screen audits are unchanged in source and were not re-run here. The native suite's `better-interface-settings-audit` and `interface-review-staged` cases were not re-run either.
- Codex was not run.
- Spend: $11.05 list price for the two arms, within the $40 ceiling. The blind grading session ran on the session's subscription, with no separate figure reported.
