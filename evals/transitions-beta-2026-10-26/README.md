# Transitions beta trial, 2026-10-26

Status: development evidence for the in-progress `transitions` skill. Machine graders plus one review by the authoring agent; no human review yet. n is 3 per arm (4 for the candidate counting the probe), so this supports observations on one task, not a quality claim or promotion.

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

Deterministic graders are in each `case.yaml`. The runner seals the workspace, so [replay.py](replay.py) rebuilds each run's final files from the scaffold and the trace's Write and Edit calls. The qualitative checklist was fixed after the probe and before the matrix ran:

- Q1: the dropdown grows from the trigger corner (origin plus slight scale).
- Q2: the toast enters from and exits toward its own edge.
- Q3: the modal's exit actually runs (the `display` flip no longer cuts it).
- Q4: under reduced motion, movement is dropped and the opacity fade remains.
- Q5: each of the three closes faster than it opens.

## Settings

Executor `claude-opus-5-5` for every run, Claude Code 2.1.310, `CLAUDE_CODE_EFFORT_LEVEL=medium` in the runner's environment (requested; the trace does not show the effort actually applied). No LLM graders, so judge cost is $0. Tokens are `null`: aggregate schema 1 reports none. Runs used `--runs 3 -j 3 --keep-temp --allow-tools Edit Write` and `--max-cost-usd` ceilings per group (none was hit). Skill tree digest of the candidate as staged: `sha256:3c8790b3f9be91ecd608eb7dddd13e449ce0f0a3c6c461ddc601d2cfbc357387` (from `stage.py`). Raw per-run data: [record.json](record.json), made by [summarize.py](summarize.py).

## Results

T-01, deterministic graders (no `transition: all`, a reduced-motion gate, a `transform-origin`, the project's duration tokens, no new dependency):

| Arm | All five pass | `transitions` loaded | `better-ui` loaded | Mean cost | Mean duration |
| --- | --- | --- | --- | --- | --- |
| candidate (probe + 3) | 4/4 | 4/4 | 4/4 | $0.34 | 55s |
| no plugin | 3/3 | n/a | n/a | $0.17 | 45s |
| baseline (`better-ui` only) | 0/3, `transform-origin` missing in all | 0/3 | 3/3 | $0.34 | 66s |

T-01, the fixed checklist read from the replayed CSS:

| Arm | Q1 origin | Q2 toast edge | Q3 modal exit | Q4 reduced motion | Q5 close faster |
| --- | --- | --- | --- | --- | --- |
| candidate | 4/4 | 4/4 | 4/4 | 4/4 | 4/4 |
| no plugin | 3/3 | 3/3 | 3/3 | 3/3 | 0/3 (runs 0 and 1 kept the dropdown at 150ms both ways; run 2 used 250ms for everything) |
| baseline | 0/3 | 0/3 | 3/3 | 3/3 | 3/3 |

T-N near miss, candidate stage: `transitions` stayed unloaded 3/3, `better-ui` loaded 3/3, the file was retuned 3/3, mean cost $0.20.

## Reading

- The candidate produced the intended choreography in every run: `@starting-style` with `transition-behavior: allow-discrete` for the hidden and display-flipped elements, origin at the trigger corner, the project's tokens (250ms open, 150ms close), the fallback pre-scales `0.97` and `0.96`, and movement gated under `no-preference` with the fade kept.
- The no-plugin arm was also competent on this small task: correct exits, origins and reduced-motion handling. The visible difference is open/close asymmetry (Q5) and that the candidate reports value sources. The machine graders do not separate these two arms, so no improvement over no plugin is claimed beyond Q5.
- The baseline arm is the notable result. With only the promoted plugin, the agent loaded `better-ui` and applied its staged-entrance recipe to all three surfaces: a dropdown below its button rising from 12px below with blur, and a bottom toast exiting upward, away from its edge. Here `better-ui` alone did worse than no plugin on choreography; the `transitions` skill, which picks a pattern before `better-ui` supplies values, corrected it in this case.
- The candidate costs about twice the no-plugin arm ($0.34 against $0.17), the same as the baseline.

## Limits

- One task, three runs per arm, one model; the reviewer is the agent that wrote the skill. Q1 to Q5 need human confirmation.
- Nothing was rendered: exits, reversal mid-close and reduced motion are read from CSS, not observed in a browser.
- Only one near-miss boundary (value tuning) was tested. Change reviews (`better-interface`), reduced-motion audits and general "make it pretty" requests were not run, and neither was a request where no pattern fits (the offer-options branch).
- No Codex run. No source-parity run against transitions.dev's own skill; source parity is not applicable to an original with influences, and its license is why no snippet was copied.

## Cost

Total paid spend $3.49 against a $10 budget: probe $0.34, candidate with/without $1.54, near miss $0.60, baseline $1.02. These are the runner's reported costs, not a billed invoice.
