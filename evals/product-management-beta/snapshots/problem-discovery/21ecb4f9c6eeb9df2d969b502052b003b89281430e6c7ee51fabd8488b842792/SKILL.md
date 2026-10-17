---
name: problem-discovery
description: Clarify the user, situation, current alternative and smallest useful problem scope. Use when an idea or proposed solution still leaves the product problem open; reuse sufficient context instead of starting another interview.
metadata:
  provenance: "https://github.com/reach0908/paul-skills/blob/main/skill-sources.json"
---

# Problem discovery

Recover the problem before proposing more product. End with a short **Problem Brief** that the next role can use. A supplied solution is a starting point for understanding the intended change, not evidence of demand.

## Recover before asking

Read the supplied conversation, decisions and relevant artifacts. Recover who encounters the situation, what they do today, what hurts or could become possible, the desired outcome, constraints and existing scope choices. Attach source locators to evidence; keep the user's account distinct from independently observed behavior.

Infer the working purpose from that context: business validation, an internal/personal tool, or learning and exploration. If the purpose would change the next decision and is genuinely unclear, ask about it. For an unanswered problem question, read [modes.md](references/modes.md) and select the matching question posture.

Ask one consequential gap at a time, only when a human answer changes the next decision. Look up recoverable facts yourself. Skip answered questions, including answers in earlier documents. Explain why the remaining gap matters and wait for that answer; no fixed question count. When the user asks to proceed, carry unresolved items as assumptions and give the settled input to the next task.

Done when the next scoped task can identify its user, situation, intended change and first boundary, or its exact blocking decision. A sufficiently defined problem proceeds directly to the brief without another interview.

## Write the Problem Brief

Use the user's language. Fit the output to the task: a concise reply or an update in the existing product document is enough unless a saved artifact is requested. Include only relevant information:

- Whose situation and problem or opportunity this is, and the intended outcome.
- Current alternatives, including a manual workaround or doing nothing.
- Evidence with locators, hypotheses and unknowns, each identified as such.
- The smallest useful first scope, later work and explicit exclusions.
- The next check or decision, with the input the next role needs.

Preserve settled choices and their reasons. Interest, compliments and signups are evidence of interest; demand and user benefit need behavior appropriate to the claim. A personal tool can succeed by helping its author, without revenue or external customers.

## Continue only within the request

Research owns source investigation, grilling owns stress-testing an existing plan, and prototype owns a runnable exploration. Discovery supplies their bounded question, evidence and fixed choices. It does not create screens, technical specifications or tickets.

If the requested work includes documenting product decisions, call the Skill tool with "product-brief". If it includes testing an unresolved assumption, call the Skill tool with "experiment-design". For a needed source investigation within the authorized task, call the Skill tool with "research". Each call names one skill. When no Skill tool or candidate is available, return the prepared input and name the missing capability; do not claim a call ran. Further steps are options, not a compulsory pipeline.

## Attribution

Selectively adapted from gstack office-hours startup diagnostic and builder brainstorm at the pinned revision in the provenance inventory. Question pressure and mandatory later phases are replaced by context recovery and task-sized completion. See [MIT notice](LICENSE.gstack).
