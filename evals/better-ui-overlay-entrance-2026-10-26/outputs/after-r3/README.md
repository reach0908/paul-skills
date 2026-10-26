# after r3 (shipped), with kept outputs

r3 adds one sentence to the `display: none` overlay recipe in `enter-exit.md` (commit `90b56bd`): the overlay rule gives no duration or easing, so the project's duration and easing tokens apply where it has them, and the example's `150ms`, `300ms` and `ease-out` are fallbacks. It answers the T4 failure in [after-r2b](../after-r2b/README.md).

Ran 2026-10-26 from 16:24 KST (07:24Z). `stage.py after` printed `stageDigest` `sha256:63a9de60469bb623520fc511a9e51436c44336a037c1f11eb59d2a5eeb9b5299` and `betterUiTree` `sha256:73207f480c73e177460aa50bae984eba8f5c5b94314a99910eedab8ff9b6fbac`. Same runner flags as the README's Settings, with `--max-cost-usd` 1.6 for O-01 and 1.2 for O-N. Executor `claude-opus-5-5`, Claude Code 2.1.310, `CLAUDE_CODE_EFFORT_LEVEL=medium`.

The folder has the same layout as after-r2b: each run's replayed `final/` files, its raw `trace.jsonl`, the runner's `aggregate-result.json` and `runner.log`, [record.json](record.json) and [blind-grades.json](blind-grades.json). No replayed edit failed to apply.

## Mechanical graders

| Case | All pass | Failing | Cost |
| --- | --- | --- | --- |
| overlay-open-close | 3/3 | none | $0.81 |
| staged-empty-state | 3/3 | none | $0.53 |

All three overlay runs use `var(--duration-*)` and no literal `ms` value appears in their `styles.css`.

## Blind checklist grade

A fresh Claude Code session graded the checklist from `review.json` without the verdicts, this record or a hint about any defect. It ran Opus 5.5 with `--model opus --effort medium`, and its brief started with `/paul-skills:code-review`. It saw each case's prompt, the original files and the final files, in a folder outside the repository.

- overlay-open-close Q1 to Q5: pass in 3/3 runs (15/15).
- staged-empty-state S1 to S4: pass in 3/3 runs (12/12).
- Outside the checklist, it noted for all three overlay runs that the closing menu and modal backdrop stay hit-testable during the `150ms` exit, because the closed state has no `pointer-events: none`. Neither the prompt nor the checklist covers this, and better-ui does not prescribe it.

Spend: $1.34 (list price).
