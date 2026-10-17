# PM conversation and AI walkthrough beta

These development fixtures exercise the office-hours conversation, fresh AI prototype task/interview workflow and PM handoff. They use synthetic products only. This is not a human usability study, source-parity proof or promotion decision.

Serve fixtures/shelf on localhost for a disposable browser walkthrough. The participant receives neutral tasks only; the moderator keeps intended behavior and comparison criteria separate. Preserve the original participant packet, actual observations and post-task interview.

See SOURCE-REVIEW.md for source identity/adaptation and RESULTS.md for actual runs, failures and limits. Skill hashes and artifacts are recorded separately from judgments.

## Try the individually installed beta

- `$office-hours`: work through an open idea; the conversation carries the chosen mode and unanswered question across turns.
- `$prototype-user-test`: supply the runnable URL, the author's intended outcome and permitted actions. The moderator withholds expected routes from fresh participants, observes their attempts and interviews them afterward.
- `$product-brief`: preserve the current decisions or prepare the next role with the selected prototype and unresolved dependencies.
- `$experiment-design`: plan a consequential test or interpret actual results, keeping AI walkthrough evidence separate from human evidence.
- `$problem-discovery`: recover missing product context without starting a second interview.

These are unnamespaced individual betas alongside the promoted Paul plugin. They are not included in that plugin's skill list. `ask-matt` in the development branch includes their optional map; a released plugin router updates only when a release containing that map is installed.

## Public evidence copies

The observations and judgments describe the original 2026-10-14 runs. Eight public artifact copies now replace only the author home-directory prefix with `$HOME`; all failures, actions and timings remain. `public-copy.json` records the original commit, original/public file hashes and ten replacements. `integrity.original.json` preserves the original manifest. Embedded freeze manifests still describe those original bytes; use the ledger to locate the corresponding public copy. Original bytes remain recoverable at the recorded Git revision.

The same ledger records the verifier as a separate maintenance amendment because it was included in the original artifact manifest. This amendment validates public copies; it is not a new observation or an edit to the historical verdicts.

Run `PYTHONDONTWRITEBYTECODE=1 python3 evals/pm-conversation-beta/verify.py` to check the public artifacts, ledger and five evaluated skill trees. This is integrity evidence, not a new behavior trial or approval to promote the beta. The earlier three-skill trial is verified separately through its recorded snapshots.
