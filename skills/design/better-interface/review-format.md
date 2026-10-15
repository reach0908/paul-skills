# Review output format

This is the format for a review `better-interface` orchestrates.

## Scope and coverage

State the exact scope, stack and styling conventions, the project convention documents found in recon and any review boundary. Then show coverage:

| Domain | Evidence inspected | Result |
| --- | --- | --- |
| Accessibility | Files, components, states or checks | Findings count or `Clear` |

Include every domain listed under **Use domain skills as the sources of truth**. `Clear` means inspected with no actionable finding; `Not reviewed` must explain why.

## Findings

One table, ordered by severity, then by reach:

| Severity | Domain | Location | Before | After | Why |
| --- | --- | --- | --- | --- | --- |
| HIGH | Accessibility | `src/Dialog.tsx:42` | `<button><XIcon /></button>` | Add `aria-label="Close"` and hide the icon from the accessibility tree | The icon-only control has no accessible name |

- **Severity** comes from **Rank by user impact**.
- **Domain** is the owning skill without the `better-` prefix.
- **Location** is `path/to/file:line`, or the exact screen and component when the artifact has no source files.
- **Before** and **After** show the current implementation and an actionable replacement, each in its own cell.
- **Why** names the violated principle and its user impact.

With no findings, omit the table and state "No actionable interface findings."

## Verification

List each check or interaction, the exact command or steps and the observed result. Separate checks that passed from checks marked **Not verified**.

Record the design/source revision when available, route, state, viewport and input method. For a live URL with no source revision, record observation time and limit conclusions to that snapshot. Source analysis, screenshots, keyboard checks and assistive-technology checks are distinct evidence.

### First impression, when in scope

Use the observation contract in the loaded `better-layout/first-impression.md`. Add a compact record of target revision/route/state/viewport, intended message and next action (or `unknown`/`not_applicable` with reason), method, original response or labeled prediction, mismatch, owning domain and preservation/recheck status. Link supported mismatches into the existing findings table instead of adding duplicate findings.

Distinguish an author/AI precheck, fresh untimed AI observation and a measured human three-second observation. Record unperformed methods as `not_run`; keep actual responses separate from the reviewer's interpretation. Missing or stale visual evidence leaves current visual conclusions unverified. The final summary must preserve these limits and must not turn an AI prediction into a human three-second pass.

## Verdict

End with one of two:

- `Block`: one or more `HIGH` findings remain. Do not ship until they are fixed.
- `Approve`: no `HIGH` findings remain. Any `MEDIUM` and `LOW` findings stay in the table as work to do.

`Approve` covers only the domains the coverage table shows as inspected. Name every `Not reviewed` domain in the verdict line.

This is a scoped design-review verdict. Human acceptance, complete accessibility conformance and release authorization require their own evidence and decisions.

## Change-scoped reviews

When `interface-review` hands the review back, use its `## Review output format`. It adds the scope block, a `Status` column and the pre-existing section to the sections above.
