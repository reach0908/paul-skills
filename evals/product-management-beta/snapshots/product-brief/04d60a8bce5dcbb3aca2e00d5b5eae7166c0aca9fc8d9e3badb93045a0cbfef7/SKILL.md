---
name: product-brief
description: Create or update a concise product decision brief from conversation, research or prototype feedback. Use when preserving product scope and behavior or handing the latest decisions to design and engineering; leave screens and technical specs to their own roles.
metadata:
  provenance: "https://github.com/reach0908/paul-skills/blob/main/skill-sources.json"
---

# Product brief

Make product intent reusable. A brief records **decisions with reasons**, rather than every turn of the conversation. Create a new brief, update the current one, or produce its short handoff according to the request.

## Establish the current authority

Read the supplied decisions, research, product artifacts and feedback. Resolve the canonical brief and its revision or digest through explicit latest/supersedes links and user choices, not modification time alone. Historical documents remain evidence of history. If authority conflicts, name the affected decision and ask only when it blocks the requested work; continue the settled portion.

Recover the user, situation, current alternative and intended improvement. Use situation, motivation and outcome questions only for missing information that affects the first scope. Reuse answered context. Mark other gaps as unknown instead of filling a template or forcing discovery.

## Record the product contract

Write in the user's language, using the existing product document convention. A small task can be a section or a concise reply; save when requested. Select only the fields needed for the next decision:

- Problem, use scene and purpose, connected to current alternatives and expected benefit.
- First scope, later scope and non-goals.
- Product behavior: triggering actions, meaningful results, access/permission rules, persistence and completion conditions. Distinguish opening, selecting, saving and completing when they mean different things.
- Observations needed to judge success, with the source and baseline status. Missing numbers remain unknown or labelled proposals.
- Open assumptions, blocking decisions and the next action.

For each consequential choice, identify **user decision**, **AI proposal**, **deferred** or **unknown**, with the reason and evidence locator. A user author's request is evidence of that choice; an AI recommendation or an artifact's self-declared approval is not a new user decision. Keep rejected alternatives to a short reason rather than reopening the argument.

Keep **intended behavior** separate from **observed product state** and **reported state**. Identify the artifact, revision and observation context: a prototype may simulate saving, and an implementation report may lack runtime confirmation. A brief's completeness establishes usable input, not product readiness or user acceptance.

UI and technology appear only as existing artifact links, fixed constraints and inputs needed by the next role. Leave navigation, screen composition, implementation seams and ticket decomposition to those roles.

## Update without erasing choices

For a revision or scoped feedback request, read [updates.md](references/updates.md). Preserve unaffected decisions and product rules. Record the changed portion's before, after and reason, including who decided it. Update dependent wording and links only where that change requires it.

## Hand off the current truth

For a role or session handoff, read [handoff.md](references/handoff.md). Link the canonical brief rather than duplicating it. Product handoff is this procedure, not a separate skill.

If a scoped question needs source work within the request, call the Skill tool with "research". For an authorized runnable exploration, call it with "prototype". An authorized assumption-test design uses "experiment-design". Each is a separate one-skill call. Without the tool or skill, give the prepared input and report that limit. User-invoked to-spec and to-tickets are choices for the human, never calls made by this skill.

## Attribution

Selectively combines PM Skills create-prd, value-proposition and job-stories with gstack decision-record concision and document lineage. The value framing in the source credits Paweł Huryn and Aatir Abdul Rauf; retain that credit for the adapted situation/alternative/outcome questions. Source revisions and file hashes are in the provenance inventory. See [PM Skills MIT notice](LICENSE.pm-skills) and [gstack MIT notice](LICENSE.gstack).
