완료했습니다.

- 실행: [로컬 와이어프레임](http://127.0.0.1:48924/runs/chain-wire/app/)
- 구현: [app/index.html](/private/tmp/paul-beta-hardening-20261014/public/runs/chain-wire/app/index.html)
- 화면 명세·검증 기록: [output/screens.md](/private/tmp/paul-beta-hardening-20261014/public/runs/chain-wire/output/screens.md)
- 캡처: [1280×900](/private/tmp/paul-beta-hardening-20261014/public/runs/chain-wire/output/desktop-1280x900.png), [320×700](/private/tmp/paul-beta-hardening-20261014/public/runs/chain-wire/output/mobile-320x700.png)

주요 구현 사항:

- `TS-00→TS-40`, `TS-90`, 닫기·복귀 및 `TR/NAV/OD` ID 보존
- 첫 확인 `pending`, 두 번째 확인 `S-72`
- 닫힌 동안 `TR-13/14/15` 진행
- 초안·목록 문맥 유지, 본문 앵커와 외부 출처 연결
- 실제 API 없이 `sessionStorage`와 지연 타이머로 경계 모의
- 명시적 초기화 버튼으로만 상태 삭제
- 양쪽 뷰포트에서 키보드 순서와 가로 넘침 0px 확인
- 최종 콘솔 오류·경고 0건

`hard-chain-wire` 세션은 검증 후 닫았습니다. 사용자 수용성이나 실제 서버 준비 상태는 판정하지 않았습니다.