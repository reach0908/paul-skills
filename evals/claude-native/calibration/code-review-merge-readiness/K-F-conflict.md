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

- **누락** `src/discount.js:7`: 스펙 5번 "Codes are case-insensitive: `save10` works like `SAVE10`"가 구현되지 않았어요. `CODES[code]`가 대소문자를 그대로 비교해서 `save10`은 `RangeError`가 나요. 조회 전에 `code.toUpperCase()`로 맞추세요.

## 머지 판단

- **충돌**: 없어요. `main`과 깨끗하게 합쳐져요.
- **판정**: 지금 상태로는 머지하지 않는 게 좋아요. 막는 이유는 소수 센트(Standards)와 대소문자 무시 누락(Spec)이에요.
- **확인하지 않은 것**: CI와 테스트는 돌리지 않았어요.
