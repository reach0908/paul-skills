---
name: user-flow
description: Specify a product task's actions, transitions and recovery paths before implementation, including unanswered requests, interruption, exit and return. Use this skill directly for flow planning; do not load state-machine unless the user explicitly invokes that separate component workbench.
metadata:
  provenance: "https://github.com/reach0908/paul-skills/blob/main/skill-sources.json"
---

# User flow

Turn a scoped task into an inspectable transition contract. Own what the person does, what the product responds with, and where the task goes next. Use the existing information architecture for destinations; leave screen layout to wireframe and production logic to implementation.

Planning task states does not authorize loading the user-invoked state-machine skill. Work from the product decisions here; an existing component workbench is a separate request from the human.

## 1. Fix the task and its facts

Read the supplied PM decisions, IA and existing behavior. Name the actor, entry context, intended outcome and observable success condition. Reuse agreed destination IDs. A missing IA document is not a reason to invent a full sitemap: identify the few destinations this task needs and flag any structural decision that remains open.

Separate supplied product policies from design proposals. Ask about a missing permission, persistence or commitment rule only when it changes the task; continue with unaffected paths. Preserve the user's fixed decisions and existing working paths.

Done when the actor can start somewhere concrete and success has an observable meaning.

## 2. Write transitions

Give the flow and its states stable IDs. For each transition, specify the origin state, user action or system event, precondition, feedback, destination state and data retained or changed. Several states may share one screen; a state change does not imply another route.

Distinguish initiating an operation from its confirmed result. Make relevant asynchronous work, repeated input, interruption and failure visible where the task can actually encounter them. Tie each branch to a supplied requirement, observed behavior or explicit assumption rather than adding every possible error to every flow.

Include the routes that let a person correct input, retry, cancel or leave when those actions are meaningful. State what survives back navigation or a failed attempt. Where a consequential policy remains unknown, keep that transition unresolved; visual design cannot decide it silently.

When closing and reopening a view preserves an operation, model view visibility separately or enumerate the operation states to which those transitions apply. Cover the state before a request exists and the confirmed outcome as well as work in progress, wherever closing is offered. Retained data depends on that state: an unstarted task has no request key or receipt to restore.

Done when every scoped action has a response and every reachable branch leads to a task outcome, an intentional exit or a named dependency.

## 3. Walk the paths

Walk the successful path and each materially different recovery or exit path from the stated preconditions. For every action offered in the state table, locate its applicable transition and verify that the destination and retained data agree. Include exit and return before starting and after completion when offered. Check that users can recognize their current state, tell whether the operation completed, and find the next action. Record an orphan state, contradictory guard or missing transition before calling the contract ready.

Keep proposed behavior distinct from observed implementation. If verifying an existing browser flow is necessary, call the Skill tool with "design-browser" and pass the expected transitions. Without a Skill tool, read its installed SKILL.md. If unavailable, honor an explicit tool choice or default to the installed Playwright CLI help, and report the observation limit.

An author's walkthrough demonstrates internal consistency, not task success with real users. If a branch is not exercised or a policy is unresolved, name that limit.

Done when each scoped path has a walkthrough result or an explicit reason it cannot yet be checked.

## 4. Hand off the contract

Save Markdown using the project's existing design artifacts. Include source revisions or equivalent locators, the task boundary, state IDs, transitions, path results and open decisions. A transition table is authoritative; add a diagram when it makes branches easier to follow, and keep it consistent with the table.

Identify the information and actions that each screen must expose, without choosing its visual composition. Preserve IDs and assumptions so wireframe can trace a control to a transition and an implementation can distinguish proposed policy from an agreed requirement.

A flow is ready for downstream drafting when its selected paths are specified. User acceptance is a separate status. End here unless the request also includes screen design. The existing state-machine skill displays implemented component states; it is not a prerequisite for designing this flow.
