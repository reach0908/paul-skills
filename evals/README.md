# Skill evaluation

Evaluation is added by this fork; the upstream library supplies authoring guidance and observable documentation, not a measured model leaderboard.

## Three distinct checks

- `npm run check` checks package/catalog/provenance consistency and deterministic helper behavior. It makes no claim about an AI following a skill.
- Public behavioral fixtures exercise an actual agent with a realistic user request and raw artifacts. The evaluator receives the task and skill, not expected answers. Preserve the task, skill revision/hash, host, observed outputs, and evaluator decision.
- Comparative trials hold task, host, permissions, and skill fixed when comparing models, or hold model/host fixed when comparing skill versions. Keep no-skill, previous-skill, and candidate arms separate. Use multiple runs and report failures as well as successes before recommending a model.

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


The [PM beta trials](product-management-beta/README.md) compare three product-context candidates with no-skill controls on synthetic tasks, including the boundary between product experiments and design QA. They preserve task/skill hashes, raw artifacts, verdict grounds and limits; they do not promote the candidates.

The [PM conversation and prototype walkthrough beta](pm-conversation-beta/RESULTS.md) records the office-hours behavioral fork, fresh AI task/interview protocol, existing-PM updates and bounded tests. It keeps original observations, host limits and user acceptance separate.
