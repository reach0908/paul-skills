Skills are organized into bucket folders under `skills/`:

- `engineering/`: daily code work
- `productivity/`: daily non-code workflow tools
- `product-management/`: product discovery, strategy, prioritization, requirements, and outcome evaluation
- `design/`: user experience, interaction, visual design, and design evaluation
- `misc/`: kept around but rarely used, not promoted
- `in-progress/`: beta: public on purpose, feedback wanted, not shipped in the plugin
- `deprecated/`: no longer used

The **promoted** buckets are `engineering/`, `productivity/`, `product-management/`, and `design/`. Every skill in them must have a reference in the top-level `README.md` and an entry in `.claude-plugin/plugin.json`'s `skills` array (the Claude Code plugin ships exactly the promoted set). Skills in `misc/`, `in-progress/`, and `deprecated/` must not appear in either.

Install commands are copied verbatim from [.agents/install-block.md](./.agents/install-block.md). `.claude-plugin/marketplace.json` is the repo's own marketplace. Claude Code and Codex both install from our own marketplace; this fork is not listed in the official marketplace. Run `claude plugin validate . --strict` after touching either manifest. [ADR 0002](./.agents/adr/0002-ship-as-a-claude-code-plugin.md) records why.

Each skill entry in the top-level `README.md` must link the skill name to its `SKILL.md`.

Each bucket folder has a `README.md` that lists every skill in the bucket with a one-line description, with the skill name linked to its `SKILL.md`. The promoted buckets' `README.md`s and the top-level `README.md` group entries into **User-invoked** and **Model-invoked**; non-promoted bucket `README.md`s (`misc/`, `in-progress/`) use a flat list.

Skills in promoted buckets also have a human-facing docs page at `docs/<bucket>/<skill-name>.md` (the docs tree mirrors their bucket folders under `skills/`). Fork docs live at `https://github.com/reach0908/paul-skills/blob/main/docs/<bucket>/<skill-name>.md`; we do not publish to aihero.dev. When you add, rename, or change the behaviour of a promoted skill, create or re-sync its docs page following [.agents/writing-docs.md](./.agents/writing-docs.md). A finished page carries four sections: **What it does**, **When to reach for it**, **Common questions**, and **It's working if**. `writing-docs.md` holds the template, the section order, and where to hunt for the questions. Skills in the non-promoted buckets (`misc/`, `in-progress/`, `deprecated/`) get **no** docs page. The one exception is a promoted skill removed outright: its page stays, marked archived (see `writing-docs.md`).

Every `SKILL.md` is either user-invoked (`disable-model-invocation: true` plus `policy.allow_implicit_invocation: false` in `agents/openai.yaml`, reachable only by the human) or model-invoked (model- or user-reachable). See [.agents/invocation.md](./.agents/invocation.md).

[`ask-matt`](./skills/engineering/ask-matt/SKILL.md) is the router that maps every user-reachable skill and how they relate. The same trigger that re-syncs a docs page applies to it: whenever you add, rename, remove, or change how a user-reachable skill fits the flows, re-read `ask-matt`'s `SKILL.md` and update it so the map stays accurate: a new skill it never mentions, or a stale one it still routes to, is a router that lies.

For isolated maintainer trials, run `scripts/link-skills.sh` with a disposable HOME to (re)link every skill outside `deprecated/` and `misc/` into the trial harness directories. The script refuses collisions with existing installs. It includes `in-progress/`, so do not run it against daily global skill directories; use the promoted plugin there.

No em-dashes anywhere in this repo's prose (`SKILL.md` files, docs, `README.md`, `CHANGELOG.md`, ADRs, changesets, code comments). Where a sentence reaches for one, rewrite it instead with a comma, colon, period, parentheses, or a conjunction, whichever the sentence actually wants; never do a blind character substitution.

## Agent skills

### Triage labels

Canonical names, unchanged. See `docs/agents/triage-labels.md`. Issues are judged against [`SCOPE.md`](./SCOPE.md).

## Paul maintenance additions

Install the promoted Paul Skills plugin once per host at user scope as the shared workflow library. Keep project-specific skills, plugins, and MCP configuration in the owning project. Do not add project-only tools to global settings or publish private project instructions in this repository. For project skills, use `.agents/skills/<name>/` as the canonical directory and a relative `.claude/skills/<name>` link when both hosts need it. Check existing project copies before moving a global skill, and preserve newer or uncommitted project work. See the installation-scope policy in [maintenance.md](./docs/maintenance.md#installation-scope).

New Paul-authored or newly migrated skills start in `in-progress/`. Passing automated checks or agent trials does not authorize promotion. Move a skill into a promoted bucket only after the user validates its behavior and explicitly approves promotion; record the evidence and choose the domain by the task it serves.

Track every skill in `skill-sources.json`, including originals and all direct sources of adaptations. Preserve immutable origin revisions; reconciliation records advance only after a complete, verified review. Read [the provenance contract](./skills/in-progress/upstream-sync/references/provenance.md) when changing it.

Run `npm run check` for a skill change. Include a Changeset, observable behavior evidence, and limitations. Model recommendations stay unmeasured until controlled comparative trials exist. The repository workflow is documented in [maintenance.md](./docs/maintenance.md).
