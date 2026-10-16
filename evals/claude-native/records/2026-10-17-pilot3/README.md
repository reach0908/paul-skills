# Pilot 3, 2026-10-17

Status: unreviewed. Machine verdicts only; every `pending_human` criterion and all quality judgements still need a maintainer. Expected verdicts are AI drafts the user accepted without itemized review.

Each case ran three times with Claude Opus 5.5 as the executor and the native judge, launched through `tools/native_eval.py run` (the launch files record the exact command and stage digest). Raw aggregates and copied traces stay in the ignored `results/` directory on the maintainer's machine.

| Case | With plugin | Without plugin | Reading |
| --- | --- | --- | --- |
| `research-*` (4 cases) | Re-read after save 0/12 | 0/12 | The research skill's step 4 ("read the file before reporting success") is not followed |
| `research-*` citations and sections | Mostly pass; R-03 citations failed 2/3 | R2 and R5 sections fail 3/3 per case | The skill adds owner citations and the required sections |
| `user-flow-export-panel` | Machine criteria 3/3 | U2, U5 and U7 fail 3/3 | The skill adds the transition contract and handoff |
| `better-interface-settings-audit` | 2/3; one run claimed a rendered check | 3/3 fail | Added value; one unverified-claim regression to watch |
| `diagnosing-bugs-scroll-reset` | Test-first loop 3/3 | Source changed before a test 2/3 | The skill enforces the red-capable loop |
| `interface-review-*` (3 cases) | Machine criteria 9/9 | n/a | Human review of I1, I5, I6 and C2 remains |
| `build-design-scoped-card` | 3/3 | 3/3 | The case does not separate the arms; it needs a harder trap |

Grader defects found by the earlier pilots and fixed before this one: `tool_used` `min` defaulting to 1 under `max: 0`, Edit grants also allowing Write, `input_match` matching file contents, R2 demanding a section where the skill cites lines, U2 rejecting undecided and not-offered rows, and an R-04 fixture whose unreadable file was invisible to the agent.
