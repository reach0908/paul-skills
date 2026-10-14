export function renderUsage(root) {
 root.innerHTML=`<section class="panel usage"><h2>이번 달 전송량</h2><p><strong>742 GB</strong> / 1,000 GB</p><progress aria-label="이번 달 전송량" max="1000" value="742"></progress><p class="muted">11월 1일에 다시 시작돼요. 팀원 12명이 사용 중이에요.</p><button type="button" data-plan>요금제 살펴보기</button><p role="status" data-status></p></section>`;
 root.querySelector('[data-plan]').addEventListener('click',()=>root.querySelector('[data-status]').textContent='팀 플랜: 월 49,000원, 전송량 2,000 GB예요.');
}
