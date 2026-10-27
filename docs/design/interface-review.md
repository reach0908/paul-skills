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

## The domain map

Before any domain owner loads, the review classifies each changed line by the surface it touches and records a **domain map**: which of the six domains the change can affect.

| The change touches | Domains loaded |
| --- | --- |
| Only server code, data, tests, configuration or performance work, with rendered output unchanged | None. The report states that no UI surface changed |
| Colors, spacing, type, markup, copy or motion | The domains those lines reach, plus accessibility |
| Anything the map cannot place | All six |

A skipped domain is reported as not reviewed, naming the surface the change lacks, never as clear.

## Common questions

**Why does it not appear in the automatic [skill](https://www.aihero.dev/ai-coding-dictionary/skill) list?**

It is deliberately user-invoked. Type its name to start it. A generic request to review UI changes can automatically load `better-interface` to give you the correct command, but the change review begins only after you invoke `interface-review` yourself.

**Does `working` compare my branch with the default branch?**

No. Both local targets start at the current `HEAD`, including when the branch already has commits:

| Target | What the review covers |
| --- | --- |
| `working` | Net current changes to tracked files plus untracked files. Earlier commits are excluded. |
| `staged` | The Git index snapshot. Unstaged edits and untracked files are excluded. |

If you stage an edit and then undo it only in your working copy, `staged` still reviews that staged edit while `working` sees the restored state. A preparation-only answer explains this scope without inspecting Git. Neither target needs the default branch or a merge base.

**What happens when there is nothing to review?**

It states that the selected scope is empty and asks you to choose another target. An empty `working` or `staged` scope does not silently expand to earlier branch commits. It does not invent a last-commit review or approve an empty scope. For the current screen as a whole, choose [better-interface](https://github.com/reach0908/paul-skills/blob/main/docs/design/better-interface.md).

**Why did it skip some domains, or all of them?**

The domain map loads a domain only when a changed line reaches its surface. A backend mapping or a memoization change that leaves the rendered output identical gets a short "no UI surface changed" result instead of six empty domain reviews. A line the map cannot place loads every domain, so an unclear change costs more rather than going unreviewed. For a review of the whole current screen, which always covers all six domains, use [better-interface](https://github.com/reach0908/paul-skills/blob/main/docs/design/better-interface.md).

## It's working if

- The report names the target, base, head, exclusions and affected surfaces.
- Each domain is either reviewed or marked not reviewed with the surface the change lacks; a change with no UI surface ends without a domain review.
- Introduced and regressed findings are separated from existing problems.
- The domain review continues without asking you to invoke the same skill twice.

## Where it fits

A review step after interface implementation. It composes [better-interface](https://github.com/reach0908/paul-skills/blob/main/docs/design/better-interface.md) while keeping the engineering [code-review](https://github.com/reach0908/paul-skills/blob/main/docs/engineering/code-review.md) verdict separate. [ask-matt](https://github.com/reach0908/paul-skills/blob/main/docs/engineering/ask-matt.md) maps both routes.
