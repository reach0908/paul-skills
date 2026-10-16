# Browser preflight and recovery

Run this once per scenario entry and after a connection, target or access change. Reuse the owning project's start command and selected tool's installed help. Preserve an explicitly chosen tool and account; preflight is not permission to install a different driver, reset shared data or widen access.

## Establish readiness

Record target URL and revision when known, chosen tool/version, session ownership, required access and the checks below. Use `ready`, `blocked`, `unknown` or `not_required` for each check, with observed evidence. `unknown` is not ready for an observation that depends on it.

| Check | Evidence needed |
| --- | --- |
| Tool available | Installed command/help or native tool capability; version if exposed, otherwise unavailable |
| Browser connection | A disposable blank/test page can be opened and inspected, or a safe fresh snapshot succeeds in the user-designated tab |
| Target reachable | The intended local server/route or remote URL responds and the expected surface loads; a redirect to login is not a missing server |
| Required access | The designated session reaches the needed authenticated state; public pages need no login check |

With a CLI, confirm the session survives between setup and the next command, not merely that launch returned an ID. With a native browser tool, use its supported snapshot sequence. Check only the current scenario's needs and reuse a working transport. Keep setup time and retries separate from task actions. For fresh-participant walkthroughs, do transport setup on a blank/test page, then give a clean starting state without UI hints. The observation time/action budget begins after readiness, not while repairing infrastructure.

## Recover without erasing the attempt

Classify the observed failure at its layer: `tool_unavailable`, `browser_unavailable`, `target_unreachable`, `access_required`, or `unknown`. Keep the error and affected check; do not guess a cause from an empty screenshot. Missing login access is different from a successful authorized action that returns a product error, which remains product evidence.

Try a bounded recovery when a specific cause and an authorized action are known, such as starting the documented local server or reconnecting the task-owned session. Retry once after that change. If the same failure persists without a new cause or changed state, stop that path and leave the unmet dependency visible. Continue independent observations where possible. A different tool or account follows the user's choice and host policy; silence is not fallback approval.

Leave a resume record with target/revision, preflight results, exact error, attempted recovery, last verified route/state/viewport, preserved artifact paths, remaining observations and the one dependency to restore before retrying. Close only owned resources. Retain earlier successful observations with their original conditions, and mark the interrupted or later attempt unavailable rather than overwriting it as a product failure or pass.
