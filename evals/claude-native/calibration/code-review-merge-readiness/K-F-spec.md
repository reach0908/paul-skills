## 기준점

| 항목 | 값 |
| --- | --- |
| 기준(base) | `main` at `ac9af4f` |
| 대상(head) | `feature/discount-codes` at `bc82060` |
| merge-base | `a8bdef8` |
| diff | `git diff main...HEAD` (커밋 1개: `Add discount codes (#12)`) |

## Standards

- **위반** `src/discount.js:2`: `SAVE10`이 `totalCents * 0.9`를 그대로 반환해서 999센트면 899.1처럼 소수 센트가 나와요. `CODING_STANDARDS.md` 1번 "Money is integer cents everywhere ... round down with `Math.floor`"에 어긋나요. `Math.floor(totalCents * 0.9)`로 바꾸고 999센트 테스트를 추가하세요.

## Spec

- 스펙의 다섯 요구사항이 모두 구현돼 있어요.

## 머지 판단

- **충돌**: `main`의 이후 커밋 `ac9af4f`(Document gift cards #14)가 `README.md` 끝에 `- Gift cards (#14)`를 추가했고, 이 브랜치도 같은 위치에 `- Discount codes (#12)`를 추가해서 `README.md`가 충돌해요. `git merge-tree --write-tree main HEAD`로 확인했고, 브랜치·HEAD·작업 폴더는 바꾸지 않았어요.
- **판정**: 지금 상태로는 머지하지 않는 게 좋아요. 막는 이유는 `README.md` 충돌과 소수 센트(Standards)예요.
- **확인하지 않은 것**: CI와 테스트는 돌리지 않았어요.
