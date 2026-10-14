import {renderQueueCard} from '../../queue.js';

const items = [
  {id: 'R-72', title: '작은 팀에서 실패 후 다시 시도하기'},
  {id: 'R-81', title: '주간 운영 회고를 30분 안에 끝내는 법'},
  {id: 'R-94', title: '고객 요청을 우선순위로 바꾸는 기준'},
  {id: 'R-103', title: '담당자가 없을 때 결정을 남기는 방법'},
  {id: 'R-117', title: '작은 장애에서 배운 내용을 공유하기'},
  {id: 'R-126', title: '반복 업무를 점검하는 월간 체크리스트'},
  {id: 'R-131', title: '급한 요청과 중요한 요청을 구분하기'},
  {id: 'R-145', title: '새 팀원이 첫 주에 알아야 할 운영 원칙'},
  {id: 'R-152', title: '회의 없이 진행 상황을 공유하는 문서'},
  {id: 'R-168', title: '의견이 갈린 결정을 기록하는 형식'},
  {id: 'R-179', title: '고객 인터뷰 메모를 함께 읽는 순서'},
  {id: 'R-184', title: '업무 인수인계에서 빠뜨리기 쉬운 항목'},
  {id: 'R-196', title: '운영 지표가 달라졌을 때 확인할 질문'},
  {id: 'R-204', title: '한 달 뒤에도 이해되는 결정 로그 쓰기'},
  {id: 'R-219', title: '긴급 대응이 끝난 뒤 해야 할 세 가지'},
  {id: 'R-227', title: '팀의 집중 시간을 지키는 알림 규칙'},
  {id: 'R-238', title: '도구를 바꾸기 전에 살펴볼 작업 흐름'},
  {id: 'R-249', title: '분기 계획에서 남겨야 할 여유 시간'},
  {id: 'R-255', title: '결정권자 부재 시 안전하게 진행하기'},
  {id: 'R-267', title: '사용자 피드백을 다음 실험으로 연결하기'},
  {id: 'R-278', title: '문제가 반복될 때 원인을 좁히는 기록법'},
  {id: 'R-286', title: '작은 팀의 접근 권한을 정기 점검하기'},
  {id: 'R-298', title: '마감 직전 변경 요청을 다루는 기준'},
  {id: 'R-305', title: '완료된 프로젝트에서 운영 지식 꺼내기'},
];

const states = [
  {id: 'no-access', label: '권한 없음', props: {canEdit: false, items: items.slice(0, 6)}},
  {id: 'loading', label: '불러오는 중', props: {status: 'loading'}},
  {id: 'error', label: '오류', props: {status: 'error'}},
  {id: 'empty', label: '비어 있음', props: {items: []}},
  {id: 'one-item', label: '자료 1개', props: {items: items.slice(0, 1)}},
  {id: 'typical', label: '일반 목록', props: {items: items.slice(0, 6)}},
  {id: 'long-list', label: '긴 목록', props: {items}},
  {id: 'refreshing', label: '새로 확인 중', props: {items: items.slice(0, 6), refreshing: true}},
  {id: 'locked', label: '잠김', props: {items: items.slice(0, 6), locked: true}},
  {id: 'refreshing-locked', label: '확인 중·잠김', props: {items: items.slice(0, 6), refreshing: true, locked: true}},
];

const defaultState = 'typical';
const queue = document.querySelector('#queue');
const switcher = document.querySelector('.state-switcher');

for (const state of states) {
  const button = document.createElement('button');
  button.type = 'button';
  button.dataset.state = state.id;
  button.textContent = state.label;
  button.setAttribute('aria-pressed', 'false');
  button.addEventListener('click', () => selectState(state.id));
  switcher.append(button);
}

function stateFromUrl() {
  const requested = new URL(location.href).searchParams.get('__state');
  return states.find((state) => state.id === requested) ?? states.find((state) => state.id === defaultState);
}

function renderState() {
  const state = stateFromUrl();
  queue.replaceChildren(renderQueueCard(state.props));
  for (const button of switcher.querySelectorAll('button')) {
    button.setAttribute('aria-pressed', String(button.dataset.state === state.id));
  }
  document.title = `${state.label} — 검토 대기 자료 상태 작업대`;
  return state;
}

function selectState(stateId) {
  if (!states.some((state) => state.id === stateId)) return;
  const scrollX = window.scrollX;
  const scrollY = window.scrollY;
  const url = new URL(location.href);
  url.searchParams.set('__state', stateId);
  history.pushState({}, '', url);
  renderState();
  window.scrollTo(scrollX, scrollY);
  switcher.querySelector(`[data-state="${stateId}"]`)?.scrollIntoView({block: 'nearest', inline: 'center'});
}

function isTypingTarget(target) {
  return target instanceof HTMLElement && (
    target.matches('input, textarea, select') ||
    target.isContentEditable ||
    Boolean(target.closest('[contenteditable="true"]'))
  );
}

document.addEventListener('keydown', (event) => {
  if (event.defaultPrevented || event.altKey || event.ctrlKey || event.metaKey || event.shiftKey || isTypingTarget(event.target)) return;

  if (event.key.toLowerCase() === 'h') {
    event.preventDefault();
    switcher.hidden = !switcher.hidden;
    return;
  }

  const currentIndex = states.findIndex((state) => state.id === stateFromUrl().id);
  let nextIndex = null;
  if (event.key === 'ArrowLeft') nextIndex = (currentIndex - 1 + states.length) % states.length;
  if (event.key === 'ArrowRight') nextIndex = (currentIndex + 1) % states.length;
  if (/^[1-9]$/.test(event.key)) nextIndex = Number(event.key) - 1;
  if (nextIndex === null || !states[nextIndex]) return;

  event.preventDefault();
  selectState(states[nextIndex].id);
});

window.addEventListener('popstate', renderState);

const initialState = stateFromUrl();
const initialUrl = new URL(location.href);
if (initialUrl.searchParams.get('__state') !== initialState.id) {
  initialUrl.searchParams.set('__state', initialState.id);
  history.replaceState({}, '', initialUrl);
}
renderState();
