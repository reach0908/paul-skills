---
name: prototype-user-test
description: Observe fresh subagents attempt tasks in a runnable prototype, interview them after their attempts and compare recorded behavior with the author's intent. Use for fresh-eye prototype usability walkthroughs; findings describe AI attempts, not human-user validation.
metadata:
  provenance: "https://github.com/reach0908/paul-skills/blob/main/skill-sources.json"
---

# Prototype user test

Watch first, interview second, compare intent last. Act as a moderator, not a critic looking for a risk list. Fresh agents attempt the product with ordinary visible information; their actions and misunderstandings are the evidence. They are **AI walkthrough participants**, not recruited people.

## 1. Prepare two separate packets

Recover the user's test question, runnable URL/version, realistic starting condition, permitted interactions and output location. Reuse settled scope. If the target is missing, ask for the URL or how to start the supplied local prototype while preparing the plan. A source-only reading cannot substitute for an attempt.

Keep the **author packet** with the moderator: core promise, intended outcomes, fixed decisions, expected behavior, mock limits and source locators. Record unknown intent honestly. Do not infer approval from a prototype detail.

Create a separate **participant packet** with only the URL, minimal use context, starting state/device, neutral outcome-based tasks, action permissions, stopping bound, unique browser session and evidence destination. Include known mock/side-effect boundaries needed for informed action. Remove expected routes, button names, suspected defects, success rubric, author explanations, previous findings and other participants' output. The author packet and source code stay outside the participant's workspace/context.

Use tasks such as “Find a saved item and return to what you were viewing,” not “click Library, open the first card and press Back.” If useful, start with a short unprompted first impression before giving one task at a time. Simulated context is a task setup, not demographic evidence.

Choose a small bounded pass, normally one or two fresh agents with explicit task/time/action limits. Keep cost, interaction and parallelism within existing authorization. A request for this test authorizes the scoped fresh participants, not unrelated external contact or provider spending.

Done when the participant packet can guide an attempt without revealing the author's expected answer.

## 2. Run fresh attempts

Read [participant.md](references/participant.md) and use its dispatch contract. Spawn each participant with **no inherited conversation**, only its packet and the participant instructions. Use a distinct writable evidence directory and isolated browser session for each. Use the same scenario/seed state when comparing attempts; report differences. Do not reset shared or user-owned data to manufacture independence.

Participants use the installed model-invoked design-browser instructions for browser operation, with this test's visible-surface restriction. With no Skill tool, read the installed skill. A named browser session does not isolate backend data: serialize mutations or use designated disposable accounts/copies. Parallel attempts are appropriate only when their state is independent.

Collect starting state, observed action sequence, resulting states, evidence paths, unassisted/assisted completion, mistaken expectations and stopping reason. Wait for actual completion and inspect the saved artifacts; a dispatch receipt or ungrounded summary is not a result. Do not coach while an attempt is underway. If intervention is necessary, preserve the unassisted result first and label the later portion assisted.

When fresh contexts or browser access are unavailable, report the affected attempt as unavailable. A moderator's own inspection can be a separate fallback, clearly labelled author-context inspection, not a fresh participant. Never invent an interview or a successful attempt.

## 3. Interview after freezing the attempt

Keep the same participant context for follow-up questions. Freeze its action record before showing any intent. Ask neutral questions grounded in what it actually did: what it thought would happen, which visible clue led to its choice, where its expectation changed, and what it would try next. Ask a follow-up when its answer changes the interpretation.

Separate its reported interpretation from observable clicks/results. Do not ask it to rationalize an unseen feature or pretend to have human feelings, habits or willingness to pay. Preserve the initial attempt even if it later learns the interface. If the author explanation is revealed, mark all subsequent responses as exposed; they cannot count as fresh evidence.

## 4. Compare behavior with intent

Read [synthesis.md](references/synthesis.md). Only after the independent records exist, compare them with the author packet. For each intended outcome mark aligned, mismatch, not reached, or intent unknown, and link the specific actions/states. Successful recovery through another route can be useful behavior rather than failure. Separate blocked tooling, prototype limitations, interface confusion and a product-policy gap.

Explain what was understood naturally, what needed guidance, what surprised the author and which next change or question follows. Fixing the prototype is a separate requested action; keep this pass's target version and records intact. To confirm a fix, use a fresh participant/version and record it as another pass, rather than recycling someone who now knows the answer.

## 5. Return and hand off

Deliver the test question, target/version, actual participant/attempt coverage, raw action and interview records, intent comparison, findings and limits. Use the product's existing artifact convention. Counts refer to these AI attempts only; no percentages implying population success, demand, human usability or production readiness.

Product meaning or policy changes go to product-brief, task/recovery design to user-flow, interface findings to the relevant design role. If the user requests the scoped brief update, call the Skill tool with "product-brief". A real-person study or consequential AI-quality/demand/feasibility decision uses experiment-design. Each model-invoked dependency is one named Skill call; without that tool, read its installed instructions and report unavailable roles. User-invoked roles remain choices for the human.

Done when the author can trace whether the intended outcome occurred, what each fresh participant actually did, what the interview adds and what remains unobserved. This is an exploratory AI usability walkthrough, not a general product review or interface audit.
