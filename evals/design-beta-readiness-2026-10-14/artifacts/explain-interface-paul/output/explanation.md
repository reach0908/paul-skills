# 두 페이지 인터페이스 구현 설명

## 증거 범위와 표기

- **측정(Measured)**: 지정된 Playwright CLI 세션에서 DOM, 네트워크 응답, CSSOM, computed style, Web Animations API와 픽셀 캡처로 직접 확인한 값입니다.
- **도출(Derived)**: 측정값 사이의 비율, 캐스케이드와 레이어 관계에서 계산한 설명입니다.
- **추정(Inferred)**: 런타임 증거로 가장 잘 설명되는 구현 방식입니다. 원본 저장소나 빌드 설정은 읽지 않았으므로 작성 도구 자체를 확정하지 않습니다.

관찰 경로는 Playwright CLI 0.1.22의 스크립트 가능한 브라우저(Headless Chrome 152)였습니다. `1280×900`, `390×844`에서 두 페이지의 밝은/어두운 테마를 모두 렌더링했고, index의 WAAPI와 `prefers-reduced-motion` 경로도 실행했습니다. 좁은 화면은 viewport resize이며 터치 기기 에뮬레이션은 아닙니다.

## 프런트엔드와 렌더링 방식

- **측정**: index는 `detail.html`, detail은 `index.html`을 가리키는 일반 `<a>` 링크를 사용합니다. index에서 링크를 눌렀을 때 detail 문서가 HTTP 200의 새 `navigation`으로 로드됐고 Performance Navigation Timing의 `type`은 `navigate`였습니다.
- **측정**: 두 페이지 모두 외부 JavaScript 요청이 없었고, 각 문서에 `classic` 인라인 스크립트 하나만 있었습니다. detail은 테마 토글만, index는 같은 테마 토글과 재생 버튼의 WAAPI를 담습니다.
- **측정**: 관찰한 리소스는 페이지 문서, `app/style.css`, `http://localhost:48914/shared.css`뿐입니다. 이미지와 author-loaded FontFace는 0개였고 favicon은 `data:` URL이었습니다.
- **측정**: Next/Nuxt/Remix/Gatsby/Astro/Svelte/Angular/React Fiber, Tailwind, CSS Modules, styled-components, Emotion, Radix, MUI에 대해 실행한 제한된 런타임 fingerprint는 모두 발화하지 않았습니다.
- **추정**: 실제 동작은 서버에서 완성된 두 HTML 문서를 각각 내리고, 문서 안의 작은 vanilla JavaScript가 상태를 바꾸는 정적 multi-page 구조로 가장 잘 설명됩니다. fingerprint 불발은 어떤 빌드 도구나 라이브러리의 절대적 부재를 증명하지 않습니다.

## CSS 전달과 캐스케이드

- **측정**: index의 스타일 순서는 같은 출처 `app/style.css` → 문서 인라인 `<style>` → 다른 출처 `http://localhost:48914/shared.css`입니다. detail에는 같은 두 외부 CSS가 있고 index 전용 빛 효과 인라인 스타일은 없습니다.
- **측정**: `app/style.css`는 CSSOM에서 읽혔고 17개 최상위 규칙을 노출했습니다. index 인라인 스타일은 7개 규칙을 노출했습니다.
- **측정**: `shared.css`는 페이지가 `127.0.0.1`이고 CSS가 `localhost`라서 `sheet.cssRules` 접근 시 `SecurityError`가 발생했습니다. 따라서 이 파일의 authored 규칙은 CSSOM 토큰/브레이크포인트 순회 결과에 포함되지 않습니다.
- **측정**: 같은 파일의 실제 HTTP 응답은 Playwright 브라우저 컨텍스트 요청으로 별도 읽었고 status 200, `text/css`, 514 bytes였습니다. 아래 `shared.css` 선언은 이 응답에서 읽은 authored 값이고, 적용 결과는 별도의 computed style 측정으로 재확인했습니다.
- **도출**: `shared.css`가 마지막에 오므로 기본 CSS의 `body { background:#f3f5f7 }`, `main { padding:16px }`, `h1 { font-size:1.5rem }` 중 앞의 두 값은 각각 `var(--surface)`와 `var(--site-space)`로 덮입니다. 제목은 데스크톱에서 우연히 같은 1.5rem이고 모바일에서 shared media query가 1.25rem로 바꿉니다.

## 토큰과 색 시스템

### 기반 토큰

`app/style.css` 응답에서 직접 읽은 값입니다.

| 그룹 | 토큰 | 값 | 근거 |
| --- | --- | --- | --- |
| 간격 | `--space-1` / `-2` / `-3` / `-4` | 8 / 16 / 24 / 32px | **측정** |
| 색 | `--brand` / `--ink` / `--surface` / `--border` | `#174b82` / `#17212b` / `#fff` / `#60758c` | **측정** |
| 형태 | `--radius` | 8px | **측정** |
| 타입 | `--type-title` / `--type-body` | 1.5rem / 1rem | **측정** |

### shared 의미 토큰과 테마

| 상태 | `--surface` | `--ink` | `--brand` | 실제 body | 근거 |
| --- | --- | --- | --- | --- | --- |
| 초기/밝음 | `#ffffff` | `#17212b` | `#174b82` | 흰 배경, `rgb(23,33,43)` 글자 | **측정** |
| `data-theme="dark"` | `#17212b` | `#f3f5f7` | `#8dbbfa` | `rgb(23,33,43)` 배경, `rgb(243,245,247)` 글자 | **측정** |

- **측정**: 테마 버튼은 `<html data-theme>`을 `dark`와 `light` 사이에서 토글합니다. 시스템 색상 선호를 dark로 에뮬레이션하고 새로 고쳐도 `data-theme`이 없는 문서는 여전히 흰 배경이었습니다. authored CSS에도 dark용 `prefers-color-scheme` 규칙은 없었습니다.
- **측정**: index를 dark로 바꾼 뒤 detail 링크로 이동하면 새 문서의 테마는 `none`, 배경은 흰색이었습니다. localStorage와 cookie도 비어 있었습니다.
- **도출**: 테마는 현재 문서에만 있는 DOM 상태이며 페이지 간에 유지되지 않습니다. 색 변경 범위는 surface/ink/brand의 의미 토큰입니다. `--border:#60758c`, index 프레임 `#14243a`, 칩 `#163e70`, 흰 프레임 글자는 테마와 무관하게 고정됩니다.
- **측정**: 키보드로 첫 링크에 초점을 두었을 때 focus-visible은 `3px solid rgb(177,63,0)`이고 offset은 3px였습니다.

## 타입과 폰트

- **측정**: body와 모든 컨트롤의 실제 font stack은 `system-ui`였습니다. `document.fonts`의 author-loaded face와 폰트 네트워크 요청은 없었습니다.
- **측정**: 본문은 16px / 25.6px, weight 400입니다. 제목은 데스크톱 24px / 38.4px, 모바일 20px / 32px, computed weight 700입니다. 문자 간격은 모두 `normal`이었습니다.
- **도출**: 모든 단계의 line-height는 1.6이고, 본문 대비 제목 비율은 데스크톱 1.5, 모바일 1.25입니다. 두 크기만 사용하므로 작은 2단계 타입 체계입니다.
- **측정**: authored CSS는 h1의 크기만 지정하고 margin이나 weight를 리셋하지 않습니다. 실제 h1 상하 margin은 데스크톱 16.08px, 모바일 13.4px였습니다.
- **도출**: 두 margin은 각 제목 크기의 약 0.67em이므로 토큰 간격이 아니라 브라우저 기본 h1 margin의 영향입니다. weight 700도 authored 선언이 아니라 실제 computed 결과로만 확인했습니다.

## 간격, 형태와 반응형 레이아웃

- **도출**: authored 간격 토큰은 8px 배수(8/16/24/32)이고 실제 컨트롤 padding 8×16px, 프레임 padding 32px, 데스크톱 main/grid 간격 24px에서 반복됩니다.
- **측정**: 1280px viewport에서 main의 border-box는 x=160, width=960px, padding=24px입니다. 내부 폭 912px의 index grid는 `592px 296px`, gap 24px로 계산됐습니다.
- **도출**: 592:296은 정확히 2:1이고 592 + 24 + 296 = 912이므로 authored `2fr 1fr`이 실제 픽셀로 해석된 결과입니다.
- **측정**: shared CSS 응답에는 단 하나의 breakpoint `@media(max-width:600px)`가 있습니다. 이 안에서 `--site-space:16px`, `--site-type:1.25rem`, `.site-grid { grid-template-columns:1fr }`가 선언됩니다.
- **측정**: 390px에서는 main padding이 16px, 콘텐츠 폭이 358px이며 index grid는 358px 한 열, gap 16px이었습니다. 제목과 300px 프레임이 위아래로 배치됐습니다. detail도 같은 main padding과 제목 크기 변경을 공유했습니다.
- **도출**: 두 페이지의 반응형 원리는 별도 컴포넌트 재배치가 아니라 shared 토큰 두 개와 grid 열 수 한 개를 같은 breakpoint에서 교체하는 것입니다.
- **측정**: 반경은 8px 하나가 index의 테마 버튼, 칩, 재생 버튼에 재사용됐습니다. 버튼 border는 1px solid `#60758c`이고 관찰한 요소에 box-shadow는 없었습니다. 프레임은 반경 0입니다.

정확한 600/601px 경계는 직접 렌더링하지 않았습니다. breakpoint 값은 fetched CSS 응답에서 측정했고, 양쪽 대표 상태는 390px과 1280px에서 확인했습니다.

## index의 겹친 빛 효과

프레임 안의 paint stack은 아래 순서입니다. pseudo-element는 후보마다 `content:none`이어서 이 효과에 참여하지 않습니다.

| 아래 → 위 | 레이어와 실제 값 | 하는 일 |
| --- | --- | --- |
| 1 | `.frame`: `position:relative`, `isolation:isolate`, `overflow:hidden`, 296×300px(데스크톱), 배경 `#14243a`, padding 32px | **측정**: 독립 stacking context와 어두운 바탕을 만들고 넘친 blur를 자릅니다. |
| 2 | `.glow`: `position:absolute`, inset -30px, z-index -2, 356×360px, `radial-gradient(circle at 35% 45%, rgba(221,76,216,.533), transparent 65%)`, `blur(24px)` | **측정**: 프레임보다 사방 30px 큰 자홍색 방사광입니다. |
| 3 | `.glass`: inset 0, z-index -1, `rgba(255,255,255,.04)`, `backdrop-filter:blur(8px)` | **측정**: 방사광 위에서 배경을 한 번 더 흐리고 아주 옅은 흰 막을 얹습니다. |
| 4 | `#chip`과 재생 버튼: 일반 흐름, 칩 `#163e70`, 흰 글자 | **측정**: 효과 위의 읽을 수 있는 전경입니다. |

- **도출**: 데스크톱에서 glow는 프레임보다 가로·세로 각각 60px 큽니다. 모바일에서도 프레임 358×300px, glow 418×360px으로 같은 60px 여유가 유지됩니다.
- **추정**: 이 음수 inset은 24px blur의 가장자리가 프레임 내부에서 잘린 듯 보이지 않게 충분한 색 면적을 확보하려는 선택으로 보입니다.
- **도출**: 핵심은 gradient 하나가 아니라 어두운 바탕 → oversized gradient+blur → 전면 backdrop blur/4% white → 콘텐츠의 네 층입니다. 마지막 shared 테마 토큰이 바뀌어도 이 네 층의 명시 색상은 변하지 않아 효과 모양은 유지됩니다.

## 모션과 reduced motion

- **측정**: 정지 상태에서 0초보다 긴 CSS transition은 없었습니다. 모션은 재생 버튼이 `#chip`에 만드는 단일 WAAPI `Animation`입니다.
- **측정**: 재생 시 기존 `#chip` animation을 모두 cancel한 다음 duration 1200ms, easing `linear`, fill `both`로 아래 keyframe을 적용합니다.

| 시간 비율 | opacity | transform | 실제 관찰 |
| --- | --- | --- | --- |
| 0% | 0 | `translateY(12px)` | currentTime 0에서 computed opacity 0, y=12px |
| 25% | 0.9 | `translateY(1px)` | 약 300.02ms에서 opacity 0.900003, y≈0.99997px |
| 100% | 1 | `translateY(0)` | 1200ms 후 `finished`, opacity 1, y=0 |

- **도출**: 전체 시간은 선형이지만 첫 300ms에 fade의 90%와 이동의 11/12(약 91.7%)가 끝납니다. 남은 900ms는 opacity 0.9→1과 마지막 1px만 천천히 정리하므로 빠르게 나타난 뒤 자리를 잡는 인상입니다.
- **측정**: `prefers-reduced-motion:reduce`에서는 클릭 직후 `#chip` inline style이 opacity 1, transform none이 되었고 `getAnimations()`와 `document.getAnimations()`는 0개였습니다.
- **측정**: reduced-motion용 CSS 규칙은 `.glow { filter:blur(24px) }`를 같은 값으로 반복하므로 실제 glow는 계속 blur(24px)였습니다. 모션 감소의 실질적인 분기는 JavaScript가 WAAPI 생성을 건너뛰는 부분입니다.

## 옮겨 쓸 수 있는 구현 원리

이 사이트의 시스템은 두 외부 CSS의 후순위 의미 토큰, 8px 기반 간격, 한 개의 600px breakpoint, 일반 문서 내비게이션과 짧은 인라인 동작으로 구성됩니다. 대표 빛 효과를 재사용하려면 격리·클리핑된 어두운 프레임 안에 프레임보다 30px씩 큰 방사광을 놓고 24px blur를 준 다음, 그 위를 8px backdrop blur와 4% 흰색 막으로 덮는 레이어 순서를 유지해야 합니다. 모션은 1.2초 전체 값보다 “첫 25%에 변화의 약 90%를 끝내는” keyframe 배분과 reduced-motion에서 animation 객체 자체를 만들지 않는 분기가 핵심입니다.

그대로 복사해도 유지되지 않는 부분은 플랫폼별 `system-ui` 글꼴의 실제 글리프, 브라우저별 backdrop-filter 렌더링, 보지 않은 중간 viewport와 다른 브라우저/DPR에서의 픽셀 결과입니다. 원본 저장소와 빌드 구성은 범위상 읽지 않았으므로 런타임에 남지 않은 작성 도구나 전처리기는 확인할 수 없습니다.
