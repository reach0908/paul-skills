# Explicit design-role fixtures

Fifteen local tasks cover interface-review, variant, state-machine, break, and explain-interface. Each role has a normal case, an edge case and a preservation or cleanup case. These are task inputs, not a record of executor performance.

`cases.json` is the public case manifest. Each case has its own `case.json`, Korean `TASK.md`, and a package-free `app/`. `prepare.py` copies only the app into a fresh workspace. Interface-review cases additionally construct small Git histories from `setup/`. Those preparation sources stay outside the executor workspace. No remote APIs or package installation are needed.

Prepare a case before starting its executor:

```sh
python3 evals/design-role-parity-2026-10-12/fixtures/explicit/prepare.py \
  --case variant-usage-density \
  --destination /tmp/explicit-variant-usage-density
```

Read the case's `TASK.md` into the executor prompt, substitute its workspace and a runner-selected free port, and start the static server there when the task requires a browser:

```sh
python3 -m http.server 8765 --bind 127.0.0.1
```

The server must run with the prepared workspace as its working directory. The runner owns the server PID and stops only that process after collecting artifacts. Browser capability must be disclosed before the run. A missing browser is a capability limitation, not evidence of correct runtime behavior. The image-only case deliberately has no browser or source-code capability and does not need a server. Files in its app directory are immutable inputs.

The preparation script creates a scoped local Git identity and local origin refs, with no actual remote. It refuses nonempty destinations and destinations inside this fixture directory. Review cases are read-only, so write reports and browser evidence outside their Git trees. The no-change case intentionally requires no app work once the lack of a review target is established.

Evaluator criteria and executable checks are kept separately under the private scratch rubric directory. Do not copy them, the preparation sources, this README, or sibling cases into an executor context. Public `evaluator_criteria_id` values are lookup keys only. Each case has a 240-second executor budget; setup, semantic scoring and human comparison are separate. Prepared Git history and file hashes are technical controls, not proof of visual quality or of parity between skill arms.
