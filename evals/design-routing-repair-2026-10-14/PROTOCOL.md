# Design review routing repair

The task is to repair the invocation boundary between `better-interface` and `interface-review`, then reassess the first nine design candidates. Promotion is a separate user decision.

## Frozen inputs

Use the previous installation trial's HTML and prompts unchanged for ordinary review, explicit `interface-review working`, unnamed uncommitted review and unrelated arithmetic. Run the unnamed uncommitted prompt in two independent contexts. Add one staged-only request to check target preservation. Each case has its own Git workspace and starts with a new `codex exec`, without conversation history or a previous result.

Install the existing 27 promoted paths plus the nine candidates as a real plugin in an isolated `CODEX_HOME`. Copy whole skill folders, compare every installed file to its source hash, and retain the original invocation metadata. The release manifest and daily installation remain outside this trial.

The existing CLI-compatible model is `gpt-5.6-sol` with `xhigh`. This is a fixed model for the routing repair, not a model comparison. A new CLI context is not evidence of a new desktop chat or a Claude Code model run.

## Acceptance

| Case | Required observation |
| --- | --- |
| Unnamed uncommitted review, twice | Load the routing skill, return `interface-review working`, inspect no diff or source, and issue no review verdict |
| Unnamed staged review | Same terminal routing behavior, with `staged` rather than `working` |
| Ordinary screen review | Automatically choose `better-interface`, load all six domain owners, preserve the keyboard finding, and declare unverified runtime behavior |
| Explicit change review | Load `interface-review`, resolve the requested scope, continue into all six owners without a routing loop, and distinguish the keyboard regression from the existing width problem |
| Unrelated arithmetic | Return 102 without tool use |
| All cases | Preserve fixture contents and finish the model turn successfully |

Inspect the actual commands and final reports as well as the mechanical checks. Skill headers in read output establish loading, not review quality. Review quality requires the known fixture causes, classification and verification limits. Source-only review cannot claim a browser test.

After the first attempt omitted the duplicate-detail writing finding, add a supplementary comparison with the previous valid screen findings: keyboard reachability, fixed minimum width, duplicate detail content and browser font preferences. Apply it to both attempts and repeat the ordinary screen request in a seventh fresh context for the final candidate. This is an observed-failure follow-up, not a predeclared or unseen test. Preserve both the first omission and any later failure.

## Reproduction and evidence

`prepare.py` creates a new trial and refuses to overwrite one. `run_session.py <case>` executes one fresh context. `probe_catalog.py` inspects the installed catalog. `collect.py` preserves results and checks both attempts, retaining a failed staged target from the first attempt. The final attempt is the default; `PAUL_TRIAL_ATTEMPT=1` selects the first attempt's locations. Change the trial date or attempt for a new execution rather than reusing completed output files.

The temporary authentication link points to the existing login solely for authorized tests and is removed after execution. Credentials are never included in the evidence. Raw CLI events remain in `.scratch`; structured evidence records commands, final answers, identities and raw-event hashes.

Do not relabel historical source-parity trials as executions of the edited bodies. Compare unchanged domain and review-rule sections, then use fresh routing and positive review tests to cover this delta. The remaining seven candidate trees must match the previous install trial. This repair does not repeat browser QA or prove behavior for every wording, model or platform.
