# after r2, second run with kept outputs (after-r2b)

Ran 2026-10-26 from 16:12 KST (07:12Z) on this branch after merging origin/main at `419a92b` (PR #36). `stage.py after` reproduced the r2 digests byte-for-byte (`stageDigest` `sha256:207153da...`, `betterUiTree` `sha256:52b9895b...`). Same runner flags as the README's Settings, `--max-cost-usd 1.6` per case. Executor `claude-opus-5-5`, Claude Code 2.1.310, `CLAUDE_CODE_EFFORT_LEVEL=medium`.

The first r1 and r2 traces were deleted during cleanup, so nobody could check their checklist verdicts again. This run keeps everything:

- `<case>/run<n>/final/`: each run's final files, rebuilt by [replay.py](../../replay.py) from the scaffold and the trace. No edit failed to apply.
- `<case>/run<n>/trace.jsonl`, `<case>/aggregate-result.json`, `<case>/runner.log`: raw runner output, unedited.
- [record.json](record.json): made by [summarize.py](../../summarize.py).
- [blind-grades.json](blind-grades.json): the blind checklist grades.

## Mechanical graders

| Case | All pass | Failing | Cost |
| --- | --- | --- | --- |
| overlay-open-close | 2/3 | T4-project-duration-tokens in run 2 | $0.86 |
| staged-empty-state | 3/3 | none | $0.53 |

Run 2 of overlay-open-close hardcodes `300ms` and `150ms` with `ease-out` instead of the project's `--duration-short` (150ms), `--duration-medium` (250ms) and `--ease-standard`. Those are better-ui's own values. The first r2 runs passed T4 in 3/3.

## Blind checklist re-grade

A fresh Claude Code session (Opus 5.5, `--model opus --effort medium`, brief starting with `/paul-skills:code-review`) graded the checklist from `review.json` without the verdicts or this record. It saw each case's prompt, the original files and the final files, in a folder outside the repository. The session reported that it graded the runs directly against the checklist and did not run code-review's git-diff process.

- overlay-open-close Q1 to Q5: pass in 3/3 runs (15/15).
- staged-empty-state S1 to S4: pass in 3/3 runs (12/12).
- The session also flagged run 2's hardcoded durations and easing on its own list of defects outside the checklist. That matches the T4 failure. The brief named hardcoded durations as an example of such a defect.

The checklist agrees with the first r2 review, but one mechanical grader fails, so this run does not pass as a whole. Spend: $1.39 (list price).
