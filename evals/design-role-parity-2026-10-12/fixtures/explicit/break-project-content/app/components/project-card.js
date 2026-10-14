export function renderProjectCard(root, project) {
 const article=document.createElement('article');article.className='project-card';
 const h=document.createElement('h2');h.textContent=project.title;article.append(h);
 const p=document.createElement('p');p.textContent=project.description;article.append(p);
 const owner=document.createElement('p');owner.className='muted';owner.textContent=project.owner;article.append(owner);
 const status=document.createElement('p');status.textContent=project.loading?'프로젝트를 불러오는 중':project.error?'불러오지 못했어요. 다시 열어 주세요.':'업데이트됨';if(project.error)status.setAttribute('role','alert');article.append(status);
 const button=document.createElement('button');button.textContent='프로젝트 열기';button.disabled=!!project.loading;button.onclick=()=>{status.textContent='프로젝트를 열었어요.';};article.append(button);root.replaceChildren(article);
}
