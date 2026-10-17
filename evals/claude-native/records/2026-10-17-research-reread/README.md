# Research read-back fix, 2026-10-17

Status: unreviewed machine verdicts. The comparison uses the same case files, criteria and Opus 5.5 executor and judge as [pilot 3](../2026-10-17-pilot3/README.md); only `skills/engineering/research/SKILL.md` step 4 changed.

Pilot 3 found that no research run read its saved file back after writing it (0/12 with the plugin), although step 4 asked for it in the middle of a paragraph and, unlike steps 1 to 3, the step had no completion criterion. The fix names the read-back in the step title and adds a completion criterion: done when the read-back made after the final write shows every scoped question answered or marked unresolved.

| Case | Read-back with the plugin, before | After | Without the plugin (control) |
| --- | --- | --- | --- |
| `research-atlas-v2` | 0/3 | 3/3 | 0/3 |
| `research-same-name-tools` | 0/3 | 3/3 | 0/3 |
| `research-requirement-conflict` | 0/3 | 3/3 | 0/3 |
| `research-unreadable-evidence` | 0/3 | 2/3 | 0/3 |

With the plugin, `research-atlas-v2` and `research-same-name-tools` now pass every machine-judged criterion in all runs and wait for human review. `research-requirement-conflict` still fails R2 in all runs under the criteria text of pilot 3, which did not yet exempt statements labelled as inference; the evaluation branch has since revised that text. `research-unreadable-evidence` failed R2 file citations in two runs.

This is one development case set with three runs per arm: evidence that the instruction change moves the observed behavior here, not a general rate.
