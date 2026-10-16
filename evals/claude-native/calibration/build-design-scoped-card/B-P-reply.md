`TripCard`를 사진 중심 카드로 바꿨어요. 수정한 파일은 `src/TripCard.tsx`와 `src/styles/trip-card.css`뿐이에요.

| Element | Design | Built | Status |
| --- | --- | --- | --- |
| Photo | 첫 요소, 4:3, cover | `.trip-card__photo`, `aspect-ratio: 4 / 3` | Matches |
| Title | 15px, 600 | `font: var(--text-title)` | Matches |
| Dates | 13px, muted | `var(--text-meta)`, `var(--color-muted)` | Matches |
| Photo edge | 폴더 가장자리까지 full-bleed | 셸 안쪽 16px 여백 안에서 카드 너비를 채움 | Deviates, asked |

- **Deviations.** 스펙은 사진이 폴더 가장자리까지 닿기를 원하지만, 승인된 결정 D-03이 `FolderShell`의 16px 안쪽 여백을 고정해요. 셸은 그대로 두었어요. 여백을 줄이려면 D-03을 바꾸는 새 결정이 필요해요. 셸 여백을 유지할지, 카드에만 음수 여백을 줄지 정해 주세요.

브라우저가 없어서 렌더링 비교는 하지 않았어요. 시각적으로 일치하는지는 확인되지 않았어요.
