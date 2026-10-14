import {renderSelection} from './components/selection-bar.js';
export const records=Array.from({length:8},(_,i)=>({id:i+1,title:'2026 성수 팝업 캠페인: 고객 인터뷰와 다음 분기 콘텐츠 제작을 위한 상세 회고'}));
renderSelection(document.querySelector('#selection'),records);
