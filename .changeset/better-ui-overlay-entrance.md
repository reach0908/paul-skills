---
"paul-skills": patch
---

`better-ui` no longer gives overlays its staged-entrance recipe. The staged entrance and its fixed `-12px` exit now name page and section content (hero, empty state, onboarding, section reveal), and a new principle moves overlays from their anchor: dropdowns, popovers, menus and tooltips grow from the trigger edge with `transform-origin`, toasts, drawers and sheets enter from and exit toward their own edge, and centered modals scale from center. The `display: none` popover recipe now scales from its trigger corner instead of rising 12px. On the overlay task that exposed the failure, `transform-origin` went from 0/3 to 6/6 runs and the toast exit from upward in 3/3 to downward in 6/6; a staged empty state kept its exact values in 3/3 before and 6/6 after. Checklist verdicts are by the authoring agent, pending human review.
