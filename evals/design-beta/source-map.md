# Design skill source map

This inventory separates direct source adaptations from independently authored skills. It covers this design work, plus the existing prototype used by the trial. Canonical records live in [skill-sources.json](../../skill-sources.json).

The [quality repair and comparison record](improvement-2026-10-10.md) documents later local instruction changes and their actual execution evidence. These repairs preserve the imported and reviewed source revisions below.

The [2026-10-12 role evaluation](../design-role-parity-2026-10-12/README.md) covers all 17 candidates with separate role tasks. Its [repair record](../design-role-parity-2026-10-12/repairs.md) adds a shared-consumer counting clarification to `interface-review`, short-screen focus and working-state preservation to `variant`, state-aware empty recovery to `better-writing`, and selection-border geometry checks to `better-ui`. These remain adaptations of the same pinned originals, not new source imports.

## Direct adaptations

All 13 rows below use the MIT-licensed Jakub source at `d574cc8a576dc24256ad38268b8d03d86724a1b3`. Each local folder retains its MIT notice and its original supporting files. Paul changes cover packaging, browser operations and the specific language, implementation or review adjustments described in [the beta protocol](README.md).

| Paul skill | Exact original entrypoint | Classification |
| --- | --- | --- |
| [better-accessibility](../../skills/design/better-accessibility/SKILL.md) | [jakubkrehel/skills: skills/better-accessibility/SKILL.md](https://github.com/jakubkrehel/skills/blob/d574cc8a576dc24256ad38268b8d03d86724a1b3/skills/better-accessibility/SKILL.md) | adapted |
| [better-colors](../../skills/design/better-colors/SKILL.md) | [jakubkrehel/skills: skills/better-colors/SKILL.md](https://github.com/jakubkrehel/skills/blob/d574cc8a576dc24256ad38268b8d03d86724a1b3/skills/better-colors/SKILL.md) | adapted |
| [better-interface](../../skills/design/better-interface/SKILL.md) | [jakubkrehel/skills: skills/better-interface/SKILL.md](https://github.com/jakubkrehel/skills/blob/d574cc8a576dc24256ad38268b8d03d86724a1b3/skills/better-interface/SKILL.md) | adapted |
| [better-layout](../../skills/design/better-layout/SKILL.md) | [jakubkrehel/skills: skills/better-layout/SKILL.md](https://github.com/jakubkrehel/skills/blob/d574cc8a576dc24256ad38268b8d03d86724a1b3/skills/better-layout/SKILL.md) | adapted |
| [better-typography](../../skills/design/better-typography/SKILL.md) | [jakubkrehel/skills: skills/better-typography/SKILL.md](https://github.com/jakubkrehel/skills/blob/d574cc8a576dc24256ad38268b8d03d86724a1b3/skills/better-typography/SKILL.md) | adapted |
| [better-ui](../../skills/design/better-ui/SKILL.md) | [jakubkrehel/skills: skills/better-ui/SKILL.md](https://github.com/jakubkrehel/skills/blob/d574cc8a576dc24256ad38268b8d03d86724a1b3/skills/better-ui/SKILL.md) | adapted |
| [better-writing](../../skills/design/better-writing/SKILL.md) | [jakubkrehel/skills: skills/better-writing/SKILL.md](https://github.com/jakubkrehel/skills/blob/d574cc8a576dc24256ad38268b8d03d86724a1b3/skills/better-writing/SKILL.md) | adapted |
| [break](../../skills/in-progress/break/SKILL.md) | [jakubkrehel/skills: skills/break/SKILL.md](https://github.com/jakubkrehel/skills/blob/d574cc8a576dc24256ad38268b8d03d86724a1b3/skills/break/SKILL.md) | adapted |
| [build-design](../../skills/in-progress/build-design/SKILL.md) | [jakubkrehel/skills: skills/build-design/SKILL.md](https://github.com/jakubkrehel/skills/blob/d574cc8a576dc24256ad38268b8d03d86724a1b3/skills/build-design/SKILL.md) | adapted |
| [explain-interface](../../skills/in-progress/explain-interface/SKILL.md) | [jakubkrehel/skills: skills/explain-interface/SKILL.md](https://github.com/jakubkrehel/skills/blob/d574cc8a576dc24256ad38268b8d03d86724a1b3/skills/explain-interface/SKILL.md) | adapted |
| [interface-review](../../skills/design/interface-review/SKILL.md) | [jakubkrehel/skills: skills/interface-review/SKILL.md](https://github.com/jakubkrehel/skills/blob/d574cc8a576dc24256ad38268b8d03d86724a1b3/skills/interface-review/SKILL.md) | adapted |
| [state-machine](../../skills/in-progress/state-machine/SKILL.md) | [jakubkrehel/skills: skills/state-machine/SKILL.md](https://github.com/jakubkrehel/skills/blob/d574cc8a576dc24256ad38268b8d03d86724a1b3/skills/state-machine/SKILL.md) | adapted |
| [variant](../../skills/in-progress/variant/SKILL.md) | [jakubkrehel/skills: skills/variant/SKILL.md](https://github.com/jakubkrehel/skills/blob/d574cc8a576dc24256ad38268b8d03d86724a1b3/skills/variant/SKILL.md) | adapted |

The existing [prototype](../../skills/engineering/prototype/SKILL.md) comes from [mattpocock/skills: skills/engineering/prototype](https://github.com/mattpocock/skills/tree/b0618bc436ad893b3c5e84e55fba86586d34a404/skills/engineering/prototype), including its UI and logic branches. Its classification is adapted; the current Paul changes use Playwright CLI and preserve the original as an available comparison outcome. The comparison mechanism was not imported from Jakub variant.

The supporting [ask-matt](../../skills/engineering/ask-matt/SKILL.md) router also comes from [mattpocock/skills: skills/engineering/ask-matt](https://github.com/mattpocock/skills/tree/b0618bc436ad893b3c5e84e55fba86586d34a404/skills/engineering/ask-matt). This follow-up only clarifies the prototype outcome; it does not add beta skills to the promoted router.

## Independently authored work

The 2026-10-12 `design-browser` repair adds an explicit before/after transition evidence rule after an observed lazy-loading coverage gap. Current and historical trial identities remain separate. This changes the independently authored procedure, not an imported source revision.

The same evaluation adds an in-page navigation check to the independently authored `wireframe` after the composition review found a skip link changing routes. The original handoff, new paired repair tasks and corrected preview remain separate evidence.

| Paul skill | Source material consulted | Boundary |
| --- | --- | --- |
| [design-browser](../../skills/design/design-browser/SKILL.md) | [Microsoft Playwright CLI README](https://github.com/microsoft/playwright-cli/blob/b85c7a736bb473bf55b584e54a09ffa698d6d871/README.md), installed Aside help and user routing requirements | Original evidence procedure with Playwright as the default and Aside for research/general browsing. It is not a fork of a Microsoft or Aside skill. |
| [information-architecture](../../skills/in-progress/information-architecture/SKILL.md) | [Impeccable shape](https://github.com/pbakaus/impeccable/blob/d631a8827f99414d2b6daba4ef08b7f8701751d7/skill/reference/shape.md) | Independent content and navigation contract. There is no one-to-one IA skill being copied. |
| [user-flow](../../skills/in-progress/user-flow/SKILL.md) | [Impeccable shape](https://github.com/pbakaus/impeccable/blob/d631a8827f99414d2b6daba4ef08b7f8701751d7/skill/reference/shape.md), [onboard](https://github.com/pbakaus/impeccable/blob/d631a8827f99414d2b6daba4ef08b7f8701751d7/skill/reference/onboard.md), [harden](https://github.com/pbakaus/impeccable/blob/d631a8827f99414d2b6daba4ef08b7f8701751d7/skill/reference/harden.md) | Independent task-transition contract. Selected ideas about context, task value and recovery inform it; no onboarding or implementation command is copied. |
| [wireframe](../../skills/in-progress/wireframe/SKILL.md) | [Impeccable new-work](https://github.com/pbakaus/impeccable/blob/d631a8827f99414d2b6daba4ef08b7f8701751d7/skill/reference/new-work.md), existing Paul prototype interface | Independent screen/state contract with optional use of prototype. Impeccable has a wireframe presentation path in this reference, not a standalone wireframe skill being forked. |

The three planning roles are original authoring, not copies renamed from Impeccable. References are recorded as influences at the exact inspected revision. A call to another installed skill is a runtime dependency, not copied source. Directly copied instructions would instead require an origin record and retained notices.

## Researched but not imported in this slice

UI UX Pro Max, Emil Kowalski, ibelick, React Doctor and Raphael Salaja informed the broader source review. None is a direct source of the 13 Jakub adaptations or a new copied skill in this slice. Specialized motion and design-system work remains a separate proposal.

The follow-up [local harness benchmark](../../.scratch/design-harness-benchmark-20261010/benchmark.md), dated 2026-10-10, compares those sources with gstack, BMAD and an explicitly unconfirmed Cursor pstack candidate. These are researched candidates, not newly imported origins. No code or instructions from the added harnesses were copied into the current beta skills.

## Audit scope

On 2026-10-09, 65 upstream file hashes (including the source license) were verified against pinned Jakub Git objects, and all 13 local adaptation tree digests matched their registered values before this follow-up. The byte-level record is local at `.scratch/design-skills-beta/source-audit-20261009.json`. This confirms file provenance and drift status, not quality or successful behavior. Later changes retain origin revisions and update only the reviewed local digest with an explicit decision.
