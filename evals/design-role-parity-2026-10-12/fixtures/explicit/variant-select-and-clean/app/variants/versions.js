export function renderVariant(root, invoice, name) {
 const rows=`<dl><div><dt>사용 기간</dt><dd>2026.10.01 ~ 10.31</dd></div><div><dt>팀 플랜</dt><dd>49,000원</dd></div><div><dt>추가 저장 공간</dt><dd>8,000원</dd></div><div><dt>총액</dt><dd>57,000원</dd></div></dl>`;
 root.innerHTML=`<section class="panel invoice ${name}"><h2>${invoice.name}</h2>${name==='ledger'?rows:`<p class="total">57,000원</p><p>팀 플랜 49,000원 + 추가 저장 공간 8,000원</p><p>2026.10.01 ~ 10.31</p>`}<button data-download>명세서 받기</button><p role="status"></p></section>`;
 root.querySelector('[data-download]').onclick=()=>root.querySelector('[role=status]').textContent='10월 명세서를 준비했어요.';
}
