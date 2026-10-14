# 자료 카드 밀도 비교안 실행 보고서

## 실행 위치

- 기본: http://127.0.0.1:48914/runs/variant-original/app/index.html
- Airy: http://127.0.0.1:48914/runs/variant-original/app/index.html?__variant=airy
- Balanced: http://127.0.0.1:48914/runs/variant-original/app/index.html?__variant=balanced
- Compact: http://127.0.0.1:48914/runs/variant-original/app/index.html?__variant=compact
- 빌드 단계가 없는 정적 페이지다.

## 범위와 축

`#target`의 자료 카드 하나가 제목·요약·메모 초안·기존 작업 버튼·저장 상태를 보여 주고 편집/저장하게 하는 조각이며, 실제 헤더·검색·도움말 문맥 안에서 **밀도**만 비교했다. 콘텐츠와 제어 순서, ID 훅, 저장 타이머는 세 안에서 동일하다. 전환은 DOM을 교체하지 않고 `data-variant`만 바꾸므로 입력값과 진행 중 작업이 유지된다.

| 변형 | 밀도 위치 | 적합한 상황 | 비용 |
| --- | --- | --- | --- |
| Airy | 가장 낮은 밀도: 32px 카드 여백, 26px 구역 간격, 136px 메모 입력 | 자료를 한 건씩 천천히 읽고 메모하는 상세 맥락 | 세로 공간을 가장 많이 사용하며 작은 화면에서 스크롤이 길다 |
| Balanced | 중간 밀도: 22px 카드 여백, 18px 구역 간격, 104px 메모 입력 | 읽기와 반복 작업의 균형이 필요한 일반 사용 | Airy의 여유와 Compact의 한 화면 정보량 모두를 일부 양보한다 |
| Compact | 가장 높은 밀도: 12px 카드 여백, 10px 구역 간격, 68px 메모 입력 | 저장 상태와 여러 작업을 빠르게 훑는 반복 사용 | 긴 메모를 입력할 때 입력창 안쪽 스크롤이 더 빨리 생긴다 |

어느 한 방향도 선택 상태로 승격하지 않았다. URL 기본값은 비교 시작점인 `Balanced`이고 picker에서 세 안을 동일하게 선택할 수 있다.

## picker와 상태 보존

- URL의 `__variant`가 활성 안의 원본이다. 버튼 포인터 클릭, `←`/`→`, 숫자 `1`/`2`/`3`으로 전환하고 `h`로 숨김/표시한다.
- 입력·textarea·select·contenteditable에서 발생한 키 입력과 수정키가 있는 키 입력은 picker가 무시한다.
- 활성 버튼에 `aria-pressed="true"`가 설정되고 picker에는 `aria-label="Variants"`가 있다.
- 320×450 및 640×450처럼 짧은 화면에서는 카드가 화면 하단에 걸리므로 picker를 상단으로 옮기고 64px 전용 공간과 포커스 스크롤 여백을 예약했다. 그 밖의 화면에서는 규격대로 하단 중앙에 둔다.

## Playwright CLI 관찰

지정된 `beta-variant-original` 세션과 설치된 `playwright-cli`만 사용했다.

### 상태 전환

- 검색을 `실패 복구`, 메모를 `편집 중인 메모 유지 확인`으로 바꾼 뒤 저장과 동시에 Airy로 전환했을 때 URL은 Airy, 상태는 `저장 요청 중`, 저장 버튼은 disabled, 카드의 `aria-busy`는 `true`였고 두 입력값이 유지됐다.
- 1.1초 후 같은 Airy 화면에서 검색/메모 값은 그대로였고 `저장 완료 S-72`, 상단 피드백 `저장됨`, 활성화된 저장 버튼을 확인했다.
- `메모 비우기`를 포인터로 누른 직후 `→`로 Balanced로 바꿨을 때 메모는 빈 값, 상태는 `메모를 비웠습니다`로 유지됐다.
- 검색 입력에 포커스가 있을 때 숫자 `3`, 메모 입력에 포커스가 있을 때 `→`는 변형을 바꾸지 않았다. 편집기 밖의 `→`는 Compact로 바꾸고 URL도 갱신했다.
- 기존 `내 보관함`/`자료함` 링크는 각각 `#saved`/`#library`로 이동했다. `오류 예시`는 `저장하지 못했습니다. 다시 시도해 주세요.`, `빈 결과 예시`는 `검색 결과가 없습니다. 검색어를 바꿔 주세요.`를 표시했다.

### 크기와 접근

- 1280×900: 세 안을 포인터/키보드로 전환하고 전면 캡처를 확인했다. Airy에서 카드 사각형은 `(176, 212)–(1104, 696)`, 하단 picker는 `(525, 841)–(755, 876)`으로 겹치지 않았으며 가로 오버플로가 없었다.
- 320×450: 헤더 링크, 검색, 메모, 기존 버튼 4개, 도움말, picker 버튼을 탭 순회로 모두 도달했다. 순회 시 각 대상은 뷰포트 안에 완전히 들어왔고 제품 제어와 picker가 겹치지 않았다.
- 320×450의 Airy/Balanced/Compact에서 제어 구역으로 스크롤한 뒤 textarea와 버튼 4개의 좌우 경계를 측정했다. 모두 320px 안에 있었고 picker와 겹치지 않았으며 문서 가로 오버플로도 없었다.
- 200% 확대의 실효 레이아웃을 보수적으로 재현한 640×450에서도 세 안의 textarea/버튼이 모두 가로 범위 안에 있고 picker와 겹치지 않았다.
- 모든 스냅샷에서 검색과 메모는 접근 가능한 이름을, 자료 작업 그룹은 `자료 작업` 이름을 가졌다. 활성 picker 버튼의 pressed 상태도 노출됐다.
- 마지막 콘솔 확인 결과: 오류 0건, 경고 0건. `node --check app/app.js`도 통과했다.

## 캡처

- `captures/airy-1280x900.png`
- `captures/balanced-1280x900.png`
- `captures/compact-1280x900.png`
- `captures/pending-airy-1280x900.png`
- `captures/airy-320x450.png`
- `captures/balanced-320x450.png`
- `captures/compact-320x450.png`
- `captures/compact-controls-320x450.png`
- `captures/compact-640x450-zoom-equivalent.png`

## 변경 파일

- `app/index.html`: 카드 내부 그룹과 실험용 picker 마크업
- `app/style.css`: 세 밀도 토큰, 반응형 카드, 접근 가능한 포커스/짧은 화면 picker 배치
- `app/app.js`: 기존 카드 동작을 유지한 URL picker, 상태를 보존하는 class 전환, pending의 `aria-busy`
- `output/report.md` 및 `output/captures/*.png`: 관찰 기록과 캡처

## 남은 미검증 범위

- 제공 앱은 실제 서버가 아니라 1초 `setTimeout`으로 완료되는 정적 데모다. BRIEF의 timeout-unknown, 상태 확인 2단계, 인증 복구/API 미정 사항은 이 카드 밀도 비교 범위에서 새로 구현하거나 검증하지 않았다.
- Playwright CLI의 단일 브라우저 세션에서만 관찰했다. 실제 화면 읽기 프로그램, 다른 브라우저/OS 조합, 네이티브 브라우저 확대 UI는 별도로 실행하지 않았다.
- 640×450은 1280×900의 200% 확대 시 생기는 실효 CSS 크기를 재현한 확인이며 운영체제 수준 확대 자체를 켠 검사는 아니다.
