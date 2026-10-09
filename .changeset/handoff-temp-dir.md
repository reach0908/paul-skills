---
"paul-skills": patch
---

`handoff` now names where the OS temp directory is (`$TMPDIR`, else `/tmp`; `%TEMP%` on Windows), so agents stop guessing ([mattpocock/skills#272](https://github.com/mattpocock/skills/issues/272)).
