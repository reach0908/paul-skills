---
"paul-skills": patch
---

`interface-review` now loads only the domain owners a change can affect. It classifies every changed line with a new surface map (markup, copy, color, type, box and flow, surface and motion) and hands `better-interface` a domain map naming which of the six `better-*` owners to load and the lines that select each one. A change with no UI surface, such as a backend data mapping or a memoization or prefetch change that leaves rendered output identical, ends with a short "no UI surface changed" result and loads no domain owner. A line the map cannot place loads all six. A skipped domain is reported as `Not reviewed: no <surface> in the change scope`, never `Clear`. Current-screen audits through `better-interface` still load all six owners.

In a trial with n=3 per arm on synthetic diffs, a data-only and a perf-only change went from six owners loaded to none, at 43% and 42% of the previous mean cost. A color and layout change loaded accessibility, layout and colors instead of all six. It kept every change-attributed finding under a blind AI grade, at 81% of the cost. No human review yet; see `evals/interface-review-scope-2026-10-28/REPORT.md`.
