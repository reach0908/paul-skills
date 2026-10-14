
const email=document.querySelector('#email');
document.querySelector('#send').onclick=()=>{ if(!email.value.includes('@')){document.querySelector('#error').textContent='이메일 주소를 확인하고 다시 입력해 주세요.';return;} document.querySelector('#status').textContent='초대를 보냈어요.'; };
document.querySelector('#help').onclick=()=>{document.querySelector('#help-text').hidden=false;};
document.querySelector('#invite').onsubmit=e=>e.preventDefault();

