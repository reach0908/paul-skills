export function renderSelection(root, records) {
 root.innerHTML=`<section class="selection panel" aria-label="선택한 기록"><strong>${records.length}개 선택됨</strong><span>${records[0].title}</span><button type="button" data-export>선택한 기록 내보내기</button><button type="button" class="secondary" data-clear>선택 해제</button><p role="status" data-status></p></section>`;
 root.querySelector('[data-export]').onclick=()=>root.querySelector('[data-status]').textContent=`${records.length}개 기록을 파일로 준비했어요.`;
 root.querySelector('[data-clear]').onclick=()=>{root.querySelector('strong').textContent='0개 선택됨';root.querySelector('[data-export]').disabled=true;root.querySelector('[data-status]').textContent='선택을 해제했어요.';};
}
