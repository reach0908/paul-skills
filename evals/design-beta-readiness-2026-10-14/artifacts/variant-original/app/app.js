const note = document.querySelector('#note');
const status = document.querySelector('#status');
const save = document.querySelector('#save');
const target = document.querySelector('#target');
const picker = document.querySelector('.variant-picker');
const variantButtons = [...picker.querySelectorAll('[data-variant]')];
const variants = variantButtons.map((button) => button.dataset.variant);
let busy = false;

function variantFromUrl() {
  const requested = new URL(window.location.href).searchParams.get('__variant');
  return variants.includes(requested) ? requested : 'balanced';
}

function applyVariant(variant, { writeUrl = true } = {}) {
  target.dataset.variant = variant;
  variantButtons.forEach((button) => {
    button.setAttribute('aria-pressed', String(button.dataset.variant === variant));
  });

  if (writeUrl) {
    const url = new URL(window.location.href);
    url.searchParams.set('__variant', variant);
    history.replaceState(null, '', url);
  }

  picker.querySelector(`[data-variant="${variant}"]`)?.scrollIntoView({ block: 'nearest', inline: 'nearest' });
}

function eventCameFromEditor(event) {
  const element = event.target;
  return element instanceof Element && Boolean(element.closest('input, textarea, select, [contenteditable="true"]'));
}

variantButtons.forEach((button) => {
  button.addEventListener('click', () => applyVariant(button.dataset.variant));
});

window.addEventListener('keydown', (event) => {
  if (event.defaultPrevented || event.altKey || event.ctrlKey || event.metaKey || event.shiftKey || eventCameFromEditor(event)) return;

  if (event.key.toLowerCase() === 'h') {
    event.preventDefault();
    picker.hidden = !picker.hidden;
    return;
  }

  const currentIndex = variants.indexOf(target.dataset.variant);
  let nextIndex = null;
  if (event.key === 'ArrowLeft') nextIndex = (currentIndex - 1 + variants.length) % variants.length;
  if (event.key === 'ArrowRight') nextIndex = (currentIndex + 1) % variants.length;
  if (/^[1-9]$/.test(event.key)) nextIndex = Number(event.key) - 1;

  if (nextIndex !== null && variants[nextIndex]) {
    event.preventDefault();
    applyVariant(variants[nextIndex]);
  }
});

window.addEventListener('popstate', () => applyVariant(variantFromUrl(), { writeUrl: false }));
applyVariant(variantFromUrl(), { writeUrl: false });

save.onclick = () => {
  if (busy) return;
  busy = true;
  save.disabled = true;
  target.setAttribute('aria-busy', 'true');
  status.textContent = '저장 요청 중';
  setTimeout(() => {
    status.textContent = '저장 완료 S-72';
    document.querySelector('#feedback').textContent = '저장됨';
    busy = false;
    save.disabled = false;
    target.removeAttribute('aria-busy');
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
