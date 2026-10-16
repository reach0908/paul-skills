---
"paul-skills": patch
---

Add `check:local` and `test:graders` commands to run the existing routing and source-read grader controls on a maintainer's machine. The full local command includes the current package checks and a whitespace check, while the GitHub Actions validation command stays unchanged. These deterministic controls do not launch model trials or establish skill quality.
