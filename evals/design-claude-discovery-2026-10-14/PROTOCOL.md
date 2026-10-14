# Claude Code design skill discovery, protocol 1

Fixed before the model matrix on 2026-10-14. This checks the released, user-scope Paul Skills 0.4.0 installation in fresh Claude Code processes. It does not re-evaluate implementation quality or upstream equivalence.

## Cases and evidence

- 17 explicit cases: start the user message with `/paul-skills:<name>`. Require the installed skill body in the host conversation and a completed model response.
- 12 implicit cases: natural Korean requests with no skill names. Require an actual successful Skill call and body load for the expected owner, not a name in the final answer.
- 5 boundary cases: natural requests near user-only roles. Require no user-only Skill invocation or body read. For changed-work review, require the explicit interface-review handoff and no change inspection. For task flow, require user-flow without state-machine.
- Every run: record the host catalog, model, tool events, permission failures, result, timing, tokens, reported cost and input hashes. Verify 12 design skills in the automatic catalog and 17 in the direct-command catalog if the host emits both lists; do not infer one list from another.
- Full-body equality is measured against the installed SKILL.md with frontmatter removed. Keep the complete file hash separately. Inspect host transcripts if direct expansion is absent from stdout. Raw traces remain local; public receipts contain only task-relevant fields.

Calibration found that init.skills contains user-only names too. It is an installation inventory, not the model-visible automatic catalog. The latter is the transcript's initial `skill_listing` attachment. Direct expansion bodies occur in transcript user messages even when stdout omits them. The collector must use these distinct records.

All requests concern preparation or bounded read-only reasoning. No browser operation, code edit, production access or deployment is authorized within the model trials. Synthetic task context is inline. A correct invitation to invoke a user-only skill is not its execution.

## Environment and stop conditions

Use the real HOME and enabled global installation, without plugin-dir, copied project skills, custom system prompts, model override or resumed sessions. Inherit the configured `opus` alias and record its resolved model. Keep unrelated installed skills visible, so competition is part of this host test.

Use Skill, Read, Glob and Grep tools, with normal permission checks and noninteractive denial of unapproved operations. Disable optional hooks for these runs with a per-process settings override and exclude unrelated MCP servers. These controls bound the experiment; this is not a test of daily hooks, all tools or an already-open interactive terminal.

Calibration: at most two fresh runs to verify transcript collection, excluded from the 34-case score. Main matrix: one run per case, no favorable-result rerolls. At most two simultaneous runs, 240 seconds and a USD 0.80 reported-cost ceiling per run. Stop dispatch when accumulated reported cost reaches USD 15 or on repeated authentication/environment failures. A provider request can cross the per-run threshold before the host stops; record actual telemetry. These are host-reported estimates, not an invoice.

Preserve failures and distinguish missing evidence, host errors and semantic routing failures. Do not alter the installed skills or relax grading criteria after observing results. Any follow-up changes need a separately labeled protocol and results.

## Primary sources

- [Claude Code skills](https://code.claude.com/docs/en/skills#control-who-invokes-a-skill): default and user-only invocation, direct command expansion and content lifecycle.
- [Programmatic runs](https://code.claude.com/docs/en/headless): noninteractive execution and structured output.
- [Hooks](https://code.claude.com/docs/en/hooks#disable-or-remove-hooks): temporary per-run hook settings.
- Local `claude --help`, Claude Code 2.1.296: supported flags. Live host traces take precedence over assumptions about event shape.
