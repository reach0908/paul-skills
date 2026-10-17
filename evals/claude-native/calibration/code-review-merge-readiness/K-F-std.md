## 기준점

| 항목 | 값 |
| --- | --- |
| 기준(base) | `main` at `ac9af4f` |
| 대상(head) | `feature/discount-codes` at `bc82060` |
| merge-base | `a8bdef8` |
| diff | `git diff main...HEAD` (커밋 1개: `Add discount codes (#12)`) |

## Standards

- 문서화된 기준을 어긴 곳은 없어요. 새 함수에 테스트가 있고 모듈 이름도 도메인을 따라요.

## Spec

- **누락** `src/discount.js:7`: 스펙 5번 "Codes are case-insensitive: `save10` works like `SAVE10`"가 구현되지 않았어요. `CODES[code]`가 대소문자를 그대로 비교해서 `save10`은 `RangeError`가 나요. 조회 전에 `code.toUpperCase()`로 맞추세요.

## 머지 판단

- **충돌**: `main`의 이후 커밋 `ac9af4f`(Document gift cards #14)가 `README.md` 끝에 `- Gift cards (#14)`를 추가했고, 이 브랜치도 같은 위치에 `- Discount codes (#12)`를 추가해서 `README.md`가 충돌해요. `git merge-tree --write-tree main HEAD`로 확인했고, 브랜치·HEAD·작업 폴더는 바꾸지 않았어요.
- **판정**: 지금 상태로는 머지하지 않는 게 좋아요. 막는 이유는 `README.md` 충돌과 대소문자 무시 누락(Spec)이에요.
- **확인하지 않은 것**: CI와 테스트는 돌리지 않았어요.
