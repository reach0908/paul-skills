# Conversation and prototype walkthrough source review

## Decision and scope

The office-hours adaptation preserves the full conversational sequence rather than reusing only a question pool. The second new skill is prototype-user-test, an original AI usability walkthrough and post-task interview protocol. A general product-review/red-team skill is deliberately not implemented after the user clarified the intended task. prototype-user-test serves design evaluation; all new skills remain in-progress until human validation and explicit promotion.

Only generalized instructions and synthetic fixtures are published. Private products, session excerpts and participant data remain in their owning workspaces.

## Immutable direct inputs

- gstack office-hours/SKILL.md.tmpl and sections/phase-2a-startup-diagnostic.md, phase-2b-builder-brainstorm.md, design-and-handoff.md at dbf400ec3f1ffb96a429f0d0b29ca932b3d6c6f0. Read all listed conversational source contents; exact hashes are in skill-sources.json. The gstack MIT notice is included unchanged.
- PM Skills pm-market-research/skills/competitor-analysis/SKILL.md at c68487d721e419ec87af1ae6412a842978eab785 supplies the product-brief benchmark reference. The existing PM Skills MIT notice is retained.
- Existing problem/brief/experiment direct inputs and historical imported/reviewed revisions remain unchanged. New local edits get new digests and explicit local decisions; this is not a repository-wide upstream reconciliation.

## Office-hours behavioral map

| Original mechanism | Local implementation | Deliberate adapter or difference |
| --- | --- | --- |
| Context and chosen purpose, startup stage | SKILL Phase 1 | Project instructions/actual decisions replace gbrain, profiles and global design searches |
| Startup diagnostic and six stage-routed questions | references/startup.md | Preserve specificity, stance, follow-ups, framing checks, status quo, wedge, observation and future-fit. Match consumer/internal stakes; personal names and discomfort are not proof |
| Builder posture and generative questions | references/builder.md | Preserve adjacent possibilities, concrete imaginative scene, smart-skip and build-oriented closing; omit mandatory commercial proof |
| Related designs and landscape | SKILL Phases 2 and 2.75 | Read authorized project artifacts; research owns cited external investigation; findings feed premises and product choices |
| Premise challenge and revision | SKILL Phase 3 | Stop for actual agreement/correction; known user decisions survive resumption |
| Optional cold read | SKILL Phase 3 | Native fresh-context review when authorized, no mandatory provider or cross-model claim |
| Two or three alternatives and real choice before final doc | SKILL Phase 4 | Minimal/long-term/lateral approaches retained; product experiences can precede technical architecture. Existing selected choices do not need reapproval |
| Concise decision record and lineage | record-and-handoff.md | Reuse canonical product-brief/PRD; one authorized workspace, no dual-write to ~/.gstack |
| Adversarial document review and bounded convergence | record-and-handoff.md | Five review dimensions, up to three rounds, original findings and unresolved blockers retained. Native evidence replaces gstack review JSON helper; no invented quality score. Failure remains unreviewed |
| Show record, approval and specific assignment/reflection | record-and-handoff.md | Preserve choice/approval waits; user skip and existing authorization prevail. Contextual reflection is not longitudinal founder profiling |
| Visual generation, persona/promotion, telemetry/runtime | Existing design roles / omitted | No gstack binaries, paid mockups, profile storage, promotional closing or startup daemon dependency |

The original startup escape hatch attempts two more questions before honoring a repeated skip. Paul honors the first direct skip instruction. Opinionated positions remain evidence-bounded rather than claiming certainty about unobserved demand. These are intentional behavioral adaptations, not claims of verbatim parity.

## Prototype-user-test contract

The moderator keeps author intent and expected outcomes in a separate packet. A fresh participant receives only a neutral task, UI access, permission/stop bounds and its own evidence path. It uses the visible interface, freezes the attempt, then answers neutral follow-up questions in the same context. The moderator compares recorded actions with intent afterward. Author context, source-code inspection or another participant's output invalidate the fresh claim for the exposed portion.

This is original authoring. Existing design-browser is a dependency, not imported third-party text. There is no copied strategy-red-team material. A fresh AI walkthrough remains distinct from a human usability study, a general interface audit and product approval.

## Invocation and packaging

All five candidates are model- and user-reachable so natural requests and permitted skill-to-skill routing work. office-hours triggers on deliberate idea exploration, not every product update. prototype-user-test triggers on fresh AI task/interview observations. ask-matt recommends the optional candidates only when separately available and keeps user-invoked specialist roles as human choices. The promoted plugin list and top-level skill index are unchanged.

Automated checks and isolated behavioral runs establish only their named properties. Original-quality outcome parity, natural discovery on every host and human acceptance remain to be tested; no promotion is authorized here.
