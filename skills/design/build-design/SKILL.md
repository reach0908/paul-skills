---
name: build-design
description: Builds an approved browser prototype, Markdown screen specification, Figma frame or design image with the project's existing tokens and components. Use when asked to implement a supplied design.
metadata:
  provenance: "https://github.com/reach0908/paul-skills/blob/main/skill-sources.json"
---

# Build design

This skill turns a design into code that matches it. It reads the design at its source, builds with what the project already has, then compares the result against the design before calling it done.

The approved design supplies visual intent. Read the existing decision record before asking again. Record unapproved differences as deviations and give the user a concrete choice when a decision is missing.

It owns no domain rules. Preserve working accessibility and required behavior when visual fidelity conflicts with them. Report the smallest usable alternative and its approval status as a deviation. Contrast is a requirement in `better-accessibility` and a measurement in `better-colors`. Focus and semantics are `better-accessibility`, type is `better-typography` and spacing and structure are `better-layout`. Palette is `better-colors`, copy is `better-writing` and surfaces, icons and motion are `better-ui`. Reviewing finished work is `interface-review`, exploring alternatives is `variant` and stress testing a component is `break`. These user-invoked skills are next-step choices for the human.

For browser evidence, call the Skill tool with "design-browser" and pass the task purpose and expected observations. Without a Skill tool, read its installed SKILL.md. Follow its tool routing; if unavailable, use the caller's tool policy and installed help, and report verification limits.

## 1. Read the design at its source

For a browser prototype or Markdown screen specification, read [browser-and-spec.md](browser-and-spec.md). Resolve the chosen revision, routes, states, widths and existing decisions before implementation.

A Figma link means the Figma MCP. Search the available and deferred tools for `figma` before saying it is unavailable, since the server often sits under a name you did not expect. A server that lists only an authenticate tool is connected but signed out, so ask the user to authenticate. With no Figma tool at all, ask the user to connect one, and do not build from memory or guesswork meanwhile. [figma.md](figma.md) holds which tools to call and what each returns.

A screenshot or exported image has no values to read. Sizes are ratios to the capture, so state the scale you assumed and treat every measurement as an estimate. Use supplied structured values when available; Figma is optional for a browser or specification input.

Scope the run to the frames named. Frames that show the same thing at different widths are one piece at several breakpoints, not separate pieces.

This step is done when every scoped screen and state has a source locator and known or explicitly unknown spacing, size, radius, color, type and component values. Capture rendered references when available. Keep specified, browser-computed and image-estimated values distinct.

## 2. Map the design onto the project

Read the project's tokens and component library before writing anything. Then map every design value to what exists:

| In the design | In code |
| --- | --- |
| A bound variable or style | The token with the same name or the same value |
| A raw value that equals a token | That token |
| A raw value with no token | The nearest existing token, listed in the report as rounded |
| A component instance | The export and variant traced from the reference's actual call site, rather than a name match alone |
| A component instance with no project equivalent | Plain markup in place, listed as a deviation, and ask whether a component should exist |
| A one-off group of layers | Plain markup in place, not a new component |

Never add a token, a component variant or an arbitrary value to hit a number. Stop and ask which way to go when rounding would visibly change the design. That means more than 2px on spacing or size, or a color landing on a different step.

When the request reuses existing UI, resolve the [component mapping](browser-and-spec.md#map-existing-ui-before-editing) before editing. A similar name or appearance does not identify the requested component.

Check what data the design needs and wire it to what exists. Where the backend for part of it does not exist yet, build that part as UI fed by props and name it in the report as unwired.

## 3. Build the agreed scope and preserve required states

Implement the agreed screens, responsive behavior and states. Preserve existing loading, error, empty, permission and keyboard behavior even when the reference omits them. Use established components for required states absent from the design, and record the unresolved visual treatment. A missing frame does not authorize deleting a working branch or inventing a new product flow.

Leave everything around the piece as it was. No neighbouring copy edits, no icon swaps, no "while I was here" cleanups. A diff wider than the design is the most common way this goes wrong.

## 4. Compare against the design

Render the build at each specified width and compare the properties **Read the design at its source** collected. With a visual reference, walk the build beside its matching screenshot, element by element. With a Markdown-only specification, compare the rendered values, content, states and behavior with its stated requirements; label unspecified visual choices as project defaults or unresolved assumptions. "Gap is 12px, design is 16px" is a finding. "Feels a bit tight" is not.

With a browser at hand, capture the build at each width and retain the corresponding measurements or state observations. Without one, hand over the local URL with the widths to check and say the comparison is unverified. A rendered build checked against Markdown can satisfy that specification; it cannot establish pixel fidelity to an image that was never supplied.

Fix mismatches within the agreed scope, then compare again. Record the design revision, code revision or working-tree digest, route, state and viewport with each comparison. Finish when each difference is corrected, an agreed rounding, or a recorded deviation/question. Keep usability conflicts visible even when the pixels match.

For component reuse, verify the mapped export is used at the target and compare its link destination and keyboard action in matching states. A passing build or screenshot alone cannot establish that the intended component was reused.

## 5. Report and stop

| Element | Design | Built | Status |
| --- | --- | --- | --- |
| Card padding | 20px | `p-5` | Matches |
| Title size | 15px | `text-sm`, 14px | Rounded to token |
| Badge | Filled pill | Text label | Deviates, asked: no badge component exists |

Then list, one line each, and omit a list with nothing in it:

- **Unwired.** What renders from props until the backend exists.
- **Missing states.** What the design does not draw.
- **Domain conflicts.** Where the design breaks a rule, with the owning skill.
- **Deviations.** The reference difference, reason, usable alternative and approved or pending status.

Close by saying where the build is running and at which widths you compared.

## Before you finish

| You notice | Fix |
| --- | --- |
| "Figma isn't connected" written before any tool search | Search the tools for `figma` first |
| A Figma-derived value backed only by an estimated screenshot measurement | Read it from the Figma design context |
| A specification-based value presented as measured from an absent image | Cite the supplied requirement or mark the project-default assumption |
| An arbitrary utility such as `w-[343px]` or a raw hex in the diff | Map it to a token, or ask if rounding shows |
| A new file under the components directory for a frame that is not a component | Inline it as plain markup |
| A required loading or error branch absent from the reference | Preserve working behavior and record its unresolved visual treatment |
| Unrelated files changed by this run | Remove only this run's unrelated edits; preserve pre-existing user work |
| Fidelity would remove focus, lower required contrast or break keyboard access | Preserve usable behavior and report the deviation with its owner and approval status |
| A comparison claimed with no rendered build evidence | Capture each specified width and the required state observations, or say it is unverified |
| Hard-coded sample data with no mention in the report | List it under **Unwired** |
