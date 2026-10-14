async (page) => {
 const rows=[],errors=[];
 page.on('pageerror',e=>errors.push(String(e)));
 const assert=(condition,message)=>{if(!condition)throw new Error(message)};
 const controls='a[href],button:not(:disabled),input:not(:disabled),textarea:not(:disabled),select:not(:disabled),summary';
 async function observe(){return page.evaluate(()=>({url:location.href,view:document.querySelector('.state-id')?.textContent,draft:document.querySelector('#note')?.value,state:JSON.parse(sessionStorage.getItem('chain-wire-t-save-v1')),padding:getComputedStyle(document.querySelector('main')).paddingLeft,overflow:{document:document.documentElement.scrollWidth-innerWidth,elements:[...document.body.querySelectorAll('*')].filter(e=>e.getClientRects().length&&getComputedStyle(e).visibility!=='hidden').map(e=>({tag:e.tagName,id:e.id,left:e.getBoundingClientRect().left,right:e.getBoundingClientRect().right})).filter(e=>e.left < -1 || e.right>innerWidth+1)}}));}
 async function waitState(state){await page.waitForFunction(s=>document.querySelector('.state-id')?.textContent.includes(s),state,{timeout:6000});}
 async function tabTo(selector){for(let i=0;i<50;i++){if(await page.evaluate(s=>document.activeElement?.matches(s),selector))return;await page.keyboard.press('Tab');}throw new Error('Keyboard target unreachable: '+selector);}
 async function keyActivate(selector,key='Enter'){await tabTo(selector);await page.keyboard.press(key);}
 async function reset(){if(!await page.locator('[data-action="reset"]').count())await page.locator('[data-route="library"]').click();await page.locator('[data-action="reset"]').click();await waitState('TS-00');}
 for(const stage of ['chain-build']) for(const width of [1280,320]){
  const url=`http://127.0.0.1:48924/runs/${stage}/app/`,name=`${stage}-${width}`,states=[];
  await page.setViewportSize({width,height:width===1280?900:700});await page.goto(url);await reset();
  await page.goto('about:blank');await page.goto(url);
  assert(await page.evaluate(()=>document.activeElement.tagName)==='BODY',name+' initial keyboard focus must be BODY');
  const expected=await page.locator(controls).evaluateAll(es=>es.filter(e=>e.getClientRects().length&&getComputedStyle(e).visibility!=='hidden').map((e,index)=>({index,tag:e.tagName,name:e.textContent||e.id})));
  const seen=new Set(),focus=[];
  for(let i=0;i<expected.length+3;i++){
   await page.keyboard.press('Tab');
   const x=await page.evaluate(selector=>{const es=[...document.querySelectorAll(selector)].filter(e=>e.getClientRects().length&&getComputedStyle(e).visibility!=='hidden'),e=document.activeElement,b=e.getBoundingClientRect();return{index:es.indexOf(e),tag:e.tagName,text:(e.textContent||e.id).slice(0,90),left:b.left,right:b.right,top:b.top,bottom:b.bottom,width:innerWidth,height:innerHeight}},controls);
   if(x.index>=0){seen.add(x.index);focus.push(x);assert(x.left>=-1&&x.right<=width+1&&x.top>=-1&&x.bottom<=x.height+1,name+' focused control clipped '+x.text);}
  }
  assert(expected.length>=10 && seen.size===expected.length,name+' keyboard coverage incomplete');
  await tabTo('#note');await page.keyboard.type('검증 메모 '+width+' · 초안 보존');const draft=await page.locator('#note').inputValue();
  const captures=[];
  async function capture(label){const o=await observe();assert(o.overflow.document<=1&&!o.overflow.elements.length,name+' overflow '+label);states.push({label,...o});const path=`/Users/jinhokim/dev/paul-skills/evals/design-beta-hardening-2026-10-14/evidence/${name}-${label}.png`;await page.screenshot({path,fullPage:true});captures.push(path);}
  await capture('draft');
  await keyActivate('[data-action="close"]');let o=await observe();assert(o.state.taskState==='TS-00'&&o.state.jobKey===null&&o.state.receipt===null,name+' draft close created key');
  await keyActivate('[data-action="reopen"]','Space');assert(await page.locator('#note').inputValue()===draft,name+' draft lost');
  await keyActivate('a[href="#article-body"]');o=await observe();assert(o.state.route==='item'&&o.state.draft===draft&&o.state.taskState==='TS-00',name+' internal link changed task');
  await keyActivate('[data-action="save"]');await waitState('TS-10');await page.keyboard.press('Enter');
  await page.locator('[data-action="close"]').click();o=await observe();assert(o.state.taskState==='TS-10'&&o.state.taskView==='V-CLOSED',name+' pending close not exercised');states.push({label:'pending-closed',...o});
  await waitState('TS-20');await page.locator('[data-action="reopen"]').click();await capture('unknown');
  await page.locator('[data-action="close"]').click();await page.locator('[data-action="reopen"]').click();o=await observe();assert(o.state.taskState==='TS-20'&&o.state.saveRequests===1,name+' unknown restart');
  await page.locator('[data-action="check"]').click();await waitState('TS-21');await page.locator('[data-action="close"]').click();states.push({label:'first-check-closed',...await observe()});await waitState('TS-30');await page.locator('[data-action="reopen"]').click();
  o=await observe();assert(o.state.statusChecks===1&&o.state.receipt===null,name+' first check completed too early');states.push({label:'server-pending',...o});
  await page.locator('[data-action="close"]').click();await page.locator('[data-action="reopen"]').click();assert((await observe()).state.taskState==='TS-30',name+' pending query state lost');
  await keyActivate('[data-action="check"]','Space');await waitState('TS-31');await page.locator('[data-action="close"]').click();states.push({label:'second-check-closed',...await observe()});await waitState('TS-40');await page.locator('[data-action="reopen"]').click();
  await capture('success');o=await observe();assert(o.state.saveRequests===1&&o.state.statusChecks===2&&o.state.receipt==='S-72'&&o.state.draft===draft,name+' success identity mismatch');
  await page.locator('[data-action="close"]').click();await page.locator('[data-action="reopen"]').click();o=await observe();assert(o.state.receipt==='S-72'&&o.state.saveRequests===1,name+' success close lost result');
  await page.locator('[data-action="back-list"]').click();assert(await page.locator('#query').inputValue()==='작은 팀',name+' query lost');assert(await page.locator('#tag').inputValue()==='운영',name+' tag lost');assert(await page.locator('#sort').inputValue()==='newest',name+' sort lost');
  await page.locator('[data-action="open-item"]').click();await page.reload();o=await observe();assert(o.state.context.item==='R-72'&&o.state.receipt==='S-72'&&o.draft===draft,name+' return or reload lost state');states.push({label:'return-reload',...o});
  const source=await page.locator('[data-source-link]').first().getAttribute('href');assert(source==='https://example.com/',name+' source destination changed');
  await reset();await page.locator('[data-action="save"]').click();await waitState('TS-20');await page.locator('[data-action="require-auth"]').click();await waitState('TS-90');await page.locator('[data-action="recover-auth"]').click();await capture('auth-unresolved');o=await observe();assert(o.state.taskState==='TS-90'&&o.state.receipt===null&&o.state.saveRequests===1,name+' invented auth result');
  assert(states.every(s=>s.overflow.document<=1&&!s.overflow.elements.length),name+' overflow in recorded task state');
  await reset();
  rows.push({id:name,status:'pass',width,height:width===1280?900:700,initialFocus:'BODY',expectedFocusable:expected.length,observedFocusable:seen.size,focus,states,captures,sourceLink:source,sourceLinkLimit:'Destination inspected; external site was not opened by this evaluator.'});
 }
 assert(rows.length===2,'Expected two viewport combinations');assert(!errors.length,'Page errors: '+errors.join(';'));
 return {expectedCombinations:2,actualCombinations:rows.length,pageErrors:errors,rows};
}
