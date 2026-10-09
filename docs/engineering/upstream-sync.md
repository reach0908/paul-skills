## What it does

Compares a skill's source version, the newer upstream version, and the local copy. It identifies improvements worth adopting while preserving local requirements. A newer upstream file is a candidate for review, never proof that replacing our copy is correct.

## When to reach for it

Type `/upstream-sync` (or `$upstream-sync` in Codex), or let the agent reach for it when a task fits. Reach for it when:

- A benchmark repository changed.
- You need to identify where a skill came from.
- You want to apply selected upstream improvements.

Ordinary package upgrades belong in the package manager's workflow.

## Prerequisites

A Git source checkout and a local skill workspace. Python 3.9 or newer runs the bundled comparison helper. `skill-sources.json` records the source mappings; if it is missing, the skill first reconstructs evidence and reports what remains unknown.

## Three-way review

| Situation | Result |
| --- | --- |
| Source evolved and our behavior still fits | Adopt the compatible improvement. |
| Source evolved and we customized the same behavior | Adapt the useful part and retain the local requirement. |
| We intentionally diverge | Keep the local behavior and record why. |
| A dependency, origin, or evaluation is missing | Defer the change without advancing its review baseline. |

- A report-only request produces findings.
- An apply request produces the authorized patch and verification.

Metadata distinguishes direct copies, adaptations, composite skills, and original work influenced by other repositories.

## Common questions

**Can it follow repositories other than the fork parent?**

Yes. Each skill can have multiple pinned sources. Each source is compared and reconciled independently.

**Does checking a new commit mean we have adopted it?**

No. The import revision stays fixed. The reviewed revision advances only after every difference has a recorded decision; a deferred change stays pending. A deliberate decision to retain local behavior counts as reviewed, but not as copied.

## It's working if

- The report shows source commits, changed files, and local behavior that would otherwise be lost.
- An unavailable source is marked unknown rather than current.
- Deferred work is still visible on the next check.
- A selected improvement works locally and the report distinguishes that from release or installation.

## Where it fits

Standalone maintenance for the skill library. [writing-for-agents](https://github.com/reach0908/paul-skills/blob/main/docs/productivity/writing-for-agents.md) helps express an adopted behavior concisely; [code-review](https://github.com/reach0908/paul-skills/blob/main/docs/engineering/code-review.md) checks the resulting diff. [ask-matt](https://github.com/reach0908/paul-skills/blob/main/docs/engineering/ask-matt.md) remains the map of the inherited skills.
