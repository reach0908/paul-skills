# Patterns

One row per pattern: match the element the user sees and what it does, then read the row's notes. Rows are grouped by verb. The selection approach is adapted from transitions.dev's decision rules; the grouping, wording and notes are this skill's own. A row marked _paul-skills_ has no transitions.dev counterpart.

## Open and close

| Element and verb | Pattern | What moves | Notes |
| --- | --- | --- | --- |
| A menu, popover, select list or date picker that opens from a trigger | **Anchored grow** | The surface: opacity plus a slight scale from just under `1`, origin at the trigger edge | Asymmetric. Flip the origin when placement flips. Prefer this over a modal whenever the content fits beside its trigger. |
| A centered dialog with a backdrop | **Centered scale** | Surface: opacity plus slight scale from its center. Backdrop: opacity only | Asymmetric. The backdrop never scales or blurs in. Native `<dialog>` needs the discrete-transition recipe to animate its close. |
| A circular trigger that becomes the surface it opens (a `+` button expanding into a menu) | **Trigger morph** | One element changes size, radius and content | Heavier than an anchored grow. Use it only when the trigger visibly turns into the surface; a separate popover is an anchored grow. |
| A drawer or sheet attached to a screen edge | **Edge slide** | The sheet: full translate from its edge. Backdrop: opacity | The one place full-distance travel is right, because the edge is where it lives. Close is a little shorter than open, still to the same edge. |
| A panel that appears inside a region of the page (an inspector, a details pane) | **Region reveal** | The panel content: short slide toward its resting place plus opacity; neighbors resize if they must | Asymmetric. If only the size of the region changes, use **Resize** instead. |
| A toast or snackbar | **Edge toast** | The toast: short travel from the edge it is anchored to plus opacity; others in a stack shift by its height | Asymmetric. An actionable or error toast stays until dismissed (`better-accessibility`). New toasts push older ones, never cover them. |
| A tooltip or hint on hover or focus | **Intent tooltip** | The bubble: opacity plus a very slight scale from its arrow side | Brief intent delay on the first open, none for neighbors while one is open, instant close. Focus opens it with no delay. |
| A disclosure, FAQ item or collapsible settings group | **Height reveal** | The body's height via a grid-row track from `0fr` to `1fr`, content fading in; the chevron flips | Symmetric. Padding goes on the inner element, never on the collapsing track. |

## Swap in place

| Element and verb | Pattern | What moves | Notes |
| --- | --- | --- | --- |
| Two icons in one slot (play/pause, copy/copied) | **Icon cross-fade** | Both icons, overlapping | `better-ui` owns this with exact values; call it and use its recipe. |
| A label whose old and new text share nothing ("Processing" to "Done") | **Text swap** | Old text exits a few pixels one way, new text enters from the other, with a light blur | Symmetric. Reserve the wider label's width so neighbors do not jump. |
| A label that keeps a shared prefix or suffix ("Follow" to "Following") | **Text morph** | Only the changing letters | Use **Text swap** if the stack cannot split text without breaking accessible names. |
| A number that changes (a count, a price, a total) | **Digit roll** | Each changed digit rolls vertically in the direction of change | Tabular figures keep the width steady (`better-typography`). Values that tick several times a second get no animation. |
| Many values update because the data behind a view changed (period, currency, unit) | **Soft refresh** | Each changed value: a quiet opacity dip and return | Same timing for all values. No travel; the layout must not move. |
| The active option in tabs or a segmented control | **Sliding indicator** | One indicator element moves and resizes between options | Tab switches are high-frequency: `better-ui` gives them instant feedback or a fade of `150ms` or less. Offer a sliding indicator only when the user asks for one, and keep it at that ceiling. Place it without a transition on first paint and resize. |
| Two screens in sequence: list to detail, step 1 to step 2 | **Page slide** | The outgoing and incoming page sections, a short distance in the navigation direction, with a cross-fade | Symmetric, reversed on back. The View Transitions API suits this where supported (_paul-skills_). |

## Resize and reveal

| Element and verb | Pattern | What moves | Notes |
| --- | --- | --- | --- |
| A card or container whose content changes its size | **Resize** | The container's measured size, then the new content fades in | Lowest-overhead option for any "something grew". Measure, then animate; never animate to `auto` without the grid or measurement technique. |
| A placeholder that becomes loaded content | **Skeleton to content** | The skeleton fades out as the content fades in over it | Swap in place; the content must occupy the skeleton's exact box. A one-off "generating" effect is a moment, never a loading state for small or frequently shown UI. |
| A headline group, empty state or onboarding step entering | **Staged entrance** | Semantic chunks (title, body, actions) in sequence | `better-ui` owns the values and the stagger; this skill only decides the chunks. |
| A small badge or count appearing on a trigger | **Badge pop** | The badge only, from a slight offset, with an optional small overshoot | The trigger stays still. |

## Confirm and reject

| Element and verb | Pattern | What moves | Notes |
| --- | --- | --- | --- |
| A completed action (saved, sent, paid) | **Inline check** | A checkmark drawn by stroke, replacing the control's label or spinner | Lower overhead than any overlay celebration. Pair with **Icon cross-fade** when a spinner turns into the check. |
| An invalid field or wrong code | **Error nudge** | The field: a short horizontal shake, once | The error message and border carry the meaning; the shake is never the only cue, and it is gated by reduced motion. |
| A search or filter field being cleared | **Clear fade** | The text: quick fade, optionally drifting toward the clear button | Instant is acceptable; the field must be empty and focused when the motion ends. |

## No pattern

Hover-only decoration (3D tilt, glare, magnetic buttons) and ambient loops (shimmer text, animated loaders) are not state changes. Offer them only when the user asks by name, keep them behind `@media (hover: hover)` or reduced motion respectively, and treat everything else in this file as the default.
