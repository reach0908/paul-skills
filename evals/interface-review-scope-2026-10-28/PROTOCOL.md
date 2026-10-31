# Protocol: interface-review domain scope, 2026-10-28

Written and committed before any model run in this directory. Results go in [REPORT.md](REPORT.md); this file is not edited after the first run except to append a dated amendment.

## Question

`interface-review` hands a change review to `better-interface`, whose `audit-procedure.md` loads all six `better-*` owners on every route. In two real sessions (a data-only category merge and a home-page speed change, private, not reproduced here) the review loaded color and UI owners and then reported no color or component change. Does a change review that loads only the owners whose surface the diff touches, and none when no UI surface changed, cost less without losing the findings of a real UI diff?

## Arms

| Arm | Skills | Source |
| --- | --- | --- |
| main | every promoted skill at `794b5721e9c923c63df6ba9781a2750caf4823ef` (origin/main, v0.5.0) | `stage.py main` |
| branch | every promoted skill in this branch's working tree at the commit that records the after run | `stage.py branch` |

Only `skills/design/interface-review` and `skills/design/better-interface` may differ between arms; `stage.py` prints tree digests for both and for the cases. The same staged cases run in both arms.

## Cases

Synthetic fixtures built by [cases/base.sh](cases/base.sh) plus each case's `scaffold.sh`: a React feed app on `main` and one commit on a feature branch. The prompt is identical in every case: `/paul-skills:interface-review main...HEAD` with a read-only, source-only instruction.

| Case | Diff | Expected on the branch arm |
| --- | --- | --- |
| S-01 `data-only-category-merge` | server ingest alias map, its test and a SQL migration | no `better-*` domain owner loaded; short "no UI surface" result |
| S-02 `perf-only-home` | `Promise.all`, `useMemo` and an article prefetch in `Home.tsx` and `api/feed.ts`; returned JSX, render conditions, strings and styles unchanged | as S-01 |
| S-03 `color-layout-toolbar` | accent token `#2563eb` to `#60a5fa`; toolbar from wrapping flex to `repeat(5, 160px)` grid with a raw `12px` gap | accessibility, layout and colors loaded; findings equivalent to main |

## Measures

- **Owners loaded**: from each trace's `Skill` tool calls and their results (plus any `Read` of a `better-*/SKILL.md`), never from the agent's plan or report. Recorded by [summarize.py](summarize.py).
- **Machine graders**: in each `case.yaml`. S-01 and S-02 grade zero domain owners, a stated "no UI surface", no `Clear` coverage row and no Block verdict. S-03 grades the three owners, the contrast and 320px findings by regex, and a Block verdict. Read-only and eval-isolation graders apply to all.
- **Findings kept (S-03)**: [review.json](review.json) holds the checklist. A fresh session grades every S-03 final message blind to arm, with run IDs shuffled. A finding is kept when the branch arm reports it in at least as many runs as main and at the same severity. Any `Introduced` or `Regression` finding main reports that the branch never reports is a loss and is listed.
- **Cost**: runner `costUsd` (list price), trace `usage` (input, output, cache read, cache creation, thinking tokens) and `durationSeconds`. Missing telemetry is `null`, never zero.

## Settings

Executor `claude-opus-5-5`, judge none (no LLM graders), `CLAUDE_CODE_EFFORT_LEVEL=medium`. Runner: `claude plugin eval <stage> --eval-dir evals/irscope --ablation none --scaffold --keep-temp --no-publish --trust-plugin --allow-tools 'Bash(git:*)' --model claude-opus-5-5 --runs 3 -j 3 --max-cost-usd <cap>`. One runner invocation per arm runs all three cases.

## Budget and stops

Ceiling $40 list price for the whole trial, $12 per arm invocation. If a run errors, keep it and report it; rerun only a whole arm, never a single run, and keep the failed attempt. If the branch arm loses an S-03 finding, report it as a regression and do not claim improvement.

## Decision

Claim a cost reduction only where the branch arm's mean cost is lower and its graders pass. Claim equivalence on S-03 only if no main finding is lost. Anything else is reported as mixed or weak. Promotion and release are outside this trial.

## Amendment, 2026-10-28, after the main run and before the branch run

- `S3-reflow-finding` used `\b320\b`, which cannot match `320px` (no word boundary between `0` and `p`); all three main runs state the 320px overflow and failed only on that. The pattern is now `\b320(px)?\b`.
- `RO-no-checkout-mutation` matched `apply` inside `rebase-apply` in the mid-operation check that `scope-resolution.md` prescribes (`git rev-parse --git-path rebase-apply`, read-only); one main run failed on it. The pattern now requires the verb not to follow a word character or hyphen. Controls: `git checkout`, `git stash`, `git switch`, `git add` still match; `rebase-apply`, `git diff`, `git log` do not.
- The runner's own verdicts for main stay in `outputs/main/aggregate-result.json`. [regrade.py](regrade.py) re-applies only these two graders to the kept traces (`outputs/<arm>/regrade.json`); the branch arm runs with the amended `case.yaml` directly.
- The arms also differ in one router line of `skills/engineering/ask-matt/SKILL.md` (the change-review row). The summary records whether any run loads `ask-matt`.

## Amendment, 2026-10-28, after code review

Code review of the branch found ways a UI change could be read as "no UI surface". The fixes changed the skill text (commit `5c0e655`), so the whole branch arm ran again as r2, with the same cases, graders, settings and cap. r1 stays in `outputs/branch/`; r2 is in `outputs/branch-r2/`. A second fresh session graded main against r2 blind (`outputs/blind-r2/`). Nothing was rerun per run.
