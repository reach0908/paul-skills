---
name: ask-matt
description: Ask which skill or flow fits your situation. A router over the skills in this repo.
disable-model-invocation: true
metadata:
  provenance: "https://github.com/reach0908/paul-skills/blob/main/skill-sources.json"
---

# Ask Matt

You don't remember every skill, so ask.

Before stating what a skill does or recommending a step be skipped, read that skill's SKILL.md: the summaries here are for orientation only.

A **flow** is a path through the skills. Most paths run along one **main flow**, and two **on-ramps** merge onto it. Everything else is standalone, or a vocabulary layer that runs underneath.

## The main flow: idea → ship

The route most work travels. You have an idea and want it built.

1. **Choose the unresolved question.** For a product problem, decision update or product assumption, use the optional PM beta entry below when available. For an existing idea needing a deliberate stress-test, **`/grill-with-docs`** sharpens it by interview. When that interview is wanted in a working directory, use this wrapper, retaining what it learns in `GLOSSARY.md` and ADRs. (No working directory? Use `/grill-me` instead, covered under Standalone. Both run the same `/grilling` primitive; `grill-with-docs` is the one that leaves a paper trail, which makes it the better of the two whenever a repo is there to leave it in.)
2. **Branch: can you settle every question in conversation?** If a question needs a runnable answer (state, business logic, a UI you have to see), detour through a prototype, bridged by **`/handoff`** in both directions (a prototype lives in its own directory, which is exactly what `/handoff` is for; see Phase boundaries):
   - **`/handoff`** out, then open a fresh session against that file,
   - **`/prototype`** to answer the question with throwaway code,
   - **`/handoff`** back what you learned, and reference it from the original idea thread.
3. **Branch: is this a multi-session build?**
   - **Yes** → **`/to-spec`** (turn the thread into a spec), then **`/to-tickets`** to split it into tracer-bullet tickets, each declaring its **blocking edges**. Then work the tickets one of two ways:
     - **`/implement`** per ticket, **`/clear`ing context between each one**. On a local tracker that's one file per ticket under `.scratch/<feature>/issues/`, worked blockers-first by hand; on a real tracker the edges become native blocking links, so any ticket whose blockers are done can be grabbed. Each ticket is self-contained, so the last one's context is disposable.
     - **`/implement-spec`** for the whole spec in one run. It reads the tickets as a **task graph**, runs implementer subagents across the ready **frontier** in parallel, and lands everything on one **integration branch**. Reach for it when you'd rather orchestrate the build than drive each ticket yourself.
   - **No** → **`/implement`** right here, in the same context window.

   Either way, the code gets built by driving **`/tdd`** (one red-green slice at a time) and closes out with **`/code-review`**, a two-axis review (Standards + Spec) of the diff. `/implement` runs both per ticket; `/implement-spec`'s implementers each drive `/tdd`, and it runs one `/code-review` over the integration branch. Reach for **`/tdd`** on its own when you just want to build a concrete behaviour test-first without a full spec, and **`/code-review`** on its own whenever you want to review a branch or PR against a fixed point.

   When the work goes up as a pull request, **`/pr`** shapes the body: the smallest visual that shows the change, before/after evidence that it works, and a one-way or two-way door call. It's model-invoked, so the agent reaches for it whenever it writes a PR.

4. **`/retro`** closes the loop. After a build, and especially one that went sideways, it looks back over the session and suggests changes to the agent's **environment**, not the code: navigation pointers, automated checks, the coding standards `/code-review` enforces, steering files, tooling. Mechanical mistakes become deterministic checks; judgement calls become coding standards. The next build then starts from a better environment.

### Context hygiene

Keep steps 1–3 in **one unbroken context window** (don't compact or clear until after `/to-tickets`) so the grilling, spec, and tickets all build on the same thinking. Each `/implement` then starts fresh, working from the ticket. Run `/retro` in the session it's looking back on, before you clear; after clearing, point it at that session's log instead.

The limit on this is the **[smart zone](https://www.aihero.dev/ai-coding-dictionary/smart-zone)**: the window (~150k tokens on state-of-the-art models) within which the model still reasons sharply. If a session approaches it before `/to-tickets`, don't push on degraded; `/compact` at the nearest phase boundary and carry on (see Phase boundaries).

## Product → design → engineering (optional PM beta)

These candidates are in `in-progress/`, outside the promoted plugin. Recommend one only when the user has made that candidate available in an isolated trial or installed it individually; otherwise identify it as an optional beta, not an installed prerequisite. Read its actual SKILL.md before describing its behavior.

| Open work | Entry | Result and next role |
| --- | --- | --- |
| Explore an idea together, challenge its framing or find the exciting version | `/office-hours` | Startup or builder dialogue, explicit premise/approach choices and a canonical decision record |
| User situation, current alternative or first problem scope is unclear | `/problem-discovery` | Short Problem Brief; skip the interview when context is already sufficient |
| Existing decisions or prototype feedback need to become reusable product input | `/product-brief` | Current decision brief, scoped before/after record and short product handoff |
| A consequential assumption needs evidence before a product commitment, or its results need interpretation | `/experiment-design` | Bounded hypothesis, criteria, stop budget and result-dependent next decision |
| Have fresh agents use the prototype, interview them and compare actual behavior with intent | `/prototype-user-test` | Neutral task attempts before author-intent comparison; AI evidence, not human validation |
| Navigation, task transitions, screen hierarchy or interface quality is the open question | Available design role: information-architecture, user-flow, wireframe or interface-review/better-interface respectively | Preserve the brief's scope and product rules; return design artifacts and actual observations |
| Agreed behavior needs technical synthesis or implementation slices | `/to-spec`, then `/to-tickets` when needed | Preserve the canonical product contract and latest design inputs; their existing prerequisites still apply |

The stages preserve intent through **product context → design decisions → engineering decisions and verification**. They are not required documents or a compulsory sequence. A small settled task can start at design or engineering. Screen variants, focus checks and clipping QA go directly to design; experiment-design is for a product assumption and the decision its evidence changes. When usability is the assumption, PM defines the test and verdict conditions, while design supplies the task artifact and scoped browser evidence.

The product-brief handoff links the purpose, latest decisions and reasons, observed/reported/intended state, remaining gaps, exact canonical inputs and one next action. Mark superseded inputs as historical. Design owns IA, flows, screens and interface review. Engineering owns technical specs, tickets, code and checks. A policy or feasibility gap returns to its decision owner without reopening unaffected choices. AI suggestions, user decisions, mock behavior and observed implementation keep their status across every stage.

The design roles are promoted separately; these beta additions do not promote them again. Verify each installed SKILL.md and invocation policy before recommending execution. prototype remains the runnable exploration role; variant, state-machine and break remain user-invoked choices for component alternatives, coded-state workbenches and boundary scenarios. design-browser collects observations, not the product verdict.

The five optional candidates are model-invoked, but this router recommends and stops. office-hours is the idea-development conversation; problem-discovery is quick context recovery; grilling stress-tests an existing plan. Do not chain their interviews by default. prototype-user-test serves design evaluation and separates its private author packet from fresh participant prompts. product-brief carries accepted decisions and the tested/simulated limits into the next role. An exploratory prototype can feed back into product decisions before formal design without restarting settled choices. User-invoked engineering or design roles are choices for the human; other skills cannot call them. Model-invoked dependencies use a separate Skill tool call for each included task.

## On-ramps

A starting situation that generates work, then merges onto the main flow.

- **Bugs and requests piling up** → **`/triage`**. It moves issues through triage roles and produces agent-ready issues, which **`/implement`** later picks up.

  Triage is only for issues **you didn't create**: bug reports, incoming feature requests, anything that arrives raw. Tickets that `/to-tickets` produced are already agent-ready, so **don't triage them**.

- **Something's broken** → **`/diagnosing-bugs`**. For the hard ones: the bug that resists a first glance, the intermittent flake, the regression that crept in between two known-good states. It refuses to theorise until it has a **tight feedback loop** (one command that already goes red on *this* bug), then fixes with a regression test. Once the fix is in, run **`/retro`** in the same session to ask what would have prevented the bug; where the real finding is that there's no good seam to lock it down, that's a job for **`/improve-codebase-architecture`**.

- **A huge, foggy effort: a greenfield project or a huge feature build, too big for one session** → **`/wayfinder`**, the most cognitively demanding flow here. When the way from here to the destination isn't visible yet, it charts a **shared map** of **decision tickets** on the issue tracker and resolves them one at a time, producing **decisions, not deliverables**, until the fog is pushed back and the way is clear. Where **`/grill-with-docs`** sharpens an idea you can hold in one session, wayfinder is for the idea you can't, and it's slower and denser, so save it for exactly that, never a well-scoped feature.

  When the map clears, **it hands off, it doesn't build**: merge onto the main flow at **`/to-spec`**, which collapses the map's linked decisions into a buildable plan, then `/to-tickets` and `/implement` as usual. Looping the map straight into `/implement` skips that collapse and throws the linked detail away, so go straight to `/implement` only when the effort turned out genuinely small.

## Codebase health

Not feature work, just upkeep.

- **`/improve-codebase-architecture`** runs whenever you have a spare moment to keep the codebase good for agents to operate in. It surfaces **deepening opportunities**; picking one _generates an idea_ you can take into the main flow at `/grill-with-docs`. It's the survey that finds the candidates; **`/codebase-design`** (below) is the bench you design the chosen one on.

## Design

Use this route once the product intent is known. Enter at the first unsettled step; existing decisions do not need another planning pass. A review preserves deliberate design choices; a prototype comparison can conclude that the original should stay.

| Situation | What to recommend |
| --- | --- |
| Organize agreed content and findability | **`/information-architecture`** for destinations, labels and navigation |
| Specify task actions, outcomes, interruption or recovery | **`/user-flow`** for the transition contract, including exit and return |
| Decide screen hierarchy and responsive action placement | **`/wireframe`** for local interactive screens plus Markdown |
| Implement an approved prototype, screen specification or image | **`/build-design`** for reference-to-export mapping, preserved behavior and matching-state comparison |
| Work on the reachable states of one existing component | Ask the user to invoke **`/state-machine`** for a removable state workbench |
| Observe one component under plausible hostile content | Ask the user to invoke **`/break`** for a single-look stress page |
| Explain how a specific site or visual effect works | Ask the user to invoke **`/explain-interface`** for measured and qualified explanations |
| Choose among visual directions for one component | Ask the user to invoke **`/variant`** for a comparison in its real page |
| Review a screen or flow across disciplines | **`/better-interface`**, which loads all six domain owners and consolidates one report |
| Review what a branch, PR, staged or uncommitted change caused | **`better-interface`** is the first and only automatic entry, even when the request names specific UI domains; ask the user to invoke **`/interface-review`** with their target before inspecting files. That explicit invocation owns scope and classification, then composes `better-interface` |
| Keyboard, focus, semantics, names or announcements | **`/better-accessibility`** |
| Grouping, spacing, reading order, responsive structure or RTL | **`/better-layout`** |
| Labels, errors, empty states, confirmations or product vocabulary | **`/better-writing`** |
| Type scale, wrapping, truncation, font behavior or text selection | **`/better-typography`** |
| Palettes, semantic color tokens or contrast measurement | **`/better-colors`** |
| Surfaces, icon states, optical details or motion | **`/better-ui`** |
| Browser observations for a review or comparison | **`/design-browser`** for readiness checks, observations and a resume record when blocked; Playwright CLI for development checks and Aside for research or general browsing, unless the user specifies a tool |

The planning chain is `information-architecture → user-flow → wireframe → build-design`. Pass source revisions, stable destination/state IDs and unresolved decisions forward; continue only through the steps the user requested. Product flow planning uses `user-flow` directly and does not authorize loading the `state-machine` workbench. Broader throwaway UI or logic questions belong to `prototype`, which reuses the approved brief and baseline, fixes the conditions each alternative must preserve, and varies the unresolved question. `better-writing` handles a substantive copy pass within that scope.

`state-machine`, `break`, `explain-interface`, `variant` and `interface-review` are user-invoked and may be hidden from the automatic list while installed. In Codex, recommend `$paul-skills:interface-review staged` for staged changes only and `$paul-skills:interface-review working` for all uncommitted changes. In Claude Code, use `/paul-skills:interface-review` with the same target. Keep the engineering `code-review` Standards and Spec verdict separate from the interface verdict.

## Vocabulary underneath

Two model-invoked references that run *beneath* the other skills, each the single source of truth for its vocabulary. Reach for them directly when the **words**, not the process, are the problem; or let the skills above pull them in.

- **`/domain-modeling`**: sharpen the project's *domain* language: challenge a fuzzy term, resolve an overloaded word ("account" doing three jobs), record a hard-to-reverse decision as an ADR. It's the active discipline `/grill-with-docs` drives to keep `GLOSSARY.md` a clean glossary.
- **`/codebase-design`** is the deep-module vocabulary (module, interface, depth, seam, adapter, leverage, locality) for designing a module's *shape*: a lot of behaviour behind a small interface at a clean seam. `/tdd` and `/improve-codebase-architecture` both speak it.

## Phase boundaries

A **phase** is a chunk of work inside a session: the grilling, the implementation, the QA. At the **boundary** between two of them you have five options, and picking between them is the fuzziest decision in this whole map:

- **Continue**: stay put. Costs nothing, loses nothing.
- **`/clear`**: empty the window, when nothing here matters to what's next.
- **`/handoff`** writes a portable markdown file. Narrow: only for a **new harness**, a **new directory**, a **colleague**, or forking a side task **mid-phase**. What it buys is portability.
- **Subagent**: send a tightly-scoped task to its own window and get a report back.
- **`/compact`** compresses this context and seeds a fresh session with it. The **default**, at the bottom of the tree rather than the first reach.

Read [PHASE-BOUNDARIES.md](PHASE-BOUNDARIES.md) for the ordered tree: the five questions, the reasoning behind each branch, and why the primary-source cost makes **Continue** the one to rule out first. Make the decision **at** a boundary; mid-phase, continue or split the rest into subagents.

## Standalone

Off the main flow entirely.

- **`/grill-me`**: the same relentless interview as `/grill-with-docs`, but **stateless**: it saves nothing locally and builds no `GLOSSARY.md`. Reach for it when you are **not working in a working directory** (sharpening a plan, a design, a piece of writing, anything with no repo under it). If you are in a working directory, use `/grill-with-docs` instead: it runs the same interview and leaves a paper trail, so it is strictly the better one.
- **`/grilling`** is the interview primitive itself: rounds, the frontier, facts are the agent's job and decisions are yours. `/grill-me` and `/grill-with-docs` are the two named ways in, and `/triage`, `/wayfinder` and `/improve-codebase-architecture` all run it internally. Reach for it directly only when you want the interview with no wrapper around it.
- **`/prototype`** is a small, throwaway program that answers one design question: does this state model feel right, or what should this UI look like. Throwaway is a constraint on how the code is written, not a promise to destroy it: the answer folds into the real code, and the prototype itself is kept as a **primary source** on a `prototype/<name>` branch out of main, pointed at from the implementation issue. It's the detour in step 2 of the main flow, but reach for it any time a design question is hard to settle on paper. When comparing an existing UI, keeping the original can settle the question without an implementation change.
- **`/research`**: investigate a bounded question against **primary sources**, using local material directly and the **Aside CLI** for web discovery. It checks scope and evidence, then leaves one cited Markdown file with verification limits and unresolved gaps. An existing research executor does the work directly; a standalone caller can delegate while continuing other work. Take the file into the main flow at `/grill-with-docs` to inform the decision.
- **`/to-questionnaire`** comes in when the thing blocking you isn't in your head or the codebase but in **someone else's**, and it writes them a questionnaire to fill in. It's the inverse of `/grill-me`: instead of interviewing you about the subject, it interviews you about the **send** (who it's going to, what you need back) and aims the questions at the gap. What comes back is material for `/grill-with-docs` or `/to-spec`.
- **`/wizard`** is for the steps only a **human** can take: provisioning infrastructure, setting up credentials or CI secrets, clicking through an unfamiliar third-party dashboard, running a one-off migration or cutover. It generates an interactive bash script that opens each URL, captures each value, and writes it into `.env` and GitHub secrets, so the procedure stops being something you re-explain to an agent every time. Model-invoked, so the agent reaches for it the moment it hits a wall only you can pass. If the agent could just do it itself, it should; this is for where a human is genuinely in the loop.
- **`/wait-what`** is the corrective for a message that didn't land. Use it mid-conversation, inside any other skill, and the agent re-pitches what it just said with the context you were missing, in plain English, using the `GLOSSARY.md` vocabulary. It works after the fact; `/grill-with-docs` is the upfront cure, because a shared language agreed early is what stops the jargon arriving at all.
- **`/teach`**: learn a concept over multiple sessions, using the current directory as a stateful workspace.
- **`/writing-for-agents`** is the reference for writing documents agents consume: skills, AGENTS.md, pointed-at docs.

## Precondition

**`/setup-matt-pocock-skills`**: run before your first engineering flow to configure the issue tracker, triage labels, and doc layout the other skills assume. Custom issue trackers also work.
