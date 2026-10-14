
let count=0;
const send=document.querySelector('#send');
document.querySelector('#invite').onsubmit=e=>{e.preventDefault();send.setAttribute('aria-disabled','true');send.innerHTML='<span aria-hidden="true">◌</span>';const value=document.querySelector('#email').value;setTimeout(()=>{if(!value.includes('@')){document.querySelector('#error').textContent='이메일 주소를 확인하고 다시 입력해 주세요.';}else{count++;document.querySelector('#count').textContent=count;document.querySelector('#status').textContent='초대를 보냈어요.';}send.removeAttribute('aria-disabled');send.textContent='초대 보내기';},700);};
document.querySelector('#remove').onclick=()=>document.querySelector('#request').remove();
document.querySelector('#next').onclick=()=>{document.querySelector('#status').textContent='Jae의 요청을 열었어요.';};
document.querySelector('#details').onclick=()=>{document.querySelector('#modal').hidden=false;};
document.querySelector('#close').onclick=()=>{document.querySelector('#modal').hidden=true;};

