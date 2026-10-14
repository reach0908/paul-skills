export function renderSaveButton(root) {
 const button=document.createElement('button');button.className='save-button';button.type='button';button.textContent='기록 저장';button.addEventListener('click',()=>{const event=new CustomEvent('record-save',{bubbles:true});button.dispatchEvent(event);});root.replaceChildren(button);
}
