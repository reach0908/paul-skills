# 모래시계 본체와 3D 모래 구현 방향

- 조사일: 2026-10-16
- 범위: `sources/`의 K1, K2만 확인했다.

## 결론

본체는 DepthKit `TransparentMaterial` 메시로 만들고, 그 안에 모래 파티클을 넣는다 [K2 §Transparent materials]. 버튼과 툴바에는 GlassKit `glassEffect()`를 쓴다 [K1 §Overview].

## 근거

| 주장 | 자료 | 위치 |
| --- | --- | --- |
| 투명 메시 안 파티클 렌더 | K2 | §Transparent materials |
| glassEffect는 컨트롤과 툴바용 | K1 | §Overview |

## 한계

- 두 문서만 봤다.

## 남은 질문

- 모래 파티클 수에 따른 성능.
