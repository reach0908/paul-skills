# 내보내기 패널 전이 계약

## 근거와 범위

- 근거: 요청에 함께 제공된 정책 9개. 기존 구현은 확인하지 않았다.
- actor: 로그인한 편집자. 진입: `exports-panel`. 복귀 부모: `documents-list`.
- 목표: 선택한 옵션으로 내보내기를 요청하고, 서버가 완료를 확인하면 결과를 내려받는다.
- 성공 조건: 서버 완료 확인 뒤 receipt가 기록되고 다운로드할 수 있다.
- 범위 밖: 화면 배치, 구현, 취소 기능.

## 상태

operation과 visibility를 따로 둔다.

- operation: `idle`(미시작), `running`(진행), `failed`(실패), `done`(완료)
- visibility: `open`, `closed`
- 데이터: 옵션 O, request key K, receipt R

## 전이

| ID | 출발 상태와 조건 | 행동 또는 사건 | 피드백과 도착 | 보존 또는 변경 데이터 |
| --- | --- | --- | --- | --- |
| T1 | idle/open, 옵션 유효 | 시작 | 처리 중 안내; running/open | O 유지, 새 K 생성, R 없음 |
| T2 | running/open | 시작 재클릭 | 이미 처리 중 안내; running/open | 같은 O, K 유지, 새 요청 없음 |
| T3 | running/임의, 응답 K 일치 | 서버 실패 | 열림이면 실패와 재시도 안내; failed/기존 visibility | O, K 유지, R 없음 |
| T4 | failed/open | 재시도 | 처리 중 안내; running/open | 같은 O, K, R 없음 |
| T5 | running/임의, 응답 K 일치 | 서버 완료 확인(R) | 열림이면 다운로드 표시; done/기존 visibility | O, K 유지, R 기록 |
| T6 | idle, running, failed, done 중 하나/open | 닫기 | `documents-list`로 복귀; 같은 operation/closed. 요청은 취소하지 않는다 | 해당 상태 데이터 유지. idle에는 K, R 없음 |
| T7 | 임의 operation/closed | 다시 열기(같은 세션) | `exports-panel`에 최신 operation 표시; 같은 operation/open | idle=O, running과 failed=O, K, done=O, K, R |
| T8 | done/open, R 있음 | 다운로드 | R의 다운로드 진입; done/open | O, K, R 유지 |
| T9 | 임의 | 새로고침 | 미정(Q1). 이후 전이를 확정하지 않는다 | 보존 여부 미정 |

## 경로 확인

- 성공: T1 → T5 → T8. 시작 뒤 서버 확인 전에는 receipt가 없다.
- 실패와 재시도: T1 → T3 → T4 → T5. 재시도는 같은 K를 쓴다.
- 닫기와 다시 열기: 네 operation 각각에서 T6 → T7. idle은 O만, done은 R까지 복원한다.
- 닫힌 동안 완료: T1 → T6 → T5 → T7. 다시 열면 done으로 보인다.
- 새로고침: Q1이 정해질 때까지 확인할 수 없다.

이 확인은 문서 안의 일관성 검토다. 구현 동작이나 실제 사용자 검증이 아니다.

## 화면이 보여 줄 정보와 행동

- idle: 옵션, 시작(T1), 닫기(T6)
- running: 처리 중 상태, 시작 재클릭 안내(T2), 닫기(T6)
- failed: 실패 이유, 재시도(T4), 닫기(T6)
- done: 다운로드(T8), 닫기(T6)

## 미결 사항

- Q1: 새로고침 뒤 operation과 데이터를 복원할지 정해지지 않았다. T9와 새로고침 이후 경로가 이 결정에 의존한다.
