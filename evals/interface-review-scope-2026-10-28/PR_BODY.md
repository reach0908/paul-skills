## Summary

`interface-review` now loads only the `better-*` domain owners whose surface the change reaches. A change with no UI surface loads none and ends with a short result.

```diff
 /interface-review <target>
   resolve scope, read both sides of every hunk
+  map changed lines to domains (surface-map.md)
+  if no line has a UI surface
+    read stated intent
+    report: scope block, six rows "Not reviewed: no UI surface in the change scope", no verdict
+    stop: no consumer expansion, no better-interface, no domain owner
   expand to consumers
-  better-interface: load all six owners
+  better-interface: load the owners the domain map marks; skipped = "Not reviewed: no <surface> in the change scope"
   rank, consolidate, verdict
```

The surface map is a table. Each row is a kind of changed line (markup, copy, color, type, box and flow, polish and motion, unclassified), and it lists the domains that row loads:

- Accessibility loads for every row.
- A line that cannot be placed loads all six.
- The map can grow during review and never shrinks.

Current-screen audits through `better-interface` still load all six owners.

Files:

| Area | Files |
| --- | --- |
| Skill behaviour | `skills/design/interface-review/SKILL.md`, new `skills/design/interface-review/surface-map.md`, `skills/design/better-interface/{SKILL.md,audit-procedure.md,review-format.md}` |
| Router and docs | `skills/engineering/ask-matt/SKILL.md` (one row), `docs/design/interface-review.md`, `docs/design/better-interface.md` |
| Provenance and release | `skill-sources.json` (three `keep-local` decisions), `.changeset/interface-review-domain-map.md` (patch) |
| Eval | `evals/interface-review-scope-2026-10-28/`: protocol, cases, `stage.py`, `summarize.py`, `regrade.py`, `review.json`, `REPORT.md`, raw outputs; link in `evals/README.md` |

## Evidence

The trial ran through `claude plugin eval` on staged plugins:

- Executor `claude-opus-5-5`, Claude Code 2.1.312, effort medium, `Bash(git:*)`, n=3 per arm.
- Synthetic fixture: a React feed app with one feature-branch commit, reviewed with `/paul-skills:interface-review main...HEAD`.
- main is `794b572`. Branch r1 is `d032162`. Branch r2 is `5c0e655`, the shipped text after the code-review fixes.

Owners are read from the trace's `Skill` calls, not from the reports. Costs are runner list price. Times and tokens are per-run means.

| Case | Owners loaded: main → r2 | Graders: main / r1 / r2 | Findings kept vs main | Cost: main → r1 → r2 | Wall time: main → r2 | Tokens out / cache read / cache write: main → r2 |
| --- | --- | --- | --- | --- | --- | --- |
| S-01 data-only category merge (server alias map, test, migration) | six + `better-interface` → none | 0/3 / 3/3 / 3/3 | n/a (no UI) | $0.76 → $0.33 → $0.34 | 111s → 59s | 6,856 / 586k / 63k → 3,497 / 194k / 29k |
| S-02 perf-only home page (`Promise.all`, `useMemo`, prefetch; JSX unchanged) | six + `better-interface` → none | 0/3 / 3/3 / 2/3 | n/a (no UI) | $0.68 → $0.28 → $0.30 | 90s → 51s | 5,749 / 394k / 60k → 2,925 / 126k / 27k |
| S-03 color + layout (accent token 5.17 → 2.54:1, fixed 880px toolbar grid, raw 12px gap) | six + `better-interface` → accessibility, layout, colors + `better-interface` | 3/3* / 3/3 / 3/3 | r2: F1, F2, F3 at the same severity in 3/3. r1: F3 lost its own row in 1/3 | $0.90 → $0.73 → $0.75 | 141s → 146s | 10,404 / 548k / 73k → 10,477 / 451k / 56k |

\* After the dated grader amendment (`\b320\b` could not match `320px`). The runner's original verdicts are kept.

Notes on the table:

- **Spend.** Arm totals: main $7.02, r1 $4.03, r2 $4.17; $15.22 overall. Input tokens were 8 to 32 per run in every arm, and thinking tokens are in `record.json`.
- **S-02 r2 failure.** The run wrote the skip reason only in Korean, not the specified string. It loaded no owner.
- **S-03 findings.** They were graded blind to arm by two fresh AI sessions, with IDs shuffled. Neither arm had other change-attributed findings.
- **Raw outputs.**
  - Traces: `evals/interface-review-scope-2026-10-28/outputs/{main,branch,branch-r2}/<case>/run<n>/trace.jsonl`.
  - Runner verdicts: `aggregate-result.json` and `runner.log`.
  - Per-run records: `record.json`, with re-graded amendments in `regrade.json`.
  - Blind grades: `outputs/blind/` (main vs r1) and `outputs/blind-r2/` (main vs r2), with verbatim grader reports.
  - Write-up: `REPORT.md`.

Checks: `npm run check` passes (73 tests), and `claude plugin validate . --strict` passes. `npm run check:local` passes with exit 0, but only with a temporary `rg` shim on `PATH`, because `rg` exists only as a shell function on this machine.

## Code review

`/paul-skills:code-review` against `origin/main`, with separate Standards and Spec sub-agents.

**Standards.** 3 hard findings and 7 judgement calls:

- Fixed:
  - Missing quality-floor section in REPORT; now "not compared".
  - `summarize.py` wrote 0 for a missing trace; now null.
  - "surface" had three meanings; the row is now "Polish and motion".
  - Self-contradiction in `audit-procedure.md`.
  - Stale docs heading and a prose branch; now a table.
  - Missing `ask-matt` provenance decision.
  - Private PR numbers in REPORT.
  - Duplicated wording inside `interface-review/SKILL.md`.
  - `js()` renamed.
- Left as is:
  - The `Not reviewed` wording repeated across the two skills (each needs it).
  - The S-02 graders sharing the `S1-` prefix (renaming would break correspondence with the recorded runs; documented).
  - The `OWNERS` list repeated in the case regexes.

**Spec.** No missing deliverables. The data matched the traces on all 18 main and r1 runs.

- Fixed in `5c0e655`, then re-run as r2:
  - Mapping gaps where a UI change could pass as "no UI surface": hooks whose returned state flips a render condition, i18n key references, shown formatters, text-switching conditions, excluded binaries that render.
  - The no-UI exit skipping the stated-intent check.
  - The data-vs-copy contradiction for constants files.
- Corrected in REPORT and changeset: the overstated "kept every finding" for r1, the missing permission-denial disclosure and the wrong CLI version.
- Left as is: the review counted the clause on token consumers' domains as scope creep. It was shortened, not removed.

Verdict: no open hard finding. Two known weaknesses remain and are recorded in REPORT:

- In 3 of 6 branch S-03 runs, the skipped-domain reason sits in the evidence cell instead of the Result cell. It is never `Clear`.
- One of 6 r2 no-UI runs translated the required string.

## Merge Danger

**Door:** two-way. This is prompt text in two skills plus docs; reverting the commits restores the six-owner load.

**Blast radius:** change reviews only. A mis-mapped line could skip a domain that had a real finding. The risk is bounded by these rules:

- Accessibility loads on any UI line.
- Unclassified lines load all six.
- Skipped domains are reported as `Not reviewed`, never `Clear`.

Current-screen audits are unchanged.

## Limits

- **Coverage.** Three synthetic diffs, one model, one host, n=3. No human review, and the checklist was written by the change's author. The blind graders run on the same model family as the executor.
- **Untested rows.** Only the color and box-and-flow rows and the no-UI path were exercised. Markup, copy, type, polish-and-motion, unclassified and the r2 additions (hooks, i18n keys, formatters, binaries, stated intent) have no case.
- **Not run.** Codex, the native-suite `interface-review-staged` and `better-interface-settings-audit` cases, any current-screen audit, and a paired run against Jakub's originals (quality floor not compared).
- **Not replayed.** The two private sessions that motivated this; the fixtures only imitate their shape.
- **Run order.** The arms ran sequentially, not interleaved.
- **Permissions.** Every run but one hit 1 to 3 Bash permission denials from compound shell commands outside the `Bash(git:*)` grant, at a similar rate in all arms.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
