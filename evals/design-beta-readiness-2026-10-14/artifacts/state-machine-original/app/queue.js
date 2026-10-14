export function renderQueueCard({status='ready',items=[],canEdit=true,locked=false,refreshing=false,onRetry=()=>{},onSelect=()=>{}}={}){
 const root=document.createElement('section');root.className='card';root.setAttribute('aria-label','검토 대기 자료');
 const heading=document.createElement('h2');heading.textContent='검토 대기 자료';root.append(heading);
 if(!canEdit){root.insertAdjacentHTML('beforeend','<p>이 자료를 검토할 권한이 없습니다.</p>');return root;}
 if(status==='loading'){root.setAttribute('aria-busy','true');root.insertAdjacentHTML('beforeend','<p role="status">자료를 불러오는 중</p>');return root;}
 if(status==='error'){root.insertAdjacentHTML('beforeend','<p role="alert">자료를 불러오지 못했습니다.</p>');const b=document.createElement('button');b.textContent='다시 시도';b.onclick=onRetry;root.append(b);return root;}
 if(!items.length){root.insertAdjacentHTML('beforeend','<p>대기 중인 자료가 없습니다.</p>');return root;}
 if(refreshing){root.setAttribute('aria-busy','true');root.insertAdjacentHTML('beforeend','<p role="status">기존 자료를 보여주며 새로 확인하는 중</p>');}
 const ul=document.createElement('ul');ul.className='queue-items';
 for(const item of items){const li=document.createElement('li');const b=document.createElement('button');b.className='queue-label';b.textContent=item.title;b.disabled=locked;b.onclick=()=>onSelect(item.id);li.append(b);ul.append(li);}root.append(ul);
 if(locked)root.insertAdjacentHTML('beforeend','<p>검토가 잠겨 있습니다.</p>');return root;
}
