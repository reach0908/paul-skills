document.querySelector('#copy').addEventListener('click',()=>document.querySelector('#notice').textContent='공유 링크를 복사했어요.');
document.querySelector('#close').addEventListener('click',()=>document.querySelector('[role=dialog]').hidden=true);
import { renderArchive } from './archive.js';
renderArchive(document.querySelector('main'));
