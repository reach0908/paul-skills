## What it does

Reviews grouping, alignment, reading order, spacing and responsive structure. It tests whether the layout still works when resized, translated or mirrored. An existing spacing scale or usable density is respected; a different preferred gap is not a finding.

## When to reach for it

Type `/better-layout`, or the [agent](https://www.aihero.dev/ai-coding-dictionary/agent) reaches for it automatically for clipping, ordering, grouping or responsive structure. Use [better-typography](https://github.com/reach0908/paul-skills/blob/main/docs/design/better-typography.md) for wrapping and truncation within text.

## Hold structure until it breaks

Breakpoints follow the content and task. Related controls stay grouped, primary actions remain distinct, and translated or longer content gets room to grow. The report needs a visible failure such as overlap, clipping, a broken mirror or a misleading group.

## Common questions

**Must the mobile page look like a smaller desktop page?**

No. Reading order and task importance govern the narrow layout. The [skill](https://www.aihero.dev/ai-coding-dictionary/skill) preserves useful structure and changes it when the content no longer fits.

**Will it replace our spacing tokens?**

It uses the project scale and density. Its example numbers are defaults for projects without a system.

## It's working if

- Requested widths and content states are named in the evidence.
- A proposed change fixes a demonstrated grouping or space problem.
- Translated text and reading order remain usable where they were in scope.

## Where it fits

A standalone layout review within [better-interface](https://github.com/reach0908/paul-skills/blob/main/docs/design/better-interface.md). It works with [better-accessibility](https://github.com/reach0908/paul-skills/blob/main/docs/design/better-accessibility.md) when spatial changes affect control access. Find the broader route with [ask-matt](https://github.com/reach0908/paul-skills/blob/main/docs/engineering/ask-matt.md).
