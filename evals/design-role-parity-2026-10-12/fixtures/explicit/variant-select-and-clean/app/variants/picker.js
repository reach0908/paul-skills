const names=['compact','ledger','spotlight'];
export function mountPicker(render) {
 const nav=document.createElement('nav');nav.className='variant-picker';nav.setAttribute('aria-label','Variants');document.body.append(nav);
 function activate(name){const url=new URL(location);url.searchParams.set('__variant',name);history.replaceState(null,'',url);render(name);nav.innerHTML=names.map(n=>`<button data-variant="${n}" aria-pressed="${n===name}">${n}</button>`).join('');nav.querySelectorAll('button').forEach(b=>b.onclick=()=>activate(b.dataset.variant));}
 document.addEventListener('keydown',e=>{if(e.defaultPrevented||e.metaKey||e.ctrlKey||e.altKey||e.shiftKey||e.target.closest('input,textarea,select,[contenteditable]'))return;if(e.key.toLowerCase()==='h'){nav.hidden=!nav.hidden;return;}let i=names.indexOf(new URLSearchParams(location.search).get('__variant'));if(e.key==='ArrowRight')i=(i+1)%3;else if(e.key==='ArrowLeft')i=(i+2)%3;else if(/^[123]$/.test(e.key))i=Number(e.key)-1;else return;e.preventDefault();activate(names[i]);});
 activate(names.includes(new URLSearchParams(location.search).get('__variant'))?new URLSearchParams(location.search).get('__variant'):'compact');
}
