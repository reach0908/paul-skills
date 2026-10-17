# Pilot 4: new cases, 2026-10-17

Status: unreviewed machine verdicts. Opus 5.5 executor and judge, three runs per arm. Both cases' LLM graders were calibrated first: Opus and the Codex cross-judge agreed with every expectation (27 of 27 and 72 of 72 per judge).

| Case | With plugin | Without plugin | Reading |
| --- | --- | --- | --- |
| `build-design-same-name-card` (B-02) | 2/3 machine pass; one run claimed a rendered comparison | 3/3 machine pass | `build-design` was never loaded; the base model resolves the same-name trap on its own |
| `code-review-merge-readiness` (K-01) | 0/3: base, head and merge-base SHAs not reported | 0/3 | `code-review` was never loaded and no review subagents ran, although every run found both planted defects, the README conflict and the right verdict |

Both cases point at invocation rather than execution: the skill descriptions do not name these requests. `code-review` lists branch, PR and "since X" reviews but not "can this merge"; `build-design` lists implementing a supplied design while its body also covers reusing existing UI. Changing a description changes routing across the library, so it is a separate decision.
