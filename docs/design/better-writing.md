## What it does

Writes and reviews interface labels, errors, empty states, confirmations and product terms. It uses the product’s existing voice and checks whether the words match the action and tell people what they can do next. A stylistic preference alone is not a defect.

## When to reach for it

Type `/better-writing`, or the [agent](https://www.aihero.dev/ai-coding-dictionary/agent) reaches for it automatically for interface copy. Use [better-typography](https://github.com/reach0908/paul-skills/blob/main/docs/design/better-typography.md) for how the words render and [better-accessibility](https://github.com/reach0908/paul-skills/blob/main/docs/design/better-accessibility.md) for their markup and announcement.

## One voice, one vocabulary

The same object and action retain their names across the flow. Errors offer a real recovery path, destructive actions explain the consequence, and empty states account for what the user can actually do. Korean copy follows the product’s register and the available locale context.

On explanatory pages, each heading, explanation, proof and action has a reader-facing purpose. Repeated claims need a useful role. Research bookkeeping stays with the evidence, while genuine product limitations remain visible when they affect a decision.

## Common questions

**What if I mention this domain while reviewing staged changes?**

The automatic catalog makes the change-review route take priority over the domain words, before this domain document is loaded. [better-interface](https://github.com/reach0908/paul-skills/blob/main/docs/design/better-interface.md) first supplies the explicit change-review command. This domain resumes after the authorized handoff; ordinary screen audits and requested fixes still enter it directly.

**Can it improve Korean copy without changing our tone?**

Yes. It inventories existing terms and register first. It reports ambiguity, misleading promises or inconsistent terminology rather than rewriting everything into a new voice.

**Is a clearer label enough if the action does something else?**

The report must expose the mismatch. A promise to open detail is not fulfilled by merely repeating content already shown.

**Should verification status appear in public copy?**

Internal collection IDs or editorial notes belong in source records. A real pending review, unavailable result or uncertain estimate can matter to the reader and should remain clear. Removing internal jargon does not authorize stronger claims.

## It's working if

- Labels and results describe the same action.
- Error and empty-state copy offer a possible next step.
- Proposed strings reuse the product’s terms and locale conventions.

## Where it fits

A standalone copy role composed by [better-interface](https://github.com/reach0908/paul-skills/blob/main/docs/design/better-interface.md). It coordinates with [better-layout](https://github.com/reach0908/paul-skills/blob/main/docs/design/better-layout.md) when translated text needs more space. [ask-matt](https://github.com/reach0908/paul-skills/blob/main/docs/engineering/ask-matt.md) maps its neighbors.
