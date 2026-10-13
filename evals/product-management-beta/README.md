# PM beta evaluation

These are public development cases with a synthetic Pocket Cards product, not copied private projects or session extracts. The candidates start in in-progress and are not promoted by this record.

## Protocol

Compare a no-skill baseline with a supplied candidate on identical Korean task and raw artifact bytes. Use fresh in-session Codex collaboration agents, inheriting the same parent settings with no model or effort override. Give each worker only its own task/input folder and, for the candidate arm, a copied skill tree with its applicable references. The baseline must not read/invoke skills. Both arms are offline, may edit only their supplied product artifacts and produce result.md. No network, external contacts, paid calls, services or delegation. Candidates receive no rubric, expected answer or other arm output.

The evaluator owns criteria outside worker folders and reads raw outputs after execution. Check sufficient-context progression; scoped decision/rule preservation; AI-proposal status; opening/selection/saving/completion and prototype/actual-state distinctions; inconclusive/budget stopping and next decisions; current-authority handoff; UI-QA boundary. Each check is a concrete observation, not a prose quality score. Record weaknesses in either arm. One run per arm/case provides smoke evidence only.

The maintainer trial harness uses scripts/link-skills.sh in a disposable HOME, linking all eligible baseline skills plus candidates without changing daily installs. This is link-harness evidence, not automatic host activation. Actual workers explicitly read copied workflows; no Skill tool execution receipt is claimed.

## Records

See RESULTS.md for observed outcomes and any bounded repair/recheck. trials.json records parent revision, per-skill tree digest, host/settings visibility, raw artifact paths and decisions. cases/ preserves identical task and input bytes; artifacts/ preserves raw outputs and edited products. Candidate snapshots preserve the exact loaded trees. Missing duration/token/cost telemetry is null. No model ranking, statistical superiority, product quality, customer effect or human acceptance is claimed.

## Reproduce

Use the recorded repository revision and candidate snapshot/digest. Create a disposable directory outside daily installs and copy each cases/<case>/input tree twice. Give both fresh agents the same task.md and offline permissions; load only that case's candidate in the second arm. Ask each to write result.md and keep the grading material outside both folders. Judge with the above observation criteria after collecting the outputs. Preserve failed runs and any repair separately. The fixtures are public smoke cases, not hidden holdouts.

For installation mechanics alone, run HOME=/path/to/disposable-home bash scripts/link-skills.sh in a child process. The isolated agent arms here do not require credentials or a paid API matrix. Additional repeated trials, realistic-user acceptance and host routing tests are follow-up work after this bounded comparison.
