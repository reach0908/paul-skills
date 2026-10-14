`filter: blur(8px)`는 해당 요소와 그 안의 텍스트·이미지 등 렌더링 결과 전체를 흐리게 하지만, 요소 뒤의 배경에는 영향을 주지 않습니다. 반면 `backdrop-filter: blur(8px)`는 요소 뒤로 비치는 배경만 흐리게 하므로 요소 안의 텍스트는 선명하게 유지됩니다. 효과가 보이도록 보통 요소 배경을 투명하거나 반투명하게 설정합니다.

```html
<div class="scene">
  <div class="card filter">이 글자까지 흐려집니다</div>
  <div class="card backdrop">이 글자는 선명합니다</div>
</div>

<style>
  .scene { background: url("background.jpg") center / cover; }
  .card { padding: 20px; background: rgb(255 255 255 / 30%); }
  .filter { filter: blur(8px); }
  .backdrop { backdrop-filter: blur(8px); }
</style>
```

결과는 [ANSWER.md](/private/tmp/paul-beta-hardening-20261014/public/runs/negative-explain-interface/ANSWER.md)에 저장했습니다. 요청에 따라 브라우저 렌더링 검증은 하지 않았으며, 예시의 `background.jpg`는 설명용 경로입니다.