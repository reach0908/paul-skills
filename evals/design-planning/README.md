# Design planning beta

Three independently authored skills connect an agreed PM brief to screen structure. They live in `in-progress/`, outside the promoted plugin and router. Their [source map](../design-beta/source-map.md) distinguishes influences from direct adaptations.

## Contracts

| Skill | Decision owned | Inputs | Output | Completion signal |
| --- | --- | --- | --- | --- |
| information-architecture | Where content belongs and how it is found | PM scope, content, retrieval tasks, existing navigation | Destinations, labels, navigation and content coverage in Markdown | Each scoped content type and retrieval task maps to a destination or explicit unresolved dependency |
| user-flow | What each action does and how the task recovers | Task outcome, product policy, relevant destinations | State IDs, authoritative transition table, walkthrough results | Each reachable scoped branch reaches success, intentional exit or a named dependency |
| wireframe | How screens expose information and actions | Content, destinations, task transitions and existing UI context | Local interactive wireframe and Markdown screen/state mapping | Each scoped path is operable and observed, or explicitly unverified/unwired |

A later stage consumes locators and IDs rather than rewriting the brief. Document names and separate files are optional; the decisions are what matter. An existing structure can be retained. Simulated actions and unresolved policies stay visible. A runnable artifact is neither user acceptance nor production readiness.

The three skills are Model-invoked, also callable explicitly. This resolves the research proposal's tentative User-only choice in favor of composability with narrow task descriptions. Their scope is the requested role; they do not automatically run the remaining stages. User-only beta skills such as variant and state-machine remain explicit user choices.

## Development scenario

[brief.md](brief.md) is a synthetic Korean reading-library task, independent of the live INFLFEED article. It supplies product decisions and raw content, not a preferred answer. Use fresh output directories and give the executor the brief and the three skill paths. For browser work, expose design-browser and the installed Playwright CLI. Supply prototype only if an actual structural comparison is requested.

The first exercise is a candidate development smoke, not a no-skill comparison, blind holdout or model ranking. Automatic host discovery is separate from explicit skill-path execution. A passing package checker does not prove this workflow works.

## Evaluation ownership

The maintainer checks outputs after execution for scope, content coverage, ID continuity, transition consistency, preservation of the supplied navigation and policies, browser behavior, and honest limits. Keep the executor's outputs and runtime observations together. Record failed or interrupted attempts and repairs, with missing telemetry as null. The executor receives the brief, not this assessment paragraph or previous conclusions.

Separate authoring from actual use: the source map and registry prove attribution; package checks prove inventory consistency; a browser scenario demonstrates bounded behavior; only human use can accept the designs and authorize promotion.

## First development exercise

[Results recorded on 2026-10-10](results-2026-10-10.json) describe one independent executor using explicit skill paths. The executor created IA, a transition contract, a screen specification and a single runnable Korean wireframe. Official Playwright CLI observations cover selected success, failure, retry, pending, empty, unavailable and removal paths at 1280×900, with long-content, keyboard and navigation checks at 390×844. The record preserves untested branches and a superseded early observation made before rendering completed.

The maintainer checked stage continuity and scope, read the execution evidence and viewed the desktop and mobile captures. This was an artifact audit, not a second browser replay. Inputs and outputs are hashed; detailed artifacts remain in the ignored local directory `.scratch/design-planning-trial-20261009/`. The fixture is synthetic, the interface uses local memory and timers, and no comparative quality, human acceptance or promotion follows from this exercise.

The later [browser-routing clarification](../design-beta/browser-routing-2026-10-10.md) changes the current instructions. The saved manifest and results identify the earlier tested inputs and are intentionally not restamped as validation of the new routing policy.
