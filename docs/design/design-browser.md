## What it does

Runs a bounded browser scenario and returns observable evidence. The calling reviewer owns the criteria and verdict; a browser summary by itself is not a pass. A whole-page request covers the full page even when its URL includes an anchor.

## When to reach for it

Type `/design-browser`, or the [agent](https://www.aihero.dev/ai-coding-dictionary/agent) reaches for it automatically when interface work needs browser observations.

| Purpose | Default tool |
| --- | --- |
| Research, references and general browsing | Aside |
| Interaction QA, responsive checks, performance and design comparison | Playwright CLI |
| Other browser work without a specified route | Playwright CLI |

An explicit tool choice takes precedence. Source analysis can stay with the responsible reviewer when it already answers the question.

## Prerequisites

The selected CLI must be available, and the target needs an accessible URL or local preview. The [skill](https://www.aihero.dev/ai-coding-dictionary/skill) checks installed help and project instructions; a missing tool is reported rather than silently replaced.

## Evidence answers the question

Capture the requested items, states, widths and interactions with expected counts, completed counts and raw observations. Keyboard checks begin through natural entry. Overflow needs an assertion, not just a number in a log. Performance results name what was measured and how many samples support it.

## Common questions

**Do we need Figma?**

No. Local images, Markdown, browser prototypes and product code can supply the reference. The comparison records which local artifact and states it used.

**Does a screenshot prove the flow works?**

It proves an observed visual state. Flow completion requires the requested interactions, state changes and counts, with failures preserved. Tool efficiency claims need a separate controlled comparison.

## It's working if

- Artifacts identify the route, state, viewport and interaction.
- Expected and completed counts agree, or omissions are reported.
- Only task-owned browser resources are closed; existing user sessions remain available.

## Where it fits

A shared evidence provider for [better-interface](https://github.com/reach0908/paul-skills/blob/main/docs/design/better-interface.md) and focused domain reviews. [research](https://github.com/reach0908/paul-skills/blob/main/docs/engineering/research.md) handles a broader source investigation. Use [ask-matt](https://github.com/reach0908/paul-skills/blob/main/docs/engineering/ask-matt.md) to select the work that needs these observations.
