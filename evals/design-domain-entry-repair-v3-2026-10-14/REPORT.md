# Domain discovery and reference-reading repair, candidate 7

**HOLD.** Codex passed 27/27 fresh sessions and Claude passed 26/27. The remaining Claude failure is preserved in [authorized-handoff](claude/authorized-handoff.json): its scope and finding were correct, but only accessibility was loaded after the router, omitting five installed domain owners. The [next candidate](../design-domain-entry-repair-v4-2026-10-14/REPORT.md) qualifies direct-review exclusion and strengthens the all-six-owner handoff.

## Changes and native evidence

The shortened Codex catalog omitted the later ordering guard in [candidate 5](../design-domain-entry-repair-2026-10-14/REPORT.md). Moving the ordering guard to the front in [candidate 6](../design-domain-entry-repair-v2-2026-10-14/REPORT.md) made it visible but did not stop co-loading. Candidate 7 instead excludes direct discovery of change/regression reviews from each domain. All 27 Codex receipts retain the actual delivered descriptions.

Reference reading now uses resolved native paths and checks each result. The earlier unpassed shell positional parameter is replaced by ordinary prose. This also avoids Claude substituting invocation arguments into the instruction. Exact-body checks retain that mutation as a failure in candidates 5 and 6.

The color preparation repeats completed 17 exact reference reads in Codex and 11 in Claude, without a reference-read error. Source identity, native cwd, call IDs and complete content are checked; filename mentions alone do not count. [Reference evidence](reference-reads.json).

## Matrix

| Cases per host | Codex | Claude |
| --- | --- | --- |
| Eleven automatic/explicit referral boundaries | 11/11 | 11/11 |
| Ten normal entries, including repeated color preparation | 10/10 | 10/10 |
| Three explicit working preparations | 3/3 | 3/3 |
| Three actual HEAD/index/working handoffs | 3/3 | 2/3 |
| Total | 27/27 | 26/27 |

The actual fixtures put main behind HEAD and deliberately disagree between index and working contents. Staged must find Panel's index Regression; working must exclude the canceled Panel change and include untracked New.html. All scopes passed. Failure to load every domain is still a failure even when the final finding is correct.

All 54 sessions completed without retries, timeouts or environment failures. Claude reported USD 12.6856912 at list prices; actual billing is unavailable. Codex token usage is recorded without an invented dollar conversion. Models are gpt-5.6-sol/medium and claude-opus-5-5/xhigh. Daily 0.4.1 installs were not changed.

## Verification and limits

The frozen bundle contains 175 files. Original 0.4.1 domain rule bodies remain unchanged after excluding the new entry and reference-reading guidance; the existing audit procedure is preserved. Package checks passed 38 tests, and this candidate's grader controls passed 24 tests. Native expected no-match exits and relative-path evidence corrections are explained in [GRADER-NOTES.md](GRADER-NOTES.md), with controls that retain real missing-file errors as failures.

Run `python3 evals/design-domain-entry-repair-v3-2026-10-14/verify_evidence.py` to verify frozen evidence. An integrity pass does not turn the failed handoff into a behavioral pass. This is an adaptive repair matrix with a maintainer-agent semantic review, not an independent blinded comparison or proof of 17-role superiority. No rendered product QA, publication or global installation of this candidate was performed.
