# AI walkthrough participant packet

You are the single fresh AI participant in an exploratory prototype walkthrough. Read `participant-instructions.md` and the installed browser skill at `$HOME/.codex/plugins/cache/paul-skills/paul-skills/0.4.1/skills/design/design-browser/SKILL.md` before the UI attempt. Do not read any other files outside your workspace except that installed browser skill and its necessary CLI help. Do not read memory, repository, source code, author intent, sibling outputs, tests, network traffic, storage or hidden DOM. Your workspace and evidence directory is `/private/tmp/pm-conversation-beta-20261014/runs/prototype-recheck/participant/`.

## Scenario

- URL: http://127.0.0.1:48617
- This is a disposable synthetic bookshelf prototype; visible in-session actions are authorized. Do not submit anything to external services or modify the app.
- Starting state: a new isolated browser session, initial URL, no prior app interaction.
- Viewport: 390 x 844. This is a viewport resize, not a claim of touch emulation.
- Unique session: `prototype-recheck-participant-1`. Use it on every Playwright command.
- No free exploration or first-impression phase is requested.

## One task

‘별의 지도를 나중에 읽기 위해 담고, 내가 담은 책에서 소개를 살펴본 뒤 방금 보던 목록으로 돌아오세요.’

## Browser transport and pre-task preparation

Host-side browser preflight succeeded with playwright-cli 0.1.22, Chrome, isolated session, two separate shell calls. Normal sandbox curl could not access this host local service. Use `tools.exec_command` with `sandbox_permissions: "require_escalated"` and prefix_rule `["playwright-cli"]` for Playwright. This is a verified permission/transport setup, not a UI hint. Open your isolated session on about:blank, resize it to 390x844 and verify a snapshot before starting. Keep your working directory at your evidence directory. Record setup separately. No prototype state has been inspected by you yet.

## Stop bounds and recording

- The UI attempt is at most 3 minutes of measured wall-clock time, including tool overhead, and at most 8 UI actions, whichever comes first. Start the clock immediately before navigating your prepared blank session to the supplied target URL. Initial target navigation and snapshots/screenshots are observation/setup, not UI actions, but are inside the 3-minute time bound.
- UI actions include clicks, typing/filling, key presses, scrolls, navigation/back/reload after the initial target load. Count each distinct interaction. Decide only from current rendered snapshots/screenshots. Capture each resulting state before the next choice. No eval, run-code, network tools, app API, storage tools or injection.
- Check the actual time before every subsequent interaction. Stop if the task is reached, no plausible next step remains, a blocking tool failure occurs, or time/action limit is reached. Label any in-flight observation after deadline as late; do not continue acting then.
- Record actual times, action count, observed results, contemporaneous expectations where captured, artifact paths, stopping reason and completion basis. Do not ask where to click or claim an unobserved result.
- Save and freeze the raw UI attempt (`attempt.md` and optionally structured JSON plus snapshots/screenshots). Do not rewrite it during interview. Return its paths and actual bounds, then keep this context/session available for one subsequent moderator interview. Do not begin an interview yourself.
- Do not close your session until after that follow-up or an instruction to close it.
