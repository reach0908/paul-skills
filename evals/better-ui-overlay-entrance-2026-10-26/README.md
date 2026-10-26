# better-ui overlay entrance repair, 2026-10-26

Status: development evidence for a local repair of the promoted `better-ui` skill. Machine graders plus one checklist review by the agent that wrote the fix; no human review yet. n is 3 per arm, so this supports observations on two tasks, not a quality claim.

## Failure

In the [transitions beta](https://github.com/reach0908/paul-skills/pull/36) baseline arm (promoted plugin only), the agent loaded `better-ui` for an overlay task and applied its staged-entrance recipe to every surface: a dropdown below its button rose from 12px below with blur, and a bottom toast exited upward, away from its own edge. `transform-origin` was missing in 3/3 runs.

## Harness

Copied from that trial and adapted so it needs no `transitions` skill. [stage.py](stage.py) stages the promoted plugin outside the repository, so the runner is `claude plugin eval` on the same 44 skills in both arms:

| Arm | `better-ui` | `betterUiTree` |
| --- | --- | --- |
| before | as at `e5438096` (origin/main when this branch started) | `sha256:f0c8fc8b023310f4ef87120aa68dd613e132879019ac9eb41eea1e5e527e7f0e` |
| after | this branch | `sha256:b3564384e0a9f09fe5e08c7b2ce1f60b904eb9cd11f4b847ebdd1264634b3edd` |
| ablation skill-only | this branch's `SKILL.md`, base `enter-exit.md` | `sha256:072653fe029e5cd7b80a0f13ce72cf8bef2c02ed43bcc5f6ccec4f86de67d796` |
| ablation reference-only | base `SKILL.md`, this branch's `enter-exit.md` | `sha256:539175c76deb124b6b93c9418c7ce668637dea7f2dd59b48eb1ef24026afef6a` |

Every other promoted skill is byte-identical between arms. The ablations ran once each to locate the cause; they are diagnostic and not pooled.

## Cases

- [overlay-open-close](cases/overlay-open-close/) (O-01): the transitions beta's T-01 fixture and prompt unchanged. An account dropdown and a bottom toast toggle `hidden` and pop; a delete modal uses `transition: all 400ms` with a `display` flip, so it never animates. The prompt asks for open and close transitions on all three.
- [staged-empty-state](cases/staged-empty-state/) (O-N): a near miss where the staged entrance does apply. A first-view empty state (icon, title, description, actions) appears all at once; the prompt asks for a nicer entrance. The fix must leave better-ui's exact staged values in place.

Deterministic graders are in each `case.yaml`. The runner seals the workspace, so [replay.py](replay.py) rebuilds each run's final files from the scaffold and the trace's Write and Edit calls. The checklist in [review.json](review.json) was committed (`45a76ee`) before any run:

- Q1 the dropdown grows from its trigger; Q2 the toast enters from and exits toward its own edge; Q3 the modal exit actually runs; Q4 reduced motion keeps only the opacity fade; Q5 the centered modal card scales from center or only fades.
- S1 chunks staggered 100ms apart; S2 opacity, 4px blur, 12px translateY over 300ms ease-out; S3 reduced-motion gate with nothing left invisible; S4 no overlay rule misapplied.

## Settings

Executor `claude-opus-5-5` for every run (the trace's `modelUsage` confirms it), Claude Code 2.1.310, `CLAUDE_CODE_EFFORT_LEVEL=medium` in the runner's environment (requested; the trace does not show the effort actually applied). Flags: `--ablation none --scaffold --keep-temp --allow-tools Edit Write --runs 3 -j 3` with a `--max-cost-usd` ceiling per group (none was hit). No LLM graders, so judge cost is $0. Tokens come from each trace's `result` event; costs are the runner's list-price figures (`costBasis: list`), not a billed invoice. Raw per-run data: [record.json](record.json), made by [summarize.py](summarize.py).

## Results

O-01, deterministic graders (T1 no `transition: all`, T2 reduced-motion gate, T3 `transform-origin`, T4 project duration tokens, T5 no new dependency):

| Arm | All pass | Failing | `better-ui` loaded | `enter-exit.md` read | Mean cost | Mean duration |
| --- | --- | --- | --- | --- | --- | --- |
| before | 0/3 | T3 in 3/3 | 3/3 | 3/3 | $0.31 | 56s |
| ablation skill-only | 1/1 | none | 1/1 | 1/1 | $0.28 | 58s |
| ablation reference-only | 1/1 | none | 1/1 | 1/1 | $0.28 | 45s |
| after | 3/3 | none | 3/3 | 3/3 | $0.30 | 56s |

O-01, checklist read from the replayed CSS (`partial`: the direction or origin is only half right):

| Arm | Q1 origin | Q2 toast edge | Q3 modal exit | Q4 reduced motion | Q5 modal from center |
| --- | --- | --- | --- | --- | --- |
| before | 0/3 (1 fail, 2 partial) | 0/3 (3 partial: enters from below, exits up) | 3/3 | 3/3 | 0/3 (3 partial: 12px slide) |
| ablation skill-only | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 |
| ablation reference-only | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 |
| after | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |

O-N near miss: the five graders (100ms, `blur(4px)`, `translateY(12px)`, 300ms `ease-out`, reduced-motion gate) pass 3/3 before and 3/3 after, and S1 to S4 pass 6/6. All six runs produced the same structure: four chunks at 0, 100, 200 and 300ms, hidden state only in the `from` keyframe, movement under `no-preference`. Mean cost $0.17 before, $0.18 after; mean duration 23s both.

## Reading

- The before outputs match the recipe text: a fixed `-12px` exit on every surface, `12px` with `4px` blur on enter, and `@starting-style` with `allow-discrete` taken from the popover recipe in `enter-exit.md`. `transform-origin` appears nowhere in the base `better-ui` tree.
- After the fix all three runs set `transform-origin: top right` with a `0.96` pre-scale on the dropdown, slide the toast from and back toward the bottom, and scale the modal card from center.
- Either half of the fix alone also passed once. With n=1 that does not show either half is sufficient; the shipped fix keeps both, so neither file contradicts the other.
- The toast offset is not prescribed: after runs used `16px` twice and `calc(100% + 24px)` once.
- The near miss is at ceiling in both arms, so it shows no regression in this case and cannot show an improvement.
- Q1 to Q5 encode the fix's own rule and were judged by its author, so they show the outputs changed the way the new text prescribes, not independent evidence that the outputs are better. The no-plugin arm of the transitions beta already got Q1 and Q2 right 3/3.

## Quality floor

Under the [quality floor](../design-beta/quality-floor.md), against Jakub's original `better-ui` at the pinned `d574cc8`: **Not compared**. No paired run against the original was made. The staged-entrance outcome the original defines is kept in this case (O-N, 3/3 before and after); other original outcomes were not re-run.

## Limits

- Two tasks, n=3 per arm, one model, one host; the reviewer wrote the fix. The checklist needs human confirmation.
- Nothing was rendered: directions, exits and reduced motion are read from CSS, not watched in a browser.
- Only a bottom toast and a below-right dropdown were tested. Flipped placements, tooltips, drawers, sheets, React or Motion projects, review tasks (`better-interface` handoff) and Codex were not run.
- The `0.96` pre-scale in the recipe reuses better-ui's press value; no trial compared other values.

## Cost

Total paid spend $3.46 against an $8 budget: before O-01 $0.94, ablations $0.56, after O-01 $0.91, before O-N $0.52, after O-N $0.53. These are the runner's list-price figures, not a billed invoice.
