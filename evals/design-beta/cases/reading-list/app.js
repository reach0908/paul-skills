const list = document.querySelector('#articles');
const count = document.querySelector('#count');
const message = document.querySelector('#message');
const input = document.querySelector('#url');
function syncCount() {
  count.textContent = `${list.children.length}개`;
  document.querySelector('#empty').hidden = list.children.length > 0;
}
list.addEventListener('click', event => {
  const button = event.target.closest('.remove');
  if (!button) return;
  button.closest('li').remove();
  syncCount();
});
document.querySelector('#save').addEventListener('click', () => {
  message.className = '';
  message.textContent = '저장 중…';
  const value = input.value.trim();
  window.setTimeout(() => {
    if (!value.startsWith('https://') || value.includes('fail')) {
      message.textContent = '문제가 발생했어요.';
      return;
    }
    const item = document.createElement('li');
    item.className = 'article';
    const text = document.createElement('div');
    const title = document.createElement('h3');
    title.textContent = '방금 저장한 글';
    const source = document.createElement('p');
    source.textContent = value;
    text.append(title, source);
    const button = document.createElement('button');
    button.className = 'remove';
    button.innerHTML = '<span aria-hidden="true">×</span>';
    item.append(text, button);
    list.append(item);
    message.textContent = '글을 저장했어요.';
    message.className = 'success';
    input.value = '';
    syncCount();
  }, 450);
});
