# Maintaining Paul Skills

The upstream authoring workflow is the default. Our additions are provenance, deterministic comparison checks, and observable behavior evaluations. Existing skill names remain compatible with upstream; this fork's source and installation identity are separate.

## One change through the process

1. Capture the real task or failure and the result the human should be able to observe.
2. Read `writing-for-agents` and its `SKILL-MECHANICS.md`; choose the invocation boundary and disclose branch-specific detail through references. Use `AGENTS.md` for bucket and packaging rules.
3. Create or update the skill. Register every direct source in `skill-sources.json`; retain upstream copyright and in-file credits. New independent code can cite influences without pretending it is a direct import.
4. For a promoted skill, update the root and bucket README, `ask-matt`, human docs, and plugin skill list. Experimental work stays in `in-progress/` until its behavior can be checked.
5. Add a Changeset for `paul-skills`. Run `npm run check` and `claude plugin validate . --strict`. Use a realistic task to check behavior, not only prompt wording. The [evaluation protocol](../evals/README.md) defines the evidence boundary.
6. Review the diff with its tests and limitations. Publish and merge within the user's authorization. The Release workflow opens the version PR; its version command keeps `package.json` and the plugin manifest aligned.
7. After that version PR merges, the workflow tags the release. Confirm remote tag SHA, workflow outcome, installed manifest, and a fresh host session separately.

Forked workflows may initially be disabled. Enabling the repository's Actions does not grant its token permission to create PRs. If GitHub denies the version PR, keep that error visible and create the same version diff through an authorized maintainer account; do not silently broaden token permissions. The inherited workflow creates Git tags, not an npm package or a GitHub Release page.

## Source review

Use `upstream-sync` for one or more registered sources. It first reports changed paths and local drift; read full instructions only for affected behavior. Compare maintenance files separately from skill contents. Selective decisions protect fork identity, local authorization rules, installation instructions, and evaluation requirements.

Every imported skill has a frontmatter pointer to the canonical source inventory. The inventory records the historical import and the completed review independently. Upstream changes can be intentionally rejected without losing their history. See [the provenance contract](../skills/engineering/upstream-sync/references/provenance.md).

## Migration order

The first pilot is the original `upstream-sync` skill. The existing forked catalog stays available. Next, migrate owned skills in small PRs after checking duplicate names, embedded helpers, runtime dependencies, licenses, and publication visibility. The private research inventory and backup stay local; a public fork is not permission to publish private skill bodies.

The next bounded candidates are `grilling`, `diagnosing-bugs`, and the PRD/spec workflow. Choose one canonical behavior per capability and preserve compatibility only when it earns its maintenance cost. Do not move paul-loop runtime, hooks, memory services, or agent orchestration into this library merely to import a skill.

## Development installs

`scripts/link-skills.sh` links promoted and in-progress skills for maintainers. It now refuses existing files or foreign symlinks before writing anything. Test with a disposable HOME; a successful isolated install does not migrate a user's existing global installs.

## Intentional fork differences

- Repository/package/marketplace identity and install commands point to Paul Skills.
- New original skills and evaluation tooling are in scope.
- `skill-sources.json` and `metadata.provenance` track provenance.
- `upstream-sync`, tests, and a validation workflow add repeatable checks.
- Maintainer links refuse collisions. Maintainer Claude context lives under `.claude/`, avoiding the root-plugin context warning while retaining `AGENTS.md` as the source.
- Upstream pending Changesets are retargeted to the fork package so their already-present behavior is described in its first release.

Historical upstream changelogs, ADRs, credits, and source documentation retain attribution. This fork does not claim upstream's official marketplace listing, newsletter, website publishing, or measured model performance.

## Release toolchain

Use Node 22.11 or newer and npm 10.9 or newer (the packageManager field pins npm 10.9.4). The initial inherited Changesets 2 lockfile reported 18 development dependency advisories. Changesets 3.0.3 preserves the same release workflow and removes those reported advisories; version-plan and release execution are checked before adoption. These Node packages are maintainer tooling, not dependencies of installed skill prompts.
