---
"paul-skills": patch
---

`diagnosing-bugs` Phase 5 now has the agent `diff` a forced mutation against a pristine copy before trusting the red, so an edit that silently changed nothing can't pass as a failing test ([mattpocock/skills#955](https://github.com/mattpocock/skills/issues/955)).
