## What it does

Reviews what a branch, pull request or working-tree change introduced or worsened in the interface. It owns the change scope and classifies findings as Introduced, Regression or Pre-existing. Existing problems alone do not block the change.

## When to reach for it

You invoke this by typing `/interface-review`; the [agent](https://www.aihero.dev/ai-coding-dictionary/agent) will not start it automatically. In Codex use `$paul-skills:interface-review <target>`; in Claude Code use `/paul-skills:interface-review <target>`.

| Your target | Argument |
| --- | --- |
| All uncommitted work | `working` |
| Staged changes only | `staged` |
| Current branch | `branch` |
| A pull request | `pr <number>` |
| A chosen reference or range | The exact ref or range |

## Prerequisites

A Git repository and an identifiable change. Pull request inspection also needs access to its repository. Rendered checks need a cheap project preview or your request for browser verification.

## A diff is not a surface

A shared component can affect unchanged screens. The review follows relevant consumers, reads removed lines and keeps the original checkout intact. It passes the resolved scope to [better-interface](https://github.com/reach0908/paul-skills/blob/main/docs/design/better-interface.md) for domain checks and consolidation.

## Common questions

**Why does it not appear in the automatic [skill](https://www.aihero.dev/ai-coding-dictionary/skill) list?**

It is deliberately user-invoked. Type its name to start it. A generic request to review UI changes can automatically load `better-interface` to give you the correct command, but the change review begins only after you invoke `interface-review` yourself.

**What happens when there is nothing to review?**

It states the repository facts and asks you to choose a target. It does not invent a last-commit review or approve an empty scope. For the current screen as a whole, choose [better-interface](https://github.com/reach0908/paul-skills/blob/main/docs/design/better-interface.md).

## It's working if

- The report names the target, base, head, exclusions and affected surfaces.
- Introduced and regressed findings are separated from existing problems.
- The domain review continues without asking you to invoke the same skill twice.

## Where it fits

A review step after interface implementation. It composes [better-interface](https://github.com/reach0908/paul-skills/blob/main/docs/design/better-interface.md) while keeping the engineering [code-review](https://github.com/reach0908/paul-skills/blob/main/docs/engineering/code-review.md) verdict separate. [ask-matt](https://github.com/reach0908/paul-skills/blob/main/docs/engineering/ask-matt.md) maps both routes.
