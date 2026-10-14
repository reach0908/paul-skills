## What it does

Render one real component under plausible hostile content and mark what visibly breaks on a temporary page. The run builds the scenarios, looks once and reports observations without fixing the component.

## When to reach for it

You invoke this by typing `/break`; the agent will not reach for it on its own.

Use it for a quick stress check of content, containers and supported states. A full standards review or performance investigation needs a different scope.

## Prerequisites

A writable local project or prototype workspace. Existing-component work needs that component and its data boundary; browser verification needs a working local browser tool.

## Common questions

**How does it avoid a narrow-screen check that never stresses the content?**

It combines a plausible long value with the narrowest selected container before the browser visit. The bound comes from product constraints or existing content, or is labeled an assumption. A predicted failure is never reported as observed.

## It's working if

- The page imports the real component and includes only scenarios it can receive.
- Visible breaks are marked beside their scenarios and assigned to the relevant domain owner.
- When observation is unavailable, you receive the page and scenario list with that limit, without invented findings.

## Where it fits

It is a standalone stress check. [better-interface](https://github.com/reach0908/paul-skills/blob/main/docs/design/better-interface.md) owns a standards review, while [state-machine](https://github.com/reach0908/paul-skills/blob/main/docs/design/state-machine.md) keeps one component state available for visual work. See [ask-matt](https://github.com/reach0908/paul-skills/blob/main/docs/engineering/ask-matt.md) for the full routing map.
