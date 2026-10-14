# Design beta

This beta imports Jakub Krehel's 13 skills from the revision and file hashes in `upstream-manifest.json`. The source files remain retrievable at that immutable commit. Each installed adaptation retains the MIT notice. `design-browser` is an independently written evidence adapter: Playwright is the default, Aside serves research and general browsing, and the reviewing agent owns the verdict.

## Prepare separate arms

Use a read-only clone of https://github.com/jakubkrehel/skills containing the pinned commit. The preparer reads Git objects, verifies every source hash and adds the source license to each isolated skill directory. It does not use a potentially modified checkout as the baseline.

```bash
python3 evals/design-beta/prepare_trial.py /tmp/design-none --arm no-skill
python3 evals/design-beta/prepare_trial.py /tmp/design-original --arm upstream --upstream /path/to/jakub-skills
python3 evals/design-beta/prepare_trial.py /tmp/design-paul --arm paul
```

Every destination must be new. A workspace gets the same task, an output directory and a content manifest. Only the skill condition changes. The Paul arm includes the browser adapter; the common task requires the same CLI in every arm so a driver change does not masquerade as a design improvement.

Start a fresh host with only that arm's skills discoverable. Inspect the host's discovered catalog before running. A copied directory alone does not isolate an inherited plugin, user configuration or conversation. When using a subagent without independent discovery, supply the explicit skill paths and record that limitation. Never give the agent this rubric, another arm's result or the expected findings.

For a complete maintainer link smoke check, use `scripts/link-skills.sh` with a disposable home. That checks installation of the catalog; it is separate from these minimal arm workspaces. Never run it against daily global skill directories.

## What changed from Jakub

- Packaging: beta paths, Paul provenance and per-skill MIT notices; original names and the eight Model/five User invocation policies remain.
- Browser operations: every imported role passes its purpose and expected observations to `design-browser`. Explicit tool choices win; research/general browsing uses Aside, development verification and unclassified browser work default to Playwright CLI.
- `break`: its one-look budget permits one CLI session. Tool installation, browser debugging and a separate run for every scenario remain outside that scope.
- `build-design`: browser/Markdown references, state/revision evidence, preservation of required states and usable accessibility, explicit deviations instead of fidelity-induced regressions.
- Korean: natural action-label grammar, realistic translated content, script-aware measure and wrapping. Latin character recipes do not become Korean pass/fail thresholds.
- Review: explicit Model skill calls, scoped verdicts and independent Standards/Spec code-review reports.
- `variant`: an explicit one-component request owns one exploration harness. Existing `prototype` stays available for broader UI/logic questions. Its browser driver now follows the user's CLI preference.

`ask-matt` remains a promoted-skill router per the maintenance policy. Beta discovery uses the in-progress index and explicit trial prompts. Promoting these routes will require the router, docs and manifests to move together. No design skill is promoted by this trial.

## First product and boundaries

The human selected the entire inflfeed article in `cases/inflfeed.md`. Public browsing can test review behavior without copying project-private sources into this library. Raw page captures and product-specific findings stay local unless separately approved for publication.

A live page is mutable. Record observation time and, when supplied, deployment revision. A later three-arm comparison should use frozen permitted evidence or the same controlled local product revision. Sequential live runs alone do not establish causal quality differences.

## Evaluation protocol

The [original-quality floor](quality-floor.md) is the first acceptance gate for this design work. The original is the minimum outcome baseline; local improvements cannot compensate for lost original capabilities. Keep per-role and per-case evidence separate from an overall parity claim.

The [2026-10-10 repair record](improvement-2026-10-10.md) preserves intermediate misses, final candidate comparisons and the separate Markdown-only implementation check. Its decisions apply to executed cases, not to all 17 design candidates. Current source identities and local digests are in the [post-repair audit](source-audit-2026-10-10-repair.json).

Hold model, reasoning setting, host, permissions, CLI/browser version, budget, task, product revision and inputs fixed. Run no-skill, original and Paul conditions separately with repeated runs. Record failed and interrupted runs, retries, human intervention and unavailable telemetry as null. Do not rank models from this pilot.

Inspect actual outputs for:

- Whole-page coverage rather than only the anchor, with state and viewport evidence.
- Correct invocation boundaries and domain ownership. User-only skills are never automatic follow-up actions.
- Korean readability and actionable interface findings, distinguished from aesthetic preference.
- Evidence appropriate to claims: source, visual, keyboard and motion are different checks.
- Honest scope limits when source, reference or deployment identity is absent.
- No production edits, unintended submissions, secret capture or global session cleanup.

Use a separate implementation task later to evaluate `build-design`, and explicit user requests for `variant`, `state-machine`, `break`, `interface-review` and `explain-interface`. A review trial cannot validate these unexecuted behaviors. Human review decides visual acceptance and eventual promotion.

## Tool record

The requested shared executable is `@playwright/cli`, not the separate MCP server. On 2026-10-09 the installed package was updated from 0.1.1 to 0.1.22 and its actual browser behavior was checked. Projects own their session, profile and output settings. Installing the executable does not install or promote Paul beta skills.

The adapter was authored against [Microsoft's pinned README](https://github.com/microsoft/playwright-cli/blob/b85c7a736bb473bf55b584e54a09ffa698d6d871/README.md). That source's token-efficiency claims were not independently benchmarked here. Read installed CLI help before relying on options from a newer repository snapshot.

On 2026-10-10, the user clarified the route policy and allowed controlled task-class comparisons. [The routing change record](browser-routing-2026-10-10.md) separates the new instructions from prior Playwright runtime evidence. Static analysis belongs to the responsible agent and analyzers; a browser is only needed for a missing runtime observation. No Aside-versus-Playwright quality or efficiency winner has been measured.

## Validation limits

The [2026-10-09 result record](results-2026-10-09.json) contains one independent candidate smoke run. It covered the whole public page at 1440, 390 and 320 CSS px, keyboard navigation and reduced motion. Eight applicable skills were read, and the candidate's 82 bundled files were unchanged after execution. The original and no-skill arms were prepared but not executed. Explicit skill-path loading does not validate automatic host discovery.

The local Korean review is at `.scratch/design-skills-beta/trials/paul/output/review.md`, with an execution record in the same directory and `evidence-manifest.json` in its parent. Raw product observations are not included in the public bundle; their digests are recorded. The maintainer checked the reported label-name mismatch against the captured accessible names and visible card text. This supports the bounded review outcome, not a model ranking or measured skill improvement.

The repository checker validates the paired Claude and Codex invocation policies. The bundled Codex `quick_validate.py` accepts the nine Model skills but rejects `disable-model-invocation` on the five User skills because that validator's allowed-key list excludes it. Keep the field required by this repository and the matching Codex `allow_implicit_invocation: false`; this compatibility limitation is not a reason to make User skills automatically callable.

## Follow-up human feedback

The user preferred the existing page over both later design directions while finding the interactive prototype comparison useful. This accepts the comparison mechanism, not the redesigns or all beta skills. The prototype workflow now explicitly preserves the original as an option and keeps tool usefulness separate from design acceptance. The [source map](source-map.md) identifies the original repo and exact entrypoint of every skill in this design work. The [planning beta](../design-planning/README.md) fills the IA, flow and wireframe roles through independent authoring.
