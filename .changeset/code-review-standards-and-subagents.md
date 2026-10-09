---
"paul-skills": patch
---

`code-review` now searches the repo for standards files and always hands `CODING_STANDARDS.md` / `CONTRIBUTING.md` to the Standards sub-agent ([mattpocock/skills#1065](https://github.com/mattpocock/skills/issues/1065)), runs both sub-agents in the foreground and uses their returned reports ([mattpocock/skills#1073](https://github.com/mattpocock/skills/issues/1073)), and resolves the issue tracker through the provided tracker doc instead of a hard-coded path ([mattpocock/skills#937](https://github.com/mattpocock/skills/issues/937)).
