## What it does

Build low-fidelity interactive screens with a Markdown screen specification. Controls follow agreed task transitions, while neutral styling leaves brand direction undecided.

## When to reach for it

Type `/wireframe`, or the agent reaches for it automatically when a task fits.

Use it to settle information hierarchy, action placement and mobile priority before visual refinement. One coherent solution is the default; a broader design question may justify a prototype comparison.

## Prerequisites

A writable local project or prototype workspace. Existing-component work needs that component and its data boundary; browser verification needs a working local browser tool.

## Common questions

**Do we need Figma or a complete backend?**

No. The default deliverables are local browser screens and Markdown. Network, permission and persistence effects can be mocked, but the report must identify those boundaries and any unwired paths.

## It's working if

- You can operate the selected task, recovery and exit paths locally.
- Screen and state IDs trace back to the flow, including unresolved decisions.
- Keyboard and wide/narrow checks have observations or explicit verification limits.

## Where it fits

It is the screen step after [user-flow](https://github.com/reach0908/paul-skills/blob/main/docs/design/user-flow.md). An accepted screen reference can go to [build-design](https://github.com/reach0908/paul-skills/blob/main/docs/design/build-design.md); [prototype](https://github.com/reach0908/paul-skills/blob/main/docs/engineering/prototype.md) answers broader open design questions. See [ask-matt](https://github.com/reach0908/paul-skills/blob/main/docs/engineering/ask-matt.md) for the full routing map.
