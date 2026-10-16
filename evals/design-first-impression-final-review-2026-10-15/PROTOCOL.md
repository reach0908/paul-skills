# Final review dependency repair

The Standards review of PR #26 at `dda64d7a227f9db7b66fa80e16120537b5a8ab8b` found that wireframe directly read another skill's first-impression reference, contrary to `.agents/invocation.md`. Repair only that requested-validation dependency to invoke model-invoked better-layout, retaining the no-Skill-tool fallback and optional/pending behavior.

Run one matched pair before merging. Baseline is the reviewed commit above; candidate is the complete plugin tree frozen in `freeze.json`. Only `skills/design/wireframe/SKILL.md` differs between plugin trees. Use the original brand fixture byte for byte and the same task asking wireframe for a screen specification and a requested three-second precheck. No expected answer, earlier review or grading rule is supplied to either session.

Use fresh neutral working directories, the installed inherited Claude model, explicit low effort, session-local plugins, Skill/Read/Glob/Grep only, disabled hooks/memory, and no file mutations or browser. Per-attempt native cost threshold USD 1, timeout 240 seconds, aggregate reservation USD 3. One pair only; preserve any failure instead of retrying or changing the profile.

Pass criteria: successful better-layout Skill invocation, full first-impression reference read, screen intent and preserved approved brand scope, and explicit distinction between untimed precheck and unperformed human/fresh-AI observation. Invocation must precede use of the owner's reference. Do not count self-reported use as successful invocation. Native completion, source hashes, unchanged input and semantic result remain separate. The implementing maintainer grades final answers unblinded and records response hashes.

Existing evaluation records and frozen source versions are immutable. This pair covers the previously untested requested-validation dependency, not a new complete workflow matrix or human usability test. No-Skill-tool fallback, Codex behavior and installed activation are outside this candidate pair.
