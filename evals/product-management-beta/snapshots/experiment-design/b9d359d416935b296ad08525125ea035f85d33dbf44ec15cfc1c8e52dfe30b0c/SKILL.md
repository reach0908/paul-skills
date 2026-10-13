---
name: experiment-design
description: Design a bounded test of a consequential product assumption or interpret its results. Use for demand, usability, AI quality or feasibility decisions with outcome-dependent next actions; ordinary interface QA, screen variants and browser checks belong to design roles.
metadata:
  provenance: "https://github.com/reach0908/paul-skills/blob/main/skill-sources.json"
---

# Experiment design

Turn the most consequential unknown into a **decision test**. Own the hypothesis, evidence needed, resource/stop bounds and next decision. Design owns screen and flow work, interface quality and browser observations; engineering owns technical implementation and verification.

## Select the decision

Read the current brief, assumptions, observations and available instrumentation. Identify what decision remains open and what evidence could change it. For an existing product, recover its observed baseline; for a new product, keep analogy and intended behavior distinct from evidence about this product.

Select the assumption whose failure would most change the next scoped commitment, explaining impact, uncertainty and dependencies in words. Use sourced numbers only on their stated scale. Avoid inventing RICE/ICE scores or mixing confidence scales into a risk formula. When reviewing an existing plan's failure possibilities, read [failure-review.md](references/failure-review.md); ordinary new-test design does not require a pre-mortem.

Classify the question as demand, usability, AI quality or technical feasibility. Keep separate tests when the evidence cannot answer the same question. For a pure UI check such as clipping, focus order, state rendering or reference fidelity, return the scenario to the appropriate design/QA role. A walkthrough tests internal consistency; observing real users attempt a task tests a usability assumption. Neither establishes demand by itself.

## Design the smallest useful test

Read [methods.md](references/methods.md) for the selected evidence type. Reuse existing analytics, logs and artifacts before proposing instrumentation. Match the method to the decision and available resources. Record a concise plan in the user's language or update the existing experiment artifact:

- Hypothesis, its evidence/unknowns and the decision it informs.
- Method, participants or test material, relevant comparison/baseline and what to observe.
- Success, failure and **inconclusive** conditions, including missing/invalid evidence.
- Needed sample, duration, cost and attempt budget, with the basis and status of each. Unsupplied quantities are proposals or unknowns; a small convenience sample is exploratory, not population proof.
- Stop conditions and the next decision for each result, including what happens when the budget expires without a verdict.

Choose criteria before execution. If a consequential human decision is missing, ask only that gap while preparing the settled plan. A plan is not execution approval: external contact, paid calls and service changes require the authorization for those actions. Do not execute them merely because the test is designed.

## Interpret results and stop

When results are supplied, recover the original plan, criteria, run conditions and raw observation locators first. Separate **planned**, **executed** and **observed**. Check denominators, missing data, guidance, mock boundaries and deviations before applying the criteria. If criteria were absent, record a retrospective interpretation with that limitation, not a predeclared pass.

Update the tested assumption as supported within the observed scope, contradicted, or unresolved. Record the verdict, evidence, limitations and its next action. Local PASS, mock output, an expert's rating and signup interest answer different questions; none automatically proves user effect or validated demand.

When a stop condition is reached, end this evaluation and apply the recorded next decision. Leave unresolved evidence as inconclusive. Additional trials, extra budget or changed criteria are separately proposed work, not an automatic extension or a retroactive success threshold.

## Deliver the next input

Give the next role the hypothesis, fixed product rules, required observation, plan/result artifact revision and remaining gap. Label test-only operating choices and AI-proposed policy changes separately from user-approved product rules. A manual-test access rule or delivery constraint does not become a requirement for the real product by appearing in the handoff. Prototype owns a runnable test artifact; design roles own flow/screens and interface QA; design-browser owns browser evidence; engineering owns feasibility probes and implementation tests. For a runnable artifact included in the request, call the Skill tool with "prototype". For authorized browser evidence, call it with "design-browser". Verify availability and invocation policy first; any other authorized model-invoked design role is also one named skill per call. Without that tool or installed role, return the prepared input and the missing execution capability. User-invoked roles remain choices for the human.

If updating the product brief is included, call the Skill tool with "product-brief" and pass the scoped result; otherwise return the result for that later update. Done when the test can inform its stated decision or the result has a bounded verdict and next action. Product quality and human acceptance remain separate.

## Attribution

Selectively adapted from PM Skills identify-assumptions-existing/new, prioritize-assumptions, brainstorm-experiments-new and, for the existing-plan branch only, pre-mortem. The upstream cites Teresa Torres and Alberto Savoia for its risk/experiment concepts; this adaptation makes no claim to reproduce or validate their complete methods. Exact source files and changes are in the provenance inventory. See [MIT notice](LICENSE.pm-skills).
