for (const [group, status, values] of [
  ['location', 'location-status', {garden:'정원 입구에서 받아요.',desk:'안내 데스크에서 받아요.'}],
  ['receipt', 'receipt-status', {short:'간단한 확인서를 보여 줘요.',full:'자세한 확인서를 보여 줘요.'}],
]) {
  document.querySelectorAll('.'+group+' button').forEach(button => button.addEventListener('click', () => {
    document.querySelectorAll('.'+group+' button').forEach(item => item.setAttribute('aria-pressed', String(item === button)));
    document.getElementById(status).textContent = values[button.id];
  }));
}
