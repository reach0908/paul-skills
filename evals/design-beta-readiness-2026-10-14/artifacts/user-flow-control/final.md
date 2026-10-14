작업을 완료했습니다.

- [T-SAVE 상태·전이 명세](</private/tmp/paul-beta-readiness-20261014/public/runs/user-flow-control/output/flow.md>)
- [작업 보고서](</private/tmp/paul-beta-readiness-20261014/public/runs/user-flow-control/output/report.md>)
- 실행 URL: `http://127.0.0.1:48914/runs/user-flow-control/`

화면 코드는 변경하지 않았습니다. Playwright는 Chrome 시작이 `SIGABRT`/`TargetClosedError`로 차단되어 페이지 관찰과 캡처를 수행하지 못했으며, 이를 보고서에 명시했습니다. 인증 복구 API와 실패 후 재시도 정책은 미결로 유지했습니다.