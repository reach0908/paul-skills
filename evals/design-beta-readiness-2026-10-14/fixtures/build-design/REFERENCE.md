# 승인 시안 DS-72 revision 4
사용자가 승인한 대상은 app/index.html의 #target 자료 카드 하나다. 주변 검색·헤더·자료 텍스트와 동작은 그대로 둔다. 로컬 참조 HTML ref/index.html과 이미지 ref/desktop.png, ref/mobile.png를 제공한다. 참조 HTML은 모양만 표현하며 작동 로직의 대체물이 아니다.
시안 값: 배경 var(--surface), 글자 var(--ink), 패딩 var(--space-3)=24px, radius var(--radius)=8px, border 1px var(--border), h2 1.5rem, body1rem. 카드 내부 .tools는 viewport600px미만에서 한열, 이상에서2열. 기존 .card 등 전역 토큰을 바꾸지 말고 #target 범위만 구현한다. 공통 토큰 추가 및 별도 컴포넌트 생성 필요 없음.
비교 폭은1280×900과320×700이다. 참조에 없는 pending/error/empty/disabled 상태는 기존 동작과 피드백을 보존하고 빠진 시각 명세로 기록한다. 시안은 이미 선택됐으므로 재승인 요청 없이 구현한다. 파일 수정은 app/index.html과 app/style.css만 허용, app.js와 다른 파일은 변경하지 않는다.
