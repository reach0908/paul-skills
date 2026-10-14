async (page) => {
 const result={state:[],break:[]};
 for(const arm of ['original','paul']) {
  const base=`http://127.0.0.1:48914/runs/state-machine-${arm}/app/states/queue-card/`;
  await page.setViewportSize({width:1280,height:900}); await page.goto(base);
  const ids=await page.locator('[data-state]').evaluateAll(es=>es.map(e=>e.dataset.state));
  const states=[];
  for(const id of ids) { await page.locator(`[data-state="${id}"]`).click(); states.push({id,url:page.url(),text:await page.locator('#queue').innerText(),disabled:await page.locator('#queue button:disabled').count()}); }
  await page.locator('[data-state="loading"]').click(); await page.waitForTimeout(250); const held=(await page.locator('#queue').innerText());
  await page.locator('[data-state="locked"]').click(); await page.reload(); await page.setViewportSize({width:320,height:700});
  const persisted={url:page.url(),active:await page.locator('[aria-pressed="true"]').getAttribute('data-state'),overflow:await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth)};
  await page.evaluate(()=>{let e=document.createElement('input');e.id='root-probe';e.setAttribute('aria-label','Root keyboard probe');document.body.prepend(e);});
  await page.locator('#root-probe').focus(); await page.keyboard.press('ArrowRight'); await page.keyboard.press('1'); await page.keyboard.press('h');
  const inputGuard={url:page.url(),hidden:await page.locator('.state-switcher').evaluate(e=>e.hidden),value:await page.locator('#root-probe').inputValue()};
  await page.locator('#root-probe').evaluate(e=>e.blur());
  await page.keyboard.press('Alt+ArrowRight'); await page.keyboard.press('Shift+H');
  const modifierGuard={url:page.url(),hidden:await page.locator('.state-switcher').evaluate(e=>e.hidden)};
  await page.evaluate(()=>document.addEventListener('keydown',e=>e.preventDefault(),{capture:true,once:true}));
  await page.keyboard.press('ArrowRight'); const preventedGuard=page.url();
  await page.keyboard.press('h');const hidden=await page.locator('.state-switcher').evaluate(e=>e.hidden);await page.keyboard.press('h');
  await page.keyboard.press('1');const numeric=page.url();await page.keyboard.press('ArrowRight');const arrow=page.url();
  await page.screenshot({path:`/Users/jinhokim/dev/paul-skills/evals/design-beta-readiness-2026-10-14/evidence/state-${arm}-mobile.png`});
  result.state.push({arm,ids,states,held,persisted,inputGuard,modifierGuard,preventedGuard,hToggle:hidden,numeric,arrow});
 }
 for(const arm of ['original','paul']) {
  await page.setViewportSize({width:1280,height:900}); await page.goto(`http://127.0.0.1:48914/runs/break-${arm}/app/stress/`);
  const geometry=await page.locator('.queue').evaluateAll(es=>es.map(e=>({scenario:e.parentElement.parentElement.innerText.slice(0,150),width:e.getBoundingClientRect().width,scrollWidth:e.scrollWidth,clientWidth:e.clientWidth,overflows:[...e.querySelectorAll('.queue-label')].map(b=>({text:b.textContent,right:b.getBoundingClientRect().right,parentRight:e.getBoundingClientRect().right,overflow:b.getBoundingClientRect().right>e.getBoundingClientRect().right+1})).filter(x=>x.overflow)})));
  const other=await page.evaluate(()=>({classes:[...document.querySelectorAll('[class]')].map(e=>e.className).filter((v,i,a)=>a.indexOf(v)===i),pageWidth:document.documentElement.scrollWidth,viewport:innerWidth}));
  await page.screenshot({path:`/Users/jinhokim/dev/paul-skills/evals/design-beta-readiness-2026-10-14/evidence/break-${arm}.png`,fullPage:true});
  result.break.push({arm,geometry,other});
 }
 return result;
}
