# DS-72 revision 4 구현 보고서

## 실행 위치와 변경 파일

- source revision: `DS-72 revision 4`
- 실행 URL: http://127.0.0.1:48914/runs/build-design-original/app/
- 수정: `app/style.css` — `#target`의 패딩, 제목 크기, 도구 그리드와 600px 미만 반응형 규칙만 추가
- 변경 없음: `app/index.html`, `app/app.js` — 기존 마크업, ID 훅, 검색·헤더·자료 문구와 동작 보존
- 생성: `output/report.md` 및 아래 비교·상태 캡처
- 빌드 단계: 없음(정적 HTML/CSS/JS)

## 시안 대조

| 요소 | 승인 시안 | 실제 렌더 | 결과 |
| --- | --- | --- | --- |
| 카드 배경/글자 | `var(--surface)` / `var(--ink)` | `rgb(255, 255, 255)` / `rgb(23, 33, 43)` | 기존 토큰과 일치 |
| 카드 패딩 | `var(--space-3)` = 24px | 24px | 일치 |
| 카드 테두리/radius | `1px var(--border)` / `var(--radius)` = 8px | `1px rgb(96, 117, 140)` / 8px | 기존 토큰과 일치 |
| h2 | 1.5rem | 24px | 일치 |
| 본문 | 1rem | 16px 상속 | 일치 |
| 도구 간격 | `var(--space-1)` = 8px | 8px | 일치 |
| 1280px 도구 배치 | 2열 | 435px + 435px 2열 | 일치 |
| 320px 도구 배치 | 1열 | 238px 1열 | 일치 |
| 모바일 가로 폭 | 오버플로 없음 | `scrollWidth` 320px = `clientWidth` 320px | 일치 |

1280×900과 320×700에서 실제 HTML을 렌더해 로컬 참조 PNG와 비교했다. 두 폭 모두 출력 PNG의 SHA-256이 각 참조 PNG와 같았고 파일도 바이트 단위로 동일했다.

## 캡처

- `output/desktop-1280x900.png` — 1280×900 기본 상태, `ref/desktop.png`와 동일
- `output/mobile-320x700.png` — 320×700 기본 상태, `ref/mobile.png`와 동일
- `output/pending-disabled-card-320.png` — 저장 요청 중 카드와 비활성 저장 버튼
- `output/error-empty-320x700.png` — 오류 상태와 빈 결과 피드백이 함께 보이는 모바일 화면

## 관찰한 상태와 동작

- 초기: 카드 상태가 `저장 전`으로 표시됐다.
- pending/disabled: 저장 실행 직후 `저장 요청 중`, 저장 버튼 `disabled=true`; 기존 disabled opacity가 적용됐다.
- 완료: 약 1초 뒤 `저장 완료 S-72`, 검색 피드백 `저장됨`, 저장 버튼 `disabled=false`로 복귀했다.
- error: `저장하지 못했습니다. 다시 시도해 주세요.`가 카드 상태에 표시됐다.
- empty: `검색 결과가 없습니다. 검색어를 바꿔 주세요.`가 검색 피드백에 표시됐다.
- 메모 비우기: textarea가 빈 문자열이 되고 `메모를 비웠습니다`가 표시됐다.
- 키보드: Tab 순서로 저장과 이후 버튼에 도달했다. 저장, 메모 비우기, 오류 예시, 빈 결과 예시를 Enter로 실행해 각 상태 변화를 확인했다. 저장 버튼의 포커스 링은 3px, outline offset은 3px였다.
- 브라우저 콘솔: 앱 URL에서 오류와 경고가 없었다.

## 미결 시각 처리와 확인 한계

- 승인 시안에는 pending/error/empty/disabled 전용 시각 명세가 없다. 새 시각 처리를 설계하지 않고 기존 텍스트 피드백과 disabled 스타일을 보존했다.
- 지정된 두 viewport와 현재 Playwright 브라우저에서만 확인했다. 다른 브라우저 엔진과 실제 보조기기에서의 `role=status` 음성 안내는 확인하지 않았다.
- 지정 범위 안에서 남은 시각 차이는 관찰되지 않았다. 백엔드 연결이 필요한 새 UI나 하드코딩한 샘플 데이터도 추가하지 않았다.
