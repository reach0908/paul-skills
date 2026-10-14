구현을 완료했습니다.

- `#target` 카드 스타일만 [app/style.css](/private/tmp/paul-beta-readiness-20261014/public/runs/build-design-paul/app/style.css)에 추가
- `app/index.html`, `app/app.js`는 변경하지 않음
- 실행 URL: <http://127.0.0.1:48914/runs/build-design-paul/app/>
- 캡처: [1280×900](/private/tmp/paul-beta-readiness-20261014/public/runs/build-design-paul/output/desktop-1280x900.png), [320×700](/private/tmp/paul-beta-readiness-20261014/public/runs/build-design-paul/output/mobile-320x700.png)
- 상태·키보드 관찰과 미결 사항: [output/report.md](/private/tmp/paul-beta-readiness-20261014/public/runs/build-design-paul/output/report.md)

두 캡처는 제공된 대응 참조 PNG와 파일 해시가 동일했습니다. Pending, disabled, success, error, empty와 키보드 순서를 실제로 확인했습니다. PB-72의 `timeout-unknown → 상태 확인` 흐름은 수정 금지된 기존 `app.js` 동작과 달라 미결 사항으로 기록했습니다.

지정 Playwright 세션만 사용했으며 관찰 후 닫았습니다.