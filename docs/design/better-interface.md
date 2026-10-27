## What it does

Reviews a screen or flow across accessibility, layout, writing, typography, color and UI polish, then combines the evidence into one ranked report. It owns review coordination; the six domain [skills](https://www.aihero.dev/ai-coding-dictionary/skill) own their rules.

A review preserves deliberate product choices. A different visual preference is not a defect, and keeping the original interface can be the right result.

When first impression or simplification is in scope, it connects intended meaning, the observation method, supported mismatches and preservation checks to the same six-domain report.

## When to reach for it

Type `/better-interface`, or the [agent](https://www.aihero.dev/ai-coding-dictionary/agent) reaches for it automatically for a UI review. It chooses the route from your request before inspecting files:

| Request | Route |
| --- | --- |
| Review the current screen, flow or repository interface | Review across the six domains |
| Review what uncommitted, staged, branch, PR or commit-range changes caused | Return the explicit [interface-review](https://github.com/reach0908/paul-skills/blob/main/docs/design/interface-review.md) command with that target and a brief reason; scope resolution starts after you invoke it |

## One report, six owners

A current-screen audit loads all six domain owners before the surface or optional first-impression reference is inspected, including for a one-attribute change or missing screenshot. A change review from `interface-review` loads only the owners its domain map selects from the changed lines; each skipped domain is reported as not reviewed, with the surface the change lacks. The report separates successful owner loads from artifact verification. An unsuccessful load leaves the audit incomplete and prevents approval. Each loaded domain must then have evidence or a named verification limit. Findings with one root cause are combined; independent causes remain separate even when they affect the same component. The result includes coverage, severity, a proposed fix and a verdict, with a cap of 15 findings.

## Common questions

**Does mentioning accessibility or layout start those reviews immediately?**

For a staged or other change review, this router is the only automatic entry, even when the request names specific domains. The domain descriptions exclude direct change attribution; that work starts after the explicit change-review handoff. An ordinary current-screen audit can still request those domains directly.

The entry document is read on its own; the full review procedure loads only for a current-screen audit or an authorized change-review handoff. A Git status check or diff summary cannot be bundled with that read: without the explicit handoff, its next action is the invocation guidance, not repository inspection.

For an authorized audit, the procedure is also read on its own before artifact inspection. Its owner-loading instructions must arrive before the agent starts examining the screen.

**Will it redesign a screen I already like?**

A review is read-only by default. It reports supported failures and respects the existing visual language; implementation needs your request.

Declared prototype boundaries are part of the review scope. Unimplemented destinations outside that contract and unconfirmed visual risks stay in verification notes; missing required implementations remain findings. Source facts are not reported as observed clicks.

**Why did it return a command instead of reviewing my changes?**

Change attribution belongs to the directly invoked `interface-review`. Its absence from the automatic skill list does not mean it is uninstalled. Here, staged means the Git index, not a staging deployment. For all uncommitted changes, use `$paul-skills:interface-review working` in Codex or `/paul-skills:interface-review working` in Claude Code. This guidance also works before a repository is available. Invoking `better-interface` again does not authorize a change review.

**Is a first-impression check another review domain?**

No. Layout supplies its protocol and the cause keeps its existing owner. AI predictions, fresh AI observations and measured human responses remain separate; the final verdict does not certify human comprehension.

## It's working if

- Every domain has evidence or a clear limit in the report: all six for a screen audit, and the mapped owners plus a named reason for each skipped one in a change review.
- The report distinguishes confirmed defects from taste and untested behavior.
- An unnamed change request ends with the correct invocation instead of a guessed diff review.

- First-impression evidence and pending human checks remain explicit in the final summary.

## Where it fits

A standalone cross-discipline review. [interface-review](https://github.com/reach0908/paul-skills/blob/main/docs/design/interface-review.md) supplies change scope when you explicitly ask for it, and [design-browser](https://github.com/reach0908/paul-skills/blob/main/docs/design/design-browser.md) supplies rendered observations. Use [ask-matt](https://github.com/reach0908/paul-skills/blob/main/docs/engineering/ask-matt.md) to choose the next role.
