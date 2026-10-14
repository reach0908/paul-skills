# In Progress

Beta. These skills are public on purpose: try them and tell me what breaks. They're excluded from the plugin and the top-level README until they graduate to a stable bucket, they get no docs pages, and they can change or disappear without warning.

The plugin won't give you these. Install one directly:

```bash
npx skills@latest add reach0908/paul-skills --skill=<name>
```

- **[loop-me](./loop-me/SKILL.md)**: Grill yourself into implementable workflow specs over multiple sessions, using the current directory as a stateful workspace. User-invoked.
- **[writing-beats](./writing-beats/SKILL.md)**: Shape an article as a journey of beats, choose-your-own-adventure style. Pick a starting beat, write only that beat, then pivot to the next, until the article reaches a natural end.
- **[writing-fragments](./writing-fragments/SKILL.md)**: Grilling session that mines you for fragments (heterogeneous nuggets of writing) and appends them to a single document as raw material for a future article.
- **[writing-shape](./writing-shape/SKILL.md)**: Take a markdown file of raw material and shape it into an article paragraph by paragraph, arguing format choices at each step.
- **[claude-handoff](./claude-handoff/SKILL.md)**: Hand the current conversation off to a fresh background agent that picks up the work immediately, seeded with a handoff summary via `claude --bg`. User-invoked.
- **[setup-ts-deep-modules](./setup-ts-deep-modules/SKILL.md)**: Wire dependency-cruiser into a TypeScript repo so each package is a deep module: implementation hidden in subfolders, reachable only through its entry-point files, tests exercising it through those. User-invoked.

- **[chief-of-staff](./chief-of-staff/SKILL.md)**: Coordinate a stateful personal work overview. Experimental, outside the default plugin.
- **[upstream-sync](./upstream-sync/SKILL.md)**: Review source repository changes and selectively improve local skills. Awaiting user validation and promotion approval; intended destination is `productivity/`.

- **[break](./break/SKILL.md)**: Renders a component you choose under every scenario that can reach it on a temporary page and stress tests it. User-invoked.
- **[build-design](./build-design/SKILL.md)**: Builds an approved browser prototype, Markdown screen specification, Figma frame or design image with the project's existing tokens and components. Use when asked to implement a supplied design. Model-invoked.
- **[explain-interface](./explain-interface/SKILL.md)**: Explains how a website, a visual effect or an animation was built, from a live URL or a screenshot. User-invoked.
- **[state-machine](./state-machine/SKILL.md)**: Renders every state of a component you choose on a throwaway page, with mock data and a switcher, so you can work on each state. User-invoked.
- **[variant](./variant/SKILL.md)**: Builds multiple variants of a component you're working on and helps you iterate and pick one. User-invoked.

- **[information-architecture](./information-architecture/SKILL.md)**: Maps scoped content to destinations, labels and navigation using the agreed product brief. Model-invoked.
- **[user-flow](./user-flow/SKILL.md)**: Specifies task actions, branches, feedback and recovery with stable state references. Model-invoked.
- **[wireframe](./wireframe/SKILL.md)**: Builds low-fidelity interactive screens and a Markdown specification from agreed content and task flows. Model-invoked.
