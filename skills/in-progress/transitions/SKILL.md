---
name: transitions
description: "Transition choice. Picks and builds the enter, exit or state-change transition for one UI element: a dropdown, modal, drawer, toast, tooltip, accordion, tabs, page or step swap, or a text, number or icon change. Use when an element pops with no motion or the user asks which transition fits. Tuning existing motion values belongs to better-ui, change reviews to better-interface, reduced-motion audits to better-accessibility."
metadata:
  provenance: "https://github.com/reach0908/paul-skills/blob/main/skill-sources.json"
---

# Transitions

This skill picks the transition **pattern** for one element's state change, choreographs it and builds it in the project's existing stack. The pattern is the decision: which pieces move, from where, in what order, and how the exit differs from the enter. Values come last and mostly come from elsewhere.

The selection method, choreography rules and implementation traps are adapted from [transitions.dev](https://transitions.dev) by Jakub Antalik, rewritten in this skill's own words. No transitions.dev snippet, token file or catalog entry is included; its license forbids republishing the collection.

## Ownership

`better-ui` owns exact motion values, and wherever it gives one, its value wins over anything here. Before writing any value, call the Skill tool with "better-ui" and read its motion sections. `better-accessibility` owns the reduced-motion requirement, which `better-ui`'s opacity cross-fade fallback satisfies. Reviews of what a change introduced belong to `better-interface`, and retuning motion that already exists belongs to `better-ui`. When the request turns out to be one of those, say which skill owns it and stop.

## 1. Read the state change

Before choosing anything, establish five facts from the code:

- **Element**: what the user sees change (a menu anchored to a button, a centered dialog, a value in a table cell).
- **Verb**: open/close, swap in place, resize, reveal after loading, move between positions, or confirm/reject.
- **Frequency**: how often one user triggers it. Keystrokes, row hovers and tab switches are high-frequency, and `better-ui` gives them no animation or a fade of `150ms` or less. Say so instead of designing a pattern for them.
- **Mount mechanism**: conditional render, `display: none`, the `hidden` attribute, a native `<dialog>` or `popover`, a headless-library `data-state`, or a class toggle. This decides whether an exit can run at all.
- **Stack**: plain CSS, CSS modules, Tailwind (which major version), or a motion library already in `package.json`, plus any motion tokens the project defines.

The step is done when you can state all five in one line each. An unknown mount mechanism or stack is not a guess: read the component and `package.json` until it is known.

## 2. Match one pattern

Look the element and verb up in [references/patterns.md](references/patterns.md) and pick **one** pattern. Match on what the element is and does, never on how it is currently styled.

- When two patterns fit, prefer the **lower-overhead** one: a resize over a panel reveal, a dropdown over a modal, an inline confirmation over a celebratory overlay. Take the heavier pattern only when the design clearly calls for that surface.
- When nothing fits with confidence, offer two or three candidate patterns, one line each on what would move, and let the user pick. A guessed pattern is worse than a question.
- When the user named a pattern, use it, and mention a lower-overhead alternative only if theirs fights the element (a slide-in page for a two-item menu).

## 3. Choreograph

These rules apply to every pattern:

- **Origin follows the trigger.** An anchored surface grows from the edge nearest its trigger, so set `transform-origin` from its actual placement, including when it flips above the trigger. A centered surface scales from its center. A surface entering a region slides from the side it belongs to.
- **Move the pieces, not the frame.** Animate the part that carries the meaning: the dot on a badge, the sections inside a page, the content chunks inside a card. Animating the outer container drags everything inside along and usually triggers layout.
- **Exits are quieter than enters.** An open/close pair closes faster and with less travel than it opens, using `better-ui`'s exit values. Swaps that the user moves back and forth through (a tab indicator, an accordion, a page or step pair, an icon or text swap) are the exception: they run the same duration and easing both ways.
- **Overshoot belongs to small entrances only.** A badge or count may land with a slight overshoot when the product's tone allows it. A close never overshoots, and motion-library springs keep `better-ui`'s `bounce: 0`.
- **Delay only for intent.** A hover-triggered surface such as a tooltip waits briefly so a passing pointer does not fire it, and once one is open its neighbors open at once. Never delay a close or a hover-out. When motion feels late, shorten the duration before adding any delay.
- **Stagger infrequent entrances only.** Use `better-ui`'s stagger between semantic chunks, and stop staggering once the last chunk would start more than about `300ms` after the first: stagger the first few items and bring the rest in together.
- **Small distances.** Enter and exit travel stays within `better-ui`'s small translate. Travel past about `40px` reads sluggish, except for a drawer or page whose destination carries meaning. A pre-scale below about `0.9` reads as a zoom rather than an appearance.
- **Interruptible by default.** Toggled states use transitions, which reverse mid-flight. Keyframes are for sequences that play once, as `better-ui` sets out.

## 4. Build it in the project's stack

Read [references/implementation.md](references/implementation.md) before editing. It covers each mount mechanism and stack, the implementation traps, and the fallback values to use only where neither the project nor `better-ui` defines one.

Value precedence is fixed: the project's own motion tokens, then `better-ui`'s exact values, then the fallback table. Keep the diff to the files the transition needs. Never add a motion library or a token file the project does not already use.

## Before you finish

| Check | Done when |
| --- | --- |
| Properties | Every transition names its properties; no `transition: all` or Tailwind `transition-all` |
| Exit | The exit runs before the element unmounts or hides, and a reopen during the exit starts from the resting closed state |
| First render | State indicators (tab pill, selected icon) appear in place on load and only animate on change |
| Reduced motion | Movement, scale and blur run only under `prefers-reduced-motion: no-preference`; the opacity fade remains |
| Static cue | The new state is legible without the motion (label, icon, color or focus move) |
| Value sources | Every value is traceable to a project token, `better-ui`, or the fallback table |
| Verification | Rendered behavior checked through the `design-browser` skill when a browser is available; otherwise each unrendered check is reported as `Not verified` |

## Report

State the five facts from step 1, the pattern chosen and why (including the lower-overhead alternative you rejected, if any), each value with its source, the files changed, and every check you could not run. If the user wants a ready-made recipe instead, they may install one themselves from transitions.dev (for example `npx transitions-dev add <name>`); offer this only as their option, and never run it.
