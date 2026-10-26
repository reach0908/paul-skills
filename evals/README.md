# Skill evaluation

Evaluation is added by this fork; the upstream library supplies authoring guidance and observable documentation, not a measured model leaderboard.

## Three distinct checks

- `npm run check` checks package/catalog/provenance consistency and deterministic helper behavior. For local validation with routing and source-read grader controls, use [`npm run check:local`](../docs/maintenance.md#local-validation). These checks make no claim about an AI following a skill.
- Public behavioral fixtures exercise an actual agent with a realistic user request and raw artifacts. The evaluator receives the task and skill, not expected answers. Preserve the task, skill revision/hash, host, observed outputs, and evaluator decision.
- Comparative trials hold task, host, permissions, and skill fixed when comparing models, or hold model/host fixed when comparing skill versions. Keep no-skill, previous-skill, and candidate arms separate. Use multiple runs and report failures as well as successes before recommending a model.

## Claude native suite

The [Claude native suite](claude-native/README.md) runs repeatable cases through `claude plugin eval` and turns grader results into rubric verdicts. Required criteria gate each run instead of a weighted score, unjudged graders stay unknown, and LLM graders count as final only for a judge calibrated against labelled pass, fail and boundary artifacts. A Codex model cross-checks the Claude judge. Its thirteen development cases cover `research`, `interface-review`, `user-flow`, `build-design`, `better-interface`, `diagnosing-bugs` and `code-review`; nine reproduce behavior seen in recent real sessions, which stay private. `npm run eval:check` and `npm run eval:plan` make no model calls; calibration and group runs are paid.

## First pilot

`upstream-sync/make_fixture.py` creates isolated Git histories for inspect and apply tasks. It makes no network or model call. The independent agent works only in the generated workspace. The maintainer checks actual file changes and outputs afterward. These public development cases are smoke tests, not hidden holdout evidence.

```bash
PYTHONDONTWRITEBYTECODE=1 python3 evals/upstream-sync/make_fixture.py /tmp/upstream-trial --scenario apply
```

Supply `task.json` and the skill to an independent agent. Do not supply this evaluation rubric or another trial's conclusions. Judge task completion, local-policy preservation, scope compliance, dependency awareness, and honest evidence boundaries. A denied unauthorized operation is still an attempted scope violation; a sandbox rejection is not behavioral success.

## Records and decisions

The [design beta](design-beta/README.md) adds pinned Jakub, Paul and no-skill workspaces with one shared browser-review task. Its first candidate smoke uses an explicitly loaded bundle against a public page. This is separate from automatic host discovery and from the repeated controlled trials needed to compare skill quality.

The [design planning beta](design-planning/README.md) exercises IA, user-flow and wireframe as separate roles on one synthetic brief. Its source map distinguishes original authoring from the Jakub adaptations.

The [design inventory and quality record](design-beta/inventory-and-quality-2026-10-10.md) audits the 17 candidates and the original-quality acceptance floor. Its bounded paired reading-list exercise compares actual review outputs, without treating one case as proof of role parity.

The [17-role design evaluation](design-role-parity-2026-10-12/RESULTS.md) records repeated source comparisons, no-skill controls, observed repairs and the local IA-to-review handoff. Representative results, subjective acceptance and untested branches are reported separately.

The [INFLFEED article field review](design-field-trial-2026-10-14/REPORT.md) reconstructs five completed local stages from one real product session, with preserved evidence, nine loaded design skills, and explicit QA limits. It records local results and release status separately and adds no controlled source-parity trials or promotion decision.

Its [QA repair](design-field-trial-2026-10-14/QA-REPAIR.md) strengthens count and overflow assertions and natural keyboard coverage, with 24 capture paths, 18 browser negative controls and process-failure tests. These are harness checks, not additional controlled skill trials.

The [installation and discovery trial](design-install-discovery-2026-10-14/REPORT.md) checks isolated plugin installation and fresh Codex CLI selection. The follow-up [review routing repair](design-routing-repair-2026-10-14/REPORT.md) preserves failed attempts, verifies explicit and implicit review boundaries, and reassesses the first nine candidates without executing promotion.

`model-recommendations.json` separates measured recommendations from unmeasured candidates. A record includes skill revision or content digest, exact model and reasoning effort, host/version, protocol version, case IDs, trial count, evidence location, and decision status. Missing telemetry is `null`, never zero. Unsupported models/settings are explicit outcomes, not silently substituted.

Record input/output/cache/reasoning tokens when supplied by the host, duration, retries, human interventions, and provider cost. Distinguish estimated list-price cost from actual billed cost. Cost per successful task includes failed trials and retries; total experiment cost also includes judges and infrastructure. Do not claim token savings from prompt length alone.

Human review owns qualitative acceptance. Reuse deterministic output checks where possible; calibrate any model judge against human decisions. A candidate must not edit its own grading criteria or holdout. Keep private holdout cases outside the candidate checkout, with a versioned evaluator-owned protocol. Publish only redacted, permitted evidence.

Before a paid matrix, choose models from currently supported host options, fix a budget/stop condition, and get any needed spending authorization. The initial in-session trials use inherited host settings and support no model-ranking claim.

The [approved nine-skill promotion](design-promotion-2026-10-14/REPORT.md) records user authorization, unchanged evaluated skill files, current package checks and release/install evidence. Historical trial snapshots stay separate from the promoted catalog.

The [remaining eight-skill readiness review](design-beta-readiness-2026-10-14/REPORT.md) records new source comparisons and the break and user-flow weaknesses. Its [hardening follow-up](design-beta-hardening-2026-10-14/REPORT.md) preserves those results, tests bounded repairs and actual invocation, and passes generated IA, flow and screen artifacts into subsequent stages. Neither report is a promotion authorization.

- [Remaining eight design skills: promotion and installation](design-final-promotion-2026-10-14/REPORT.md) records user approval, unchanged candidate files, packaging and fresh discovery.
- [Claude Code discovery and invocation for all 17 design skills](design-claude-discovery-2026-10-14/REPORT.md) records actual global-installation model runs, explicit command expansion, natural selection and user-only boundaries. It preserves and excludes exploratory runs whose working-directory names could prime selection.
- [Claude review-routing repair and regression evidence](design-claude-routing-repair-2026-10-14/REPORT.md) distinguishes the released baseline, session-only candidates, all 17 normal entry points, target-preserving routing and an actual local Git review handoff. Failed attempts and grader corrections remain visible.

- [Design routing patch 0.4.1 release](./design-routing-patch-release-2026-10-14/REPORT.md): both global installs verified; fresh Claude 6/6 and Codex 5/6, with one remaining staged-routing failure and two initial model compatibility failures preserved.
- [Codex staged-routing repair and Claude regression checks](./design-staged-routing-repair-2026-10-14/REPORT.md): preserves three candidate attempts, exact source loads, routing-order failures and ordinary domain-entry checks. This is an unreleased local candidate, not a global-installation update or a new design-quality parity claim.

- [Native review entry and local-scope repair](design-review-scope-repair-2026-10-14/REPORT.md) separates the routing entry from execution, verifies HEAD/index semantics in divergent fixtures, and keeps Codex native reads separate from Claude tools.

- [Domain discovery and reference-reading repair](design-domain-entry-repair-v4-2026-10-14/REPORT.md) checks the actual shortened Codex catalog, preserves three failed candidates, verifies native reference reads and repeats the full cross-host routing/scope matrix.

- [Final routing and reference proof](design-contrast-reference-proof-2026-10-14/REPORT.md) records the release recommendation, unchanged-dependency evidence, fresh color regressions, explicit source-reading proofs and retained diagnostic failures. That record describes the pre-release candidate; the subsequent 0.4.2 installation record below covers publication and global activation.

- [Design routing patch 0.4.2 release](design-routing-0.4.2-release-2026-10-14/REPORT.md) records the immutable release tag, both actual user installations, complete installed-source equality, fresh host sessions, and retained execution limitations.

- [Color evidence consistency](design-color-evidence-2026-10-14/REPORT.md) preserves the historical contradiction, records non-reproduction in fixed repeats, and compares a preventive reporting clarification in 24 fresh native sessions. The candidate passes 12/12; one ancillary baseline Claude overclaim remains recorded. Global installations were still at 0.4.2 during that pre-release trial.

- [Color evidence patch 0.4.3 release](design-color-0.4.3-release-2026-10-14/REPORT.md) records the immutable patch tag, both updated global installations and 12 fresh native sessions. Answer consistency passes 12/12, while source application passes 10/12: one Codex reference read and one Claude automatic invocation remain missing. Failed receipts and the evidence-verifier amendment are preserved.

- [First-impression workflow comparison](design-first-impression-2026-10-15/REPORT.md) records the five-file implementation, unchanged baseline/candidate snapshots, preserved execution-limit failures and eight completed pairs in a separate budget-constrained profile. Explicit reference reading, partial audit coverage and human validation remain distinct.

- [First-impression scope and owner repair](design-first-impression-repair-2026-10-15/REPORT.md) compares eight fresh pairs, preserves the original failed evidence, and distinguishes successful six-owner invocation from three failed ordering checks. Its [entry-order follow-up](design-first-impression-order-2026-10-15/REPORT.md) tests the isolated procedure read with a separate frozen candidate and four pairs.

- [PR #26 final review](design-first-impression-final-review-2026-10-15/REPORT.md) records separate Standards and Spec reviews, the wireframe dependency repair, and a fresh matched pair for requested first-impression validation. Historical trial evidence remains pinned to its original source.

- [First-impression workflow 0.4.4 release](design-first-impression-0.4.4-release-2026-10-15/REPORT.md) records PR #26 and version PR #27 merges, the immutable tag and both installed updates. Claude completes four fresh cases with an ancillary screen-specification error retained; Codex preserves two CLI/model compatibility failures and two unstarted cases. Installation, native execution and human validation remain separate.

- [CLI compatibility and wireframe CSS follow-up](design-cli-css-repair-2026-10-15/REPORT.md) preserves the failed 0.4.4 records, updates the active Codex CLI and completes all four installed cases. A browser oracle and four Claude pairs support a bounded responsive-evidence clarification; both arms explain CSS values correctly, so no accuracy improvement is claimed. A separate diagnostic's unmeasured blocking verdict remains recorded.

- [Wireframe evidence patch 0.4.5 release](wireframe-0.4.5-release-2026-10-15/REPORT.md) records PR #29 and version PR #30 merges, the immutable tag, both global updates and one fresh wireframe case per host. Historical failures and the tied comparison remain intact; installation activation does not establish an accuracy gain or human validation.

The [PM beta trials](product-management-beta/README.md) compare three product-context candidates with no-skill controls on synthetic tasks, including the boundary between product experiments and design QA. They preserve task/skill hashes, raw artifacts, verdict grounds and limits; they do not promote the candidates.

The [PM conversation and prototype walkthrough beta](pm-conversation-beta/RESULTS.md) records the office-hours behavioral fork, fresh AI task/interview protocol, existing-PM updates and bounded tests. It keeps original observations, host limits and user acceptance separate.

The [PM beta integration repairs](pm-beta-integration-2026-10-16/REPORT.md) reconcile the main merge, optional routing policy and provenance baseline, separate historical and current-tree verification, and trace public-copy redactions. Local verifier controls do not promote the candidates or replace behavior evidence.

The [transitions beta trial](transitions-beta-2026-10-26/README.md) runs the in-progress `transitions` skill through `claude plugin eval` on a plugin staged outside the repository, with candidate, no-plugin and promoted-baseline arms on one overlay task and one value-tuning near miss. It records machine graders, an author-agent checklist review and $5.11 of runner-reported cost over two skill revisions; it is not a promotion decision.
