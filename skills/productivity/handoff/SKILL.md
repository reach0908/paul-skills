---
name: handoff
description: "Compact the current conversation into a handoff document in the OS temp directory for another agent to pick up. Use when the user asks for a handoff, or to carry this work into a new session, directory, harness or colleague. Not for routine context pressure (compact instead) or a summary the user wants in chat."
argument-hint: "What will the next session be used for?"
metadata:
  provenance: "https://github.com/reach0908/paul-skills/blob/main/skill-sources.json"
---

Write a handoff document summarising the current conversation so a fresh agent can continue the work. Save to the temporary directory of the user's OS (`$TMPDIR`, else `/tmp`; `%TEMP%` on Windows) - not the current workspace.

Include a "suggested skills" section in the document, naming which skills the next agent should call the Skill tool for.

Do not duplicate content already captured in other artifacts (specs, plans, ADRs, issues, commits, diffs). Reference them by path or URL instead.

Redact any sensitive information, such as API keys, passwords, or personally identifiable information.

If the user passed arguments, treat them as a description of what the next session will focus on and tailor the doc accordingly.
