# Retrospective improvements: local verification

Status: candidate source changes and bounded local verification completed. No release or global installation performed.

## Scope

The user selected the remaining findings from a seven-day Codex/Claude retrospective and required local verification. Private session histories remain outside this repository. The fixtures here are synthetic reproductions of the observed task classes.

| Priority | Finding | Candidate change |
| --- | --- | --- |
| P1 | F1: confusing similar components | Map reference route/section/state to an actual export, target call site and preserved behavior; verify same-state captures and interactions |
| P1 | F2: existing grader tests outside the normal entry point | Already completed in `7465b52`: local check command, with GitHub workflow unchanged |
| P2 | F3: drifting prototype criteria and public-copy roles | Reuse approved brief/baseline; hold benefits and approved elements fixed; assign string roles and keep internal notes separate from useful product status |
| P2 | F4: repeated and incomplete reads | Complete-read contract, contextual reuse and explicit reload conditions; existing exact-body/trace controls reused |
| P2 | F5: unavailable browser reruns | Check tool, connection, target and access readiness; bounded recovery; preserve earlier observations and leave a resume record |

Promoted skill roles, invocation policies and default browser routing remain unchanged. Shared guidance does not add project-specific content rules or install a host-wide read cache. The unmerged PM beta is preserved; its installed prototype-user-test already delegates infrastructure checks to design-browser, so no beta source or global install was changed.

## Evidence boundary

See [the fixed protocol](PROTOCOL.md) and [structured results](results.json). Package checks and grader controls validate repository consistency and grading behavior. Fresh-agent fixture results and record replay are reported separately. They cannot establish a general improvement rate, token savings, human usability or production readiness. No CI, remote publication, release or global installation is part of this pass.

Local adaptations retain all immutable imported and reviewed revisions and existing reconciliation digests in `skill-sources.json`. The new decisions record local behavior changes; no upstream review was performed or advanced.

## Observed candidate behavior

| Case | Actual result | Evidence and limits |
| --- | --- | --- |
| F1, existing component | The agent distinguished two identically named exports through their call sites. Only the Collection branch changed, using the same topic-card export and data as Library. Both component bodies and CSS remained byte-identical. | [Implementation report](outputs/reuse/WORK-REPORT.md), [browser observations](outputs/reuse/evidence/after-results.txt). Four route/viewport cases at 390 and 1280px passed item counts, styles, bounds, natural Tab/Shift+Tab, focus and both Enter destinations; recommended-writer action remained intact. |
| F3, comparison and copy | Three alternatives retained the original baseline, three agreed benefits, wordmark, cream/green direction, CTA wording/destination and useful offline status. Internal research identifiers stayed outside the page. Each alternative answered the same grouping/sequence question. | [Comparison report](outputs/prototype/WORK-REPORT.md), [browser observations](outputs/prototype/evidence/browser-observations.txt). Six cases at 320 and 390px covered overflow, keyboard switching and reload state; bottom-content bounds were also recorded. Original header/main/footer markup remained present in baseline A. Preference and comprehension remain unmeasured. |
| F4/F5, continuation from records | Six read decisions distinguished reusable current instructions from context loss, a new version, a changed branch, truncated output and failed loading. Four browser records kept v1 evidence separate from v2, classified browser/server/access blockers and stopped unchanged retries. | [Decisions](outputs/records/decisions.json), [analysis report](outputs/records/WORK-REPORT.md). These are decisions about synthetic records, not live authentication/server failure experiments or an observed read-cache implementation. |

The coordinator inspected changed source, structured observations and representative screenshots rather than accepting summaries alone. The fixture's original components/styles and prototype baseline were compared byte-for-byte; rendered product copy was checked for the synthetic internal identifiers. Original and retained artifact digests are recorded in [retention.json](retention.json), with personal path redactions and exclusions stated explicitly.

Both implementation agents reported initial local socket/cache permission failures. A task-owned server, writable temporary browser state and supported session transport allowed subsequent local observations. Those recovery reports remain visible. The prototype agent also reported an overly broad temporary-directory listing while looking for instructions; it reported no reads of other case contents or prior conclusions. This is bounded fresh-context evidence, not a sealed holdout or a claim of flawless process compliance.

## Local checks

- `npm run check:local`: passed. Package/plugin/lock metadata matched 0.4.5; 56 skill records and 44 promoted paths remained consistent; 38 helper tests and 26 existing grader controls passed. The extra controls remain outside GitHub Actions.
- `claude plugin validate . --strict`: passed.
- Skill Creator `quick_validate.py`: five changed model-invoked skills passed. `retro` and `ask-matt` were rejected for their existing `disable-model-invocation` field. The same diagnostic occurred on their unchanged baseline. Repository and plugin validators accept this required explicit-only policy, so it was preserved.
- Source inventory invariants: imported/reviewed revisions, source definitions and reconciliation digests unchanged.
- Authored Markdown references, document sections and whitespace were checked locally. New FAQ material came from the retrospective and the user's local-verification question; the optional question wiki was absent and the existing changelog supplied historical context.

## Remaining limits

These explicit candidate checks do not measure automatic Codex/Claude discovery, compare against the previous skill version, prove human usability, or establish lower token cost. Real-service benchmarks, login recovery, live deployment and global plugin activation were not exercised. F4 supplies a read contract and existing grading controls, not a global cache or complete host adapter. Project-specific editorial checks stay in their owning products.

The next validation opportunity is real use of these source changes. Preserve any future failures with their source revision and observed state before considering further instructions or promotion.
