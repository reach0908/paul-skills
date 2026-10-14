# renderQueueCard 상태 작업대 보고서

관찰 시각: 2026-10-14 12:07:05 KST (+0900)

## 결과

`app/queue.js`의 실제 `renderQueueCard(props)`를 import하고, 프로덕션과 같은 `app/style.css`를 상속하는 상태 작업대를 만들었다. 이 컴포넌트는 `app/index.html`의 `#queue`에서 검토 대기 자료를 보여 주며, 데이터 경계는 `status`, `items`, `canEdit`, `locked`, `refreshing` props다.

- 실행 URL: <http://127.0.0.1:48914/runs/state-machine-paul/app/states/queue-card/?__state=typical>
- 직접 상태 URL 형식: `...?__state=<state-id>`
- 작업대 폴더: `app/states/queue-card/`
- 한 단계 정리 범위: `app/states/queue-card/` 폴더 하나
- 원본 `app/queue.js`, `app/style.css`, `app/index.html`은 수정하지 않았다.

## 만든 파일

- `app/states/queue-card/index.html`: 프로덕션 스타일 연결, 프로덕션 문맥의 메모 입력, 독립적인 상태 스위처
- `app/states/queue-card/queue-card-states.js`: 실제 컴포넌트 import, 제품 형태의 fixture, URL/키보드 상태 전환
- `output/captures/`: 상태·상호작용 스냅샷과 대표 화면 캡처
- `output/report.md`: 이 보고서

## 실제 코드에서 확인한 상태

| 상태 ID | 공급한 props/자료 | 관찰 결과 |
| --- | --- | --- |
| `no-access` | `canEdit: false` | 권한 없음 문구, 항목 0개 |
| `loading` | `status: 'loading'` | `aria-busy="true"`, 불러오는 중 status, 항목 0개 |
| `error` | `status: 'error'` | alert와 다시 시도 버튼 |
| `empty` | `items: []` | 대기 자료 없음 문구 |
| `one-item` | 실제 형태 자료 1개 | R-72 제목 1개 |
| `typical` | 실제 형태 자료 6개 | 선택 가능한 버튼 6개 |
| `long-list` | 실제 형태 자료 24개 | 선택 가능한 버튼 24개, 스크롤 가능한 긴 페이지 |
| `refreshing` | 자료 6개, `refreshing: true` | 기존 목록과 새로 확인 중 status, `aria-busy="true"` |
| `locked` | 자료 6개, `locked: true` | 버튼 6개 모두 disabled, 잠김 문구 |
| `refreshing-locked` | 자료 6개, 두 플래그 모두 true | 갱신 status와 잠김 문구, 버튼 6개 모두 disabled, `aria-busy="true"` |

Playwright의 독립 기대값으로 항목 수, disabled 수, `aria-busy`, 대표 문구, 활성 `aria-pressed`를 검사했고 10/10 상태가 일치했다. `loading`은 500ms 뒤에도 그대로였고 작업대에는 자동 완료 타이머가 없다.

코드에 없는 요금제, 소유자/멤버 역할, 기능 플래그, 체험, 사용 한도, 부분 요청 pending, 페이지네이션 상태는 만들지 않았다. `locked + empty`처럼 선행 반환 때문에 `empty`와 같은 화면이 되는 조합과, `no-access` 선행 반환에 가려지는 조합도 별도 상태로 늘리지 않았다.

## 스위처와 URL

URL의 `__state`가 단일 기준이다. 파라미터가 없거나 알 수 없는 값이면 `typical`로 정규화한다. 클릭, 화살표, 숫자키는 URL과 렌더링을 동시에 바꾸며 popstate도 다시 렌더링한다.

숫자키는 스펙대로 앞의 아홉 상태에 대응한다.

1. `no-access`
2. `loading`
3. `error`
4. `empty`
5. `one-item`
6. `typical`
7. `long-list`
8. `refreshing`
9. `locked`

열 번째 `refreshing-locked`는 버튼, 화살표, 직접 URL로 접근한다. `H`는 스위처를 숨기거나 다시 보인다.

## Playwright CLI 관찰

- 도구: `playwright-cli 0.1.22`, 세션 `beta-state-machine-paul`
- 브라우저: Headless Chrome 152.0.0.0 (`MacIntel`)
- 데스크톱 뷰포트: 1280×720
- 좁은 뷰포트: 390×844
- 최초 제공 세션의 `about:blank`를 snapshot한 뒤 작업 URL로 이동했다.
- `one-item` URL을 reload한 뒤에도 URL, 항목 1개, 활성 스위처가 모두 유지됐다.
- `one-item`에서 `ArrowRight`는 `typical`, 이어 `ArrowLeft`는 `one-item`으로 이동했다.
- 숫자 `8`은 `refreshing`으로 이동했다.
- `H`를 한 번 누르면 스위처가 숨고 다시 누르면 나타났으며 상태는 `refreshing`으로 유지됐다.
- 메모 입력에 `작업 중`을 넣고 입력 포커스를 유지한 채 `ArrowRight`, `2`, `h`를 눌렀다. 값은 `작업 중2h`, 상태와 활성 버튼은 `typical`, 스위처는 표시 상태여서 단축키가 입력 중 무시됨을 확인했다.
- 스위처의 오류 버튼 클릭은 URL을 `error`로 바꾸고 alert를 렌더링했다.
- 좁은 화면의 `long-list`에서 문서 너비는 390/390으로 가로 넘침이 없었고 카드 경계는 x=16..374였다. 스위처는 client 366px, scroll 764px로 내부 가로 스크롤을 제공했다.
- 좁은 화면의 `long-list`에서 scrollY 489인 상태로 활성 상태를 다시 선택한 뒤에도 scrollY 489가 유지됐다.
- 마지막 `typical` 화면에서 콘솔 오류와 경고는 0개였다.

## 캡처

상태별 접근성 스냅샷:

- `output/captures/no-access.yml`
- `output/captures/loading.yml`
- `output/captures/error.yml`
- `output/captures/empty.yml`
- `output/captures/one-item.yml`
- `output/captures/typical.yml`
- `output/captures/long-list.yml`
- `output/captures/refreshing.yml`
- `output/captures/locked.yml`
- `output/captures/refreshing-locked.yml`

상호작용 스냅샷:

- `output/captures/reload-one-item.yml`
- `output/captures/key-arrow-right.yml`
- `output/captures/key-number-8.yml`
- `output/captures/switcher-hidden.yml`
- `output/captures/input-shortcuts-ignored.yml`
- `output/captures/click-error.yml`

화면 캡처:

- `output/captures/typical-desktop.png`
- `output/captures/loading-desktop.png`
- `output/captures/long-list-mobile.png`
- `output/captures/long-list-mobile.yml` (390×844 box 포함 snapshot)

## 남은 검증 한계

- 제공 앱은 정적 ES module이고 백엔드·인증·계정이 없으므로 실제 네트워크 응답, 권한 서버, 캐시 동기화는 검증 대상에 없었다.
- `onRetry`와 `onSelect`의 외부 부작용은 상태 렌더링 범위 밖이며, 제공 코드의 기본 no-op 콜백 그대로 두었다.
- 물리 모바일/터치 입력은 확인하지 않았다. Chrome 데스크톱 세션의 390×844 viewport reflow만 관찰했다.
- Firefox, WebKit 및 실제 보조기기 동작은 이번 관찰에 포함하지 않았다.
