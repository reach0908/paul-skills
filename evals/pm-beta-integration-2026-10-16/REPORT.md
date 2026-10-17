# PM beta integration review repairs

Date: 2026-10-16

## Scope and fixed inputs

Integrate the five PM and prototype-evaluation candidates from PR #10 while keeping them in `skills/in-progress/`. The user authorized conflict resolution, documentation and provenance repairs, local validation, merging into main, and cleanup of the completed branch and worktree. CI is excluded from this operation.

- Beta source: `97931a18539bcec549724a0695611ba8d76875e0`.
- Main integration base: `0f4cb92c5e07d3b96714c00a6877c837bd8f8df1`.
- Historical three-skill evaluation baseline: `aa676799bb33ed0ec311a5cd7b6c3c9e6e7d8f20`.
- Candidates: office-hours, problem-discovery, product-brief, experiment-design and prototype-user-test.

## Repairs and observable evidence

| Review finding | Repair | Evidence boundary |
| --- | --- | --- |
| Main and beta conflict in the evaluation index and source registry | Retain the main index, source records and decisions; append the PM evidence and five beta records | The merge retains both histories; this is not a new upstream reconciliation |
| ask-matt's local provenance digest advanced without a complete upstream review | Restore main's `sha256:654c276d311f2661a81fef6a30977eb209a6ee0c69e3c5aa05dff7bc31761d2b` baseline and record the repair | Origin revisions and main reconciliation records remain unchanged |
| Maintenance policy excludes optional beta routing although the requested router exposes it | Document conditional routing for separately available betas and synchronize the ask-matt FAQ | Source on main and a conditional route do not install or promote a candidate |
| Historical evaluation requires current skills to equal an older snapshot | Pin the original three source records and verify historical snapshots by default; make current-tree equality an explicit `--check-current` option | Historical evidence can remain valid after a later skill change; the later five-skill verifier checks the current candidate |
| Public raw evidence contains author home-directory paths | Replace ten occurrences across eight public copies; preserve original hashes, the original manifest and the source revision in a transformation ledger | Original failures, actions, observations and timing remain recorded; embedded freeze hashes refer to original bytes |
| Verifier changes need failure controls | Add ten local regression controls for valid historical drift and rejected evidence, snapshot, source-pin, current-tree, ledger and manifest corruption | These are deterministic verifier checks, not fresh model behavior trials |

The public-copy verifier itself is an explicit maintenance amendment in the ledger. The ledger preserves the original 151-artifact membership and five skill-tree hashes. Its README is outside that historical manifest. During implementation, the first verifier run rejected the changed verifier's original hash; an attempted README manifest update also failed because that file was not a member. The explicit maintenance entry corrects the first issue, and the README remains outside the historical manifest. These development failures do not alter any historical trial verdict.

## Local verification

- `npm run test:pm-beta`: passed both evidence verifiers and all ten regression controls.
- `npm run check:local`: passed version alignment, the 61-skill registry and packaging checks, 38 repository tests, 26 grader controls, both PM evidence verifiers, ten PM verifier controls and the working-tree whitespace check. Total: 74 tests.
- `claude plugin validate . --strict`: passed.
- Packaging, provenance and public-copy invariants: passed. All five beta trees equal the beta source; the 44-skill manifest, root README, marketplace, lockfile and workflows equal the main base. All 56 existing main source records retain their origin data, with only the router's decisions extended. Eight public copies equal the original bytes with exactly ten home-directory prefix replacements. Both PM evaluation directories contain no author home-directory prefix.

`test:pm-beta` is part of `check:local`. The existing CI command remains `npm run check`, and workflow files are unchanged from the main integration base.

The broader staged whitespace comparison against the old beta parent reports six pre-existing generated CHANGELOG lines imported from main. The final diff against main reports two untouched raw-evidence whitespace findings: a trailing space in `artifacts/coordinator/frozen-attempt-before-interview/browser-version.txt` and a final blank line in `artifacts/prototype-recheck/participant/session-close.md`, both under `pm-conversation-beta`. Their bytes already exist at the beta source revision and remain covered by the original manifest. They are preserved as recorded output. The repair adds no new whitespace finding; the local command's working-tree check passes. This is not a claim that the entire historical patch passes `git diff --check` against main.

## Limitations and next decision

No fresh native model session or human usability test ran during this repair. Existing [three-skill trials](../product-management-beta/README.md) and [five-skill observations](../pm-conversation-beta/RESULTS.md) retain their original verdicts and limitations. The prototype walkthrough is AI participant evidence, not human validation. Model recommendations remain unmeasured beyond their recorded trials.

The promoted plugin remains at 44 skills and version 0.4.6. The five candidate skill trees stay unchanged from the beta source and remain excluded from the plugin manifest, root skill index and promoted docs. The existing beta Changesets and the repair Changeset remain pending. No release, global installation update or promotion is part of this integration. Repeated real use and explicit user approval are still required before promotion.
