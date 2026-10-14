# Unspecified-target grader correction

The initial matcher rejected any target-bearing command anywhere in the answer. The actual answer first supplied the bare `/paul-skills:interface-review` command, explicitly stated that no target had been selected, and then listed optional examples. Those examples are not an invented selection.

The [initial receipt](initial-unspecified.json) retains the mechanical failure. The corrected matcher checks the primary command's suffix. A negative control still rejects a selected `working` target when the request has none; an added control accepts a bare primary command followed by optional examples. The frozen prompt, source, model response and protocol criterion are unchanged. No model rerun was used for this correction. Manual review must still check that prose does not contradict the primary command.

## Current-screen audit

The initial current-audit matcher also confused a mention with an action: any `/paul-skills:interface-review` string failed the no-redirect condition. The [initial receipt](initial-current-audit.json) shows a current-screen plan that names all six owners and only conditionally explains the separate change-review command. The requested screen audit is not blocked on that command. This semantic distinction is now assessed explicitly in [manual-review.json](../manual-review.json), by the parent agent, and fails closed if that assessment is missing. It is not a new model run or a change to the task or acceptance criterion.
