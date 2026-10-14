export function renderQueue(root, model) {
 const panel=document.createElement('section');panel.className='panel';panel.innerHTML='<h2>공유 파일 전송</h2>';
 if(!model.enabled) { panel.insertAdjacentHTML('beforeend','<p>관리자가 파일 전송 기능을 꺼 두었어요.</p>'); }
 else if(model.plan==='free' && model.used>=model.limit) { panel.insertAdjacentHTML('beforeend','<p>이번 달 무료 전송 20건을 모두 사용했어요. 다음 달에 다시 전송하거나 팀 플랜을 확인해 주세요.</p><button data-plan>팀 플랜 확인</button>');panel.querySelector('[data-plan]').onclick=()=>model.onPlan?.(); }
 else if(model.status==='loading') { panel.insertAdjacentHTML('beforeend','<p role="status" aria-busy="true">전송 목록을 불러오고 있어요.</p>'); }
 else if(model.status==='error') { panel.insertAdjacentHTML('beforeend','<p role="alert">목록을 불러오지 못했어요.</p><button data-retry>다시 시도</button>');panel.querySelector('[data-retry]').onclick=()=>model.onRetry?.(); }
 else if(!model.files.length) {panel.insertAdjacentHTML('beforeend','<p>전송할 파일을 추가해 주세요.</p>');}
 else { const ul=document.createElement('ul');model.files.forEach(file=>{const li=document.createElement('li');li.textContent=file.name+' · '+(file.status==='pending'?'전송 대기':file.status==='failed'?'전송 실패: 파일을 다시 추가해 주세요.':'전송 완료');if(file.status==='pending')li.setAttribute('aria-busy','true');ul.append(li);});panel.append(ul);}
 root.replaceChildren(panel);
}
