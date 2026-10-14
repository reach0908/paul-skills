## What it does

Reviews a screen or flow across accessibility, layout, writing, typography, color and UI polish, then combines the evidence into one ranked report. It owns review coordination; the six domain [skills](https://www.aihero.dev/ai-coding-dictionary/skill) own their rules.

A review preserves deliberate product choices. A different visual preference is not a defect, and keeping the original interface can be the right result.

## When to reach for it

Type `/better-interface`, or the [agent](https://www.aihero.dev/ai-coding-dictionary/agent) reaches for it automatically for a UI review. It chooses the route from your request before inspecting files:

| Request | Route |
| --- | --- |
| Review the current screen, flow or repository interface | Review across the six domains |
| Review what uncommitted, staged, branch, PR or commit-range changes caused | Return the explicit [interface-review](https://github.com/reach0908/paul-skills/blob/main/docs/design/interface-review.md) command with that target and a brief reason; scope resolution starts after you invoke it |

## One report, six owners

Each domain must have evidence or a named verification limit. Findings with one root cause are combined; independent causes remain separate even when they affect the same component. The result includes coverage, severity, a proposed fix and a verdict, with a cap of 15 findings.

## Common questions

**Will it redesign a screen I already like?**

A review is read-only by default. It reports supported failures and respects the existing visual language; implementation needs your request.

**Why did it return a command instead of reviewing my changes?**

Change attribution belongs to the directly invoked `interface-review`. Its absence from the automatic skill list does not mean it is uninstalled. For all uncommitted changes, use `$paul-skills:interface-review working` in Codex or `/paul-skills:interface-review working` in Claude Code. This guidance also works before a repository is available. Invoking `better-interface` again does not authorize a change review.

## It's working if

- All six domains have evidence or a clear limit in the report.
- The report distinguishes confirmed defects from taste and untested behavior.
- An unnamed change request ends with the correct invocation instead of a guessed diff review.

## Where it fits

A standalone cross-discipline review. [interface-review](https://github.com/reach0908/paul-skills/blob/main/docs/design/interface-review.md) supplies change scope when you explicitly ask for it, and [design-browser](https://github.com/reach0908/paul-skills/blob/main/docs/design/design-browser.md) supplies rendered observations. Use [ask-matt](https://github.com/reach0908/paul-skills/blob/main/docs/engineering/ask-matt.md) to choose the next role.
