---
name: wireframe
description: Turn agreed task flows and content into low-fidelity interactive screens and a Markdown screen specification. Use when deciding screen hierarchy, controls and responsive order before visual design or production implementation.
metadata:
  provenance: "https://github.com/reach0908/paul-skills/blob/main/skill-sources.json"
---

# Wireframe

Make the scoped task usable as a low-fidelity screen sequence. Own information hierarchy, action placement and responsive order. Preserve upstream product and transition decisions; visual direction, design-system creation and production implementation remain separate tasks.

## 1. Resolve the screen contract

Read the supplied brief, IA, flow and existing product context. Reuse their IDs, content, routes and settled decisions. Accept equivalent information already present in the request rather than requiring three named files.

Map flow states to screens or in-place states. Record the information needed to act, the main action, secondary actions and feedback in each. Carry unresolved upstream choices forward. Ask only for a decision that blocks a screen's behavior, and draft the unaffected parts.

For each screen/state, record its purpose, the first message a viewer should understand, the next action when the task calls for one, and information or controls that must remain available. Derive these from the existing brief and flow; mark missing intent as unresolved instead of inventing a conversion goal. A reading or gallery surface may have no primary action. These fields describe intended communication, not an observed test result.

Done when each scoped flow state has a screen/state destination or an explicit exclusion.

## 2. Build one coherent wireframe

Use the existing page and component context where available, with realistic content lengths and density. On a new surface, use simple semantic HTML or the project's existing UI primitives. Neutral styling should make hierarchy and behavior legible without implying an approved brand direction.

Render the content and controls necessary to complete the task. Wire navigation and state transitions to local mock behavior; identify simulated network, permission and persistence effects. Keep the real product's forms and mutations outside this prototype. Provide a reset or scenario control where it helps reproduce a required state.

Determine mobile information priority deliberately. Keep primary information and actions reachable rather than merely stacking every desktop region. Use native controls, labels, visible focus and meaningful reading order even at low fidelity.

A wireframe normally needs one coherent solution. If the user is choosing between materially open structures, call the Skill tool with "prototype" for that bounded comparison. Without a Skill tool, read its installed SKILL.md; if unavailable, build the requested local comparison directly and state that substitution. Pass the question, fixed content, flow IDs and existing baseline. Its comparison UI supports the decision; alternative appearance alone does not establish improvement. Keep the original as an option when evaluating an existing screen.

Done when the scoped transitions are operable or individually marked as unwired, and each control corresponds to a flow action.

## 3. Walk it in the browser

Call the Skill tool with "design-browser" for implementation verification and evidence, passing the required flow, states and widths. Without a Skill tool, read its installed SKILL.md. If unavailable, honor an explicit tool choice or default to the installed Playwright CLI help. If the selected tool cannot run, deliver the runnable artifact with browser verification explicitly pending.

Walk the task from its entry to success and the specified recovery/exit paths. Check keyboard operation and the requested wide and narrow layouts. If no widths are specified for a responsive web task, start with a desktop viewport and a narrow viewport appropriate to the content; record the actual dimensions. Exercise relevant long, empty and error content rather than treating a single screenshot as full coverage.

Compare observed controls, destinations, retained data and feedback against the flow contract. Repair screen-level mismatches. Return policy or flow contradictions to their source as open decisions instead of changing the upstream contract silently.

Distinguish navigation between screens from movement within a screen. If the prototype uses URL fragments for routes, exercise its skip and section links as well as Back. Moving focus or scrolling within the current screen must not accidentally navigate away, discard input or cancel the task.

Done when each scoped path has observed evidence or a stated verification limit.

## 4. Deliver screen and state references

Provide the runnable URL or file and Markdown in the existing project location. Include the input revisions, screen/state IDs, flow mapping, content hierarchy, intended first message, next action or its absence, information and controls to preserve, action behavior, responsive changes, mock boundaries, observations and unresolved decisions. Record the artifact revision or digest used for the walkthrough.

When first-impression or three-second validation is requested, read `first-impression.md` from the installed `better-layout` directory and use its observation and evidence contract. If unavailable, leave that check pending with the missing reference named. Otherwise pass the intent fields forward without adding an unsolicited test gate.

Distinguish three outcomes: rendered, behavior checked, and user accepted. A working browser demo does not establish user acceptance or production readiness. The downstream designer or builder must be able to identify exactly which screens and states are settled and which still need a decision.
