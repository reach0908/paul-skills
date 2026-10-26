# Transitions beta trial, 2026-10-26

Status: development evidence for the in-progress `transitions` skill. Machine graders plus one review by the authoring agent; no human review yet. n is 3 per arm, so this supports observations on one task, not a quality claim or promotion.

## Why outside the native suite

`evals/claude-native` stages only the promoted plugin, and its README keeps episodes needing an in-progress skill outside the suite. This trial uses the same runner (`claude plugin eval`) on a plugin staged outside the repository by [stage.py](stage.py):

| Arm | Plugin |
| --- | --- |
| candidate | the promoted plugin plus `skills/in-progress/transitions` (45 skills) |
| no plugin | the runner's `with-without` ablation arm of the candidate stage |
| baseline | the promoted plugin as on this branch (44 skills), so `better-ui` is reachable and `transitions` is not |

`evals/claude-native` is untouched.

## Cases

- [transitions-account-overlays](cases/transitions-account-overlays/) (T-01): a vanilla page where an account dropdown and a toast toggle the `hidden` attribute and pop, and a delete modal uses `transition: all 400ms` with a `display` flip, so it never animates. The project defines `--duration-short` (150ms), `--duration-medium` (250ms) and `--ease-standard`. The prompt asks for open and close transitions on all three.
- [transitions-timing-near-miss](cases/transitions-timing-near-miss/) (T-N): transitions already exist; the prompt asks to polish their durations and easing. That is `better-ui`'s job, so `transitions` must stay unloaded.

Deterministic graders are in each `case.yaml`. The runner seals the workspace, so [replay.py](replay.py) rebuilds each run's final files from the scaffold and the trace's Write and Edit calls. The qualitative checklist was fixed after the probe and before the matrix ran, and its verdicts are in [review.json](review.json):

- Q1: the dropdown grows from the trigger corner (origin plus slight scale).
- Q2: the toast enters from and exits toward its own edge.
- Q3: the modal's exit actually runs (the `display` flip no longer cuts it).
- Q4: under reduced motion, movement is dropped and the opacity fade remains.
- Q5: each of the three closes faster than it opens.

## Settings

Executor `claude-opus-5-5` for every run, Claude Code 2.1.310, `CLAUDE_CODE_EFFORT_LEVEL=medium` in the runner's environment (requested; the trace does not show the effort actually applied). No LLM graders, so judge cost is $0. Tokens are `null`: aggregate schema 1 reports none. Runs used `--runs 3 -j 3 --keep-temp --allow-tools Edit Write` and `--max-cost-usd` ceilings per group (none was hit). Raw per-run data: [record.json](record.json), made by [summarize.py](summarize.py); checklist verdicts: [review.json](review.json).

Two skill revisions ran. `transitionsTree` is the digest `stage.py` prints for `skills/in-progress/transitions`:

| Revision | Commit | `transitionsTree` | Runs |
| --- | --- | --- | --- |
| r1 | `a6e695e` | `sha256:3c8790b3f9be91ecd608eb7dddd13e449ce0f0a3c6c461ddc601d2cfbc357387` | probe, candidate, no-plugin, baseline, near miss |
| r2 | after code review | `sha256:edeed1c035b4af67c4a4e989d798f3ca5545bda6ac9cc978e59a2d435028f93f` | candidate and near miss, repeated |

r2 removed fallback values that contradicted `better-ui`, dropped overshoot, trimmed the pattern list and widened the description's exclusions. The baseline and no-plugin arms do not depend on the skill and were not repeated.

## Results

The probe was one candidate run made before the checklist was fixed; it is reported separately and not pooled.

T-01, deterministic graders (no `transition: all`, a reduced-motion gate, a `transform-origin`, the project's duration tokens, no new dependency):

| Arm | All five pass | `transitions` loaded | `better-ui` loaded | Mean cost | Mean duration |
| --- | --- | --- | --- | --- | --- |
| probe (r1, 1 run) | 1/1 | 1/1 | 1/1 | $0.34 | 55s |
| candidate r1 | 3/3 | 3/3 | 3/3 | $0.34 | 55s |
| candidate r2 | 3/3 | 3/3 | 3/3 | $0.34 | 54s |
| no plugin | 3/3 | n/a | n/a | $0.17 | 45s |
| baseline (promoted plugin) | 0/3, `transform-origin` missing in all | 0/3 | 3/3 | $0.34 | 66s |

T-01, the fixed checklist read from the replayed CSS (`partial`: some of the three surfaces):

| Arm | Q1 origin | Q2 toast edge | Q3 modal exit | Q4 reduced motion | Q5 close faster |
| --- | --- | --- | --- | --- | --- |
| candidate r1 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| candidate r2 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| no plugin | 3/3 | 3/3 | 3/3 | 3/3 | 0/3 (2 partial: dropdown 150ms both ways; 1 fail: everything 250ms both ways) |
| baseline | 0/3 | 0/3 | 3/3 | 3/3 | 3/3 |

T-N near miss: `transitions` stayed unloaded 3/3 on r1 and 3/3 on r2, `better-ui` loaded in all six, and the file was retuned in all six. Mean cost $0.20.

## Reading

- The candidate produced the same structure in all six matrix runs: `@starting-style` with `transition-behavior: allow-discrete` for the hidden and display-flipped elements, origin at the trigger corner, the project's tokens (250ms open, 150ms close), pre-scales `0.97` and `0.96`, and movement gated under `no-preference` with the fade kept.
- The no-plugin arm was also competent on this small task: correct exits, origins and reduced-motion handling. The visible difference is open/close asymmetry (Q5). The machine graders do not separate these two arms, so no improvement over no plugin is claimed beyond that one check.
- With only the promoted plugin, the agent loaded `better-ui` and applied its staged-entrance recipe to all three surfaces: a dropdown below its button rising from 12px below with blur, and a bottom toast exiting upward, away from its edge. T3 and Q1 to Q5 encode this skill's own choreography and were judged by its author, so this is an observation that the outputs differ in the way the skill prescribes, not independent evidence that they are better. It is worth a human look at `better-ui`'s routing for overlays either way.
- The candidate costs about twice the no-plugin arm ($0.34 against $0.17), the same as the baseline.

## Limits

- One task, three runs per arm, one model; the reviewer is the agent that wrote the skill. Q1 to Q5 need human confirmation.
- Nothing was rendered: exits, reversal mid-close and reduced motion are read from CSS, not observed in a browser.
- Only one near-miss boundary (value tuning) was tested. Change reviews (`better-interface`), reduced-motion audits and general styling requests were not run, and neither was a request where no pattern fits (the offer-options branch).
- No Codex run.
- Source parity: the closest source workflow is transitions.dev's own `transitions-dev` skill at the pinned revision, whose overlapping capability is choosing and applying a transition for an element. Under the [quality floor](../design-beta/quality-floor.md) this is **Not compared**: no paired run against it was made.

## Cost

Total paid spend $5.11 against a $10 budget: probe $0.34, candidate with/without $1.54, near miss r1 $0.60, baseline $1.02, candidate r2 $1.01, near miss r2 $0.61. These are the runner's reported costs, not a billed invoice. One r2 launch failed on a shell quoting error before any run started and cost nothing.
