import { renderQueueCard } from '../queue.js';

const typicalItem = {
  id: 'R-72',
  title: '작은 팀에서 실패 후 다시 시도하기',
};

const realisticItems = [
  typicalItem,
  { id: 'R-73', title: '운영 회고를 다음 실험으로 연결하는 방법' },
  { id: 'R-74', title: '작은 조직의 의사결정 기록 만들기' },
];

const manyItems = Array.from({ length: 30 }, (_, index) => ({
  id: `R-${100 + index}`,
  title: `${index + 1}번째 검토 자료: 작은 팀의 운영 기록`,
}));

const scenarios = [
  {
    label: '제목 길이 — 빈 문자열',
    finding: '제목이 없는 클릭 가능한 버튼이 작은 빈 테두리로만 표시됩니다.',
    owner: 'better-writing',
    props: { items: [{ id: 'empty-title', title: '' }] },
  },
  {
    label: '제목 길이 — 한 단어',
    props: { items: [{ id: 'one-word', title: '회고' }] },
  },
  {
    label: '제목 길이 — 일반 제목',
    props: { items: [typicalItem] },
  },
  {
    label: '제목 길이 — 여러 문장',
    props: {
      items: [{
        id: 'sentences',
        title: '작은 팀에서 실패한 뒤 무엇을 기록해야 할까요? 다시 시도할 시점을 정하고, 다음 실험의 책임자와 확인 방법을 함께 남깁니다.',
      }],
    },
  },
  {
    label: '제목 길이 — 공백 없는 긴 문자열',
    props: {
      items: [{
        id: 'unbreakable',
        title: 'https://example.com/library/operations/retrospective/retry/decision-record/abcdefghijklmnopqrstuvwxyz0123456789',
      }],
    },
  },
  {
    label: '목록 수량 — 0개',
    props: { items: [] },
  },
  {
    label: '목록 수량 — 1개',
    props: { items: [typicalItem] },
  },
  {
    label: '목록 수량 — 현실적 3개',
    props: { items: realisticItems },
  },
  {
    label: '목록 수량 — 현실적 수량의 10배인 30개',
    props: { items: manyItems },
  },
  {
    label: '컨테이너 — 320px',
    width: '320px',
    props: { items: [typicalItem] },
  },
  {
    label: '상태 — 권한 없음',
    props: { canEdit: false, items: [typicalItem] },
  },
  {
    label: '상태 — 로딩',
    props: { status: 'loading', items: [typicalItem] },
  },
  {
    label: '상태 — 오류',
    props: { status: 'error', items: [typicalItem] },
  },
  {
    label: '상태 — 기존 자료를 표시하며 새로고침 중',
    props: { refreshing: true, items: [typicalItem] },
  },
  {
    label: '상태 — 잠김',
    props: { locked: true, items: [typicalItem] },
  },
];

const root = document.querySelector('#scenarios');

for (const scenario of scenarios) {
  const section = document.createElement('section');
  section.dataset.scenario = scenario.label;
  if (scenario.width) section.style.width = scenario.width;

  const label = document.createElement('h2');
  label.textContent = scenario.label;
  section.append(label);

  if (scenario.finding) {
    const note = document.createElement('p');
    note.textContent = `관찰된 깨짐 (${scenario.owner}): ${scenario.finding}`;
    section.append(note);
  }

  section.append(renderQueueCard(scenario.props));
  root.append(section);
}
