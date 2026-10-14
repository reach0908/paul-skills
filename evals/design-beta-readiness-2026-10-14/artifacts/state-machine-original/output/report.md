# `renderQueueCard` 상태 작업대 결과

## 실행 위치

- 실행 URL: `http://127.0.0.1:48914/runs/state-machine-original/app/states/queue-card/?__state=ready`
- 상태 URL 형식: 위 URL의 `__state` 값을 아래 상태 ID로 바꾼다.
- 대상: `app/queue.js`의 `renderQueueCard` 하나. 팀 운영 자료 화면에서 검토 대기 자료를 표시하며, 이 정적 번들에서는 페이지가 넘긴 props를 데이터 경계로 사용한다.
- 정리: `app/states/queue-card/` 폴더 하나를 삭제하면 작업대 라우트, fixture, 스위처가 함께 제거된다.

## 도달 가능한 상태

| 키 | 상태 ID / URL 값 | 실제 관찰 |
| --- | --- | --- |
| 1 | `no-access` | 권한 없음 문구, 목록 0개 |
| 2 | `loading` | “자료를 불러오는 중”, `aria-busy="true"`; 자동 완료하지 않음 |
| 3 | `error` | 오류 문구와 “다시 시도” 버튼 |
| 4 | `empty` | “대기 중인 자료가 없습니다.”, 목록 0개 |
| 5 | `one-item` | R-72 “작은 팀에서 실패 후 다시 시도하기” 1개 |
| 6 | `ready` | 제품 형태 제목 8개 |
| 7 | `long-list` | 제품 형태 제목 18개 |
| 8 | `refreshing` | 기존 8개를 유지하며 확인 중 문구, `aria-busy="true"`; 자동 완료하지 않음 |
| 9 | `locked` | 8개 항목 버튼 모두 비활성화, 잠금 문구 |

`canEdit`, `status`, `items`, `refreshing`, `locked`에 존재하는 원본 분기만 사용했다. 요금제·명명된 역할·페이지네이션·부분 완료 분기는 원본 코드에 없어서 만들지 않았다. 조합 상태도 원본이 별도 분기하지 않으므로 교차 곱으로 추가하지 않았다.

## 생성 파일

- `app/states/queue-card/index.html`: 원본 `style.css` 상속, 작업대 마크업
- `app/states/queue-card/workbench.js`: 실제 `renderQueueCard` import, 모의 props, URL/키보드 스위처
- `app/states/queue-card/switcher.css`: 제품 디자인 토큰과 분리된 고정 스위처 스타일
- `output/queue-card-ready.png`: 1280×900, ready 전체 페이지
- `output/queue-card-long-list.png`: 1280×900, long-list 전체 페이지
- `output/queue-card-long-list-narrow.png`: 375×812, long-list 전체 페이지와 가로 스크롤 스위처
- `output/report.md`: 이 보고서

원본 `app/queue.js`, `app/style.css`, `app/index.html`은 수정하지 않았다.

## Playwright CLI 관찰

- 지정 세션 `beta-state-machine-original`을 처음 snapshot 했을 때 URL은 `about:blank`이었다. 이후 지정된 로컬 URL로 이동했다.
- 9개 상태 URL을 각각 실제로 로드했다. 각 상태의 활성 버튼 `aria-pressed` 값이 URL의 `__state`와 일치했고, 위 표의 문구·항목 수·busy/disabled 상태가 실제 DOM에 나타났다.
- `locked`에서 reload 후에도 URL과 활성 상태가 `locked`이고 목록 8개가 유지됐다.
- `locked`에서 `ArrowLeft`는 `refreshing`, 이어 `ArrowRight`는 `locked`로 이동했다.
- 숫자키 `1`, `6`, `7`, `9`는 각각 `no-access`, `ready`, `long-list`, `locked`로 이동했다.
- `H`를 누르면 스위처가 `hidden=true`/계산 스타일 `display:none`이 됐고, 다시 누르면 `hidden=false`/`display:flex`가 됐다.
- 메모 입력에 포커스한 상태에서 `2`, `H`, `ArrowRight`를 눌렀을 때 URL과 활성 상태는 `no-access`에서 변하지 않았다. 입력값은 `2H`, 포커스는 `memo`에 남았고 당시 스위처 hidden 값도 바뀌지 않았다.
- 375×812에서 스위처는 `clientWidth=351`, `scrollWidth=707`로 가로 스크롤됐다. 화살표 이동 후 `refreshing`과 `locked` 활성 버튼은 모두 스위처 경계 안에 완전히 표시됐다.
- 마지막 전체 순회와 상호작용 뒤 콘솔 오류 0건, 경고 0건이었다.

관련 자동 snapshot에는 `.playwright-cli/page-2026-10-14T03-03-37-981Z.yml`(첫 URL 진입), `.playwright-cli/page-2026-10-14T03-06-34-101Z.yml`(수정 후 locked reload), `.playwright-cli/page-2026-10-14T03-06-57-796Z.yml`(최종 reload)이 남았다.

## 확인 범위와 남은 미확인

- 이 입력은 백엔드 없는 정적 ES 모듈이다. `onRetry`와 `onSelect`는 작업대에서 콘솔 콜백으로 공급했으며, 서버 동작은 확인 대상이 아니다.
- 입력 중 단축키 무시는 실제 `input`으로 확인했다. 구현에는 `textarea`, `select`, `contenteditable`, modifier/default-prevented 무시도 포함했지만 각각의 별도 브라우저 상호작용은 하지 않았다.
- 시각 상태를 바꾸거나 평가하지 않았고, 원본 컴포넌트/스타일도 변경하지 않았다.
- 이 폴더에는 사용할 수 있는 Git 저장소 메타데이터가 없어 Git diff 기반 확인은 실행할 수 없었다. 파일 변경 범위는 위 생성 파일에 한정했다.
