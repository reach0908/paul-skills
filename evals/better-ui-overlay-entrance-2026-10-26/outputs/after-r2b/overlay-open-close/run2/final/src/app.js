const accountButton = document.getElementById('account-button');
const menu = document.getElementById('account-menu');

accountButton.addEventListener('click', () => {
  const open = menu.hidden;
  menu.hidden = !open;
  accountButton.setAttribute('aria-expanded', String(open));
});

document.addEventListener('click', (event) => {
  if (!menu.hidden && !event.target.closest('.account')) {
    menu.hidden = true;
    accountButton.setAttribute('aria-expanded', 'false');
  }
});

const toast = document.getElementById('toast');
let toastTimer;
document.getElementById('save-button').addEventListener('click', () => {
  toast.hidden = false;
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => { toast.hidden = true; }, 3000);
});

const modal = document.getElementById('delete-modal');
document.getElementById('delete-button').addEventListener('click', () => modal.classList.add('is-open'));
document.getElementById('cancel-delete').addEventListener('click', () => modal.classList.remove('is-open'));
