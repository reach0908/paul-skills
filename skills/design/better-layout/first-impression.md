# First impression and safe simplification

Use this procedure for first-impression checks, competing emphasis or screen simplification. Layout owns grouping and hierarchy; other causes keep their existing domain owner. A three-second glance is a bounded communication check, not a universal usability, accessibility or conversion score.

## Establish intent and the target

Reuse the brief, flow and screen/state IDs. Record purpose, intended first message, next action if applicable, and information and controls to preserve. Mark absent intent as unknown; a reviewer proposal is not an approved product decision.

Match the question to the surface: a landing page may communicate value and an action; a work tool, current state and the next task; reading, topic and structure; a gallery, the artifact and its entry points. Mixed surfaces can have different purposes by state. Avoid adding a CTA to satisfy the test.

Bind every observation to the artifact revision or digest, route, state and viewport. For a live URL with no revision, use observation time. Missing or stale screenshots leave current visual conclusions unverified; source inspection alone cannot establish what a viewer saw.

## Choose and label the observation

| Method | Evidence to retain | Permitted conclusion |
| --- | --- | --- |
| Author or AI precheck | Current screenshot and the analyst's interpretation; disclose prior knowledge of intent | Predicted hierarchy or comprehension risk, untimed |
| Fresh AI observation | A fresh context, fixed screenshot, neutral questions and verbatim response frozen before comparison | Untimed AI first impression, not human behavior |
| Human three-second observation | Actual three-second exposure and hiding procedure, timing record, original answers, prior familiarity and repeated exposure | What that participant understood or recalled under those conditions |

For a fresh observer, supply only the fixed screenshot and neutral questions: “What is this screen for?”, “What do you remember first?” and, for an actionable surface, “What could you do next?” Keep author intent, source/DOM, grading criteria and earlier answers out of that packet. Collect the response before revealing the intended answer. If neutral observation is unavailable, use a labeled precheck or mark the observation `not_run`; do not invent a participant or silently substitute a simulation.

For a human run, show the target for three seconds, hide it, then ask the questions. Record deviations, timing uncertainty and familiarity; repeated exposure is not a fresh first impression. No human run means human validation is `not_run`. Keep human and AI results separate, including denominators. Never report “three-second passed” from an AI precheck, an untimed answer or an unperformed test.

A squint or reduced-detail view can reveal competing visual emphasis. It does not establish message comprehension or measured recall. Capture the original as the observation target and distinguish any transformed view used for hierarchy analysis.

## Compare, then simplify

1. Compare intended meaning with the recorded observation. Quote the relevant response when one exists. Distinguish an observed mismatch from an analyst's prediction; an already clear screen can need no change.
2. Locate the cause and its owner. Use the six laws below as questions, not numerical pass thresholds. Keep one finding per root cause.
3. Prefer a bounded adjustment to grouping, emphasis, order or wording. Before proposing deletion or disclosure, account for required facts, prices and conditions, warnings, recovery, frequent actions, accessible names, keyboard/focus behavior and the approved visual identity. Keep preserved items reachable and understandable in their required state. If a proposed change alters policy, task scope or an approved design, return that decision to its owner.
4. For an authorized implementation, repeat the relevant observation on the changed revision and recheck the affected task, narrow viewport and accessibility behavior. Use a fresh participant for a fresh-impression claim. If only a proposal exists or a recheck is unavailable, report it as pending; never infer improvement from fewer elements.

| Law | Diagnostic question | Primary owner or handoff |
| --- | --- | --- |
| Hick | Are choices understandable for this task and level of expertise, without hiding needed options? | Layout; writing for labels |
| Fitts | Are required targets reachable and usable in the relevant input mode? | Accessibility; layout for placement |
| Jakob | Are familiar meanings and interactions preserved? | User-flow and writing; build-design for approved conventions |
| Proximity | Do related information and controls read as a group? | Layout |
| Von Restorff | Does the important element remain distinguishable amid competing emphasis? | Layout; typography and colors for expression |
| Serial Position | Are important items placed deliberately at the beginning/end while preserving task and reading order? | Wireframe and layout |

## Report the evidence boundary

Record intended message/action, method, original observation or prediction, mismatch, owning domain, proposed change and preservation/recheck status against the exact target. Use `not_run` for an unperformed method, `unknown` for missing intent, and `not_applicable` with a reason where an action or check does not fit. A scoped review verdict does not certify human comprehension.

Concept references: [Duarte's glance test](https://www.duarte.com/resources/guides-tools/the-glance-test/), [Impeccable layout](https://github.com/pbakaus/impeccable/blob/abf5779cabc20147fd9c013fa4705088c200bf8a/skill/reference/layout.md), [Impeccable distill](https://github.com/pbakaus/impeccable/blob/abf5779cabc20147fd9c013fa4705088c200bf8a/skill/reference/distill.md). This is an independently authored protocol; the slide-oriented glance test's usefulness for a given interface remains to be evaluated.
