## What it does

Builds and audits color ramps, semantic tokens, notation and contrast. It measures the actual color pair being judged and reuses the project’s existing system. A palette preference is not a failure; a broken role mapping or failing measured pair is.

## When to reach for it

Type `/better-colors`, or the [agent](https://www.aihero.dev/ai-coding-dictionary/agent) reaches for it automatically when a color system or contrast check fits.

| Need | Work |
| --- | --- |
| A new palette | Define the roles that consume each ramp step |
| Existing tokens | Check semantic mapping and theme consistency |
| A suspected contrast failure | Measure the relevant pair and report the observation |

[better-accessibility](https://github.com/reach0908/paul-skills/blob/main/docs/design/better-accessibility.md) owns which accessibility requirement applies.

## Every step has a job

Color values serve roles such as text, background, border and selection. Components consume semantic tokens so a theme can change those roles without scattering new values through every component.

## Common questions

**Will it force a new notation or design system?**

No. A consistent existing system is retained. New ramps and tokens need a role that actually uses them.

**Can it estimate contrast from a screenshot?**

A reported ratio must be measured. Transparency, gradients and CSS precedence can change the pair, so the report must state what was measured and what remains uncertain.

## It's working if

- Contrast claims identify their colors, backgrounds and measurement method.
- Token names describe roles and keep the same meaning across themes.
- Unused ramp steps and unexplained palette expansion are avoided.

## Where it fits

A standalone color-system role used by [better-interface](https://github.com/reach0908/paul-skills/blob/main/docs/design/better-interface.md). [better-accessibility](https://github.com/reach0908/paul-skills/blob/main/docs/design/better-accessibility.md) interprets required thresholds; [ask-matt](https://github.com/reach0908/paul-skills/blob/main/docs/engineering/ask-matt.md) helps choose between a focused and complete review.
