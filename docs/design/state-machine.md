## What it does

Render every reachable state of one existing component on a removable local workbench. It imports the real component unchanged and feeds mock data through an existing data boundary.

States appear in named groups beside the component. When that layout will not fit, a grouped select sits above it and uses the browser's native keyboard controls. Switching and resizing preserve the state selected in the URL.

## When to reach for it

You invoke this by typing `/state-machine`; the agent will not reach for it on its own.

Use it when you need to inspect or work on component states one at a time. Planning a product task belongs to user-flow and does not automatically open this workbench.

## Prerequisites

A writable local project or prototype workspace. Existing-component work needs that component and its data boundary; browser verification needs a working local browser tool.

## Common questions

**Does it add missing states or change the component?**

No. States come from reachable code branches. Missing design states are listed separately; adding a data seam needs its own decision. The workbench stays available until you request removal.

## It's working if

- Every listed state shows its intended mock data, including held loading states.
- A switcher and shareable state URLs let you return to each case.
- A long state list remains reachable on a narrow screen. Outside editable controls and the native select, arrow keys cross groups and `H` hides or restores the controls.
- The real component keeps its production styling, and the temporary setup can be removed together.

## Where it fits

It is a standalone component workbench. [user-flow](https://github.com/reach0908/paul-skills/blob/main/docs/design/user-flow.md) defines product task transitions; [break](https://github.com/reach0908/paul-skills/blob/main/docs/design/break.md) displays hostile scenarios together for one observation. See [ask-matt](https://github.com/reach0908/paul-skills/blob/main/docs/engineering/ask-matt.md) for the full routing map.
