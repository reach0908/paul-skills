import {renderAttachments} from '../attachment.js';

const typical = {name: '회의록_다음분기_검토.pdf'};
const oneWord = {name: '보고서.pdf'};
const maxUnbroken = {name: `${'A'.repeat(216)}.pdf`};
const longWords = {name: `${'분기 검토 자료와 후속 조치 및 담당자 의견 '.repeat(12).slice(0, 216)}.pdf`};
const shapedNames = [
  {name: '📎_Crème_Brûlée_회의록_최종본_🧑🏽‍💻.pdf'},
  {name: 'تقرير_الربع_الثالث_OpenAI_검토본.pdf'},
];
const realistic = [
  typical,
  {name: '예산안_2027.xlsx'},
  {name: '고객인터뷰_요약.docx'},
];
const many = Array.from({length: 30}, (_, index) => ({
  name: `첨부_${String(index + 1).padStart(2, '0')}_검토자료.pdf`,
}));

const scenarios = [
  {id: 'normal-760-nowrap', label: '정상 · 760px · 단일행 · 대표 파일명 1개', width: 760, props: {items: [typical]}},
  {id: 'normal-280-nowrap', label: '정상 · 280px · 단일행 · 대표 파일명 1개', width: 280, props: {items: [typical]}},
  {id: 'normal-760-wrap', label: '정상 · 760px · 줄바꿈 · 대표 파일명 1개', width: 760, props: {items: [typical], wrapNames: true}},
  {id: 'normal-280-wrap', label: '정상 · 280px · 줄바꿈 · 대표 파일명 1개', width: 280, props: {items: [typical], wrapNames: true}},
  {id: 'one-word', label: '길이 · 760px · 단일행 · 짧은 한 단어', width: 760, props: {items: [oneWord]}},
  {id: 'long-spaced-280-nowrap', label: '길이 · 280px · 단일행 · 공백 포함 220자', width: 280, props: {items: [longWords]}},
  {id: 'long-spaced-280-wrap', label: '길이 · 280px · 줄바꿈 · 공백 포함 220자', width: 280, props: {items: [longWords], wrapNames: true}},
  {id: 'max-760-nowrap', label: '길이 · 760px · 단일행 · 끊을 수 없는 220자', width: 760, props: {items: [maxUnbroken]}},
  {id: 'max-280-nowrap', label: '길이 · 280px · 단일행 · 끊을 수 없는 220자', width: 280, props: {items: [maxUnbroken]}},
  {id: 'max-760-wrap', label: '길이 · 760px · 줄바꿈 · 끊을 수 없는 220자', width: 760, props: {items: [maxUnbroken], wrapNames: true}},
  {id: 'max-280-wrap', label: '길이 · 280px · 줄바꿈 · 끊을 수 없는 220자', width: 280, props: {items: [maxUnbroken], wrapNames: true}},
  {id: 'shape-280-wrap', label: '문자 형태 · 280px · 줄바꿈 · 이모지/발음 구별 기호/RTL 혼합', width: 280, props: {items: shapedNames, wrapNames: true}},
  {id: 'zero', label: '수량/상태 · 760px · 항목 0개(빈 상태)', width: 760, props: {items: []}},
  {id: 'one', label: '수량 · 760px · 항목 1개', width: 760, props: {items: [typical]}},
  {id: 'realistic', label: '수량 · 760px · 현실적인 3개', width: 760, props: {items: realistic}},
  {id: 'many', label: '수량 · 760px · 현실적 수량의 10배(30개)', width: 760, props: {items: many}},
  {id: 'loading', label: '상태 · 760px · 로딩', width: 760, props: {loading: true}},
  {id: 'readonly', label: '상태 · 760px · 읽기 전용(대표 파일명 1개)', width: 760, props: {items: [typical], readOnly: true}},
];

const findings = {
  'long-spaced-280-nowrap': '관찰: 파일명 버튼이 카드 오른쪽 경계를 넘어 페이지 바깥 방향으로 길게 확장됩니다. 담당: better-typography.',
  'max-760-nowrap': '관찰: 파일명 버튼이 카드 오른쪽 경계를 넘어 페이지 바깥 방향으로 길게 확장됩니다. 담당: better-typography.',
  'max-280-nowrap': '관찰: 파일명 버튼이 카드 오른쪽 경계를 넘어 페이지 바깥 방향으로 길게 확장됩니다. 담당: better-typography.',
};

document.querySelector('#result-summary').textContent = '관찰 결과: 단일행 장문 3개 시나리오에서 실제 깨짐을 확인했습니다. 나머지 시나리오에서는 화면상 깨짐을 보지 못했습니다.';

const target = document.querySelector('#scenarios');
for (const scenario of scenarios) {
  const block = document.createElement('section');
  block.dataset.scenario = scenario.id;
  block.style.width = `${scenario.width}px`;
  block.style.maxWidth = '100%';
  const label = document.createElement('p');
  const strong = document.createElement('strong');
  strong.textContent = scenario.label;
  label.append(strong);
  block.append(label);
  if (findings[scenario.id]) {
    const finding = document.createElement('p');
    finding.textContent = findings[scenario.id];
    block.append(finding);
  }
  block.append(renderAttachments(scenario.props));
  target.append(block);
}
