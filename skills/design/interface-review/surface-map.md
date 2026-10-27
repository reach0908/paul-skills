# Surface map

How the changed lines become the domain map: which of the six `better-*` owners the review loads. Classify the lines a hunk adds or removes, on both sides, after [exclusions](scope-resolution.md#excluded-paths). A file's extension or the change's stated intent never decides a row.

## Classify each changed line

A line falls in every row it matches. A domain loads when any changed line falls in a row marked for it.

| Surface | Changed lines that count | Accessibility | Layout | Writing | Typography | Colors | UI |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Markup | Rendered elements and components, their attributes (`aria-*`, `role`, `tabindex`, `alt`, `href`, `type`, `disabled`), event handlers on elements, focus calls, and the conditions that choose which element or state renders (loading, empty, error, disabled, open) | load | load | | | | load |
| Copy | A user-facing string added, removed or reworded: text nodes, rendered literals and constants, labels, `alt`, `aria-label`, `title`, `placeholder`, messages, translation catalog entries | load | load when a string is added or gets longer | load | load | | |
| Color | Color values and tokens, `color`, `background`, `border-color`, `outline-color`, `fill`, `stroke`, shadow color, `opacity`, gradients, `color-scheme`, dark-mode queries, color utility classes | load | | | | load | |
| Type | `font-*`, `line-height`, `letter-spacing`, `text-*`, `white-space`, `word-break`, `overflow-wrap`, `hyphens`, `line-clamp`, type tokens and utilities, font files, an element whose type changes heading level or text role | load | | | load | | |
| Box and flow | `display`, `flex*`, `grid*`, `gap`, `margin`, `padding`, sizes and their min/max, `position`, `inset`, `overflow`, `order`, `aspect-ratio`, media and container queries, `dir` and logical properties, spacing tokens and utilities | load | load | | | | |
| Surface and motion | `border-radius`, `box-shadow`, border style and width, `transition`, `animation`, `@keyframes`, `transform`, `cursor`, `z-index`, hover and active styling, scroll and overscroll behavior, icons, SVG and images | load | | | | | load |
| Unclassified | A new file with rendered output, a style declaration or utility class this table does not name, a changed shared primitive or theme object whose rendered effect the diff does not show | load | load | load | load | load | load |

A changed `class` or `className` is classified by the declarations its old and new classes set; read them. A changed design token is classified by its value, and its consumers are reviewed in the domains that value selects: a color token's consumers are checked for contrast, not re-reviewed for layout.

## No UI surface

The change has no UI surface when no changed line falls in any row. Server and API code, migrations, data transforms, tests, build and CI configuration, types, comments, logging and performance work (memoization, caching, request batching, prefetch) qualify when the rendered elements, render conditions, strings, classes and styles stay identical.

Data that flows through an unchanged component is not a surface: a list's contents, a count or an API payload value renders through code this change did not touch. A value the interface shows verbatim, such as a label or message in a constants file, is copy.

A change with no UI surface has no blast radius to expand.

## Ambiguity loads

A line that might fall in a row falls in it. When you cannot tell whether a change reaches rendered output, it is unclassified and all six load. The map can grow during review, when an owner's check reveals a changed surface the map missed; it never shrinks.

## Domain map

Record one row per domain, in the review order, and pass it in the handoff:

| Domain | Load | Changed lines |
| --- | --- | --- |
| Accessibility | yes | `theme/palette.css:14` color token; `src/Sidebar.module.css:8-10` flex direction |
| Writing | no | no copy in the change scope |

A skipped domain's coverage row is `Not reviewed: no <surface> in the change scope`, naming the surfaces whose rows would have loaded it: `no copy`, `no copy or type`, `no color`. It is never `Clear`, which claims an inspection that did not happen.
