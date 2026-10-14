# 실행 보고서

## 결과

지정된 두 로컬 페이지를 Playwright CLI 전용 세션 `beta-explain-interface-original`에서 조사했고, 구현 설명을 [explanation.md](explanation.md)에 작성했다. 앱 소스와 운영 컨트롤은 수정하지 않았다.

## 실행 가능한 URL

- 메인: `http://127.0.0.1:48914/runs/explain-interface-original/app/index.html`
- 상세: `http://127.0.0.1:48914/runs/explain-interface-original/app/detail.html`

## 생성 파일

- 상세 분석: [explanation.md](explanation.md)
- 실행 보고서: [report.md](report.md)
- 캡처 디렉터리: [captures](captures)

## 실제 관찰 상태

- 두 페이지 모두 1280×900과 390×844에서 확인했다.
- 각 viewport에서 앱의 테마 버튼으로 밝은/어두운 상태를 확인했다.
- 운영체제 dark 선호만으로는 앱 테마가 바뀌지 않는 것도 별도로 확인했다.
- index에서 WAAPI 재생 경로와 `prefers-reduced-motion: reduce` 분기를 확인했다.
- detail에서 첫 번째 키보드 Tab 대상의 focus-visible 계산 스타일을 확인했다.
- 네트워크 요청, DOM/프레임워크 지문, CSS 토큰, computed type/spacing/color/layout, pseudo-element, animation 객체를 조사했다.

## 캡처

- [index · 1280×900 · 밝음](captures/index-1280x900-light.png)
- [index · 1280×900 · 어두움](captures/index-1280x900-dark.png)
- [index · 390×844 · 밝음](captures/index-390x844-light.png)
- [index · 390×844 · 어두움](captures/index-390x844-dark.png)
- [detail · 1280×900 · 밝음](captures/detail-1280x900-light.png)
- [detail · 1280×900 · 어두움](captures/detail-1280x900-dark.png)
- [detail · 390×844 · 밝음](captures/detail-390x844-light.png)
- [detail · 390×844 · 어두움](captures/detail-390x844-dark.png)

## 관찰된 핵심 결과

- 배포 결과는 일반 HTML 링크로 연결된 정적 2페이지 구조이고, 동작은 짧은 인라인 JavaScript가 담당한다.
- 공통 CSS는 8px 기반 간격 토큰과 semantic 색 토큰을 사용한다. 공유 CSS가 24px/16px 반응형 site 토큰과 600px breakpoint를 제공한다.
- index의 효과는 frame, oversized radial glow, 24px blur, 4% glass, 8px backdrop blur, 전경 콘텐츠의 순서로 쌓인다.
- chip 재생은 1200ms WAAPI이며 첫 25% 구간에 변화 대부분을 배치한다. 감소 모션에서는 animation을 생성하지 않고 즉시 최종 상태를 쓴다.
- 웹폰트·이미지·외부 JavaScript 번들은 관찰된 요청에 없었다. 특정 프레임워크의 부재를 이 사실만으로 단정하지 않았다.

## 한계와 미검증 범위

- `http://localhost:48914/shared.css`는 페이지와 호스트명이 달라 CSSOM `cssRules` 접근이 차단됐다. 브라우저 네트워크 응답 본문과 각 상태의 computed style로 보완했지만 CSSOM 전체 열거는 하지 못했다.
- 1280px/390px 이외의 중간 폭, hover/disabled, 현재 DOM에 없는 form/card 도우미 클래스의 실제 렌더링은 검증하지 않았다.
- 배포 이전의 원본 프레임워크·빌드 도구는 정적 산출물만으로 식별할 수 없다.
- 정적 서버 프로세스는 건드리지 않았으며, 관찰에 사용한 전용 Playwright CLI 세션만 종료한다.
