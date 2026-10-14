export function renderBooking(root){
 root.innerHTML='<section class="booking-summary" aria-label="예약 요약"><p class="muted">선택한 공간</p><h2>성수 촬영실: 브랜드 인터뷰와 제품 촬영을 위한 작업 공간</h2><p>12명 · 10월 14일 오후 2시부터 5시까지</p><button type="button" data-confirm>이 일정으로 예약 확인</button><p role="status"></p></section>';
 root.querySelector('[data-confirm]').onclick=()=>root.querySelector('[role=status]').textContent='일정을 확인했어요. 아직 예약하지 않았어요.';
}
