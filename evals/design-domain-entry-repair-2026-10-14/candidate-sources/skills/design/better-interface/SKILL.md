---
name: better-interface
description: "First entry for UI change reviews, including staged/index, working/uncommitted, branch, PR and commit ranges, even when a domain is named. Read this entry alone before any repository or domain lookup; it returns the explicit review command. Also coordinates current-screen audits."
metadata:
  provenance: "https://github.com/reach0908/paul-skills/blob/main/skill-sources.json"
---

# Cross-discipline review entry

Choose one route from the user's request before inspecting the repository or selecting domain skills. Reading this entry is a separate tool action. The request itself supplies the route; Git status, diffs, file discovery and domain documents come only after an authorized execution route.

## Changes introduced or worsened

For a request about what a change introduced or regressed, finish with the matching command and one sentence explaining that the user must invoke the change-review owner. This completes the routing task. Preserve the user's verification and mutation constraints in that sentence.

| Requested scope | Command target |
| --- | --- |
| Git staged, index, 스테이징된 변경, 스테이징에 올라간 변경 | `staged` |
| All uncommitted or working-tree changes | `working` |
| Current branch | `branch` |
| Named pull request | `pr <number>` |
| Named ref or range | The exact ref or range |
| Unspecified | Omit the target |

Use `$paul-skills:interface-review <target>` in Codex or `/paul-skills:interface-review <target>` in Claude Code. Git staging is the index, not a deployed staging environment. Naming accessibility, layout, writing, typography, color or motion still takes this route. An explicit `better-interface` or domain invocation also takes this route when the task is change attribution.

`interface-review` is user-invoked and may be hidden from the automatic catalog. The routing answer leaves it unopened: no lookup or body load of that owner, repository inspection, domain loading, review preparation or verdict. A generic review request and this referral are not its explicit invocation.

## Authorized execution

Continue into [audit-procedure.md](audit-procedure.md) for either of these routes:

- **Current-screen audit:** examine a screen, flow, feature or repository as it is now. A repository audit does not attribute problems to a diff.
- **Explicit change-review handoff:** the user invoked `interface-review`, and it supplied its resolved base, head, file inventory, affected surfaces and permitted verification. Keep its scope and change classifications. The cap and verdict cover only `Introduced` and `Regression`; pre-existing findings alone cannot block the change. Continue the handoff without another invocation.

Load the procedure only for the selected execution route. It owns severity, evidence, consolidation, coverage and the verdict. Domain rules remain with the six `better-*` owners; they are not duplicated here.
