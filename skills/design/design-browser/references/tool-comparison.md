# Comparing browser routes

Read this when a user requests a tool comparison or an unresolved tool choice warrants a bounded experiment. It changes no user-specified tool choice on its own.

1. Define one task class and its acceptance criteria before running either route: source retrieval, general navigation, interaction QA, performance collection or reference comparison. Freeze the task, permitted actions, product/reference revision, data and initial state. Record the agent/model, permissions, browser/version, viewport and authentication available to each route. If equivalent access is impossible, compare the supported scopes separately.
2. Run both routes in owned sessions, reset the fixture between runs and alternate execution order across repeated cases. Keep the work budget and required evidence equal. Record failed attempts, retries, human intervention and setup separately from recurring execution time. A single development smoke can expose problems but cannot establish a general winner.
3. Have the analysis or QA agent assess the artifacts against the same criteria: task completion, correct observations, missed or unsupported findings, evidence reproducibility and coverage. Human judgment decides visual acceptance. Record elapsed time, tokens and cost when available; missing telemetry stays unknown.
4. Save commands, artifacts, outcomes and limitations in the project's evaluation location. Recommend a route only for the task class the results support. Default to Playwright for unclassified work while evidence is inconclusive; retain Aside for the specified research/general-browsing branch and honor explicit user overrides.

Comparing browser routes and comparing design skills are separate experiments. Keep the driver fixed when measuring a skill change, and keep the skill/task fixed when measuring a driver change. No outcome here installs tools, changes global settings or promotes a beta skill.
