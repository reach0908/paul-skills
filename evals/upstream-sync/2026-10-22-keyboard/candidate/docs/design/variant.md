## What it does

Build several versions of one component along a chosen design axis in its real page. It presents tradeoffs and leaves the choice with the user.

The chosen axis labels a grouped picker beside the piece. At narrower widths, the same choices appear in a select above it with the browser's native keyboard controls. The URL preserves the selected variant across layout changes.

## When to reach for it

You invoke this by typing `/variant`; the agent will not reach for it on its own.

Use it when the component and its job are fixed but structure, density, emphasis, type or voice remains open. The default comparison has three deliberately different positions on one primary axis.

## Prerequisites

A writable local project or prototype workspace. Existing-component work needs that component and its data boundary; browser verification needs a working local browser tool.

## Common questions

**Must an alternative replace the original?**

No. A comparison can support keeping the original. Switching appearances must preserve working inputs and task state; a reset, when needed, is separate. Only your choice starts adoption and cleanup.

## It's working if

- Variants differ on a named axis while sharing the same accessibility floor.
- You can switch variants at real size without losing task state or hiding focused controls behind the picker.
- The picker stays usable beside the piece or above it after resizing. Outside editable controls and the native select, arrow keys cross choices and `H` hides or restores it.
- The tradeoff table identifies costs without declaring an unsolicited winner.

## Where it fits

It is a standalone component comparison. [prototype](https://github.com/reach0908/paul-skills/blob/main/docs/engineering/prototype.md) covers broader throwaway UI or logic questions; [build-design](https://github.com/reach0908/paul-skills/blob/main/docs/design/build-design.md) implements an already approved reference. See [ask-matt](https://github.com/reach0908/paul-skills/blob/main/docs/engineering/ask-matt.md) for the full routing map.
