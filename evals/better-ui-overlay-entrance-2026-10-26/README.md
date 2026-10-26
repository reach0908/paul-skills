# better-ui overlay entrance repair, 2026-10-26

Status: development evidence for a local repair of the promoted `better-ui` skill. Machine graders plus one checklist review by the agent that wrote the fix; no human review yet. n is 3 per arm, so this supports observations on two tasks, not a quality claim.

## Failure

In the [transitions beta](https://github.com/reach0908/paul-skills/pull/36) baseline arm (promoted plugin only), the agent loaded `better-ui` for an overlay task and applied its staged-entrance recipe to every surface: a dropdown below its button rose from 12px below with blur, and a bottom toast exited upward, away from its own edge. `transform-origin` was missing in 3/3 runs.

## Harness

Copied from that trial and adapted so it needs no `transitions` skill. [stage.py](stage.py) stages the promoted plugin outside the repository, so the runner is `claude plugin eval` on the same 44 skills in both arms:

| Arm | `better-ui` | `betterUiTree` |
| --- | --- | --- |
| before | as at `e5438096` (origin/main when this branch started) | `sha256:f0c8fc8b023310f4ef87120aa68dd613e132879019ac9eb41eea1e5e527e7f0e` |
| after r1 | the fix as first committed (`61b6d04`) | `sha256:b3564384e0a9f09fe5e08c7b2ce1f60b904eb9cd11f4b847ebdd1264634b3edd` |
| after r2 | the text after code review (`9793470`) | `sha256:52b9895b9050b9349d01066af08d1a8f4348708f8d6f61c22a5774f272ee9d0e` |
| after r3 | this branch as shipped: r2 plus one sentence pointing the overlay recipe at project motion tokens (`90b56bd`) | `sha256:73207f480c73e177460aa50bae984eba8f5c5b94314a99910eedab8ff9b6fbac` |
| ablation skill-only | this branch's `SKILL.md`, base `enter-exit.md` | `sha256:072653fe029e5cd7b80a0f13ce72cf8bef2c02ed43bcc5f6ccec4f86de67d796` |
| ablation reference-only | base `SKILL.md`, this branch's `enter-exit.md` | `sha256:539175c76deb124b6b93c9418c7ce668637dea7f2dd59b48eb1ef24026afef6a` |

Every other promoted skill is byte-identical between arms. The ablations ran once each to locate the cause; they are diagnostic and not pooled. r2 differs from r1 in three sentences only: the overlay principle's lead no longer repeats the surface list, its clause restating the universal reduced-motion gate is gone, and the popover recipe says its placement is assumed rather than given. Because the shipped text changed, both after cases were run again; r1 stays in the record. Each stage's printed digests are in [stages.json](stages.json).

## Cases

- [overlay-open-close](cases/overlay-open-close/) (O-01): the transitions beta's T-01 fixture and prompt, unchanged apart from the scaffold's header comment. An account dropdown and a bottom toast toggle `hidden` and pop; a delete modal uses `transition: all 400ms` with a `display` flip, so it never animates. The prompt asks for open and close transitions on all three.
- [staged-empty-state](cases/staged-empty-state/) (O-N): a near miss where the staged entrance does apply. A first-view empty state (icon, title, description, actions) appears all at once; the prompt asks for a nicer entrance. The fix must leave better-ui's exact staged values in place.

Deterministic graders are in each `case.yaml`; `IND-` graders are indicators (a skill loaded, a reference read) and `C4-` graders confirm the agent never read the eval files. The runner seals the workspace, so [replay.py](replay.py) rebuilds each run's final files from the scaffold and the trace's Write and Edit calls. The checklist in [review.json](review.json) was committed in `45a76ee` at 06:41:29Z, before the first run started at 06:41:35Z (`startedAt` in the record):

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
| after r1 | 3/3 | none | 3/3 | 3/3 | $0.30 | 56s |
| after r2 | 3/3 | none | 3/3 | 3/3 | $0.26 | 47s |

O-01, checklist read from the replayed CSS (`partial`: the direction or origin is only half right):

| Arm | Q1 origin | Q2 toast edge | Q3 modal exit | Q4 reduced motion | Q5 modal from center |
| --- | --- | --- | --- | --- | --- |
| before | 0/3 (1 fail, 2 partial) | 0/3 (3 partial: enters from below, exits up) | 3/3 | 3/3 | 0/3 (3 partial: 12px slide) |
| ablation skill-only | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 |
| ablation reference-only | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 |
| after r1 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| after r2 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |

O-N near miss: the five graders (100ms, `blur(4px)`, `translateY(12px)`, 300ms `ease-out`, reduced-motion gate) pass 3/3 before, 3/3 after r1 and 3/3 after r2, and S1 to S4 pass 9/9. All nine runs produced the same structure: four chunks at 0, 100, 200 and 300ms, hidden state only in the `from` keyframe, movement under `no-preference`. Mean cost $0.17 to $0.18 per run in every arm; mean duration 21s to 23s.

## Reading

- The before outputs match the recipe text. The toast and modal card exit with a fixed upward `-12px` in 3/3 and enter from `12px` below, with `4px` blur in most surfaces; `@starting-style` with `allow-discrete` mirrors the popover recipe in `enter-exit.md`. The dropdown varied: from 12px below in run 1, from above (12px in run 0, 4px in run 2) in the others, never with an origin. `transform-origin` appears nowhere in the base `better-ui` tree.
- After the fix all six runs set `transform-origin: top right` with a `0.96` pre-scale on the dropdown, slide the toast from and back toward the bottom, and scale the modal card from center.
- Either half of the fix alone also passed once. With n=1 that does not show either half is sufficient; the shipped fix keeps both, so neither file contradicts the other.
- The toast offset is not prescribed: after runs used `16px` three times, `12px` once and `calc(100% + 24px)` twice.
- The near miss is at ceiling in both arms, so it shows no regression in this case and cannot show an improvement.
- Q1 to Q5 encode the fix's own rule and were judged by its author, so they show the outputs changed the way the new text prescribes, not independent evidence that the outputs are better. The no-plugin arm of the transitions beta already got Q1 and Q2 right 3/3.

## Quality floor

Under the [quality floor](../design-beta/quality-floor.md), against Jakub's original `better-ui` at the pinned `d574cc8`: **Not compared**. No paired run against the original was made. The staged-entrance outcome the original defines is kept in this case (O-N, 3/3 before and 6/6 after); other original outcomes were not re-run.

## Limits

- Two tasks, n=3 per arm (12 after runs per task across r1, r2, the r2 rerun and r3), one model, one host; the reviewer wrote the fix. The checklist needs human confirmation.
- Nothing was rendered: directions, exits and reduced motion are read from CSS, not watched in a browser.
- Only a bottom toast and a below-right dropdown were tested. Flipped placements, tooltips, drawers, sheets, React or Motion projects, review tasks (`better-interface` handoff) and Codex were not run.
- The `0.96` pre-scale in the recipe reuses better-ui's press value; no trial compared other values, and Q1 asks for a slight scale, so it partly grades the recipe's own choice.
- The `[popover]` recipe, like the base one, gates nothing behind reduced motion itself; the skill's reduced-motion principle covers it.

## Second after-r2 run

The first traces were not kept, so after r2 ran again on both cases with outputs saved in [outputs/after-r2b](outputs/after-r2b/README.md). A blind re-grade passes the checklist in 27/27 run items. Overlay run 2 fails T4 (hardcoded `300ms` and `150ms` instead of the project tokens), so the mechanical graders pass 5/6. Spend $1.39.

## after r3

r3 adds one sentence to the popover recipe: the project's duration and easing tokens apply where it has them, and the recipe's `150ms`, `300ms` and `ease-out` are fallbacks. Both cases ran again with outputs in [outputs/after-r3](outputs/after-r3/README.md). Mechanical graders pass 6/6 (O-01 3/3 including T4, O-N 3/3), and a blind re-grade by a fresh session passes the checklist in 27/27 run items. Spend $1.34.

## Cost

Total paid spend $7.49: $4.76 against the first $8 budget, then $1.39 for after-r2b and $1.34 for after r3, each under its own cap. The first $4.76 splits as before O-01 $0.94, ablations $0.56, after r1 O-01 $0.91, before O-N $0.52, after r1 O-N $0.53, after r2 O-01 $0.78, after r2 O-N $0.52. These are the runner's list-price figures, not a billed invoice.
