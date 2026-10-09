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

`model-recommendations.json` separates measured recommendations from unmeasured candidates. A record includes skill revision or content digest, exact model and reasoning effort, host/version, protocol version, case IDs, trial count, evidence location, and decision status. Missing telemetry is `null`, never zero. Unsupported models/settings are explicit outcomes, not silently substituted.

Record input/output/cache/reasoning tokens when supplied by the host, duration, retries, human interventions, and provider cost. Distinguish estimated list-price cost from actual billed cost. Cost per successful task includes failed trials and retries; total experiment cost also includes judges and infrastructure. Do not claim token savings from prompt length alone.

Human review owns qualitative acceptance. Reuse deterministic output checks where possible; calibrate any model judge against human decisions. A candidate must not edit its own grading criteria or holdout. Keep private holdout cases outside the candidate checkout, with a versioned evaluator-owned protocol. Publish only redacted, permitted evidence.

Before a paid matrix, choose models from currently supported host options, fix a budget/stop condition, and get any needed spending authorization. The initial in-session trials use inherited host settings and support no model-ranking claim.
