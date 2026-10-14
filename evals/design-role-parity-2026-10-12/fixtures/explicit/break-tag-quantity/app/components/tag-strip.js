export function renderTags(root, tags) {
 const section=document.createElement('section');section.className='tag-strip';section.setAttribute('aria-label','프로젝트 태그');
 if(!tags.length) {const p=document.createElement('p');p.textContent='등록한 태그가 없어요.';section.append(p);}
 for(const label of tags) {const span=document.createElement('span');span.className='tag';span.textContent=label;section.append(span);}
 root.replaceChildren(section);
}
