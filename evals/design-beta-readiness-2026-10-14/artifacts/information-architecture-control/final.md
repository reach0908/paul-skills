작업을 완료했습니다.

- [정보 구조 지도](/private/tmp/paul-beta-readiness-20261014/public/runs/information-architecture-control/output/map.md)
- [한국어 작업 보고서](/private/tmp/paul-beta-readiness-20261014/public/runs/information-architecture-control/output/report.md)
- 실행 URL: <http://127.0.0.1:48914/runs/information-architecture-control/output/map.md>

기존 4개 목적지, 콘텐츠–목적지 표, 진입·검색·필터·복귀 경로, 저장 상태 흐름, 좁은 화면 우선순위와 미결 권한을 정리했습니다.

Playwright 세션은 Chrome 시작 직후 `SIGABRT`와 `kill EPERM`으로 종료되어 URL 렌더링과 화면 캡처는 확인하지 못했습니다. 다른 드라이버나 우회는 사용하지 않았으며, 해당 관찰 한계를 보고서에 기록했습니다. 지정 세션은 최종적으로 열려 있지 않음을 확인했습니다.