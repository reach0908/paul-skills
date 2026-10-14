const note = document.querySelector('#note');
const status = document.querySelector('#status');
const save = document.querySelector('#save');
const target = document.querySelector('#target');
const picker = document.querySelector('.variant-picker');
const variantButtons = [...picker.querySelectorAll('[data-variant]')];
const variants = variantButtons.map((button) => button.dataset.variant);
let busy = false;

const setVariant = (variant, { updateUrl = true } = {}) => {
  const nextVariant = variants.includes(variant) ? variant : 'balanced';
  target.dataset.variant = nextVariant;

  variantButtons.forEach((button) => {
    const active = button.dataset.variant === nextVariant;
    button.setAttribute('aria-pressed', String(active));
    if (active) {
      const buttonLeft = button.offsetLeft;
      const buttonRight = buttonLeft + button.offsetWidth;
      const visibleLeft = picker.scrollLeft;
      const visibleRight = visibleLeft + picker.clientWidth;

      if (buttonLeft < visibleLeft) picker.scrollLeft = buttonLeft;
      if (buttonRight > visibleRight) picker.scrollLeft = buttonRight - picker.clientWidth;
    }
  });

  if (updateUrl) {
    const url = new URL(window.location.href);
    url.searchParams.set('__variant', nextVariant);
    history.pushState({ variant: nextVariant }, '', url);
  }
};

const initialVariant = new URL(window.location.href).searchParams.get('__variant');
setVariant(initialVariant, { updateUrl: !variants.includes(initialVariant) });

variantButtons.forEach((button) => {
  button.addEventListener('click', () => setVariant(button.dataset.variant));
});

window.addEventListener('popstate', () => {
  const variant = new URL(window.location.href).searchParams.get('__variant');
  setVariant(variant, { updateUrl: false });
});

window.addEventListener('keydown', (event) => {
  const source = event.target;
  if (
    event.defaultPrevented ||
    event.altKey || event.ctrlKey || event.metaKey || event.shiftKey ||
    source.matches('input, textarea, select, [contenteditable="true"]')
  ) return;

  if (event.key.toLowerCase() === 'h') {
    picker.hidden = !picker.hidden;
    return;
  }

  const number = Number(event.key);
  if (Number.isInteger(number) && number > 0 && number <= variants.length) {
    setVariant(variants[number - 1]);
    return;
  }

  if (event.key !== 'ArrowLeft' && event.key !== 'ArrowRight') return;
  event.preventDefault();
  const activeIndex = variants.indexOf(target.dataset.variant);
  const direction = event.key === 'ArrowRight' ? 1 : -1;
  const nextIndex = (activeIndex + direction + variants.length) % variants.length;
  setVariant(variants[nextIndex]);
});

save.onclick = () => {
  if (busy) return;
  busy = true;
  save.disabled = true;
  status.textContent = '저장 요청 중';
  setTimeout(() => {
    status.textContent = '저장 완료 S-72';
    document.querySelector('#feedback').textContent = '저장됨';
    busy = false;
    save.disabled = false;
  }, 1000);
};

document.querySelector('#clear').onclick = () => {
  note.value = '';
  status.textContent = '메모를 비웠습니다';
};

document.querySelector('#error').onclick = () => {
  status.textContent = '저장하지 못했습니다. 다시 시도해 주세요.';
};

document.querySelector('#empty').onclick = () => {
  document.querySelector('#feedback').textContent = '검색 결과가 없습니다. 검색어를 바꿔 주세요.';
};
