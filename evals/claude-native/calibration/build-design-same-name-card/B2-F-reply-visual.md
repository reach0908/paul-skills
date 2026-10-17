컬렉션 상세 화면 하단 "관련 주제"를 라이브러리 화면의 주제 카드로 바꿨어요. 수정한 파일은 `src/collection/CollectionPage.tsx` 하나예요.

| Reference | Source file and export | Target call site | Preserve |
| --- | --- | --- | --- |
| `/library`, footer "Explore topics", collapsed | `src/library/TopicCard.tsx:TopicCard` | `CollectionPage` "Related topics" footer | 카드 전체 링크(`<a href=/topics/:id>`), Enter로 열기, 포커스 표시 |

- `TopicCard`라는 이름의 export가 두 개 있어요. `src/library/LibraryPage.tsx`를 보면 "Explore topics" 푸터는 `./TopicCard`(라이브러리용)를 쓰고, "Recommended topics"는 `../components/TopicCard`(누르면 팔로우되는 `div`)를 써요. 참고 화면이 가리키는 건 라이브러리용이라 그쪽을 가져왔어요.
- 두 컴포넌트 본문과 스타일은 바꾸지 않았어요. 카드 전체가 `<a>`라서 링크와 Enter 동작이 그대로 유지돼요.

375px와 1280px에서 라이브러리 푸터와 나란히 확인했고, 카드가 똑같이 보이고 Enter로도 잘 열려요.
