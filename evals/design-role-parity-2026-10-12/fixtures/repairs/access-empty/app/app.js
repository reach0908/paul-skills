let accessible = true;
const query = document.querySelector('#query');
const results = document.querySelector('#results');
const empty = document.querySelector('#empty');
const status = document.querySelector('#status');
function render() {
  const matches = 'Studio 회의록'.toLowerCase().includes(query.value.toLowerCase());
  results.hidden = !accessible || !matches;
  empty.hidden = accessible && matches;
}
query.addEventListener('input', render);
document.querySelector('#read').onclick = () => { status.textContent = 'Studio 회의록을 열었어요.'; };
document.querySelector('#membership').onclick = () => { accessible = false; status.textContent = '멤버십 상태를 갱신했어요.'; render(); };
document.querySelector('#help').onclick = () => { document.querySelector('#help-text').hidden = false; };
render();
