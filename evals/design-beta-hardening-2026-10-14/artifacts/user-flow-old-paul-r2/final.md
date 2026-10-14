완료했습니다: [output/flow.md](/private/tmp/paul-beta-hardening-20261014/public/runs/user-flow-old-paul-r2/output/flow.md)

포함 내용:

- `timeout-unknown`, 실제 실패, `pending`, `succeeded/S-72` 분리
- 1·2차 상태 확인 전이
- 닫기·재진입 및 초안/요청 키 보존
- 중복 저장 요청 방지
- 뒤로가기 문맥 유지
- 인증 복구 API, 만료 초대 권한, 실패 후 재시도 정책을 미결로 명시
- 성공·복구·종료 경로 워크스루

계정·라이브 API·브라우저·구현 코드는 확인하지 않았으므로 실제 서버 동작은 검증하지 않았습니다.