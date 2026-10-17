---
name: research
description: Investigate a question against primary sources and save cited Markdown findings. Use for local source investigation, docs or API facts, or web research through the Aside CLI.
metadata:
  provenance: "https://github.com/reach0908/paul-skills/blob/main/skill-sources.json"
---

Answer a bounded question from **primary sources**, then leave one cited Markdown file that the next step can use. Web discovery runs through the **Aside CLI** using this skill's own instructions and helper.

## Execution owner

The caller owns scope and scheduling. An agent already assigned a research task is the **executor**: it performs the investigation directly and returns the result to its caller.

For a standalone invocation, settle the scope first. When the harness supports delegation and the caller has independent work to continue, dispatch one background executor with the complete brief, output path, and an explicit executor role. Otherwise run inline. The executor follows the process below itself; Aside is its web engine. A caller such as `wayfinder` already supplies the executor, so it needs no additional research-agent dispatch.

## Process

1. **Lock the scope.** Identify the purpose or decision, answerable questions, audience, exclusions, time/version/geography boundary, and deliverable. Reuse supplied context. Ask only about missing choices that would materially change the answer; a delegated executor returns those gaps to its caller. State reasonable task-compatible assumptions. Done when each question has a clear boundary and the destination is known. Use the caller's output path, otherwise the repo's existing notes convention; if none exists, choose a location and report it.

2. **Choose the evidence route.** Read supplied and relevant local material first. Use local investigation when those materials can answer the questions. When current websites or external facts are needed, read [web-research.md](references/web-research.md) and perform its Aside workflow. Mixed tasks retain local evidence and send Aside only the context needed for the web questions. Done when every question has an evidence route.

3. **Investigate and audit.** Follow each material claim to the source that owns it: source code, official docs, specs, first-party APIs, original records or datasets. Treat summaries and search snippets as leads. Check relevant dates, versions, conflicting evidence, and what could weaken the conclusion. Distinguish verified evidence, source-owner claims, inference, and recommendation. Mark unavailable material as not found, not accessible, or not verified. Done when every question has an evidenced answer or a specific unresolved gap; further reading needs a named gap to resolve.

4. **Save and return.** Write one Markdown findings file with the conclusion, scope and research date, evidence with nearby citations, conflicts and limitations, and unresolved questions. Cite local evidence with paths and lines or a pinned revision. For web evidence, include the [claim ledger](references/web-research.md#claim-ledger). Verify that the absolute output path exists and read the file before reporting success. Return its path, a short answer, and gaps to the caller or user. The caller decides how to connect it to a ticket, spec, or decision; follow existing publication authorization for any external write.

## Completion

Every scoped question is answered with supporting evidence or explicitly left unresolved with the reason and next check. The saved artifact distinguishes facts from analysis and states its time/version limits. An interrupted or blocked investigation returns the brief and partial evidence with its actual status, rather than claiming a completed result.
