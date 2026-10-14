# Design beta readiness, 2026-10-14

Remaining eight beta roles: information-architecture, user-flow, wireframe, state-machine, break, explain-interface, variant and build-design.

This evaluation adds one independent task pair per role to the dated representative trials. It does not change skills, promote them, install beta skills globally or authorize a release.

- `PROTOCOL.md`: evaluator criteria frozen before executor dispatch.
- `prepared.json`: original revision, protocol digest, per-run input hashes and isolated workspace paths. All eight pairs have identical task inputs.
- `SOURCE-AUDIT.md`: source-only audit written before the new outputs were judged. Its remaining-evidence list is historical to that stage; the final report resolves it against new observations.
- `artifacts/<run>/`: copied generated app, output, final response and executed command receipts. These are untrusted trial outputs, preserved without editorial repair. Their text may not follow repository prose conventions.
- `evidence/`: independent evaluator replays and captures. Evaluator observations are separate from the executor's own browser evidence.
- `run-integrity.json`: completed run receipts, source preservation, output hashes and tool failures.

The served trial workspaces are under `/private/tmp/paul-beta-readiness-20261014/public/runs/`. The isolated authentication link is outside the served directory. No credentials are included in this evaluation folder.

The original source bytes were restored from a frozen earlier trial bundle and verified against all 65 entries in `../design-beta/upstream-manifest.json`. The old temporary clone's incomplete Git metadata is not evidence of a skill regression.

To review archived apps, serve this directory through a local HTTP server. `artifacts/<run>/app/` contains the generated app and any nested workbench. The whole-site explain fixture additionally requires `shared.css` on `http://localhost:48914/shared.css`; its differing host is intentional so CSSOM access fails while computed styles remain available. The live evaluation server supplies that resource.
