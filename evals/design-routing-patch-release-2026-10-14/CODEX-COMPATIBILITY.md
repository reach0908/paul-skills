# Codex compatibility follow-up

The initial inherited-model run stopped after two environment failures before model output. CLI 0.146.0 inherited gpt-6.1-sol, reported unknown model metadata, and returned a startup message that this model is unsupported with the current ChatGPT account path. Both turns ended with retry-limit HTTP 429. This does not establish an account-wide rate limit or a skill failure.

A fresh app-server model/list response exposes gpt-5.6-sol as its default, plus gpt-5.6-terra and gpt-5.6-luna. Retry all six frozen cases in separate fresh directories with gpt-5.6-sol explicitly selected for this experiment only. Preserve the inherited reasoning effort and every other constraint. Do not edit global configuration. Keep the two original failed launches separate from the six compatibility trials, with no answer-based rerolls. This verifies the installed plugin on the supported CLI model, not gpt-6.1-sol or the already-open desktop conversation.
