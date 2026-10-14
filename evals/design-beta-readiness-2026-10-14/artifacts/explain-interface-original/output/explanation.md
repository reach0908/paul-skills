# 두 페이지 사이트 구현 설명

## 조사 범위와 근거 등급

대상은 다음 두 문서다.

- `http://127.0.0.1:48914/runs/explain-interface-original/app/index.html`
- `http://127.0.0.1:48914/runs/explain-interface-original/app/detail.html`

브라우저가 받은 문서·스타일 응답과 실제 렌더링의 계산 스타일을 함께 읽었다. 소스 저장소 파일은 직접 열지 않았다. 아래 표기는 다음 의미다.

- **[측정]** 브라우저 DOM, 네트워크 응답, CSSOM 또는 계산 스타일에서 직접 확인했다.
- **[도출]** 여러 측정값을 계산하거나 서로 대조해 얻었다.
- **[추정]** 구현 의도를 해석한 것이며 작성 당시의 원본 도구나 라이브러리를 단정하지 않는다.

## 전체 구조와 렌더링 방식

- **[측정]** 두 URL은 각각 완성된 HTML 문서를 반환한다. 페이지 간 이동은 `index.html`과 `detail.html`을 가리키는 일반 `<a>` 링크이며, 각 문서에는 짧은 인라인 스크립트만 있다.
- **[측정]** 로드된 하위 리소스는 동일 출처의 `app/style.css`와 교차 출처의 `http://localhost:48914/shared.css` 두 스타일시트뿐이었다. 외부 JavaScript 번들, 이미지, 웹폰트 요청은 두 페이지의 관찰 상태에서 나타나지 않았다.
- **[측정]** DOM/리소스 지문 검사에서 Next, Nuxt, Remix, Gatsby, Astro, Svelte, Angular, React fiber, Tailwind, CSS Modules, styled-components, Emotion의 지문이 발견되지 않았다. 이는 해당 기술의 보편적인 부재 증명이 아니라, 방문한 두 문서에서 지문이 발화하지 않았다는 뜻이다.
- **[도출]** 배포된 프런트엔드는 정적 다중 페이지 구조다. 문서가 마크업을 직접 제공하고, 브라우저의 `querySelector(...).onclick`으로 테마와 재생 동작만 덧붙인다. 별도 hydration이나 클라이언트 라우터는 관찰되지 않았다.
- **[추정]** 클래스 이름이 `.site-grid`, `.frame`, `.glow`, `.glass`처럼 의미 중심이고 CSS가 작은 규칙 집합으로 제공되므로, 배포 결과는 손으로 작성한 작은 CSS/DOM 시스템에 가깝다. 다만 배포 전 작성 도구나 빌드 과정은 이 결과물만으로 식별할 수 없다.

## CSS 출처와 cascade

- **[측정]** `app/style.css`는 CSSOM에서 17개 규칙으로 읽혔다. 이 파일은 전역 box sizing, 기본 글꼴과 행간, 공통 토큰, 컨테이너, 버튼·폼·카드·도구 모음·알림·링크·제목 규칙을 제공한다.
- **[측정]** index 문서의 인라인 `<style>`에는 7개 규칙이 있으며 빛 효과와 칩을 담당한다. detail 문서에는 이 인라인 효과 스타일이 없다.
- **[측정]** `shared.css`는 페이지의 `127.0.0.1`과 다른 호스트명인 `localhost`에서 제공되어 `CSSStyleSheet.cssRules` 접근이 예외를 냈다. 브라우저 네트워크 응답 본문은 읽을 수 있었고, 그 안에서 루트 테마 토큰, `main`, `h1`, `.site-grid`, `@media(max-width:600px)` 규칙을 확인했다.
- **[측정]** 스타일 적용 순서는 동일 출처 기본 CSS, index의 인라인 효과 CSS(해당 문서만), 교차 출처 공유 CSS다. 실제 계산값에서 공유 CSS의 `main` 패딩 24px과 body 배경 토큰이 앞선 기본값을 덮었다.
- **[도출]** 따라서 `shared.css`의 authored 선언은 네트워크 응답에서 확인한 값이고, 실제 승리 여부는 각 상태의 computed style로 별도 확인했다. CSSOM에서 breakpoint 목록이 비어 보이는 것은 규칙 부재가 아니라 교차 출처 접근 제한 때문이다.

## 토큰, 색과 테마

### 토큰 계층

- **[측정]** 기본 CSS의 간격 primitive는 `--space-1: 8px`, `--space-2: 16px`, `--space-3: 24px`, `--space-4: 32px`다. 공통 radius는 `--radius: 8px`, 기본 제목/본문 토큰은 `--type-title: 1.5rem`, `--type-body: 1rem`이다.
- **[측정]** 공유 CSS는 반응형 역할 토큰 `--site-space`와 `--site-type`을 추가한다. 데스크톱에서는 24px과 1.5rem, 600px 이하에서는 16px과 1.25rem이다.
- **[도출]** `--space-*`는 고정 primitive이고 `--site-*`는 viewport에 따라 바뀌는 사용 맥락 토큰이다. 실제 `main` 패딩과 grid gap, `h1` 크기는 후자를 사용한다.

### 밝은/어두운 색

- **[측정]** 밝은 상태의 semantic 토큰은 `--surface: #ffffff`, `--ink: #17212b`, `--brand: #174b82`, `--border: #60758c`다. 계산값은 body가 흰색 배경/`rgb(23,33,43)` 텍스트, 링크가 `rgb(23,75,130)`이었다.
- **[측정]** 테마 버튼은 `<html data-theme="dark">`를 토글한다. 어두운 상태는 `--surface: #17212b`, `--ink: #f3f5f7`, `--brand: #8dbbfa`로 세 토큰만 재정의하고 border는 그대로 둔다. body와 버튼은 어두운 surface/밝은 ink를, 링크는 밝은 brand를 실제로 사용했다.
- **[측정]** 운영체제 색상 선호만 dark로 에뮬레이션하고 `data-theme`을 두지 않았을 때도 `--surface`는 `#ffffff`이고 body는 흰색이었다. 색 테마에는 `prefers-color-scheme` 경로가 없다.
- **[도출]** 테마 상태는 문서 속성 한 개로 전달되며 두 페이지가 같은 공유 토큰 규칙을 재사용한다. 스크립트는 저장소를 쓰지 않으므로 새 문서에 들어오면 속성 없는 밝은 초기 상태로 돌아간다.
- **[측정]** 빛 효과의 색은 테마 토큰 밖에 고정되어 있다: frame `#14243a`, glow `#dd4cd8`의 약 53.3% 알파, glass 흰색 4% 알파, chip `#163e70`, frame 글자는 흰색이다. 따라서 이 효과 자체는 밝은/어두운 테마에서 동일하게 보이고 주변 페이지 표면만 바뀐다.

## 글꼴과 타입 시스템

- **[측정]** 문서 기본은 `font: 100%/1.6 system-ui`다. 로드된 `FontFace`는 0개였고, 별도 폰트 파일 요청도 없었다. 버튼은 `font: inherit`로 같은 스택을 쓴다.
- **[측정]** 본문·링크·버튼은 16px, weight 400, line-height 25.6px, letter-spacing `normal`이다. 데스크톱 `h1`은 24px, weight 700, line-height 38.4px이며 모바일은 20px, weight 700, line-height 32px다.
- **[도출]** 본문 대비 제목 비율은 데스크톱 1.5배, 모바일 1.25배다. 별도의 다단계 type scale보다 본문/제목 두 단계가 반응형 토큰으로 구성된 형태다.
- **[측정]** `--type-body: 1rem`은 선언되어 있지만 가져온 CSS 안에서 실제 속성 참조는 보이지 않았고, 본문 크기는 `html`의 100%에서 상속된다.

## 레이아웃, 간격, 표면

- **[측정]** 1280×900에서 `main`은 border-box 960px, 좌우 여백 160px, 내부 패딩 24px다. 실사용 content 폭은 912px다.
- **[측정]** index의 데스크톱 grid는 `2fr 1fr`, 계산 열 폭 592px/296px, gap 24px다. 오른쪽 frame은 296×300px이며 내부 패딩은 32px다.
- **[도출]** 912px content에서 24px gap을 제외한 888px을 2:1로 나눈 결과가 592px/296px이다.
- **[측정]** 390×844에서는 `main`이 390px 전체 폭과 16px 패딩을 사용해 content 폭이 358px이 된다. index grid는 358px 단일 열, gap 16px으로 바뀌고 frame은 358×300px이다. 가로 스크롤은 없었다.
- **[측정]** fetched 공유 CSS의 유일한 폭 breakpoint는 `@media(max-width:600px)`다. 1280px과 390px에서 각각 위 계산값이 적용되어 해당 분기를 실제로 확인했다.
- **[측정]** 버튼은 8px/16px 패딩, 1px solid `--border`, 8px radius를 사용한다. index에서는 두 버튼과 chip까지 8px radius가 3회, detail에서는 버튼에 1회 계산되었다. 관찰된 요소에는 box-shadow가 없었다.
- **[측정]** 기본 CSS에는 현재 두 DOM에서 인스턴스화되지 않은 `.card`, `.items`, `.tools`, `.notice`, form control 및 disabled 버튼 규칙도 있다. 이는 작성된 공통 표면 어휘이지만, 이번 두 페이지에서는 실제 렌더 상태를 확인할 대상이 없었다.
- **[측정]** 키보드 Tab으로 처음 링크에 진입했을 때 `#b13f00` 3px solid outline과 3px offset이 계산되었다.

## index의 빛 효과: paint 순서와 역할

1. **[측정] frame 바탕** — `.frame`이 `position: relative`, `isolation: isolate`, `overflow: hidden`, `min-height: 300px`, 배경 `#14243a`, 패딩 32px을 만든다. 음수 z-index 장식을 frame 내부 stacking context에 가두고 흐린 가장자리를 잘라내는 경계다.
2. **[측정] glow** — `.glow`는 absolute, inset -30px, z-index -2다. `circle at 35% 45%`의 radial gradient가 `rgba(221,76,216,.533)`에서 65% 지점의 투명색으로 사라지고, 전체에 `filter: blur(24px)`가 적용된다.
3. **[도출] overscan** — glow가 frame보다 사방 30px씩 커서 blur 커널의 단단한 외곽이 frame 안쪽에 들어오지 않는다. frame의 clipping과 결합되어 왼쪽 중앙의 넓고 부드러운 보랏빛 장을 만든다.
4. **[측정] glass** — `.glass`는 frame과 같은 면적(inset 0), z-index -1, 흰색 4% 배경과 `backdrop-filter: blur(8px)`을 쓴다. glow 위에 얇은 백색 막을 얹고 뒤의 gradient를 한 번 더 확산한다.
5. **[측정] 콘텐츠** — 일반 흐름의 문구와 버튼은 두 장식층 위에 그려진다. chip은 inline-block, `#163e70` 배경, 8px/16px 패딩, 8px radius다.
- **[측정]** 모든 요소의 `::before`/`::after`를 확인했지만 이 효과에 관여하는 pseudo-element는 없었다. canvas나 이미지도 없다.
- **[추정]** 이 효과의 핵심은 gradient 하나보다 `oversized radial gradient → 24px blur → 4% glass → 8px backdrop blur`의 누적이다. 복사할 때는 네 층의 순서와 frame clipping이 먼저이고, 색상만 옮기면 같은 깊이가 나오지 않는다.

## 모션과 상태 처리

- **[측정]** 정지 상태에서 CSS transition은 없었고 `document.getAnimations()`도 0개였다. 재생은 CSS animation이 아니라 버튼 핸들러의 Web Animations API 호출이다.
- **[측정]** 재생 시 기존 chip animation을 모두 cancel한 뒤 1개의 `Animation`을 만든다. duration 1200ms, easing `linear`, fill `both`, 1 iteration이다.
- **[측정]** 키프레임은 시작 `opacity:0; translateY(12px)`, 25% `opacity:.9; translateY(1px)`, 끝 `opacity:1; translateY(0)`이다. 시작 직후 런타임에서도 opacity 0과 12px 이동이 계산되었다.
- **[도출]** 첫 300ms에 opacity 변화의 90%와 이동량 12px 중 11px이 끝난다. 남은 900ms에는 opacity 10%와 마지막 1px만 진행된다. 선형 구간 두 개를 사용해 빠르게 등장하고 길게 안착하는 패턴이다.
- **[측정]** `prefers-reduced-motion: reduce`에서 재생하면 기존 animation을 cancel하고 chip에 `opacity:1; transform:none`을 인라인으로 설정한다. 확인 시 animation 수는 0이었다.
- **[측정]** CSS의 reduced-motion media rule은 `.glow`의 `blur(24px)`을 같은 값으로 다시 선언한다. 따라서 감소 설정이 빛의 정적 외형을 바꾸지는 않고, 실제 감소 처리는 JavaScript의 chip 재생 경로가 맡는다.

## 관찰 상태와 캡처

| 페이지 | viewport | 테마 | 실제 확인 | 캡처 |
| --- | --- | --- | --- | --- |
| index | 1280×900 | 밝음 | 2열, 24px site 간격, 24px 제목 | [index-1280x900-light.png](captures/index-1280x900-light.png) |
| index | 1280×900 | 어두움 | 동일 레이아웃, dark semantic 토큰 | [index-1280x900-dark.png](captures/index-1280x900-dark.png) |
| index | 390×844 | 밝음 | 단일 열, 16px site 간격, 20px 제목 | [index-390x844-light.png](captures/index-390x844-light.png) |
| index | 390×844 | 어두움 | 동일 모바일 레이아웃, dark semantic 토큰 | [index-390x844-dark.png](captures/index-390x844-dark.png) |
| detail | 1280×900 | 밝음 | 960px main, 24px 패딩 | [detail-1280x900-light.png](captures/detail-1280x900-light.png) |
| detail | 1280×900 | 어두움 | 동일 레이아웃, dark semantic 토큰 | [detail-1280x900-dark.png](captures/detail-1280x900-dark.png) |
| detail | 390×844 | 밝음 | 16px main 패딩, 20px 제목 | [detail-390x844-light.png](captures/detail-390x844-light.png) |
| detail | 390×844 | 어두움 | 동일 모바일 레이아웃, dark semantic 토큰 | [detail-390x844-dark.png](captures/detail-390x844-dark.png) |

추가로 index의 일반 모션/감소 모션 재생 경로, detail의 첫 Tab focus-visible 상태, 운영체제 dark 선호만 켠 상태를 런타임 계산값으로 확인했다.

## 한계와 옮길 수 있는 구현 레시피

- **[측정 한계]** `shared.css`는 브라우저의 same-origin 제한 때문에 CSSOM 규칙을 직접 순회하지 못했다. 네트워크 응답 본문으로 authored 규칙을 읽고 1280px/390px, 밝음/어두움의 computed style로 적용 결과를 확인했지만, 방문하지 않은 폭·상태의 승리 규칙은 확인하지 않았다.
- **[측정 한계]** 두 URL, 두 viewport, 두 테마, 기본/focus/replay/reduced-motion 상태만 관찰했다. hover, disabled, 미사용 form/card 클래스의 실제 화면은 검증하지 않았다.
- **[추정 한계]** 배포 결과만으로 원본 프레임워크나 빌드 도구가 정말 없었다고 단정할 수 없다. 확인 가능한 결론은 런타임 번들·hydration 지문 없이 정적 HTML/CSS/인라인 JS로 동작했다는 것이다.
- **[도출]** 옮길 수 있는 핵심 레시피는 “고정 최대 폭의 정적 2페이지 셸 + semantic theme 토큰 + 600px 단일 breakpoint + isolated/clipped frame 안의 oversized glow와 glass + 짧게 앞부분이 몰린 WAAPI reveal + reduce 시 즉시 최종 상태”다.
- **[추정]** 그대로 복사해도 보존되지 않는 것은 사용자의 OS별 `system-ui` 실제 글꼴 모양과 viewport에 따라 느껴지는 24px blur의 시각적 규모다. 이 둘은 대상 환경에서 다시 확인해야 한다.
