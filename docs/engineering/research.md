## What it does

`research` answers a bounded question from [primary sources](https://www.aihero.dev/ai-coding-dictionary/primary-source) and saves a cited Markdown file for the next decision or task. Questions about live websites use the Aside CLI. Supplied files, source code, and local records can be investigated directly.

The conclusion is checked against original evidence, including dates, versions, and counterevidence. Aside's report is input to that check. Every scoped question ends with an evidenced answer or an explicit unresolved gap.

## When to reach for it

Type `/research`, or the agent reaches for it automatically when a task needs an investigation.

| What you need | Route |
| --- | --- |
| A fact in supplied files or local source code | Local investigation |
| Current docs, API behavior, comparisons, or evidence on websites | Aside web research |
| A question needing both local and external evidence | Local investigation plus a scoped Aside brief |
| A decision sharpened in conversation | [grilling](https://github.com/reach0908/paul-skills/blob/main/docs/productivity/grilling.md) |
| A runnable answer about an approach | [prototype](https://github.com/reach0908/paul-skills/blob/main/docs/engineering/prototype.md) |

## Prerequisites

The findings need a writable destination. A caller can provide the path; otherwise the skill follows the repo's notes convention and reports the location.

Web research needs Python 3 and a working, authenticated Aside CLI. The skill checks the executable, version, and relevant command help before starting. CLI installation, updates, and account setup are separate actions.

## Scope and evidence

The **scope** names the purpose, questions, audience, exclusions, and time or version boundary. Existing context supplies it whenever possible. A question is asked only when a missing choice would materially change the answer.

For web questions, Aside receives a self-contained brief with the source policy, search plan, counterevidence, and required output. The default effort is `ultrabrowse`; a requested lighter pass can preserve the user's configured effort. The user's model, provider, account, host, and permission settings are retained.

The saved file distinguishes evidence, source-owner claims, inference, and recommendations. Important web claims carry a ledger with original URLs, dates or versions, confidence and its reason, and missing checks. A narrow source or an inaccessible page limits the conclusion.

## One execution owner

A [subagent](https://www.aihero.dev/ai-coding-dictionary/subagent) already assigned a research task performs it directly. For a standalone invocation, a caller with other work can delegate to one background executor. An inline run handles the task when there is no useful concurrent work or the harness lacks delegation.

The same rule applies when [wayfinder](https://github.com/reach0908/paul-skills/blob/main/docs/engineering/wayfinder.md) supplies a research executor. That executor uses Aside for web discovery and returns its findings to the caller.

## Common questions

**Does this call the separate `research-with-aside` skill?**

It runs the Aside workflow through its own reference and helper. The other skill supplied source material during authoring and has no runtime installation requirement.

**Which Aside features does research use?**

`exec` performs discovery. A known session can be resumed, steered while running, or given a queued follow-up, retaining its existing settings. The launcher rejects empty or malformed session IDs before starting any CLI work. For direct source verification, the agent reads `guide repl` and the relevant built-in site skill before reusing matching tabs and taking browser snapshots. The built-in Aside session reader can recover a specific task's metadata and answer when stdout is unavailable. Features are checked against the installed help; a newer advertised version does not prove that the installed executable supports it.

**What happens if Aside is missing or fails?**

You receive the availability or execution failure together with the brief and any partial evidence. The agent asks you to restore Aside or authorize another web engine. It retains a known session ID for resuming an interrupted investigation.

**Can research create another research agent inside its executor?**

The executor's job is to investigate and return the artifact. Its caller owns dispatch, so an existing executor performs the work directly. The instructions define that boundary; behavior trials still need to show whether each host follows it.

**When does it stop reading?**

When every scoped question has supporting evidence or a stated unresolved gap. A follow-up needs a specific gap that could change the answer. Naming the questions controls the work.

**Where should the file live, and should I commit it?**

The caller's path takes priority, followed by the repo's existing convention. The skill saves the file and reports its absolute path. Your project decides whether to retain, commit, attach, or archive it. Recheck date-sensitive findings before reusing them.

## It's working if

- You can see the scoped questions and the output destination before investigation starts.
- Local questions use the available files; web questions show an Aside availability check and run.
- An existing research executor completes the task directly, with one output artifact.
- Important claims link to original evidence and state dates, versions, and verification limits.
- The saved file states what remains unresolved and what check would settle it.
- A failed web run leaves a usable brief and its actual status.

## Where it fits

`research` is a reach-for-it-anytime standalone. [wayfinder](https://github.com/reach0908/paul-skills/blob/main/docs/engineering/wayfinder.md) supplies research tickets; [grill-with-docs](https://github.com/reach0908/paul-skills/blob/main/docs/engineering/grill-with-docs.md) can use the findings to sharpen and record a decision. [ask-matt](https://github.com/reach0908/paul-skills/blob/main/docs/engineering/ask-matt.md) routes across the full set.
