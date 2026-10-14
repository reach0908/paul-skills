(function () {
  'use strict';

  const STORAGE_KEY = 'pb72-r72-save-v1';
  const main = document.querySelector('main');
  let timeoutHandle = null;
  let statusPanelOpen = true;
  let listScrollY = 0;

  const defaultState = () => ({
    draft: '',
    status: 'idle',
    checks: 0,
    requestId: '',
    receipt: ''
  });

  function readState() {
    try {
      const saved = JSON.parse(localStorage.getItem(STORAGE_KEY));
      return Object.assign(defaultState(), saved || {});
    } catch (_error) {
      return defaultState();
    }
  }

  function writeState(state) {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
  }

  function currentView() {
    return new URL(location.href).searchParams.get('view') === 'library' ? 'library' : 'detail';
  }

  function routeUrl(view) {
    const url = new URL(location.href);
    url.search = '';
    url.hash = '';
    url.searchParams.set('view', view);
    url.searchParams.set('q', '작은 팀');
    url.searchParams.set('tag', '운영');
    url.searchParams.set('sort', 'newest');
    return url.pathname + url.search;
  }

  function navigate(view, push) {
    if (currentView() === 'library') listScrollY = window.scrollY;
    if (push) history.pushState({ view, listScrollY }, '', routeUrl(view));
    render();
  }

  function render() {
    const view = currentView();
    const template = document.querySelector(view === 'library' ? '#library-template' : '#detail-template');
    main.replaceChildren(template.content.cloneNode(true));
    main.dataset.view = view;
    document.title = view === 'library' ? '자료함 — 공유 자료함' : '작은 팀에서 실패 후 다시 시도하기 — 공유 자료함';

    bindCommonControls();
    if (view === 'detail') bindDetail();
    else bindLibrary();
  }

  function bindCommonControls() {
    document.querySelectorAll('[data-route]').forEach((link) => {
      link.addEventListener('click', (event) => {
        event.preventDefault();
        navigate(link.dataset.route, true);
      });
    });

    document.querySelectorAll('[data-jump]').forEach((link) => {
      link.addEventListener('click', (event) => {
        const target = document.getElementById(link.dataset.jump);
        if (!target) return;
        event.preventDefault();
        target.scrollIntoView({ block: 'start' });
        target.focus({ preventScroll: true });
      });
    });
  }

  function bindDetail() {
    const note = document.querySelector('#save-note');
    note.value = readState().draft;
    note.addEventListener('input', () => {
      const state = readState();
      state.draft = note.value;
      writeState(state);
      document.querySelector('#draft-hint').textContent = '메모 초안을 이 브라우저에 유지했습니다.';
    });

    document.querySelector('#save-button').addEventListener('click', beginSave);
    document.querySelector('#check-status-button').addEventListener('click', checkStatus);
    document.querySelector('#close-status-button').addEventListener('click', closeStatus);
    document.querySelector('#open-status-button').addEventListener('click', () => {
      statusPanelOpen = true;
      updateSaveUI(true);
      document.querySelector('#status-title').focus();
    });
    document.querySelector('#reset-button').addEventListener('click', resetScenario);
    updateSaveUI(false);
  }

  function beginSave() {
    const state = readState();
    if (state.status !== 'idle') {
      updateSaveUI(true);
      return;
    }
    state.status = 'pending';
    state.checks = 0;
    state.requestId = 'SAVE-R72-1';
    state.receipt = '';
    writeState(state);
    statusPanelOpen = true;
    updateSaveUI(true);

    clearTimeout(timeoutHandle);
    timeoutHandle = window.setTimeout(() => {
      const latest = readState();
      if (latest.status !== 'pending' || latest.checks !== 0) return;
      latest.status = 'unknown';
      writeState(latest);
      updateSaveUI(false);
    }, 1200);
  }

  function checkStatus() {
    const state = readState();
    if (state.status !== 'unknown' && state.status !== 'pending') return;

    if (state.checks === 0) {
      state.checks = 1;
      state.status = 'unknown';
    } else {
      state.checks = 2;
      state.status = 'succeeded';
      state.receipt = 'S-72';
    }
    writeState(state);
    statusPanelOpen = true;
    updateSaveUI(true);
  }

  function closeStatus() {
    statusPanelOpen = false;
    updateSaveUI(false);
    document.querySelector('#open-status-button').focus();
  }

  function resetScenario() {
    clearTimeout(timeoutHandle);
    localStorage.removeItem(STORAGE_KEY);
    statusPanelOpen = true;
    const note = document.querySelector('#save-note');
    note.value = '';
    updateSaveUI(false);
    note.focus();
  }

  function updateSaveUI(announce) {
    const state = readState();
    const badge = document.querySelector('#save-badge');
    if (!badge) return;
    const saveButton = document.querySelector('#save-button');
    const openButton = document.querySelector('#open-status-button');
    const duplicateNote = document.querySelector('#duplicate-note');
    const panel = document.querySelector('#status-panel');
    const message = document.querySelector('#status-message');
    const requestId = document.querySelector('#request-id');
    const receiptRow = document.querySelector('#receipt-row');
    const receiptId = document.querySelector('#receipt-id');
    const checkButton = document.querySelector('#check-status-button');

    const locked = state.status !== 'idle';
    saveButton.disabled = locked;
    saveButton.textContent = state.status === 'succeeded' ? '저장 확인됨' : locked ? '저장 요청 전송됨' : '메모와 함께 저장';
    duplicateNote.hidden = !locked;
    requestId.textContent = state.requestId || '아직 없음';
    receiptRow.hidden = state.status !== 'succeeded';
    receiptId.textContent = state.receipt || '—';

    if (state.status === 'idle') {
      badge.textContent = '저장 전';
      message.innerHTML = '<strong>저장 전입니다.</strong><p>메모를 적고 저장 요청을 시작하세요.</p>';
      checkButton.hidden = true;
    } else if (state.status === 'pending') {
      badge.textContent = '전송 중';
      message.innerHTML = '<strong>저장 요청을 보내고 있습니다.</strong><p>같은 요청을 다시 보내지 마세요. 닫아도 서버 작업은 취소되지 않습니다.</p>';
      checkButton.hidden = true;
    } else if (state.status === 'unknown' && state.checks === 0) {
      badge.textContent = '확인 필요';
      message.innerHTML = '<strong>응답 시간이 초과되어 결과를 알 수 없습니다.</strong><p>실패나 성공으로 단정하지 않습니다. 새로 저장하지 말고 기존 요청의 상태를 확인하세요.</p>';
      checkButton.hidden = false;
      checkButton.textContent = '상태 확인';
    } else if (state.status === 'unknown') {
      badge.textContent = '처리 중';
      message.innerHTML = '<strong>첫 확인 결과: 아직 처리 중입니다.</strong><p>동일한 요청을 다시 확인할 수 있습니다. 새 저장 요청은 보내지 않습니다.</p>';
      checkButton.hidden = false;
      checkButton.textContent = '다시 상태 확인';
    } else {
      badge.textContent = '저장됨';
      message.innerHTML = '<strong>저장을 확인했습니다.</strong><p>내 보관함에 자료와 메모가 있습니다. 유일한 영수증은 S-72입니다.</p>';
      checkButton.hidden = true;
    }

    panel.hidden = state.status === 'idle' || !statusPanelOpen;
    openButton.hidden = state.status === 'idle' || statusPanelOpen;
    if (announce && !panel.hidden) message.setAttribute('aria-live', 'assertive');
  }

  function bindLibrary() {
    const form = document.querySelector('#library-filters');
    form.addEventListener('submit', (event) => {
      event.preventDefault();
      document.querySelector('.results-summary').textContent = '‘작은 팀’ · ‘운영’ · 최신순 결과 3개 — 목록 문맥을 유지했습니다.';
    });

    const target = document.querySelector('#list-item-r72');
    requestAnimationFrame(() => {
      window.scrollTo(0, listScrollY || Math.max(0, target.offsetTop - 180));
    });
  }

  document.querySelector('#quick-search').addEventListener('submit', (event) => {
    event.preventDefault();
    navigate('library', true);
  });

  window.addEventListener('popstate', () => render());
  render();
})();
