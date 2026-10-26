# Patterns

One row per pattern: match the element the user sees and what it does, then read the row's notes. The idea of choosing by visible element and verb comes from transitions.dev's decision rules; this list, its grouping and its notes are this skill's own and cover only common interface elements. For anything not listed, offer two or three candidate patterns and let the user pick.

## Open and close

| Element and verb | Pattern | What moves | Notes |
| --- | --- | --- | --- |
| A menu, popover, select list or date picker that opens from a trigger | **Anchored grow** | The surface: opacity plus a slight scale from just under `1`, origin at the trigger edge | Asymmetric. Flip the origin when placement flips. Prefer this over a modal whenever the content fits beside its trigger. |
| A centered dialog with a backdrop | **Centered scale** | Surface: opacity plus slight scale from its center. Backdrop: opacity only | Asymmetric. The backdrop never scales or blurs in. Native `<dialog>` needs the discrete-transition approach to animate its close. |
| A drawer or sheet attached to a screen edge | **Edge slide** | The sheet: full translate from its edge. Backdrop: opacity | The one place full-distance travel is right, because the edge is where it lives. It closes to the same edge, using `better-ui`'s full-exit values. |
| A panel that appears inside a region of the page (an inspector, a details pane) | **Region reveal** | The panel content: short slide toward its resting place plus opacity | Asymmetric. If only the size of the region changes, use **Resize** instead. |
| A toast or snackbar | **Edge toast** | The toast: short travel from the edge it is anchored to plus opacity; older toasts in a stack shift to make room | Asymmetric; it leaves toward the same edge. An actionable or error toast stays until dismissed (`better-accessibility`). |
| A tooltip or hint on hover or focus | **Intent tooltip** | The bubble: opacity plus a very slight scale from its arrow side | Brief intent delay on the first open, none for neighbors while one is open, instant close. Focus opens it with no delay. |
| A disclosure, FAQ item or collapsible settings group | **Height reveal** | The body's height via a grid-row track from `0fr` to `1fr`, content fading in; the chevron flips | Symmetric. Padding goes on the inner element, never on the collapsing track. |

## Swap in place

| Element and verb | Pattern | What moves | Notes |
| --- | --- | --- | --- |
| Two icons in one slot (play/pause, copy/copied) | **Icon cross-fade** | Both icons, overlapping | `better-ui` owns this with exact values: call the Skill tool with "better-ui" and use its icon recipe. |
| A label whose text changes in place ("Save" to "Saving" to "Saved") | **Text swap** | Old text exits a few pixels one way, new text enters from the other | Symmetric. Reserve the wider label's width so neighbors do not jump. |
| A number that changes (a count, a price, a total) | **Digit change** | The changed digits only, vertically in the direction of change | Tabular figures keep the width steady (`better-typography`). Values that tick several times a second get no animation. |
| The active option in tabs or a segmented control | **Indicator move** | One indicator element moves between options | Tab switches fall under `better-ui`'s high-frequency rule. Offer a moving indicator only when the user asks for one, within that rule. Place it without a transition on first paint and resize. |
| Two screens in sequence: list to detail, step 1 to step 2 | **Page slide** | The outgoing and incoming page sections, a short distance in the navigation direction, with a cross-fade | Symmetric, reversed on back. The View Transitions API suits this where supported (_paul-skills_). |

## Resize and reveal

| Element and verb | Pattern | What moves | Notes |
| --- | --- | --- | --- |
| A card or container whose content changes its size | **Resize** | The container's measured size, then the new content fades in | Lowest-overhead option for any "something grew". Measure, then animate; never animate to `auto` without the grid or measurement technique. |
| A placeholder that becomes loaded content | **Skeleton to content** | The skeleton fades out as the content fades in over it | The content must occupy the skeleton's exact box. A one-off "generating" effect is a moment, never a loading state for small or frequently shown UI. |
| A headline group, empty state or onboarding step entering | **Staged entrance** | Semantic chunks (title, body, actions) in sequence | `better-ui` owns the values and the stagger; this skill only decides the chunks. |
