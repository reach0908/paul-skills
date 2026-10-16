# 작은 책장 AI 참여자 워크스루 결과

담기와 담은 책의 소개 찾기는 별도의 UI 안내 없이 수행했다. 보관함에서 연 상세의 `목록으로`는 직전 보관함 대신 추천 목록을 열었다. 참여자가 보관함 탭으로 복구했지만 그 결과는 시간 한도 이후에 관찰됐다. 과업 2는 한도 내 부분 완료다.

이 결과는 새로운 AI 참여자 1명의 탐색 기록이다. 실제 사람의 사용성, 수요, 반복 사용, 제품 승인 또는 운영 준비를 증명하지 않는다. 제작 의도 문서도 확정된 사용자 결정이 아닌 제품 계약 초안이다.

## 테스트 질문과 실제 범위

- 질문: 첫 방문에서 별의 지도를 담고, 담은 책에서 소개를 읽은 뒤 직전에 보던 목록으로 돌아갈 수 있는가?
- 대상: http://127.0.0.1:48617/ , 페이지 제목 `작은 책장`.
- 시각: 2026-10-14 UTC. 참여자의 최초 시도 09:33:59, 재시도 기준 09:36:11, 최종 UI 관찰 09:44:31.
- 대상 식별: 09:43:02 UTC HTTP 200 응답 본문의 SHA-256 `651ac3e7ddff408c13323d21caedae484b52d8edbe2cbbc2fae296237e077f8f`. 제작 버전이나 Git SHA는 제공되지 않았다. 이 값은 HTML 응답 식별자이며 전체 자산 버전의 증명은 아니다. [digest 원본](/private/tmp/pm-conversation-beta-20261014/runs/coordinator/target-digest.json).
- 브라우저: Google Chrome 152.0.7977.82, Playwright CLI 0.1.22. `/opt/homebrew/bin/playwright-cli`.
- 설치된 브라우저 지침: `$HOME/.codex/plugins/cache/paul-skills/paul-skills/0.4.1/skills/design/design-browser/SKILL.md`.
- 화면: 실제 성공한 resize로 390×844 CSS px. 기기 에뮬레이션 없음. 초기 실패 세그먼트에서는 이 화면 크기를 설정하지 못했다.
- 세션: `pmbooks-fresh-p1-20261014`. 자기 세션만 사용했고 최종 정상 작동은 지속 TTY 셸 6452 안에서 수행했다.
- 시작 상태: 첫 추천 목록, 빈 검색 입력, 별의 지도 카드의 `담기`. 사용자가 지정한 가상 책장이고 담기는 현재 브라우저 세션만의 동작이다. 외부 전송 없음은 제공된 모형 경계이며 네트워크 검증으로 독립 확인하지 않았다.
- 실제 참여: `fork_turns=none`으로 생성한 `/root/prototype_test_coordinator/fresh_participant` 1명. 처음에는 첫 인상과 과업 1만 전달했고, 원본 고정 후 과업 2를 따로 전달했다. 제작 의도, 소스, 예상 경로, 성공 판정표는 참여자에게 전달하지 않았다. 도구 시작에 대한 진행자의 개입은 있었고 UI 경로에 대한 도움은 없었다.
- 정확한 모델 빌드, 버전 및 비용 계측은 미제공이므로 알 수 없다.

## 한도와 실패를 포함한 실행 결과

| 구간 | 실제 행동과 결과 | 시간 및 판정 |
| --- | --- | --- |
| 최초 도구 준비 | daemon 로그 경로 EPERM으로 페이지를 열지 못함. UI 행동 0회 | 09:33:59~09:35:11, 약 72초. 차단된 최초 시도로 보존 |
| 권한 복구 후 첫 연결 | 같은 CLI의 open은 성공했지만 후속 resize/snapshot/screenshot이 세션을 찾지 못함. 권한을 높인 후속 명령도 실패. UI 행동 0회 | 실패를 숨기지 않고 각 원본 기록에 분리 |
| 지속 셸 복구 | 설치 지침의 동일 셸 유지 절차로 open, resize, 스냅샷과 스크린샷 확보 | 도구 복구 지원을 받은 실행. 앱 경로 안내 없음 |
| 과업 1 | 목표 카드의 `담기` 1회 클릭. 상태와 버튼 변화 확인. 이후 같은 세션의 보관함에서도 목표 책 확인 | 재시도 기준 결과 관찰까지 4분 53초. 완료, 15회 이하 |
| 과업 2 | 보관함, 목표 소개, `목록으로`까지 3회 클릭. 추천으로 복귀해 직전 목록과 달라짐. 보관함 탭을 다시 누른 복구 포함 총 4회 클릭 | 소개와 잘못된 복귀는 한도 내 관찰. 복구의 자동 사후 스냅샷은 09:44:13.387로 재시도 마감 09:44:11보다 2.387초 늦음. 한도 내 부분 완료 |

원요청의 전체 8분은 충족하지 못했다. 인프라 복구를 별도 재시도로 구분해 8분 기준을 다시 기록했으며, 그 재시도에서도 마지막 복구 호출의 처리 중 한도를 넘겼다. 최종 관찰은 09:44:31로 재시도부터 8분 20초, 최초 준비부터 10분 32초다. 마지막 클릭 순간은 별도로 측정하지 않았으므로 2.387초는 클릭 초과 시간이 아니라 사후 스냅샷 시각의 차이다. 한도 내 완전 성공으로 계산하지 않는다.

실행 시간은 도구 준비, 연결 실패, 진행자 개입, 기록과 도구 처리 비용을 포함한다. 사람의 과업 수행 시간이나 앱 성능 지표로 해석할 수 없다. 시간 한도 뒤에는 추가 UI 과업을 하지 않았고, 인터뷰와 세션 정리는 별도로 진행했다.

## 원본 행동과 인터뷰

참여자는 첫 화면을 제목 검색, 추천, 내 보관함, 책별 살펴보기와 담기를 제공하는 작은 책장으로 이해했다. 조작 전 저장한 기대는 목표 카드의 `담기`가 책을 담고 확인 표시를 줄 것이라는 내용이었다. 이 해석은 첫 클릭 전 파일과 최신 스냅샷으로 남아 있다.

| 기록 | 관찰 | 원본 증거 |
| --- | --- | --- |
| 과업 1 클릭 1 | 목표 카드의 담기 클릭 후 `내 보관함에 담았어요`, `담았어요` | [행동 원본](/private/tmp/pm-conversation-beta-20261014/runs/coordinator/frozen-attempt-before-interview/task-1-persistent-raw.md), [클릭 전 기대](/private/tmp/pm-conversation-beta-20261014/runs/coordinator/frozen-attempt-before-interview/task-1-persistent-before-action.md), [결과 스냅샷](/private/tmp/pm-conversation-beta-20261014/runs/coordinator/frozen-attempt-before-interview/task-1-after-save.md), [결과 화면](/private/tmp/pm-conversation-beta-20261014/runs/coordinator/frozen-attempt-before-interview/task-1-after-save.png) |
| 과업 2 클릭 1 | 보관함에 목표 책 1권과 담았어요 상태 | [행동 원본](/private/tmp/pm-conversation-beta-20261014/runs/coordinator/frozen-attempt-before-interview/task-2-raw.md), [보관함 스냅샷](/private/tmp/pm-conversation-beta-20261014/runs/coordinator/frozen-attempt-before-interview/task-2-saved-list.md) |
| 과업 2 클릭 2 | 목표 상세에 `소개: 우주에 관한 가상 도서입니다.`와 담은 책 안내 | [소개 스냅샷](/private/tmp/pm-conversation-beta-20261014/runs/coordinator/frozen-attempt-before-interview/task-2-introduction.md), [소개 화면](/private/tmp/pm-conversation-beta-20261014/runs/coordinator/frozen-attempt-before-interview/task-2-introduction.png) |
| 과업 2 클릭 3 | 목록으로 클릭 후 추천 활성 상태와 추천 3권 | [복귀 스냅샷](/private/tmp/pm-conversation-beta-20261014/runs/coordinator/frozen-attempt-before-interview/task-2-returned-list.md), [복귀 화면](/private/tmp/pm-conversation-beta-20261014/runs/coordinator/frozen-attempt-before-interview/task-2-returned-list.png) |
| 과업 2 클릭 4 | 보관함 탭을 다시 선택해 목표 1권 목록 복구. 한도 이후 결과 | [복구 스냅샷](/private/tmp/pm-conversation-beta-20261014/runs/coordinator/frozen-attempt-before-interview/task-2-recovered-list.md), [복구 화면](/private/tmp/pm-conversation-beta-20261014/runs/coordinator/frozen-attempt-before-interview/task-2-recovered-list.png) |

인터뷰는 원본 63개 파일을 별도 복사하고 SHA-256으로 고정한 뒤 같은 참여자에게 했다. [고정 목록](/private/tmp/pm-conversation-beta-20261014/runs/coordinator/frozen-attempt-before-interview/freeze-manifest.json), [질문 원문](/private/tmp/pm-conversation-beta-20261014/runs/coordinator/participant-dispatch-08-interview.txt), [질문과 답변 원문](/private/tmp/pm-conversation-beta-20261014/runs/coordinator/interview-raw.md), [인터뷰 고정 정보](/private/tmp/pm-conversation-beta-20261014/runs/coordinator/interview-freeze.json).

관찰과 구분한 사후 보고는 다음과 같다.

- 담기는 같은 카드 안에 목표 제목, 살펴보기, 담기 버튼이 함께 있고 상단에 담고 다시 찾으라는 문구가 있어 선택했다고 답했다. 화면 상태 변화가 확인 근거였다.
- 내 보관함이라는 탐색 이름, 목표 제목과 담았어요의 조합으로 저장한 책을 찾았다고 답했다. 제목과 소개라는 명시적 문구를 소개 확인의 근거로 들었다.
- 상세를 보관함에서 열었고 상세 화면에서도 보관함이 활성 상태여서 목록으로가 보관함으로 돌아갈 것으로 예상했다고 답했다. 이는 클릭 전 원본 기대와 일치한다. 추천 제목, 추천 활성 탭, 추천 카드 여러 권이 보인 순간 실제 목적지에 대한 판단이 바뀌었다고 설명했다.
- 복구는 직전 실제로 작동한 내 보관함 탭을 다시 선택한 것이라고 답했다. 이 인터뷰는 구현 원인이나 제작자 의도를 확인한 증거가 아니다.
- 인터뷰가 행동 기록의 해석을 바꾸거나 새로운 모순을 만들지 않아 추가 질문은 하지 않았다. 제작 의도는 인터뷰 후에도 전달하지 않았다.

## 제작 의도와 비교

출처는 진행자 전용 [제작 의도 초안](/private/tmp/pm-conversation-beta-20261014/author-intent.md:3)이다. 다음 표의 aligned, mismatch, not reached는 이 한 AI 시도와 초안 사이의 관계만 나타낸다.

| 의도와 출처 | 기대한 결과 | 실제 행동과 증거 | Alignment | 다음 결정 |
| --- | --- | --- | --- | --- |
| 읽고 싶은 책 담기와 다시 찾기, 4행 | 목표를 담고 같은 세션에서 찾음 | 과업 1 확인 상태와 과업 2 클릭 1의 보관함 목표 카드 | aligned | 이번 시도의 발견 경로와 확인 상태는 유지할 근거. 다른 사용자에게 일반화하지 않음 |
| 현재 세션의 보관함에 추가, 5행 | 담긴 책이 현재 보관함에 나타남 | 클릭 1의 확인 문구만으로 끝내지 않고 후속 과업의 보관함 카드로 재확인 | aligned | 새로고침 지속성은 범위 밖으로 유지 |
| 외부 공유 없음, 5행 | 외부 전송 없이 모형 안에서 작동 | 제공된 경계와 화면 안내를 알고 허용된 담기만 수행. 네트워크 조사는 하지 않음 | not reached | 독립 네트워크 검증을 했다고 주장하지 않음 |
| 상세에서 돌아오면 보관함 유지, 6행 | 직전에 보던 보관함 목록으로 복귀 | 과업 2 클릭 2에서 보관함 활성 상세, 클릭 3에서 추천 활성 및 3권 목록 | mismatch | user-flow 담당이 이전 목록 문맥 복귀 계약을 다룸. 구현 변경은 이번 범위 밖 |
| 상세에서 돌아오면 검색 조건 유지, 6행 | 입력한 조건이 복귀 시 유지 | 검색 입력을 사용하지 않았고 필터 상태가 없음 | not reached | 수정 확인 pass에서 비어 있지 않은 검색 상태를 별도 중립 과업으로 확인 |

사전 가설 목록을 찾는 일반 UI 감사는 하지 않았다. 이 pass의 제품에 관한 주요 발견은 상세 복귀의 목록 문맥 불일치 한 건이다. 저장, 소개 확인, 되돌아오기, 후속 탭 복구의 순서로 추적 가능하며 스크린샷 수로 발견 건수를 늘리지 않았다.

가장 작은 후속은 기존 보관함 문맥으로 복귀하는 흐름을 user-flow 및 구현 담당에게 전달하는 것이다. 이 문서는 수정 승인이나 제품 정책 확정이 아니다. 수정이 요청된다면 새 버전과 새로운 참여자로 별도 pass를 기록하고, 이미 이 동작을 배운 참여자를 새로운 첫 사용자로 재사용하지 않는다.

## 전달물과 보존 경계

- [실제 전달한 모든 참여자 메시지 목록](/private/tmp/pm-conversation-beta-20261014/runs/coordinator/actual-dispatch-manifest.json). 초기 배포 원문은 [participant-dispatch-01.txt](/private/tmp/pm-conversation-beta-20261014/runs/coordinator/participant-dispatch-01.txt). 도구 개입, 두 번째 과업, 인터뷰, 종료 메시지도 별도 원문으로 남겼다.
- [첫 실패 고정 기록](/private/tmp/pm-conversation-beta-20261014/runs/coordinator/frozen-tool-failure/manifest.json), [시도 전체 인터뷰 전 고정 기록](/private/tmp/pm-conversation-beta-20261014/runs/coordinator/frozen-attempt-before-interview/freeze-manifest.json), [인터뷰 원문](/private/tmp/pm-conversation-beta-20261014/runs/coordinator/interview-raw.md).
- 참여자 원본 작업 공간은 `/private/tmp/pm-conversation-beta-20261014/runs/participant/`이다. 설치 지침 읽기를 제외한 작업과 증거는 그 안에 두었고 CLI 자체 daemon 캐시는 인프라 실행에 필요했다.
- 앱 파일이나 fixture를 수정하지 않았다. 소스나 숨은 상태를 이용한 조작, 다른 드라이버, 외부 연락과 서비스 호출은 사용하지 않았다. 진행자는 버전 식별용 로컬 응답의 해시만 얻었고 앱 소스를 읽어 참여자에게 알려주지 않았다.
- 검색, 입력 유지, 빈 결과, 보관함 여러 권, 추천 상세에서 돌아오기, 브라우저 뒤로 가기, 새로고침, 다른 뷰포트나 기기, 다른 세션, 실제 사람은 관찰하지 않았다. 이번 결과는 이 대상과 시작 상태의 AI 시도에 한정된다.
- 본인 세션만 종료했다. CLI가 세션 closed를 보고했고 지속 셸도 종료 코드 0을 반환했다. [세션 정리 기록](/private/tmp/pm-conversation-beta-20261014/runs/coordinator/closure.md), [종료 로그](/private/tmp/pm-conversation-beta-20261014/runs/coordinator/session-close.log).
