# Component reuse work report

Request: Library 하단 Explore topics의 카드를 Collection Related topics에도 컴포넌트 자체로 재사용하고, 기존 추천 작가 영역과 현재 프로젝트 스타일을 유지한다.

## Source and mapping

Applied candidate skill: `$REPO/skills/design/build-design/SKILL.md`, its `browser-and-spec.md`, and the same checkout's `design-browser` skill, preflight and executable QA references.

The supplied local fixture is the design reference. No external image, Figma file or explicit viewport was supplied. 390 × 844 and 1280 × 844 are representative verification widths selected for this run, not supplied design values. Existing CSS values are project defaults and were verified through computed styles.

| Reference route / section | Source and actual export | Target call site | Preserved contract |
| --- | --- | --- | --- |
| `?page=library`, Explore topics, default state | `app.js:1,6` imports `CreatorCard` from `components/TopicCard.js:1` as `TopicCard` | `app.js:7`, Collection `#related` | Same export, `id/name/count` props, whole-card topic anchor, encoded topic destination, Tab and Enter, focus style |
| `?page=library`, Recommended writers | `app.js:2,6` imports another `CreatorCard` from `components/RecommendedCard.js:1` as `RecommendedCard` | Existing Library call site, unchanged | Morgan button and profile action |

Both source files export `CreatorCard`. File names and actual route call sites resolve the requested topic component, not the shared export name or similar faces graphic.

Before-change `app.js` SHA-256: `a894b83fbd6a5ce15fecb0d15296fd7cdd33fa8fe8fd4dd22e1dafc29a5aebcd`.
After-change `app.js` SHA-256: `bf0d7f14af0249106f2e5b4fd7ea44a61ade5df5a88db4fadd05d9c8f512871f`.
`TopicCard.js` remained `f7b036301535c315a7ecb3678899f9ee59c1416ef87d9e27da192165e0800af6`; `RecommendedCard.js` remained `faa5da96392ae7f1961aa2b192d37e2674c9b9ce5ba5c4e3f8adec478b4a15bd`. `style.css` remained `4ad18ba85f97cc58611974c4e851ae15234dfe78b9b6baca82f48a4615725c63`.

## Changes

Only production file changed: `app.js`, one Collection branch line. Replaced its plain Design/Science list with `topics.forEach(... TopicCard(t))`, using the same import and topic objects as Library. No duplicated component, new styling, tokens, variants or dependencies were added. Library recommendations and both component implementations were left unchanged.

Added this report and local `evidence/` scripts, measurements and screenshots. `.playwright-cli/` contains generated browser snapshots/logs. All intentional artifacts are inside this fixture. No commits, installs, remote research or live account access were performed.

## Browser evidence

Tool: installed Playwright CLI 0.1.22, Chrome 152.0.7977.82. Task-owned session: `retro-reuse-20261016`. Local URL during verification: `http://127.0.0.1:53825/`. Reference observation: 2026-10-16 10:55:57 UTC; post-change assertions: 10:56:32 UTC. Browser resized viewports, not mobile-device emulation.

Preflight: installed command/help ready; blank-page connection and follow-up snapshot ready after bounded recovery; intended Library route ready; authentication not required. Initial sandbox server start failed with `PermissionError: [Errno 1] Operation not permitted`; default CLI state location failed with `EPERM` for a cache error log. A task-owned localhost server was authorized by automatic review, and CLI daemon/profile/temp state was placed under fixture `.runtime`. Detached launches did not survive separate command invocations (`Browser 'retro-reuse-20261016' is not open`). A persistent task-owned terminal restored the connection. No user browser was attached or closed.

`evidence/before.cjs` captured reference and target before editing. `evidence/after.cjs` asserted four cases: Library and Collection at both widths. Raw structured measurements and executed scenario are saved in `evidence/before-results.txt` and `evidence/after-results.txt`.

| Element / behavior | Reference | Built and observed | Result |
| --- | --- | --- | --- |
| Component identity | `TopicCard.js:CreatorCard` aliased `TopicCard` | Same import invoked in `#related` | Source verified |
| Topic items | Design 12 writers; Science 8 writers | Exactly two anchors in each route and width | Assertions passed |
| Padding, radius, margins | 24px; 12px; 12px 0px | Identical computed values | Matches |
| Text | 18px system-ui; black | Identical computed values | Matches |
| Width at 390 / 1280 | 342px / 896px | 342px / 896px; within viewport | Matches |
| Horizontal overflow | None expected | Document scroll/client width 390/390 and 1280/1280 | Assertions passed |
| Keyboard entry | Navigation then topic anchors, with Morgan button in Library | Real Tab reached Design; next Tab reached Science; Shift+Tab returned to Design in all four cases | Assertions passed |
| Focus appearance | Existing 3px purple outline, 4px offset | Computed `rgb(83, 39, 175) solid 3px`, 4px, `:focus-visible` true | Matches |
| Enter navigation | Topic ID link | Both Design and Science reached their corresponding `?page=topic&id=...` route in every case | Assertions passed |
| Recommended writers | Morgan button | One button remains; click produces `Profile: Morgan` at both widths | Assertions passed |

Screenshots: `library-before-{390,1280}.png` and `collection-before-{390,1280}.png` capture default pre-change states. `library-after-{390,1280}.png` and `collection-after-{390,1280}.png` capture keyboard focus on Design. `collection-default-after-{390,1280}.png` capture the default target state for direct comparison with the pre-change source. All are under `evidence/`. Visual inspection confirmed the same full-width card structure, faces, content and spacing on source and target at both widths; the different heading and surrounding page content are retained as requested.

Static check: `node --check app.js` passed. Fixture has no build or test suite script. A browser console 404 for the absent `favicon.ico` was observed before the change; it is unrelated and unchanged.

## Limits and handoff

Unwired: the fixture's existing hard-coded two-topic array and Morgan data remain sample data, with no backend integration. Loading, error and empty states are not implemented in this fixture and were not invented. No real device, screen-reader, browser-engine comparison, live product deployment or user acceptance was tested. No design deviations or unresolved implementation blockers were found in the requested scope.

The task-owned browser and server are stopped after evidence collection. To view the result again, run `npm start -- --bind 127.0.0.1` in this fixture and open the printed local URL with `?page=collection`. Compare at 390px and 1280px widths.
