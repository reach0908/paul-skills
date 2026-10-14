import {renderAudit} from '../../components/audit-log.js';
const previewAuditFixtures={empty:{role:'owner',status:'ready',items:[]},loading:{role:'owner',status:'loading',items:[]}};
function show(name){const url=new URL(location);url.searchParams.set('__state',name);history.replaceState(null,'',url);renderAudit(document.querySelector('#audit'),previewAuditFixtures[name]||previewAuditFixtures.empty);document.querySelectorAll('[data-state]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.state===name)));}
document.querySelectorAll('[data-state]').forEach(b=>b.onclick=()=>show(b.dataset.state));show(new URLSearchParams(location.search).get('__state')||'empty');
