## What it does

Polishes surfaces, icons and motion after the underlying interaction works. It respects the project’s component library, tokens and density, and never ranks decorative polish above a blocked interaction.

## When to reach for it

Type `/better-ui`, or the [agent](https://www.aihero.dev/ai-coding-dictionary/agent) reaches for it automatically for radius, shadows, icon states, optical alignment and animation. Use [better-layout](https://github.com/reach0908/paul-skills/blob/main/docs/design/better-layout.md) for structure and [better-accessibility](https://github.com/reach0908/paul-skills/blob/main/docs/design/better-accessibility.md) for keyboard behavior and reduced-motion requirements.

## Motion follows state

Interactive transitions should survive interruption and reversal. Selected-state styling should not shift the control or its neighbors. High-frequency actions, reduced-motion preferences, first render and theme changes need deliberate treatment rather than a universal animation.

The staged entrance (chunks rising and unblurring in sequence) is for page and section content such as a hero, an empty state or onboarding. Overlays move from their _anchor_ instead:

| Overlay | Motion |
| --- | --- |
| Dropdown, popover, menu, tooltip | Grows from the edge facing its trigger |
| Toast, drawer, sheet | Enters from its screen edge and leaves back toward it |
| Centered modal or dialog | Scales from its center while the backdrop fades |

## Common questions

**What if I mention this domain while reviewing staged changes?**

The automatic catalog makes the change-review route take priority over the domain words, before this domain document is loaded. [better-interface](https://github.com/reach0908/paul-skills/blob/main/docs/design/better-interface.md) first supplies the explicit change-review command. This domain resumes after the authorized handoff; ordinary screen audits and requested fixes still enter it directly.

**Will it add animation everywhere?**

No. Some frequent interactions should have none. The project’s motion language remains the starting point, and a consistent visual choice is not automatically a defect.

**Will my dropdowns and toasts get the page entrance animation?**

No. Through 0.4.6 they could: in trials, a dropdown slid in with no origin at its button and a bottom toast left upward, away from its edge. Overlays now take their direction from the trigger or screen edge they belong to, and the staged entrance stays on page and section content.

**Is a screenshot enough to approve an animation?**

It can show a state, but timing, reversal and intermediate behavior need runtime observations. The report keeps those limits visible.

## It's working if

- Interaction defects are prioritized before decorative changes.
- State changes preserve geometry where movement is unintended.
- Motion checks include the relevant reversal, reduced-motion and theme states.
- A dropdown opens out of its trigger and a toast leaves toward the edge it came from.

## Where it fits

A focused polish role composed by [better-interface](https://github.com/reach0908/paul-skills/blob/main/docs/design/better-interface.md). [design-browser](https://github.com/reach0908/paul-skills/blob/main/docs/design/design-browser.md) observes the states and transitions; [ask-matt](https://github.com/reach0908/paul-skills/blob/main/docs/engineering/ask-matt.md) situates the review in the wider flow.
