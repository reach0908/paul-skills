---
"paul-skills": minor
---

Add `transitions` as an in-progress design beta: it reads one UI element's state change, picks a single transition pattern (a lower-overhead choice when two fit, a short list for the user when none fits), choreographs it and builds it in the project's existing stack. Its selection method, choreography rules and implementation traps draw on ideas from transitions.dev at a pinned revision, written in its own words; no transitions.dev snippet or catalog is included, because its license forbids republishing the collection. Exact motion values stay with `better-ui`, and the skill's few fallback values cover only what `better-ui` leaves open. The skill stays outside the promoted plugin pending user validation and promotion approval.
