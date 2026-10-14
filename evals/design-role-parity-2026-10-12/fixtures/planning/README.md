# Planning and browser fixtures

These synthetic tasks cover four directly authored roles. Original-skill parity is not applicable. A no-skill arm is a utility control, not an origin comparison.

`cases.json` lists twelve independent cases in the required execution order. Each `task` is a path relative to its `fixture_directory`. Copy that directory to a fresh writable trial directory before each run. Give the executor `TASK.md`, its input files and the same tools in every arm. The executor must not receive private evaluator rubrics, earlier outputs or other cases. No fixture requires installing a package, signing in or contacting an external service.

Planning outputs go into the case's `design/` directory. Browser outputs go into `evidence/`. Browser runtime cases include `serve.py`; run it from the copied directory and use its printed loopback URL. The server chooses an available port. All server actions use local synthetic data. Stop only the server and browser session created for that run.

Each case has a 240-second execution budget. Setup, unavailable tools and interrupted attempts must be recorded separately. An unavailable browser is a verification limit, not a completed runtime check. This directory contains fixtures only, with no trial results or quality claims.

`composition.json` and `composition/` define one separate five-stage handoff. They are not part of the twelve role cases. Pass each stage only its task, the common brief and actual outputs from the preceding stages. Preserve failed handoffs instead of silently replacing them with a prewritten solution.
