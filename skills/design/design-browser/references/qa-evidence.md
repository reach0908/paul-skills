# Executable QA evidence

Before running, make the caller's acceptance criteria a case matrix: route, revision, viewport, state, expected items and actions. Record skipped or unavailable cells individually. An interaction after a viewport loop covers only the final viewport.

## Fail on missing evidence

Assert the expected item count before iterating. Take the expectation from the task or fixture, separately from the DOM under test, so an empty or shortened list cannot pass vacuously. Assert the number of completed cases against the matrix too.

Turn measured limits into failures. For horizontal overflow, compare document scroll width with the document client width after lazy content has loaded at each viewport. Check the scoped component's bounds as well: clipped content can fail while the document still fits. Record the measurement and any deliberate tolerance. Printing an overflow flag is observation, not an assertion.

Preserve partial observations and the failed case when an assertion fails. Check both the CLI exit status and structured error output, and propagate failure through the runner. A cleanup failure must remain visible without replacing the original assertion failure.

## Keyboard cases

Start each viewport/state on a fresh navigation with no hash or previous focus. Record the initial active element, then use real Tab to reach the scoped controls. A bounded search must fail if its target is not reached; record the intervening focus path. Programmatic focus may set up a separate activation probe, but it does not prove natural keyboard reachability.

At each scoped control, verify the expected Tab and Shift+Tab order, visible focus and resulting Enter action. Record the actual viewport with the result. Return navigation can restore focus; use a fresh navigation for another entry-path test. Reuse representative activation checks only when the case matrix explicitly names that smaller scope.

## Verify the checker

When repairing a missing assertion, use a disposable local page to show that the checker rejects the corresponding defect, such as a removed item, forced horizontal overflow or a control removed from the tab order. Keep the mutation separate from the assertion under test, reset it with navigation, and retain normal and failing runs. Do not weaken the expected result to accommodate a failed test. These checks validate the harness; they do not count as independent skill-quality trials.
