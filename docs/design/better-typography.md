## What it does

Sets and reviews type scale, spacing, font behavior, wrapping, truncation, punctuation and text selection. It distinguishes measurable rendering failures from stylistic choices and writes fixes in the project’s own styling system.

## When to reach for it

Type `/better-typography`, or the [agent](https://www.aihero.dev/ai-coding-dictionary/agent) reaches for it automatically when text rendering needs work. Use [better-writing](https://github.com/reach0908/paul-skills/blob/main/docs/design/better-writing.md) to change the words and [better-colors](https://github.com/reach0908/paul-skills/blob/main/docs/design/better-colors.md) to measure their contrast.

## Truncate with a way back

Useful text remains readable, selectable and recoverable. Font fallback, user text-size preferences, Korean line breaking and mobile input sizing matter alongside the visible type scale. Source declarations alone do not prove the face that actually rendered.

## Common questions

**Does this require replacing our font or type scale?**

No. It reuses the project system and asks for a change when a supported rendering or readability problem needs one.

**Can it verify Korean wrapping from source alone?**

It can inspect language and CSS choices. Actual wrapping and font fallback require rendered evidence and remain unverified until observed.

## It's working if

- Truncated content has a usable route to its full value.
- Requested text resizing, narrow widths and font fallbacks have evidence or named limits.
- Typography findings stay separate from copy and color findings.

## Where it fits

A standalone text-rendering review within [better-interface](https://github.com/reach0908/paul-skills/blob/main/docs/design/better-interface.md). Use [design-browser](https://github.com/reach0908/paul-skills/blob/main/docs/design/design-browser.md) for the requested rendered states, and [ask-matt](https://github.com/reach0908/paul-skills/blob/main/docs/engineering/ask-matt.md) for the wider workflow.
