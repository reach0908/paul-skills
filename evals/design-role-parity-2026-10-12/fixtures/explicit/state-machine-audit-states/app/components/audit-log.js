export function renderAudit(root, data) {
 if(data.role==='member') { root.innerHTML='<section class="panel"><h2>활동 기록</h2><p>관리자만 볼 수 있어요. 팀 관리자에게 권한을 요청해 주세요.</p></section>';return; }
 if(data.status==='loading') { root.innerHTML='<section class="panel" aria-busy="true"><h2>활동 기록</h2><p role="status">기록을 불러오고 있어요.</p></section>';return; }
 if(data.status==='error') { root.innerHTML='<section class="panel"><h2>활동 기록</h2><p role="alert">기록을 불러오지 못했어요.</p><button data-retry>다시 불러오기</button></section>';root.querySelector('[data-retry]').onclick=()=>data.onRetry?.();return; }
 const section=document.createElement('section');section.className='panel';section.innerHTML='<h2>활동 기록</h2>';
 if(data.refreshing) section.insertAdjacentHTML('beforeend','<p role="status">이전 기록을 보며 새 기록을 기다리고 있어요.</p>');
 if(data.items.length===0) section.insertAdjacentHTML('beforeend','<p>아직 활동 기록이 없어요. 파일을 공유하면 여기에 표시돼요.</p>');
 else { const list=document.createElement('ol');list.className='audit-items';data.items.forEach(item=>{const li=document.createElement('li');li.textContent=`${item.actor} · ${item.action} · ${item.time}`;list.append(li);});section.append(list); }
 root.replaceChildren(section);
}
