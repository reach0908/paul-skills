---
"paul-skills": patch
---

Add a Claude native evaluation suite for `claude plugin eval`. Thirteen development cases cover `research`, `interface-review`, `user-flow`, `build-design`, `better-interface`, `diagnosing-bugs` and `code-review`; nine reproduce behavior observed in recent real Claude Code and Codex sessions with synthetic fixtures. A rubric and per-case profiles map every grader to a criterion, required criteria gate each run instead of the weighted native score, unjudged graders stay unknown and errored runs are excluded. The tooling stages a small plugin copy for each run, records the exact command, adds static, regex and `input_match` controls to `npm test`, offers a zero-cost plan check, and calibrates LLM judges against labelled artifacts, including a Codex cross-judge. Opus 5.5 was chosen as the native judge after calibration rounds in which Sonnet and Haiku passed a known-bad artifact. Expected verdicts remain AI drafts pending human confirmation.
