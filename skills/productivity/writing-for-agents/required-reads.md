# Complete reads and justified reloads

Use this contract for required skill bodies, branch references and tool instructions. Follow the host's native invocation rules first; reusing context never bypasses an explicit invocation or authorization boundary.

Keep a compact task-local read record when a workflow spans several loads: resolved path, version or content digest when available, active branch, required references, completion status, and the reason for any reload. A path mention, digest or summary locates evidence; none proves that the full instructions reached the current context. Keep full bodies in their canonical files rather than copying them into global memory.

| Current evidence | Next read |
| --- | --- |
| Complete current body and active-branch references remain in context | Reuse them; a repeated mention alone does not require another load |
| Compaction or a handoff retains only a summary or receipt | Reload the body and required references before acting on them |
| Version, source content or resolved path changed | Read the changed source; the old body does not cover it |
| Workflow branch changed | Load its required references; reuse unchanged common instructions only while complete in context |
| Required reference missing, read failed or output truncated | Keep it incomplete; recover the missing body before dependent work |

Resolve paths from the installed skill location, with a matching working directory for relative reads. Bound output to the required document or sections, and inspect each result's status and truncation signal. Independent reads can be batched when each result remains complete and attributable. For long bodies, use contiguous bounded reads and confirm coverage through the end. If a shared output cap drops part of a batch, recover the affected documents separately rather than marking the whole batch read.

Report unavailable instructions as unavailable. A failed load must not become a successful read just because later work continued. During a retrospective, inspect call/output pairs and context or version boundaries before treating repeats as waste. Reuse existing exact-body and trace-read checks where available; raw invocation counts alone establish neither completeness nor avoidable cost.
