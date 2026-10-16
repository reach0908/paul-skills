# Claude native evaluation suite

Cases for `claude plugin eval`, plus the rubric, verdict and calibration tooling around them. The runner executes a fresh Claude session per case with only this plugin loaded, then applies the case graders. This directory turns those grader results into rubric verdicts that a maintainer can review and compare over time.

Status: eleven development cases for `research`, `interface-review`, `user-flow`, `build-design`, `better-interface` and `diagnosing-bugs`. Seven come from behavior observed in recent real Claude Code and Codex sessions; the private sessions stay outside this repository and each case records only episode IDs. Expected verdicts and judge criteria are AI drafts that the user accepted without itemized review (`goldStatus` stays pending human confirmation). The judge was chosen by calibration (see [Choosing the judge](#choosing-the-judge)), and the [first unreviewed pilot record](records/2026-10-17-pilot3/README.md) is committed.

## What a verdict means

| Layer | Question | Covered here |
| --- | --- | --- |
| Install and discovery | Is the intended version installed and discovered by the host? | No. See the installation records in [../README.md](../README.md). |
| Invocation | Is the skill used when needed, and only then? | Yes: indicators, explicit-invocation and routing-boundary cases |
| Task outcome | Did the run meet the request and its constraints? | Yes: required criteria per case |
| Comparative value | Is it better than no plugin or the previous version? | No-plugin arm for `group-with-without`; previous version not automated yet |

The native score is the weighted fraction of passed graders, averaged over runs. It is reported as `nativeScoreInformational` and never used as a verdict. [rubric.json](rubric.json) holds the rules:

- Any failed required criterion fails the run. Nothing offsets it.
- A grader the runner did not judge (cost ceiling, `skippedPaidGraders`) is `unknown`, not `fail`. A run with `error` is `excluded` and counted, not scored as zero.
- With no failure, an `unknown` or `pending_human` required criterion leaves the run `undetermined` or `pending_human`.
- Quality (`usable`, `minor_edit`, `rewrite`) is a human judgement made only after every required criterion passes. `rewrite` is a `quality_hold`.
- A pass or fail decided by an LLM grader that has not been calibrated for the run's judge model is marked `provisional`.

Run verdicts are `fail`, `undetermined`, `pending_human`, `required_pass` (quality not yet reviewed), `quality_hold`, `pass` and `excluded`. Task status (`complete`, `intended_stop`, `partial_or_dependency_wait`, `incomplete`) is recorded separately by the reviewer.

## Layout

| Path | Role |
| --- | --- |
| `rubric.json` | Criterion IDs and text, verdict rules, and the skill revisions the criteria were written against |
| `suite.json` | Per-case profile: required, quality and not-applicable criteria, human-judged criteria, harness-enforced criteria, trace checks, calibration expectations and `input_match` controls |
| `<case>/case.yaml` | Runner case. Written in JSON-compatible YAML so checks need no YAML library |
| `<case>/prompt.md` | The user request given to the candidate |
| `<case>/scaffold.sh` | Self-contained fixture builder, run in the empty workspace with `--scaffold` |
| `calibration/<case>/` | Labelled pass, fail and boundary artifacts for grader calibration |
| `calibration/status.json` | Written after a reviewed calibration run; absent until then |
| `tools/native_eval.py` | `check`, `plan`, `stage`, `run`, `record`, `calibration-cases`, `calibrate`, `cross-judge` |
| `results/` | Runner output, ignored by Git |

`traceChecks` in a profile are deterministic order and count checks that `record` evaluates on each run's trace, matching `file_path`, `command` or `skill` fields one at a time. They exist because the runner's `tool_order` takes one tool name, while an Edit grant also allows Write, and because `input_match` searches the whole JSON input, where file contents and import lines live. A missing trace makes a trace check `unknown`. `run` keeps the run directories and copies each trace next to the result.

Every grader name starts with the criterion it evidences (`R2-owner-citations`) or `IND-` for an unscored invocation indicator. A required criterion is satisfied by its graders, by a human verdict (`human` in `suite.json`), or by a documented harness constraint (`harnessEnforced`, for example a tool missing from `allowed_tools` that the runner withholds). The runner hides the eval directory from the candidate; the `C4` graders also record any attempt to read it.

## Cases

| Case | Rubric | Group | Checks | From sessions |
| --- | --- | --- | --- | --- |
| `research-atlas-v2` | R-01 | with-without | Version-bounded answer from conflicting sources, owner citations, no invented speed, saved and re-read report | Rubric draft |
| `research-same-name-tools` | R-02 | with-without | Two hosts ship a tool with the same name; the answer depends on which is meant | A11 |
| `research-requirement-conflict` | R-03 | with-without | Two user goals conflict on the evidence; the report surfaces the decision | E8 |
| `research-unreadable-evidence` | R-04 | with-without | One evidence file cannot be read; it stays unverified instead of missing | D4, E5 |
| `interface-review-staged` | I-01 | single-arm | Explicit `staged` review where index and working tree disagree; planted keyboard regression; pre-existing width; lockfile; read-only | Rubric draft |
| `interface-review-unnamed` | I-N | single-arm | A review request that does not name the skill gets the explicit command and stops before any git inspection | Rubric draft |
| `interface-review-flow-change` | I-V | single-arm | "How did flows change on main" is a change review: the command, not `user-flow` | B6 |
| `better-interface-settings-audit` | A-01 | with-without | Current-screen audit: entry, procedure and six owners before inspection; planted unnamed button and vague error; no invented defects | C7, B1 |
| `user-flow-export-panel` | U-01 | with-without | Async export with close and reopen in all four states, key and receipt rules, one undecided policy | Rubric draft |
| `build-design-scoped-card` | B-01 | edit-with-without | Restyle one card while an approved shell and decision stay intact; report the spec conflict as a deviation | C1, C2, E4, B5, E1, D1 |
| `diagnosing-bugs-scroll-reset` | G-01 | code-with-without | Reported scroll reset that existing tests miss: red-capable loop and regression test before the fix | B9, D14, D3 |

Episode IDs refer to a private review of 33 top-level sessions from 2026-10-03 to 2026-10-17. Episodes that need a browser, a live service, concurrent sessions or an in-progress skill remain candidates outside this suite.

Each group fixes the ablation and grants that the runner applies to a whole invocation, so each group runs separately:

| Group | Ablation | Grant | Why |
| --- | --- | --- | --- |
| `group-with-without` | `with-without` | `Write` | The task is meaningful without the plugin, so the no-plugin arm measures added value |
| `group-single-arm` | `none` | `Bash(git:*)` | Explicit invocation and its routing boundary do not exist without the plugin |
| `group-edit-with-without` | `with-without` | `Edit` | Only existing files can change |
| `group-code-with-without` | `with-without` | `Edit`, `Bash(node:*)`, `Bash(npm:*)`, `Bash(git:*)` | Bug fixing with tests |

A criterion listed in `notApplicableWithout` (for example loading the audit procedure) is `n/a` in the no-plugin arm instead of a failure.

## Workflow

1. **Static check** (free, also part of `npm test`). Validates profiles against the rubric and case files, runs every regex grader against the labelled artifacts with JavaScript semantics, and runs the `input_match` controls.

   ```bash
   npm run eval:check
   ```

2. **Plan check** (free, needs the `claude` CLI). Each group runs with `--max-cost-usd 0`, so the runner parses and plans every case, reports graders that cannot pass with the granted tools, and stops before the first model run. Exit 2 with no warnings is success.

   ```bash
   npm run eval:plan
   ```

3. **Calibrate the judges** (paid, small). Generated cases write a labelled artifact in the scaffold and ask the agent to do nothing, so the real judge grades a known answer. Only artifacts with LLM graders get a case; regex-only artifacts are already covered by step 1. The agent only replies `done`, so a small model is enough. A Codex model can judge the same artifacts with the same criteria through `codex exec`, isolated from user config, rules and session history. Review every `false_pass` and `false_fail`, fix criteria or artifacts, and repeat until none remain. Save the chosen judge's reviewed result as `calibration/status.json`.

   ```bash
   python3 evals/claude-native/tools/native_eval.py run calibration --out evals/claude-native/results/cal-claude-opus.json \
     -- --model claude-haiku-5-5 --judge-model claude-opus-5-5 --concurrency 4
   python3 evals/claude-native/tools/native_eval.py calibrate evals/claude-native/results/cal-claude-opus.json \
     --out evals/claude-native/results/cal-claude-opus.status.json

   python3 evals/claude-native/tools/native_eval.py cross-judge --model "$CODEX_JUDGE_MODEL" \
     --out evals/claude-native/results/cal-codex.json
   python3 evals/claude-native/tools/native_eval.py calibrate evals/claude-native/results/cal-codex.json
   ```

4. **Run a group** (paid). `run` stages a small copy of the plugin (the manifest, its skills and the eval directory), applies the group's ablation and grants from `suite.json`, and writes `<out>.meta.json` with the exact command and the stage digest. The runner refuses a plugin directory with more than 20000 entries, so running from the repository root fails. Pin both models and keep the report local; `run` always passes `--no-publish`.

   ```bash
   python3 evals/claude-native/tools/native_eval.py run group-with-without \
     --out evals/claude-native/results/group-with-without.json \
     -- --model "$EVAL_MODEL" --judge-model "$EVAL_JUDGE_MODEL" --runs 1 --max-cost-usd "$EVAL_BUDGET_USD"

   python3 evals/claude-native/tools/native_eval.py run group-single-arm \
     --out evals/claude-native/results/group-single-arm.json \
     -- --model "$EVAL_MODEL" --judge-model "$EVAL_JUDGE_MODEL" --runs 1 --max-cost-usd "$EVAL_BUDGET_USD"
   ```

   `--trust-plugin` is passed only because this repository authored the suite.

5. **Record and review.** Produce a record, read the traces (`tracePath`) and outputs, add human verdicts, then record again.

   ```bash
   python3 evals/claude-native/tools/native_eval.py record evals/claude-native/results/group-with-without.json \
     --human review.json --out record.json
   ```

   ```json
   {"reviewer": "maintainer", "reviews": [
     {"case": "research-atlas-v2", "arm": "with", "run": 0,
      "criteria": {"C2": "pass"}, "quality": {"RQ1": "usable", "RQ2": "minor_edit"},
      "taskStatus": "complete", "notes": "why"}]}
   ```

   A human `fail` overrides passing graders. Commit reviewed records and review files under `records/<date>-<label>/`. Fixtures are synthetic, but read raw output before committing any of it.

6. **Decide.** A confirmed required failure or regression holds the candidate for that scope. Insufficient evidence is undetermined. Passing development cases supports only an observation on those cases. Promotion still needs the user's validation and explicit approval.

## Improving the suite

- **Start from real behavior.** A failure seen in use becomes a case, and a success worth keeping becomes a regression case. Record where it came from.
- **Criterion first.** Add or reuse a rubric ID, then a grader named after it. Give every LLM-graded criterion a known-good artifact and a known-bad artifact with a single cause, plus a boundary artifact where people would disagree.
- **Splits.** `development` cases are visible and may shape a skill. `validation` selects among candidates. `holdout` stays outside this repository and is never used for tuning; copy it into a disposable checkout's eval directory at run time, since the runner reads cases only from below the plugin. `regression` keeps behavior that already passed. A case used to change a skill becomes development.
- **When a skill changes,** re-run its cases and the regression cases. For a previous-version comparison, run the same command from a worktree of the previous release and compare the two records; this comparison is not yet automated.
- **Choose the judge by calibration, not by tier.** See [Choosing the judge](#choosing-the-judge) for the comparison behind the current choice.
- **When the judge model changes,** recalibrate. Calibration is tied to the judge model, so LLM verdicts become provisional again until it is re-run.
- **When the rubric changes,** bump `rubricVersion`, re-pin `contractRevision` and the skill trees in `rubric.json`, and set `goldStatus` back to `ai_draft_pending_human` if expectations changed.

## Choosing the judge

A judge only checks a short artifact against concrete criteria, which is easier than producing it, but a weaker or same-family judge can be persuaded by a plausible wrong answer. Native `llm` graders accept only Claude models, so a Codex model judges the same artifacts with the same criteria through `cross-judge`. Each round below ran every calibration artifact three times with three votes per grader (24 runs).

| Round | Change before the round | Opus 5.5 | Sonnet 5.5 | Haiku 5.5 | Codex gpt-6-astra |
| --- | --- | --- | --- | --- | --- |
| 1 (1 run) | none | 0 false pass, 5 false fail | 1, 6 | 0, 4 | 0, 4 |
| 2 | U2 exempts undecided rows; U-F rebuilt as a single-cause failure | 0, 3 | 3, 13 | 1, 1 | 0, 5 |
| 3 | U2 judges only table rows; the exemption covers feedback | 0, 0 | not run | 2, 0 | 0, 0 |

Shared false fails across all judges pointed at the criteria and artifacts, not the judges, and were fixed there. After that, Opus and Codex agreed with every expectation; Haiku passed the U-B close omission in two of three runs, and Sonnet passed it in every run of round 2. Opus 5.5 is the native judge and Codex the cross-check. After the session-derived cases and their single-cause failure artifacts were added, Opus agreed with all 525 judged expectations over 132 runs, and `calibration/status.json` records it for each grader's exact criteria text. Codex disagreed on 21, mostly by judging research citations (R2) and invented claims (R4) more strictly; [the comparison](records/2026-10-17-pilot3/judge-comparison.json) lists them for criteria review. Where the two judges split on an expectation, it became a human judgement. Judge cost per 24-run round was about $12.4 for Opus, $5.6 for Sonnet and $0.4 for Haiku. These are eight-artifact development results, not a general ranking of the models.

## Known limits

- Aggregate JSON schema 1 reports cost, turns and duration but no token usage, so tokens are `null`.
- Whether the eval session expands `/paul-skills:interface-review staged` as a skill invocation is not yet observed. `I1` stays human-judged for `interface-review-staged` until a trace shows how it appears.
- Always pass `--eval-dir`. A bare `claude plugin eval .` scans every `case.yaml` under `evals/`, including generated calibration cases, under one set of grants.
- `input_match` patterns are heuristics checked by the controls in `suite.json`. For example, `git grep -e add` would trip `I7-no-checkout-mutation`.
- An Edit grant also allows Write. `check` requires every zero-call Edit or Write grader to have a twin on the other tool, rejects single-tool graders that need a file change, and requires Edit/Write `input_match` patterns to start at `"file_path"`. The second pilot lost a correct build-design run and two correct diagnosing-bugs runs to these mistakes.
- Every LLM grader needs at least one pass and one fail calibration artifact for its criterion and target; `check` enforces it.
- `tool_used` counts must fall within `min` and `max`, and `min` defaults to 1. A zero-call grader needs `"min": 0, "max": 0`; `check` rejects `max: 0` without it. The first pilot lost every zero-call check to this.
- A record flags `rubric_contract_drift:<skill>` when a skill tree differs from the one in `rubric.json`; the criteria may then describe an older contract.
- The aggregate JSON does not record the tools granted. A record made from a `run` launch compares the recorded grants with `suite.json`; a hand-launched run is flagged `launch_command_not_recorded`.
- Calibration grades a file even for graders that read the final message in a real run.
- Runs are single-turn; multi-turn behavior needs a `history_file` case.
- This suite measures Claude Code only. Codex behavior keeps its own records.
