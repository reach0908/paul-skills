# 씨앗 예약 와이어프레임 화면 명세

작성 기준은 SEED-PM-8, 실제 `ia.md`, `flow.md`의 F-SEED-PICKUP-01이다. 입력 리비전과 SHA-256은 `../output/stage3/input-hashes.json`에 기록했다. IA, 흐름, 토큰, 스킬 원문을 변경하지 않았다. 새로운 정책 가정 없이 흐름의 다섯 가정을 적용했다.

실행: http://127.0.0.1:48812/composition/design/ . 산출물은 `index.html`이며 스타일 토큰은 `../app/tokens.css`의 상대 링크를 사용한다. 이는 로컬 모의 화면 초안이다. 화면 렌더링과 확인된 행동은 사용자 수용이나 제품 준비 완료를 뜻하지 않는다.

## 경로와 화면 상태

| 기존 경로 / 목적지 | 해시 경로 | 상태와 계층 | 행동 / 흐름 |
|---|---|---|---|
| /seeds, D-SEEDS | #/seeds | S-SEEDS: 제목, 한 봉지 안내, 계절, 씨앗 ID·이름·설명 | 계절 변경 T02, 정규 상세 링크 T03. 초기 autumn T01 |
| /seeds/{seedId}, D-SEED-DETAIL | #/seeds/BEAN-2 또는 #/seeds/SUN-5 | S-EDIT: 씨앗 이름·ID·한 봉지·설명, 수령 안내, 이름 입력, 모의 안내, Submit와 Back | T03/T04/T06/T11/T14 |
| 같은 상세 | 같은 해시 | S-INVALID: 필수 이름 오류를 필드에 연결, 원문 유지 | Submit T05, 수정 T04, Back T10. 오류 시 이름으로 포커스 |
| 같은 상세 | 같은 해시 | S-PENDING-FIRST / S-PENDING-RETRY: 이름 읽기 전용, 미확정 안내, 비활성 Submit, Back | 400ms T06/T09/T11, 반복 제출 무시 T07, Back 중단 T13 |
| 같은 상세 | 같은 해시 | S-FAILED: 씨앗·수령 안내·입력 유지, 첫 모의 실패, Retry와 Back | Retry T09, 수정 복귀 T10. Retry로 포커스 |
| 같은 상세 | 같은 해시 | S-CONFIRMED: SP-21, trim한 이름, 씨앗 ID·이름·수량, 토요일 시간·장소, 모의 확정 안내 | T12에서만 기록 생성. My pickups T16, Back T19 |
| 같은 상세 | 같은 해시 | S-DETAIL-RECORDED: 현재 씨앗 정보, 기존 한 건 안내 | 추가 제출 없음 T18. 기존 내역과 Reset demo 안내 |
| /my-pickups, D-MY-PICKUPS | #/my-pickups | S-PICKUPS-EMPTY: 빈 내역 안내와 Seeds. S-PICKUPS-FILLED: 같은 SP-21 기록 | 전역 이동 T16. 읽기 전용 내역 |

전역 Seeds, My pickups와 Reset demo는 모든 상태에서 보인다. Seeds는 필터를 유지한다(T15). 대기 중 경로 이동은 시도 번호와 타이머를 무효화하여 늦은 결과가 기록을 만들지 않는다(T17). Reset demo는 autumn, 빈 이름·기록·실패 이력으로 복원한다(T20). 새로고침은 현재 해시의 목적지를 새 데이터로 연다(T21). 알 수 없는 씨앗 ID는 범위 밖이다.

## 화면 우선순위와 키보드

데스크톱은 토큰의 880px 콘텐츠 폭 안에서 한 열로 과업 순서를 유지한다. 모바일에서는 페이지 여백과 카드 여백을 줄이고 제목을 24px로 조정한다. 두 목적지는 메뉴 안에 숨기지 않는다. 씨앗 정체성 다음에 수령 안내, 이름, 피드백과 다음 행동을 배치한다. 긴 이름과 장소는 줄바꿈하고 필요한 세로 스크롤을 허용한다. 데스크톱의 보조 칼럼을 모바일 끝으로 밀어 넣는 구성은 없다.

네이티브 링크·버튼·select·input, 이름 label, aria-invalid/aria-describedby, alert/status를 사용한다. 상단에 본문 건너뛰기 링크가 있다. 경로·상태 전환은 제목, 필수 오류는 이름, 실패는 Retry에 포커스를 준다. :focus-visible 토큰 윤곽을 사용한다. 입력 중 렌더를 반복하지 않아 이름 편집의 포커스를 보존한다.

## 모의 경계와 추적

| 요구사항 | 구현 위치와 관찰 대상 |
|---|---|
| I1 | seeds 상수의 두 ID·이름·설명을 원문 유지. 한 봉지. 확정 기록에 성공 시도의 씨앗 고정 |
| I2 | 메모리의 season과 정규 해시 상세. Seeds 복귀 맥락 유지. 좁은 폭에도 두 전역 링크 |
| I3 | submit의 trim 검증과 400ms setTimeout, pending 가드, 첫 실패, Retry/Back. 이름 원문은 draft 보존 |
| I4 | 재시도 완료 콜백만 record 생성. receipt 함수를 결과와 내역에서 공유. SP-21 단일 기록 |
| I5 | 문서 실행 메모리만 사용. localStorage 및 서버 요청 없음. 전역 모의 표시와 Reset demo |
| I6 | 계층·label·명시적 포커스·반응형 여백. 실제 관찰은 stage3 보고서와 로그 참조 |

## 확인 상태와 미해결 범위

브라우저 관찰의 원본은 `../output/stage3/walkthrough-log.txt`, 화면 캡처는 같은 폴더에 있다. 실제로 완료한 경로, 화면 크기, 도구 오류와 한계는 `../output/stage3/report.md`에 구분해 기록한다. 스크린리더, 실제 터치 기기, 확대, 다른 브라우저, 사용자 과업 조사, 시각 승인과 일치도는 확인하지 않았다. 후속 단계는 이 범위를 확장하거나 사용자 승인을 추정하지 않아야 한다.
