
let pending=false;
const email=document.querySelector('#email'),send=document.querySelector('#send'),error=document.querySelector('#error'),dialog=document.querySelector('#dialog');
document.querySelector('#invite').onsubmit=e=>{e.preventDefault();if(pending)return;if(!email.validity.valid||!email.value.trim()){email.setAttribute('aria-invalid','true');error.textContent='name@example.com 형식으로 이메일을 입력해 주세요.';email.focus();return;}email.removeAttribute('aria-invalid');error.textContent='';pending=true;send.setAttribute('aria-disabled','true');document.querySelector('#status').textContent='초대 보내는 중…';setTimeout(()=>{pending=false;send.removeAttribute('aria-disabled');document.querySelector('#status').textContent='초대를 보냈어요.';},600);};
document.querySelector('#details').onclick=()=>dialog.showModal();
document.querySelector('#close').onclick=()=>dialog.close();
dialog.addEventListener('close',()=>document.querySelector('#details').focus());

