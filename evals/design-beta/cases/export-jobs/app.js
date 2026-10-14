const message = document.querySelector('#message');
const input = document.querySelector('#name');
let count = 2;
let busy = false;
function start() {
  if (busy) return;
  busy = true;
  message.textContent = '내보내는 중...';
  const value = input.value;
  setTimeout(() => {
    busy = false;
    if (!value.trim() || value.includes('fail')) {
      message.textContent = '오류가 발생했어요.';
      return;
    }
    count += 1;
    document.querySelector('#count').textContent = `${count}개`;
    message.textContent = `${value} 내보내기를 완료했어요.`;
  }, 450);
}
document.querySelector('#create').addEventListener('click', start);
document.querySelector('#locked').addEventListener('click', start);
document.querySelectorAll('.download').forEach(button => button.addEventListener('click', () => {
  message.textContent = '로컬 예제에서는 파일을 내려받지 않습니다.';
}));
