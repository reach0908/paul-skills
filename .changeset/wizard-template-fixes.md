---
"paul-skills": patch
---

`wizard` template fixes: `ask` uses Readline so arrow keys move the cursor ([mattpocock/skills#741](https://github.com/mattpocock/skills/issues/741)); `write_env` single-quotes values so spaces, `#`, `$` and quotes survive `source` and dotenv ([mattpocock/skills#770](https://github.com/mattpocock/skills/issues/770)); `open_url` prints the open-it-yourself warning when no browser opener exists ([mattpocock/skills#774](https://github.com/mattpocock/skills/issues/774)); `write_env` writes through a symlinked `.env` and keeps an existing file's mode ([mattpocock/skills#811](https://github.com/mattpocock/skills/issues/811)); `ask` and `ask_secret` fail at EOF instead of looping ([mattpocock/skills#852](https://github.com/mattpocock/skills/issues/852)).
