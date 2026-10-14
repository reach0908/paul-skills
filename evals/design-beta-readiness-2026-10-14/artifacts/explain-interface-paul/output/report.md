# 실행 보고서

## 결과

- 설명: [explanation.md](explanation.md)
- 실행 URL:
  - `http://127.0.0.1:48914/runs/explain-interface-paul/app/index.html`
  - `http://127.0.0.1:48914/runs/explain-interface-paul/app/detail.html`
- 관찰 시간: 2026-10-14 12:06–12:10 KST (03:06–03:10 UTC)
- 도구: Playwright CLI 0.1.22, Headless Chrome 152.0.0.0
- 전용 세션: `beta-explain-interface-paul`
- viewport: 1280×900, 390×844. viewport resize만 사용했으며 모바일/터치 기기 에뮬레이션은 하지 않았습니다.

## 관찰한 상태

- index와 detail 각각에서 1280×900 밝음/어두움, 390×844 밝음/어두움을 렌더링하고 full-page PNG를 저장했습니다.
- 테마 버튼을 실제 클릭해 `<html data-theme>`과 computed token/body 색 변화를 확인했습니다.
- 시스템 dark 선호만 켠 초기 문서가 밝은 상태로 남는지 확인했습니다.
- index의 재생 버튼을 normal motion에서 실행해 0ms, 약 300ms, 1250ms의 WAAPI 상태를 읽었습니다.
- `prefers-reduced-motion:reduce`에서 같은 버튼을 실행해 animation 0개와 즉시 적용된 최종 inline style을 확인했습니다.
- index 효과의 frame/glow/glass/content stacking 값, 크기, pseudo-element를 읽었습니다.
- detail에서 첫 링크의 keyboard focus-visible computed style을 확인했습니다.
- index의 detail 링크를 실제로 눌러 새 문서 navigation과 테마 비영속성을 확인했습니다.

## 캡처

- [index 1280 밝음](captures/index-1280-light.png)
- [index 1280 어두움](captures/index-1280-dark.png)
- [index 390 밝음](captures/index-390-light.png)
- [index 390 어두움](captures/index-390-dark.png)
- [detail 1280 밝음](captures/detail-1280-light.png)
- [detail 1280 어두움](captures/detail-1280-dark.png)
- [detail 390 밝음](captures/detail-390-light.png)
- [detail 390 어두움](captures/detail-390-dark.png)
- [detail 390 첫 링크 focus-visible](captures/detail-390-focus.png)

모든 캡처의 실제 픽셀 크기는 파일명과 일치합니다.

## CSS와 런타임 증거의 한계

- `http://localhost:48914/shared.css`는 페이지 출처 `127.0.0.1`과 달라 CSSOM의 `cssRules` 접근이 `SecurityError`로 차단됐습니다.
- 해당 CSS는 Playwright 브라우저 컨텍스트의 HTTP 요청으로 status 200 응답 본문을 별도 읽었습니다. authored breakpoint/token은 이 응답에서, 실제 적용값은 각 상태의 computed style에서 독립적으로 확인해 설명에 구분했습니다.
- 원본 저장소, 다른 실험 arm, 이전 trial, evaluator rubric, global memory는 읽지 않았고 사이트 소스도 수정하지 않았습니다.
- 런타임 fingerprint가 발화하지 않은 기술을 “없다”고 단정하지 않았습니다. 정적 multi-page 방식은 외부 JS 요청 부재, classic 인라인 스크립트, 일반 HTML 링크의 full navigation에 근거한 추정입니다.

## 남은 미확인 범위

- 600/601px 경계 자체, 390과 1280 사이의 중간 폭은 렌더링하지 않았습니다. exact breakpoint는 fetched CSS에서 읽었습니다.
- Chrome 이외 브라우저, DPR 1 이외, 실제 터치 기기, 브라우저 확대/축소는 확인하지 않았습니다.
- hover/active/disabled 상태와 두 번째 이후의 tab 순서는 이번 전체 구현 설명의 필수 상태가 아니어서 따로 캡처하지 않았습니다.
- 애니메이션 중간 프레임은 computed 값을 시간별로 읽었고 영상 캡처는 만들지 않았습니다.
- 원본 빌드 도구, 전처리 과정, 작성 시 사용한 라이브러리는 런타임 산출물만으로 확인할 수 없습니다.
