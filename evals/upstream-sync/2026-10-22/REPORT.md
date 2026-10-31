# Registered-source sweep, 2026-10-22

The upstream-sync workflow inspected all seven registered Git sources and the 61-skill local inventory. It applied two bounded updates, preserved existing Paul behavior, and left two design-control changes pending with a concrete patch and failed observation. This is a local working-tree result. No commit, push, PR, release, global installation, or beta promotion was performed.

## Scope and pinned inputs

The starting Paul commit was `e543809` on `main`. The pre-existing untracked `.playwright-cli/` directory was excluded from the change scope. Remote heads were observed on **2026-10-22 at 02:46 KST**. Each separate bare clone matched the observed remote HEAD. No upstream setup, hook, installer, release script, or runtime was executed.

[Remote observations](remote-heads.json), [registry before this run](registry-before.json), and [all local tree digests](local-before.json) preserve the inputs. UTC timestamps in the machine records correspond to the Korean date above.

| Source | Pinned target | Review result |
| --- | --- | --- |
| mattpocock/skills | `5beb35b040e3de97e54fa9e386d7e42d15c295c2` | 38 direct mappings reconciled; wizard and chief-of-staff adapted. Three commits and all five repository changes reviewed. |
| jakubkrehel/skills | `4c66b1fa86e9ab70187b43d7da9b6fdb29f2ef63` | 11 direct mappings reconciled; state-machine and variant deferred. technical-drawing discovered as an optional candidate. |
| garrytan/gstack | `b616d6c53dd8fc0d8db210444b44a131b553b83e` | Three mappings to office-hours reconciled as keep-local; changed host/runtime integration is absent from Paul. |
| phuryn/pm-skills | `07b34f64ee828df08953f505b7f747aef85ae7c6` | Nine direct mappings unchanged and reconciled; repository delta is Cursor packaging and changelog. |
| reach0908/paul-loop | `7c95bb3f60e2ae6334bddf452be1852fbad3fd05` | Influence source unchanged from its recorded snapshot. |
| microsoft/playwright-cli | `b1a5903c5b633b8c9f843ad7b629c2a78437040c` | Referenced README unchanged; four CLI/workflow/test paths changed. No CLI update performed. |
| pbakaus/impeccable | `dad8dbb3aac21ad1fa236c110315ef4abece23e8` | Influence paths scanned for change. Retain independent Paul procedures; engine migration and detailed adoption review deferred. |

The source selectors for gstack and PM Skills now track their observed `main` branches. Immutable import revisions and paths remain unchanged. Historical influence pins and local-origin digests also remain unchanged.

## Decisions and application

[decisions.json](decisions.json) accounts for **63 direct-origin mappings** across the inventory. Several composite skills have more than one mapping. **61 mappings are reconciled and two remain deferred**. The after-comparison has 61 `UNCHANGED` mapping results and the two expected `REVIEW` results. No direct mapping is `UNKNOWN`.

Ten skills had local drift against their recorded digests at entry: ask-matt, code-review, prototype, research, retro, writing-for-agents, better-interface, better-layout, better-writing and build-design. Their local changes were reviewed and retained, including Korean copy, explicit review routing, complete reads, component mapping, product constraints and evidence boundaries. This run does not certify their behavior anew.

### Applied: wizard

Adapted the source template fixes for:

- Plain double-quoted dotenv defaults without carrying quote characters into the saved value.
- Rejection of ambiguous double-quoted escaping/interpolation instead of treating it as a decoded default.
- Making a value written to `.env` available to later stages in the same shell.
- ANSI clearing after a failed `tput clear`.
- A parsed `run_wizard` stage wrapper that survives edits while the script is running.

The unmodified upstream patch failed an additional apostrophe round-trip on macOS Bash 3.2. Replacement-string expansion added an extra backslash. Paul now uses literal concatenation to encode/decode the existing quote representation. No eval or external interpreter is used. Human documentation links to the Paul template and describes the changed behavior.

The five isolated tests in [test_wizard_template.py](../../../tests/test_wizard_template.py) use fake values and temporary files. They never open dashboards or set real secrets.

| Template | Result on Bash 3.2.57 |
| --- | --- |
| Previous Paul template | One test method passed; four methods failed, producing seven failures including subcases. |
| Pinned upstream template | Four passed; the apostrophe round-trip test failed. |
| Adapted Paul template | Five passed. |

The mid-run-edit case passed on both the old and new templates in this small fixture, so it establishes retained behavior, not a measured improvement from the wrapper. Full real-user setup and Bash versions other than the tested macOS version remain untested.

Logs: [baseline](wizard-baseline-tests.log), [upstream](wizard-upstream-tests.log), [candidate](wizard-candidate-tests.log). The first development attempt also exposed a PTY fixture problem: closing the slave before reading could lose captured output. The test now retains it through the read and checks process exit before a potentially empty read. That harness failure is distinct from the apostrophe defect.

### Applied: chief-of-staff

Adapted the upstream wiki guidance: interlinked topic pages, dated claims, code claims tied to repository commits, and explicit supersession. Reuse an authorized wiki destination and its writing rules; host-managed memory retains its own write policy. No wiki or host memory was written by this run. The skill remains user-invoked and in `in-progress/`.

This was an instruction and packaging review. No fresh agent behavior trial or human acceptance is claimed.

### Deferred: state-machine and variant

The source replaces a floating row with a grouped side list and a narrow-screen native select. The exact local proposal, including human docs and preserved Paul additions, is in [design-controls-proposal.patch](design-controls-proposal.patch). It is **not applied** to the current skill files. Their reviewed revisions and prior local digests remain at the older reconciled snapshot; each now has a `defer` decision.

A disposable fixture used the proposed Markdown HTML/CSS and a separately authored interaction adapter. [browser-result.json](browser-result.json) preserves the observations from Playwright CLI 0.1.22 and Chrome 152.0.7977.82:

- State-machine at 1280x800 passed count, focus, group crossing, URL selection, hide/show, task-state retention, resize and bounds checks.
- At 390x844, Tab reached the native select with a visible focus outline, but the ArrowDown/Enter sequence left selection unchanged. Follow-up Space/ArrowDown/Enter and repeated ArrowDown also left the value unchanged. The environment's native menu interaction was not resolved. This is not proof that the upstream design is inaccessible for a human.
- The remaining six matrix cells, including every variant cell, were **not run** after that failure. Do not report an eight-case pass.
- An initial missing favicon request was fixture noise; the saved fixtures include a data favicon. It was unrelated to the selection failure.

The two skills share the control pattern, so both remain pending. Resume by resolving the native menu keyboard observation, then run the entire eight-cell matrix against the proposed revision before adopting it. Screenshots and the exact generated pages are in [browser-fixtures](browser-fixtures/). These are authored demonstrators, not independent skill-quality trials or real-device evidence.

Reproduction assets: [make_browser_fixture.py](make_browser_fixture.py) accepts an output directory and optional source checkout containing the proposal; [check_browser.js](check_browser.js) runs through Playwright CLI `run-code --filename`. Serve the generated pages on localhost port 8973. The CLI can exit zero while the returned JSON says `failed`; inspect that field and the completed case count. The task-owned browser session and local server were closed.

## Retained source differences and discovery

The gstack office-hours diff removes duplicated invocation prose and changes gstack browser option wording and Bun runner flags. Paul preserves its explicit trigger, context recovery, decision conversation, selected-approach boundary and optional independent review. Its source-owned runtime is not part of the adaptation.

The Matt repository review retains Paul package identity, release process and existing retro authoring dependency. Upstream pending Changesets are not copied. The new out-of-scope note explains why retro loads writing-for-agents before evaluating instructions; Paul's retro still does so. Only Matt's previously established repository-review baseline is advanced.

New candidates are separate from updates: Jakub's technical-drawing, gstack's capy companion skill, and Impeccable's OMP packaging are not imported. The helper's `newCandidates` field means **present but unmapped**, including skills that already existed at the prior snapshot; it must not be read as a list of newly authored skills. A technical-drawing migration would need its own bounded beta scope and checks of the geometry, viewer and export helpers.

The three influence-only sources have no direct mappings. Changed Impeccable reference files remain leads for a later focused review, not automatic patches or newly reconciled import baselines. Their historical influence revisions stay fixed.

## Verification and limits

- `npm run check:local`: passed. This includes `npm run check`, 78 package/helper tests, 26 grader controls, PM historical evidence verifiers and 10 verifier controls, plus diff whitespace checking. The five wizard tests are included in the 78. [Log](check-local.log).
- `claude plugin validate . --strict`: passed with the existing missing-icon directory warning. No manifest or package version was changed. [Log](plugin-validation.log).
- `bash -n skills/engineering/wizard/template.sh`: passed.
- Immutable origin paths/revisions, all influence records and local-origin records were compared before/after and remain unchanged.
- Target LICENSE headings and hashes are in [licenses.json](licenses.json); registered MIT/Apache identities are consistent with the fetched files.
- [Before comparisons](before/) and [after comparisons](after/) distinguish the local tree, source baseline and pinned target. Six sources still have no completed repository-wide review baseline, so their aggregate helper result remains `UNKNOWN` for that separate dimension. This does not hide a failed skill-tree comparison.

The local source `research-with-aside-20261009` is represented by immutable file hashes, but its source directory was not found in the inspected standard skill locations. Its source bytes were not revalidated. Local adaptation and Git-origin review do not substitute for that missing source check.

No model comparison, native select human test, real iPhone test, source-wide security review, external publication, global host activation or promotion is implied. The upstream-sync skill itself remains a beta; this field run is evidence for user review, not permission to promote it.
