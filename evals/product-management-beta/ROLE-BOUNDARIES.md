# Product → design → engineering

This comparison uses the actual in-progress design skill files identified in [design-inputs.json](design-inputs.json), read without modifying or copying their work. They are ongoing beta work, not promoted plugin behavior. Existing engineering and productivity boundaries use the worktree baseline.

| Phase | Responsibility | Input preserved | Output and boundary |
| --- | --- | --- | --- |
| Product | problem-discovery, product-brief, experiment-design | Supplied situation, purpose, evidence and user decisions | Problem/decision brief or assumption test. Leave IA, screens and technical implementation to their owners. |
| Design | information-architecture, user-flow, wireframe, prototype, variant, state-machine, interface-review, better-* and break | Scope, product rules, permission/persistence/completion semantics, decision reasons and evidence status | IA, task transitions, screens, comparisons or interface verdicts. A walkthrough/browser pass is not actual-user effect or demand. |
| Engineering | to-spec, to-tickets and implementation/verification roles | Canonical product contract plus latest design artifact IDs/revisions and remaining gaps | Technical specification, slices, code and checks. Local verification is distinct from deployed product behavior and user acceptance. |

## The experiment-design overlap test

A request for clipping at 320px, keyboard focus, coded-state rendering, visual alternatives or reference fidelity belongs directly to design. better-interface owns quality criteria, interface-review owns change scope, break observes boundary content, state-machine exposes existing coded states, and design-browser executes requested browser scenarios. experiment-design does not reproduce their QA checklists, severity scales or verdicts.

A question such as whether first-time users recognize saving completion is a product usability assumption. experiment-design owns the hypothesis, participants/material, observation and validity conditions, budget/stop bounds and what the result changes. user-flow/wireframe/prototype can supply the task artifact. design-browser supplies bounded browser observations when needed. A UI author walkthrough cannot substitute for observing participants, and mock saving cannot prove persistence. Demand and AI quality require their own evidence.

## Stage handoff contract

product-brief owns the compact handoff: purpose; latest decisions and reasons through canonical links; observed/reported/intended state with locators; remaining gaps; exact inputs and supersession status; one next action with a completion signal. Downstream roles consume this contract rather than re-interviewing the product owner.

PM → design → engineering is the normal path, with loops when design exposes a policy gap or engineering exposes a feasibility gap. Preserve unaffected decisions; keep proposed adjustments distinct until decided. Entry can be at any stage with sufficient input. A small visual edit does not require discovery or three new documents. Product rules stay visible through opening, selection, saving and completion.

The three PM candidates are model-invoked in both harnesses, because bounded product-context work can be useful autonomously. They remain outside the promoted plugin and root skill catalog. ask-matt labels them conditional beta routes and recommends without executing. User-invoked to-spec/to-tickets/variant/state-machine/break remain human choices. Any authorized model-invoked dependency uses a separate one-skill Skill tool call; unavailable roles return prepared inputs and an explicit execution limit.

No cross-stage automation, global installation or assumed host-discovery behavior is added. The offline trials load a supplied skill explicitly; they do not prove natural routing or installed Claude/Codex activation.
