# Implementation

How to realise a chosen pattern in the stack the project already has, the traps that break transitions in practice, and the fallback values. The traps draw on transitions.dev's common-mistakes list, in this skill's own words; sections marked _paul-skills_ are additions with no transitions.dev counterpart.

## By mount mechanism

The exit is where transitions fail, because the element must stay rendered until its exit ends.

| Mechanism | Enter | Exit |
| --- | --- | --- |
| Class or attribute toggle on an element that stays in the DOM | Transition between the closed and open rules | Same transition in reverse. Nothing to clean up. |
| `display: none`, `hidden`, native `popover` or `<dialog>` | `@starting-style` supplies the from-state (_paul-skills_) | `transition-behavior: allow-discrete` on `display` (and `overlay` for top-layer elements) keeps it visible through the exit. `better-ui`'s enter-exit reference has the recipe; browsers without support show and hide instantly, which is an acceptable fallback. |
| Conditional render in a framework | Mount in the closed state, then switch to open on the next frame, or use the motion library already present | Keep it mounted in a closing state and unmount after the exit duration, or use `AnimatePresence` where Motion is installed |
| Headless library (`data-state="open" \| "closed"`) | Style `[data-state="open"]` and its `@starting-style`, or the library's documented enter hook | Use the library's documented exit support (for example a `forceMount` or presence prop); never fight it with your own timers |

## By stack

- **Plain CSS or CSS modules.** Put the transition on the element, with the closed state as the base rule and the open state on the attribute or class. Name every property.
- **Tailwind** (_paul-skills_). Use `data-[state=open]:` or `aria-expanded:` variants for the open state, `transition-[opacity,scale]` style property lists rather than `transition-all`, and `motion-safe:` on movement, scale and blur. Tailwind 4 has `starting:` for `@starting-style`; Tailwind 3 does not, so use the class-toggle approach there.
- **Motion or Framer Motion, only if already installed** (_paul-skills_). `AnimatePresence` for conditional exits, `initial={false}` for state swaps that must not animate on first render, `MotionConfig reducedMotion="user"` for the preference. `better-ui` sets which package name to import and the spring settings.
- **View Transitions API for page and step swaps** (_paul-skills_). Wrap the DOM update in `document.startViewTransition` after feature-detecting it, give the incoming and outgoing regions a `view-transition-name`, and style `::view-transition-old` and `::view-transition-new`. Without support the update simply happens, which is the fallback. Gate the animation with a reduced-motion media query on those pseudo-elements. Do not use it for frequent in-page toggles.

## Traps

- **Exit cleanup timing.** If a closing class or state is removed by a timer, that timer must match the exit duration, and opening again during the exit must clear it. Otherwise the next open starts from the closing scale instead of the resting closed state.
- **Replaying a one-shot animation.** Re-adding the same class does nothing unless the browser sees the removal first. Remove it, force a reflow (read `offsetWidth`) and add it again, or key the element so the framework remounts it.
- **Animating the container.** Animate the inner piece that carries the meaning. Animating a page container instead of its sections, or a trigger instead of its badge, moves things that should stay still.
- **`transition: all`.** It lets unrelated style changes animate (colors on a theme switch, layout on a resize). Name the properties.
- **Collapsing with padding on the track.** In a grid-row height reveal, padding on the collapsing track leaves a strip that never closes. Put the padding on the inner element.
- **Path morphing.** Animating an SVG `d` path works only in Chromium. To turn a chevron, flip it with `scaleY(-1)` or rotate it, which works everywhere.
- **An indicator that animates in on load.** A sliding tab indicator or similar must be placed with transitions disabled on first paint and on resize, then re-enabled; otherwise it slides in from zero.
- **`will-change` everywhere.** Add it only for observed first-frame stutter, naming the animated property, as `better-ui` sets out.

## Fallback values

These cover only what `better-ui` leaves open; everything it sets (enter, exit and drawer durations, easing, blur, stagger, the high-frequency ceiling) comes from `better-ui`. They are transitions.dev's published defaults at the pinned revision, cited as starting points; report them as fallbacks so the user can replace them with project tokens.

| Use | Fallback |
| --- | --- |
| Pre-scale for an anchored grow / centered scale | `0.97` / `0.96` |
| Intent delay before a tooltip | `80ms` |
| Swaps that run the same both ways (height reveal, page slide) | `250ms` |
