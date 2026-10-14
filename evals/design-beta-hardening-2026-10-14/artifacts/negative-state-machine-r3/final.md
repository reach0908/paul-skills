요청한 업로드 닫기·복귀 흐름을 한국어 전이표로 작성했습니다.

[UPLOAD_CLOSE_REOPEN_FLOW.md](/private/tmp/paul-beta-hardening-20261014/public/runs/negative-state-machine-r3/UPLOAD_CLOSE_REOPEN_FLOW.md)

포함 내용:

- 제출 전 초안 유지 및 요청 키 없음
- 요청 중 닫기와 실제 취소의 분리
- 닫힌 동안 완료되는 경로
- 완료 후 영수증 유지와 복귀
- 상태별 보존 데이터와 전이 규칙

계정과 라이브 API가 없어 실제 지속성은 검증하지 않았습니다. 방문 종료 기준, 영수증 보존 기간, 실패·재시도 정책은 입력에 없으므로 미결정 사항으로 명시했습니다.