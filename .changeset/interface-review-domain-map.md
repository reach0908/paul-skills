---
"paul-skills": patch
---

`interface-review` now loads only the domain owners a change can affect. It classifies every changed line with a new surface map (markup, copy, color, type, box and flow, surface and motion) and hands `better-interface` a domain map naming which of the six `better-*` owners to load and the lines that select each one. A change with no UI surface, such as a backend data mapping or a memoization or prefetch change that leaves rendered output identical, ends with a short "no UI surface changed" result and loads no domain owner. A line the map cannot place loads all six. A skipped domain is reported as `Not reviewed: no <surface> in the change scope`, never `Clear`. Current-screen audits through `better-interface` still load all six owners.

The trial ran n=3 per arm on synthetic diffs; figures are for the shipped text. A data-only and a perf-only change went from six owners loaded to none, at 45% and 44% of the previous mean cost. One of those six runs wrote the skip reason only in Korean. A color and layout change loaded accessibility, layout and colors instead of all six. It kept all three findings at the same severity under a blind AI grade, at 83% of the cost. The first revision had folded one LOW finding into another in 1 of 3 runs. No human review yet; see `evals/interface-review-scope-2026-10-28/REPORT.md`.
