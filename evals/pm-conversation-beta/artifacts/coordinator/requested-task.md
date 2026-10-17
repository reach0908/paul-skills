# 요청

prototype-user-test 지침으로 http://127.0.0.1:48617 을 390x844에서 테스트해줘. 가상 책장이고 외부 전송 없이 브라우저 세션 안에서만 담기가 가능해. 한 명의 새로운 서브에이전트를 사용해줘. 그 에이전트가 첫 인상을 간단히 본 다음, ‘별의 지도를 나중에 읽기 위해 담아보세요’, 이어서 ‘내가 담은 책 중 별의 지도를 찾아 소개를 확인하고, 방금 보던 목록으로 돌아오세요’를 차례로 수행하도록 해줘. 과업당 최대 15회 UI 행동, 전체 8분 이내. 실행 후 그 참여자에게 무엇을 예상했고 어떤 단서로 행동했는지 인터뷰하고 제작 의도와 비교해줘. 앱 수정은 하지 마.

제작 의도는 /private/tmp/pm-conversation-beta-20261014/author-intent.md 에 있어. 진행자만 읽어. 결과와 실제 배포한 참여자 프롬프트, 관찰/인터뷰 원문은 /private/tmp/pm-conversation-beta-20261014/runs/coordinator/ 에 저장해줘. 참여자 작업 공간은 /private/tmp/pm-conversation-beta-20261014/runs/participant/ 만 쓰게 해줘. 브라우저 자동화는 설치된 design-browser 지침의 Playwright CLI 경로를 사용해줘.
