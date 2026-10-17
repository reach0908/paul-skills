# Invocation descriptions, 2026-10-17

Status: unreviewed machine verdicts. Opus 5.5 executor and judge, three runs, with the plugin only (`--ablation none`). "Before" for the positive cases comes from the pilot 3 and pilot 4 traces, re-graded with the B5 and K5 trace checks.

| Case | Before | After |
| --- | --- | --- |
| `build-design-same-name-card`: build-design loaded | 0/3 | 3/3, all machine criteria pass |
| `build-design-scoped-card`: build-design loaded | 3/3 | 2/3 (request unchanged by the edit) |
| `code-review-merge-readiness`: code-review loaded | 0/3 | 3/3 |
| `build-design-near-miss` and `code-review-near-miss`: skill stays unloaded | 6/6 | 6/6 |

The description change alone routed merge questions to `code-review`, but the skill had no merge step: with it loaded, the README conflict was reported in 1 of 3 runs, against 3 of 3 without the skill (`record-after-code-review-description-only.json`). Adding step 6, Answer a merge question, gave:

| `code-review-merge-readiness` | No skill (pilot 4) | Description only | Description and Merge step |
| --- | --- | --- | --- |
| K1 target, head and merge-base SHAs reported | 0/3 | 0/3 | 3/3 |
| K3 conflict reported | 3/3 | 1/3 | 2/3 |
| K2 Standards and Spec kept apart | 3/3 | 3/3 | 2/3 |

The remaining K3 failure ran into a refused `git merge-tree` call and reported the conflict as unverified; the K2 failure used Korean section titles instead of `## Standards` and `## Spec` and left out the Merge section. In all three runs the agent reviewed the small diff itself instead of starting the two review sub-agents.
