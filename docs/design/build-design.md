## What it does

Implement an approved design using the project's existing tokens and components, then compare the rendered result with that reference. A visual match must preserve working states and accessibility.

## When to reach for it

Type `/build-design`, or the agent reaches for it automatically when a task fits.

Use it when the chosen local prototype, Markdown screen specification or design image already supplies the intended result. Exploring alternatives belongs to a separate decision.

## Prerequisites

A writable local project or prototype workspace. Existing-component work needs that component and its data boundary; browser verification needs a working local browser tool.

## Common questions

**Why did it reuse the wrong card even though the build passed?**

Names and appearance can match several components. Before editing, it maps the reference screen and section to the actual export, target location and behavior. Reuse is then checked through that export, link destination and keyboard action, alongside matching-state captures.

**Is Figma required, and can it invent missing design values?**

Figma is optional for local browser, Markdown and image inputs. Specified values, browser-computed values and image estimates stay distinct. Unspecified choices and meaningful token rounding are recorded as defaults, assumptions or deviations.

## It's working if

- Each scoped screen and state has a reference locator and a comparison result.
- The source component and target call site are named before reuse; existing decisions resolve ambiguity without another approval round.
- Existing tokens and components are reused, and meaningful deviations are visible.
- Loading, error, empty and keyboard behavior survive even when the visual reference omits them.

## Where it fits

It follows an approved [wireframe](https://github.com/reach0908/paul-skills/blob/main/docs/design/wireframe.md) or another supplied design. [design-browser](https://github.com/reach0908/paul-skills/blob/main/docs/design/design-browser.md) collects rendered evidence; an explicit [interface-review](https://github.com/reach0908/paul-skills/blob/main/docs/design/interface-review.md) request reviews the resulting change. See [ask-matt](https://github.com/reach0908/paul-skills/blob/main/docs/engineering/ask-matt.md) for the full routing map.
