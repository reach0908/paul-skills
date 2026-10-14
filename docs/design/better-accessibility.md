## What it does

Reviews and fixes semantics, accessible names, keyboard and focus behavior, forms, announcements, motion preferences and zoom. A failure cites a WCAG 2.2 criterion or a concrete task an assistive-technology user cannot complete. Conventions and optional improvements are labeled as recommendations.

## When to reach for it

Type `/better-accessibility`, or the [agent](https://www.aihero.dev/ai-coding-dictionary/agent) reaches for it automatically when these concerns fit. Use [better-colors](https://github.com/reach0908/paul-skills/blob/main/docs/design/better-colors.md) for measured color pairs and [better-writing](https://github.com/reach0908/paul-skills/blob/main/docs/design/better-writing.md) for label and error wording.

## Native elements first

The platform supplies useful behavior through real buttons, links and form controls. The [skill](https://www.aihero.dev/ai-coding-dictionary/skill) prefers restoring that behavior to rebuilding it with ARIA. A complete keyboard check includes natural entry, every requested item and state, activation, closing and focus restoration.

## Common questions

**Is one successful keyboard example enough?**

Only for a scope containing that one example. A repeated collection needs the requested items and viewports accounted for, with expected and completed counts.

**Does a source review certify screen-reader behavior?**

No. It can identify source defects, but unperformed keyboard, screen-reader and device checks remain explicitly unverified.

## It's working if

- The report names the blocked task or applicable criterion.
- Keyboard evidence shows where focus starts, how controls are reached and where it returns.
- Recommendations are kept distinct from conformance failures.

## Where it fits

A standalone domain review, also used by [better-interface](https://github.com/reach0908/paul-skills/blob/main/docs/design/better-interface.md). [design-browser](https://github.com/reach0908/paul-skills/blob/main/docs/design/design-browser.md) collects runtime evidence. [ask-matt](https://github.com/reach0908/paul-skills/blob/main/docs/engineering/ask-matt.md) helps select the appropriate scope.
