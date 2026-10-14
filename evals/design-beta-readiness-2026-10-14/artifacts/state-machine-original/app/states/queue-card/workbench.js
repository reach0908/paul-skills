import { renderQueueCard } from '../../queue.js';

const queueItems = [
  { id: 'R-72', title: '작은 팀에서 실패 후 다시 시도하기' },
  { id: 'R-81', title: '주간 운영 회고를 짧게 끝내는 법' },
  { id: 'R-94', title: '고객 요청의 우선순위를 합의하는 기준' },
  { id: 'R-103', title: '담당자가 바뀌어도 이어지는 인수인계' },
  { id: 'R-118', title: '반복되는 장애에서 학습을 남기는 방법' },
  { id: 'R-127', title: '결정이 늦어질 때 기록해야 할 세 가지' },
  { id: 'R-139', title: '작은 실험의 성공 조건을 정하는 법' },
  { id: 'R-146', title: '팀의 읽기 목록을 가볍게 관리하기' },
];

const longQueueItems = [
  ...queueItems,
  { id: 'R-155', title: '회의 없는 날을 운영하는 팀의 규칙' },
  { id: 'R-162', title: '지원 요청에서 공통 문제를 발견하기' },
  { id: 'R-171', title: '불확실한 일정에 범위를 맞추는 방법' },
  { id: 'R-184', title: '원격 팀의 의사결정 속도를 높이는 기록' },
  { id: 'R-193', title: '새 동료가 첫 주에 알아야 할 운영 원칙' },
  { id: 'R-207', title: '업무가 몰릴 때 중단할 일을 고르는 법' },
  { id: 'R-219', title: '실패한 자동화에서 배운 점 정리하기' },
  { id: 'R-228', title: '분기 목표를 주간 행동으로 연결하기' },
  { id: 'R-236', title: '고객 인터뷰 메모를 팀 자산으로 만들기' },
  { id: 'R-249', title: '운영 지표가 행동을 바꾸는 순간' },
];

const states = [
  { id: 'no-access', label: 'No access', props: { canEdit: false, items: queueItems } },
  { id: 'loading', label: 'Loading', props: { status: 'loading' } },
  { id: 'error', label: 'Error', props: { status: 'error' } },
  { id: 'empty', label: 'Empty', props: { items: [] } },
  { id: 'one-item', label: 'One item', props: { items: queueItems.slice(0, 1) } },
  { id: 'ready', label: 'Ready', props: { items: queueItems } },
  { id: 'long-list', label: 'Long list', props: { items: longQueueItems } },
  { id: 'refreshing', label: 'Refreshing', props: { items: queueItems, refreshing: true } },
  { id: 'locked', label: 'Locked', props: { items: queueItems, locked: true } },
];

const queue = document.querySelector('#queue');
const switcher = document.querySelector('.state-switcher');

function stateFromUrl() {
  const requested = new URL(window.location.href).searchParams.get('__state');
  return states.find((state) => state.id === requested) ?? states[0];
}

function render() {
  const active = stateFromUrl();
  queue.replaceChildren(renderQueueCard({
    ...active.props,
    onRetry: () => console.info('queue-card:onRetry'),
    onSelect: (id) => console.info('queue-card:onSelect', id),
  }));

  for (const button of switcher.querySelectorAll('button')) {
    button.setAttribute('aria-pressed', String(button.dataset.state === active.id));
  }
}

function selectState(id, { focus = false } = {}) {
  const url = new URL(window.location.href);
  url.searchParams.set('__state', id);
  history.pushState({}, '', url);
  render();

  const activeButton = switcher.querySelector(`[data-state="${id}"]`);
  if (focus) {
    activeButton.focus({ preventScroll: true });
    activeButton.scrollIntoView({ behavior: 'instant', block: 'nearest', inline: 'nearest' });
    const switcherBounds = switcher.getBoundingClientRect();
    const activeBounds = activeButton.getBoundingClientRect();
    if (activeBounds.left < switcherBounds.left) {
      switcher.scrollLeft -= Math.ceil(switcherBounds.left - activeBounds.left);
    }
    if (activeBounds.right > switcherBounds.right) {
      switcher.scrollLeft += Math.ceil(activeBounds.right - switcherBounds.right);
    }
  }
}

for (const state of states) {
  const button = document.createElement('button');
  button.type = 'button';
  button.dataset.state = state.id;
  button.textContent = state.label;
  button.setAttribute('aria-pressed', 'false');
  button.addEventListener('click', () => selectState(state.id));
  switcher.append(button);
}

window.addEventListener('popstate', render);
window.addEventListener('keydown', (event) => {
  if (event.defaultPrevented || event.altKey || event.ctrlKey || event.metaKey || event.shiftKey) return;

  const target = event.target;
  if (target instanceof HTMLElement && (
    target.matches('input, textarea, select') || target.isContentEditable
  )) return;

  if (event.key.toLowerCase() === 'h') {
    event.preventDefault();
    switcher.hidden = !switcher.hidden;
    return;
  }

  const activeIndex = states.findIndex((state) => state.id === stateFromUrl().id);
  let nextIndex = null;
  if (event.key === 'ArrowLeft') nextIndex = (activeIndex - 1 + states.length) % states.length;
  if (event.key === 'ArrowRight') nextIndex = (activeIndex + 1) % states.length;
  if (/^[1-9]$/.test(event.key)) nextIndex = Number(event.key) - 1;

  if (nextIndex !== null && states[nextIndex]) {
    event.preventDefault();
    selectState(states[nextIndex].id, { focus: true });
  }
});

render();
