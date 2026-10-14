작업을 완료했습니다.

- 실행 URL: http://127.0.0.1:48914/runs/break-paul/app/stress/
- 관찰 결과: 빈 제목에서 버튼이 작은 빈 테두리로만 표시되는 깨짐 1건 확인 (`better-writing`)
- 나머지 14개 시나리오에서는 이탈·겹침·잘림이 관찰되지 않았습니다.
- 실제 `renderQueueCard`를 import했으며 제품 파일은 변경하지 않았습니다.
- 전체 보고서: [output/report.md](/private/tmp/paul-beta-readiness-20261014/public/runs/break-paul/output/report.md)
- 전체 캡처: [output/stress-page.png](/private/tmp/paul-beta-readiness-20261014/public/runs/break-paul/output/stress-page.png)
- 하네스: [app/stress/harness.js](/private/tmp/paul-beta-readiness-20261014/public/runs/break-paul/app/stress/harness.js)

결과 페이지는 유지했고, 전용 Playwright 세션만 종료했습니다.