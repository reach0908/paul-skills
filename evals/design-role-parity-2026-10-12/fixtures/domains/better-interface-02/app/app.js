
let count=0;
document.querySelector('#export').onsubmit=e=>{e.preventDefault();const b=document.querySelector('#send');b.setAttribute('aria-disabled','true');b.innerHTML='<span aria-hidden="true">◌</span>';const name=document.querySelector('#name').value;setTimeout(()=>{b.textContent='PDF 준비';b.removeAttribute('aria-disabled');if(!name.endsWith('.pdf')){document.querySelector('#message').textContent='Something went wrong.';}else{count++;document.querySelector('#count').textContent=count;document.querySelector('#message').textContent='PDF가 준비됐어요.';}},700);};
document.querySelector('#preview-button').onclick=()=>{const p=document.querySelector('#preview');p.classList.remove('running');void p.offsetWidth;p.classList.add('running');};

