export function renderOrder(root,order){
  root.innerHTML='<section class="order" aria-label="종이책 주문 요약"><h2>봄호 종이책</h2><p>동네 사람들의 작은 작업실을 소개하는 계간지예요.</p><div class="quantity"><button type="button" data-less aria-label="수량 줄이기">−</button><output data-quantity aria-label="선택 수량"></output><button type="button" data-more aria-label="수량 늘리기">+</button></div><label class="gift"><input type="checkbox" data-gift> 선물 포장</label><button type="button" class="quote" data-quote>견적 확인</button><p role="status" data-status></p></section>';
  const update=()=>{root.querySelector('[data-quantity]').textContent=order.quantity+'권';root.querySelector('[data-less]').disabled=order.quantity===1;root.querySelector('[data-more]').disabled=order.quantity===12;root.querySelector('[data-gift]').checked=order.gift;root.querySelector('[data-status]').textContent=order.feedback;};
  root.querySelector('[data-less]').onclick=()=>{if(order.quantity>1)order.quantity--;order.feedback='수량을 변경했어요.';update();};
  root.querySelector('[data-more]').onclick=()=>{if(order.quantity<12)order.quantity++;order.feedback='수량을 변경했어요.';update();};
  root.querySelector('[data-gift]').onchange=e=>{order.gift=e.target.checked;order.feedback='포장 선택을 변경했어요.';update();};
  root.querySelector('[data-quote]').onclick=()=>{order.feedback=order.quantity+'권'+(order.gift?' · 선물 포장':' · 기본 포장')+' 견적을 표시했어요. 실제 주문은 없어요.';update();};
  update();
}
