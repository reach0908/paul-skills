# Maintaining Paul Skills

The upstream authoring workflow is the default. Our additions are provenance, deterministic comparison checks, and observable behavior evaluations. Existing skill names remain compatible with upstream; this fork's source and installation identity are separate.

## One change through the process

1. Capture the real task or failure and the result the human should be able to observe.
2. Read `writing-for-agents` and its `SKILL-MECHANICS.md`; choose the invocation boundary and disclose branch-specific detail through references. Use `AGENTS.md` for bucket and packaging rules.
3. Create or update the skill. Register every direct source in `skill-sources.json`; retain upstream copyright and in-file credits. New independent code can cite influences without pretending it is a direct import.
4. New Paul-authored or newly migrated skills start in `in-progress/`. Keep them outside the default plugin, root skill index, and promoted router until the user validates their behavior and explicitly approves promotion. Tests and agent trials supply evidence, not approval. After approval, choose `engineering/` or `productivity/` by the task served and update the root and bucket README, `ask-matt`, human docs, and plugin skill list together.
5. Add a Changeset for `paul-skills`. Run `npm run check` and `claude plugin validate . --strict`. Use a realistic task to check behavior, not only prompt wording. The [evaluation protocol](../evals/README.md) defines the evidence boundary.
6. Review the diff with its tests and limitations. Publish and merge within the user's authorization. The Release workflow opens the version PR; its version command keeps `package.json` and the plugin manifest aligned.
7. After that version PR merges, the workflow tags the release. Confirm remote tag SHA, workflow outcome, installed manifest, and a fresh host session separately.

Forked workflows may initially be disabled. Enabling the repository's Actions does not grant its token permission to create PRs. If GitHub denies the version PR, keep that error visible and create the same version diff through an authorized maintainer account; do not silently broaden token permissions. The workflow publishes the current `paul-skills@<version>` tag explicitly. It does not publish an npm package. Full Git history keeps existing tags available for idempotent reruns.

## Independent versions

Paul Skills starts at **0.1.0**, independently of Matt Pocock's release numbers. The earlier Paul 1.4.0 pilot and all inherited upstream tags/changelog entries remain historical records. Never delete or move them to reset the version. New tags use `paul-skills@<version>` to avoid collisions with inherited `v1.0.0` and later tags.

`package.json` owns the Paul version. `scripts/sync-plugin-version.mjs` synchronizes the plugin manifest and both root lockfile version fields. Changesets continues to produce subsequent version PRs and changelog entries: fixes use `patch` (0.1.0 to 0.1.1), additions use `minor` (0.1.x to 0.2.0), and breaking changes before 1.0 use `minor` with explicit migration notes. Reaching 1.0 is a deliberate maintainer decision. The tag publisher creates only the namespaced Paul tag, because Changesets' single-package `git-tag` command uses the inherited `v<version>` namespace.

The one-time reset sets the version and changelog directly in its release PR, with no pending bump Changeset. Later changes follow the normal Changeset process. Upstream package versions, release tags, changelog entries, and pending Changesets are source evidence, not instructions to overwrite Paul's version state. Describe only deliberately adopted changes in new Paul Changesets. `skill-sources.json` continues tracking immutable source commits and review baselines independently.

An installed 1.4.0 pilot may not automatically update to the numerically lower 0.1.0. Refresh the marketplace, inspect the installed version, and use the host's uninstall/reinstall flow if it retains 1.4.0. Verify in a fresh session. New installs follow the marketplace's current source.

## Source review

The experimental `upstream-sync` skill can review one or more registered sources when explicitly installed for testing. It remains in `in-progress/`, outside the default plugin, pending user validation and explicit promotion approval. Its intended destination is `productivity/`, because it maintains the skill library. It first reports changed paths and local drift; read full instructions only for affected behavior. Compare maintenance files separately from skill contents. Selective decisions protect fork identity, local authorization rules, installation instructions, and evaluation requirements.

Every imported skill has a frontmatter pointer to the canonical source inventory. The inventory records the historical import and the completed review independently. Upstream changes can be intentionally rejected without losing their history. See [the provenance contract](../skills/in-progress/upstream-sync/references/provenance.md).

## Migration order

The first pilot is the original `upstream-sync` skill. Its development checks and release rehearsal are recorded, but user acceptance is still pending. The existing forked catalog stays available. Next, migrate owned skills into `in-progress/` in small PRs after checking duplicate names, embedded helpers, runtime dependencies, licenses, and publication visibility. The private research inventory and backup stay local; a public fork is not permission to publish private skill bodies.

The next bounded candidates are `grilling`, `diagnosing-bugs`, and the PRD/spec workflow. Choose one canonical behavior per capability and preserve compatibility only when it earns its maintenance cost. Do not move paul-loop runtime, hooks, memory services, or agent orchestration into this library merely to import a skill.

## Development installs

`scripts/link-skills.sh` links promoted and in-progress skills for maintainers. It now refuses existing files or foreign symlinks before writing anything. Test with a disposable HOME; a successful isolated install does not migrate a user's existing global installs.

## Intentional fork differences

- Repository/package/marketplace identity and install commands point to Paul Skills.
- New original skills and evaluation tooling are in scope.
- `skill-sources.json` and `metadata.provenance` track provenance.
- `upstream-sync`, tests, and a validation workflow add repeatable checks.
- Maintainer links refuse collisions. Maintainer Claude context lives under `.claude/`, avoiding the root-plugin context warning while retaining `AGENTS.md` as the source.
- The initial 1.4.0 pilot included upstream pending Changesets to describe already-present behavior. Subsequent releases use Paul Changesets only for reviewed, adopted changes.

Historical upstream changelogs, ADRs, credits, and source documentation retain attribution. This fork does not claim upstream's official marketplace listing, newsletter, website publishing, or measured model performance.

## Release toolchain

Use Node 22.11+ on the 22.x line (or 24.x / 26+) and npm 10.9 or newer (the packageManager field pins npm 10.9.4). The initial inherited Changesets 2 lockfile reported 18 development dependency advisories. Changesets 3.0.3 preserves the same release workflow and removes those reported advisories; version-plan and release execution are checked before adoption. These Node packages are maintainer tooling, not dependencies of installed skill prompts.
