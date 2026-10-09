# Canonical installation commands

This fork uses its own marketplace. It is not listed in `claude-plugins-official`. Choose either the plugin or editable skills per host; installing both duplicates skill names. Marketplace installation and updates are separate from upstream source reconciliation.

## Claude Code

```bash
claude plugin marketplace add reach0908/paul-skills
claude plugin install paul-skills@paul-skills
```

To update manually:

```bash
claude plugin marketplace update paul-skills
claude plugin update paul-skills@paul-skills
```

Custom-marketplace auto-update is a host setting. Enable it for `paul-skills` in `/plugin` > Marketplaces if desired; do not assume the official marketplace's defaults apply to this fork.

## Codex

```bash
codex plugin marketplace add reach0908/paul-skills
codex plugin add paul-skills@paul-skills
```

The host manages the installed bundle. Release versions come from `package.json` and are synchronized to the plugin manifest. Inspect the installed version after an update; source HEAD alone does not prove activation in an existing session.

## Editable or individual skills

```bash
npx skills@latest add reach0908/paul-skills --skill upstream-sync
```

For other skills, replace `upstream-sync` with the desired name. Run `npx skills@latest update` for existing installs; re-run `add` for new skills. These editable copies need manual updates.

Inherited engineering flows still use `/setup-matt-pocock-skills` and `/ask-matt`; those names are retained for compatibility. `upstream-sync` is standalone and does not need the issue-tracker setup.
