# 실행 보고서

## 결과

PB-72 revision 3의 D-ITEM / T-SAVE 흐름을 조작 가능한 로컬 와이어프레임으로 만들고 지정된 Playwright CLI 세션에서 확인했다.

- 실행 URL: <http://127.0.0.1:48914/runs/wireframe-paul/app/index.html>
- 관찰 시각: 2026-10-14 12:13 KST
- 브라우저 도구: `playwright-cli 0.1.22`
- 브라우저: Chromium `152.0.7977.82`
- 세션: `beta-wireframe-paul`

## 생성·변경 파일

- `app/index.html` — D-ITEM, D-LIB, T-SAVE 상태 화면
- `app/app.js` — 모의 저장 상태 기계, 로컬 지속성, 화면·내부 이동
- `app/style.css` — 1280×900 / 320×700 반응형 와이어프레임
- `output/screens.md` — 화면·상태·전이 명세
- `output/report.md` — 이 실행 보고서
- `output/captures/` — 스냅샷과 화면 캡처

## 실제 관찰

- 1280×900에서 키보드로 메모 `다음 회고에서 중단 기준을 먼저 합의하기`를 입력했다. 첫 저장 직후 `전송 중`, 요청 `SAVE-R72-1`, 비활성 저장 버튼을 관찰했다.
- 1.2초 뒤 `응답 시간이 초과되어 결과를 알 수 없습니다`가 표시되고, 성공·실패를 단정하지 않은 채 `상태 확인`만 제공됐다.
- 첫 확인은 `아직 처리 중`, 두 번째 확인은 `저장됨`과 유일 영수증 `S-72`였다. 저장 버튼은 계속 비활성이라 새 요청을 만들 수 없었다.
- 별도 `시나리오 재설정` 버튼으로만 새 시나리오를 시작했다. `전송 중`에 상태 패널을 닫은 뒤에도 저장소 상태가 `pending`, 메모가 유지됐고, timeout 뒤 다시 열었을 때 `unknown`이었다. 이후 같은 요청으로 S-72까지 완료했다.
- 상태 패널을 닫고 목록으로 나가도 `q=작은 팀`, `tag=운영`, `sort=newest`, 보던 자료 R-72가 표시됐다. 상세 재진입과 브라우저 뒤로/앞으로 뒤에도 초안, 저장 결과, 중복 잠금이 남았다.
- pending 중 목록으로 이동해 timeout을 기다린 경우에도 콘솔 오류 없이 목록 문맥이 유지됐고, 상세 복귀 시 같은 요청 `SAVE-R72-1`, 초안, `확인 필요` 상태가 복원됐다.
- 새로고침 뒤 320×700에서 메모와 `S-72`가 복원됐다. 마지막 관찰 저장값은 `status=succeeded`, `checks=2`, `requestId=SAVE-R72-1`, `receipt=S-72`였다.
- `본문으로 건너뛰기`와 `출처 구역으로 이동`은 URL을 바꾸지 않고 각각 `article-body`, `source-region`에 포커스를 옮겼다.
- 실제 Tab 입력으로 1280×900과 320×700 모두 건너뛰기 링크 → 헤더 메뉴 → 검색 → 목록 복귀 → 본문/출처 내부 이동 → 메모 입력 순서에 도달했다. 관찰한 포커스 윤곽선은 `solid 3px`; 320 폭에서 Shift+Tab은 메모에서 `출처 구역으로 이동`으로 돌아갔다.
- 가로 넘침 단언 결과:
  - 1280×900: 문서 `scrollWidth=1280`, `clientWidth=1280`; main `960=960`; 경계 밖 요소 0.
  - 320×700: 문서 `scrollWidth=320`, `clientWidth=320`; main `320=320`; 경계 밖 요소 0.
- 최종 콘솔 확인: 오류 0, 경고 0.

내부 이동 확인 중 처음 사용한 전역 `본문으로 건너뛰기` 선택자는 동일 이름 링크 두 개 때문에 strict-mode 오류가 났다. `자료 안에서 이동` 내비게이션으로 범위를 좁혀 다시 실행했고 최종 단언은 통과했다.

## 주요 캡처

- `output/captures/desktop-pending.yml` — 첫 저장의 pending
- `output/captures/desktop-timeout-unknown.yml`, `.png` — timeout-unknown
- `output/captures/desktop-check-1-pending.yml` — 첫 상태 확인 pending
- `output/captures/desktop-success.yml`, `.png` — 두 번째 확인과 S-72
- `output/captures/desktop-status-closed.yml` — 패널 닫기 후 잠금·초안 유지
- `output/captures/desktop-library-context.yml`, `.png` — 목록 문맥 보존
- `output/captures/desktop-browser-back-library.yml` / `desktop-browser-forward-detail.yml` — 브라우저 왕복
- `output/captures/mobile-restored-success.yml`, `.png` — 320×700 새로고침 복원
- `output/captures/desktop-final-success.yml` — 진행 중 닫기 시나리오의 최종 성공

## 확인하지 못했거나 범위 밖인 항목

- 실제 서버 저장, 계정, 인증 복구, 권한, D-SAVED 서버 반영은 모의 경계 밖이라 확인하지 않았다.
- 원문 자리표시자 외부 페이지를 열지는 않았다.
- 터치 기기 에뮬레이션, 스크린 리더 음성 출력, 실제 사용자 수용성은 확인하지 않았다.
- 인증 복구 API와 만료된 초대의 읽기 권한은 입력 결정본대로 미결이다.

와이어프레임은 렌더링되고 지정 흐름의 동작을 확인했지만, 사용자 승인 또는 프로덕션 준비 완료를 의미하지 않는다.
