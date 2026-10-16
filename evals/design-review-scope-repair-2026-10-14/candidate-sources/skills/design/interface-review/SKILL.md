---
name: interface-review
disable-model-invocation: true
description: Reviews a branch, pull request or uncommitted change for the interface problems it introduced or regressed, across accessibility, layout, writing, typography, color and UI.
metadata:
  provenance: "https://github.com/reach0908/paul-skills/blob/main/skill-sources.json"
---

# Interface review

This skill reviews a change rather than a screen. It resolves the scope, expands the changed files to the surfaces they affect, reads both sides of the diff and classifies every finding.

It owns the scope, the classification and the change-scoped report. Domain rules belong to the `better-*` skills. Severity, consolidation, coverage, the cap and the verdict belong to `better-interface`, which this skill hands the review to.

Correctness, tests, security and performance belong to the project's general code review. Name such a concern once, point at that review and drop it. Keep Paul `code-review`'s Standards and Spec reports separate from this design verdict. Share the base, head, working-tree scope and design revision, not a merged score.

For browser evidence, call the Skill tool with "design-browser" and pass the task purpose and expected observations. Without a Skill tool, read its installed SKILL.md. Follow its tool routing; if unavailable, use the caller's tool policy and installed help, and report verification limits.

## Entry condition

Start only when the user explicitly invokes `interface-review` by name. A generic change-review request or another skill's referral is not an invocation. If reached that way, return the user-facing invocation with their target and stop before resolving scope. In Codex use `$paul-skills:interface-review`; in Claude Code use `/paul-skills:interface-review`.

Being hidden from the automatic skill list is expected for this user-invoked skill. `better-interface` can be loaded automatically to recommend this command, but that recommendation alone leaves this workflow unopened. The user's explicit `interface-review` invocation opens the change-review workflow below and authorizes the model-invoked `better-interface` handoff without a second invocation.

## The change, not the codebase

The author is asking "did I make this worse?". Report what the change caused and stay mostly quiet about what it merely touched. Three pre-existing findings is a courtesy; thirty is a different review and one nobody asked for.

Read the whole diff before forming an opinion of it. A skimmed diff produces findings about code the next hunk already fixed.

## Core principles

### 1. Resolve the change scope first

Read the target before choosing a base, including when the user asks only for preparation. Explicit local targets use this contract:

| Target | Base | Reviewed state and inventory |
| --- | --- | --- |
| `working` | Current `HEAD` SHA | Net tracked difference from `HEAD` to the working tree (`git diff HEAD`), plus untracked files (`git ls-files --others --exclude-standard`). Includes staged and unstaged work as it exists now; excludes earlier commits. |
| `staged` | Current `HEAD` SHA | Index snapshot only (`git diff --cached HEAD`). Read reviewed files with `git show :path`; exclude unstaged edits and untracked files. |

Neither local target requires the default branch or a merge base, even when `HEAD` is ahead or detached. A staged edit reversed in the working tree belongs to `staged` but not the net `working` change. State zero committed changes for both targets. Resolve the full SHA only when actual inspection is authorized; a preparation answer explains the contract without running Git.

For `branch`, `pr <n>`, a ref or a range, use [Scope resolution](scope-resolution.md). The target is the scope token or range in the invocation, not its surrounding natural-language instructions.

**Only with no target supplied**, resolve in this order and stop at the first match:

1. `HEAD` is ahead of `git merge-base origin/<default-branch> HEAD`. Review that range **plus** any uncommitted changes, stating the commit count and the uncommitted file count separately.
2. The working tree is dirty. Review the uncommitted changes.
3. Neither. There is no change to review, so follow **With no change, ask rather than invent one**.

Record the base commit of the resolved range as `$BASE` and name it in the scope block. Every command in this skill and its references uses it.

Exclude lockfiles, snapshots, generated output, vendored code and binaries per [Excluded paths](scope-resolution.md#excluded-paths), and name what you excluded. If nothing survives the exclusions, treat it as no change.

### 2. With no change, ask rather than invent one

An explicit `working` or `staged` target with an empty selected inventory has no change to review, even if the branch contains earlier commits. Report that selected scope as empty and ask for another target without widening it. For no-target discovery, a clean tree with nothing ahead of the merge base means there is no change to review. Never fall back to `HEAD~1..HEAD` on your own. The last commit is whatever happened to land, often a merge or someone else's work.

For no-target discovery, gather the facts in [Nothing to review](scope-resolution.md#nothing-to-review), state them, then offer these routes and wait:

- **The open pull request** on the current branch, first when there is one. A branch whose commits already landed resolves to no change, while its pull request is still exactly what the user meant.
- **The last commit**, `HEAD~1..HEAD`, named by short SHA and subject so the user sees what they would get.
- **A target they name**, such as `pr <n>`, a branch, a ref or a range.
- **A whole-repository interface audit**, which is not a change review. Hand it to `better-interface` as a repository-scope review, without this skill's scope block, statuses or pre-existing section.

Where exclusions emptied the scope, name the excluded files in the offer. Never report a review of nothing as `Approve`.

### 3. A diff is not a surface

A changed file is evidence, not the review subject. Its **blast radius** is the set of surfaces it renders in; review those.

Expand one hop by default, to the direct importers and callers. Expand a second hop only for design tokens, theme values and shared primitives, where one line reaches the whole product.

Review at most five consumers in total across both hops, ordered by [the rule in Scope resolution](scope-resolution.md#expanding-to-consumers). Count each distinct consumer reviewed, including an intermediate stylesheet or shared component: one shared stylesheet plus four routes uses all five slots. State how many you did not expand, since an unstated cutoff reads as completeness.

### 4. Read the removed lines

Regressions are invisible in the post-change state. Read the `-` side of every hunk against [Removed signals](removed-signals.md).

A signal is a lead, not a finding. A removal is a regression only when nothing in the change replaces it, and the domain skill owns that judgement. Route each unmatched removal to its owner, report only what that skill confirms and status it `Regression`.

### 5. Classify every finding

Give every finding one status:

- `Introduced`: the change created it.
- `Regression`: the change weakened something previously correct.
- `Pre-existing`: present before the change and not made worse by it.

Status by cause, not by location. A finding a changed line causes is `Introduced` or `Regression` wherever it surfaces, including an untouched consumer of a changed token. A finding the change neither created nor worsened is `Pre-existing`, even three lines from a hunk.

To check whether a line predates the change, blame the reviewed range. A `^` prefix marks a line unchanged since the base:

```bash
git blame -L <line>,<line> "$BASE"..<head-ref> -- path/to/file
```

For uncommitted work, drop the range. A line marked `Not Committed Yet` or blamed on a commit inside `$BASE..HEAD` belongs to the change.

### 6. Hold the change to its stated intent

Read the pull request title and body, the linked issue and the commit messages, then review whether the interface delivers what they claim.

This is how you find the **incomplete** change, which a surface review misses because it inspects only the states that exist. Look for the absent ones:

- A new variant, size or theme applied to some states but not all of hover, focus, active, disabled, loading and selected.
- A new user-facing string with no entry in the translation catalogue the project maintains.
- A new component with no empty, loading, error, disabled or narrow-width state.
- A control added to one surface but not to the siblings that already carry its peers.

Do not report scope creep. Whether a change does too much is a process question, not an interface one.

### 7. Hand the review to `better-interface`

Call the Skill tool with "better-interface". If the host exposes no Skill tool, read its installed SKILL.md and applicable references. Supply an explicit handoff containing:

- The user's `interface-review` invocation and target.
- The resolved scope block: base, head, committed and uncommitted scope, file inventory and exclusions.
- The affected surfaces, expansion limits and permitted verification.
- A status on every candidate finding, with before/after evidence for the owning domain to confirm.

This is the authorized change-review branch of `better-interface`. It keeps this scope and the report format below while applying its six domain checks, ranking and consolidation. Continue through the handoff rather than requesting the same user invocation again.

If `better-interface` is unavailable, report the resolved scope and the file inventory, name it as the missing skill and stop. Do not invent a severity scale, a cap or a verdict.

### 8. Never mutate the working tree

A change review is read-only, including the checkout. `git fetch` writes only to `.git` and is permitted. `gh pr checkout`, `git checkout`, `git switch` and `git stash` rewrite the files the author has open, so they are never permitted. Fetch pull request refs and read them in place.

Rendered verification is opt-in here, in place of `better-interface`'s **Verify what can be verified**. Mark visual and runtime claims **Not verified** unless the project exposes a cheap preview or the user asks for a rendered review. For `working` and `branch`, the checkout already is the head, so render it in place. For any other target, render an isolated worktree such as `git worktree add /tmp/review-<n> refs/remotes/pr/<n>` and remove it when done.

## Before you finish

| Mistake | Fix |
| --- | --- |
| A no-target discovery counts only uncommitted files while `HEAD` is ahead of the merge base | Include the branch range and uncommitted changes; explicit `working` and `staged` still use `HEAD` with zero committed changes |
| A report on `HEAD~1..HEAD` the user never chose | State the facts and offer the routes in **With no change, ask rather than invent one** |
| A changed shared component with no consumer under `Surfaces expanded` | Expand to its consumers and name the ones you skipped |
| A deleted `aria-label`, `outline` or `prefers-reduced-motion` with no finding and no note | Route it to its owner through [Removed signals](removed-signals.md) |
| A `Regression` whose removed attribute reappears elsewhere in the diff | Check the [equivalent replacements](removed-signals.md#equivalent-replacements) first |
| A finding on an untouched consumer of a changed token statused `Pre-existing` | The change caused it, so it is `Introduced` or `Regression` |
| A line outside every hunk statused `Introduced` with no causing change named | Blame it against the reviewed range |
| `gh pr checkout` or `git switch` in the command log | Fetch the ref and read files with `git show` |
| A cited line that does not match `git show <head-ref>:path` | Cite against the head ref named in the scope block |

## Review output format

Open with the scope block:

| Field | Value |
| --- | --- |
| Target | `branch`, `working`, `staged`, `pr 482` or the range as entered |
| Base ref | Resolved base SHA; for `working` and `staged`, `HEAD` at that SHA |
| Head ref | Working tree, index snapshot, or resolved head ref and SHA |
| Commits | Committed and uncommitted counts; local targets have 0 committed |
| Files in scope | 12 after exclusions |
| Excluded | `pnpm-lock.yaml`, `src/__snapshots__/`, lockfile and snapshots |
| Surfaces expanded | `CheckoutPage`, `SettingsPanel`; 3 further `Button` consumers not expanded |

The coverage table from `better-interface` follows it. A domain with no evidence in the change scope is `Not reviewed: no evidence in the change scope`, which is a coverage statement rather than a gap.

Then the findings, with a `Status` column per **Classify every finding**:

| Severity | Domain | Status | Location | Before | After | Why |
| --- | --- | --- | --- | --- | --- | --- |
| HIGH | Accessibility | Regression | `src/Dialog.tsx:42` | `aria-label="Close"` removed in this change | Restore `aria-label="Close"` on the icon-only control | The close control had an accessible name before this change and no longer does |

With no `Introduced` or `Regression` findings, omit the table and state "No actionable interface findings in this change."

Then `Pre-existing` findings, at most three, highest severity first, stated plainly as not this change's responsibility. Omit the section when there are none.

| Severity | Domain | Location | Issue |
| --- | --- | --- | --- |
| MEDIUM | Typography | `src/Toolbar.tsx:7` | Numeric badges use proportional figures; predates this change |

Verification and the verdict follow in `better-interface`'s format.
