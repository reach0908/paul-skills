async (page) => {
 const results=[];const errors=[];page.on('pageerror',e=>errors.push(e.message));page.on('dialog',d=>d.accept());
 for(const arm of ['control','paul'])for(const width of [1280,320]){
  const start=errors.length;const url=`http://127.0.0.1:48914/runs/wireframe-${arm}/app/`;
  const s=arm==='paul'?{memo:'#save-note',save:'#save-button',check:'#check-status-button',close:'#close-status-button',open:'#open-status-button',status:'#status-message',back:'[data-route="library"]',return:'#list-item-r72 [data-route="detail"]',source:'[data-jump="source-region"]'}:{memo:'#memo',save:'#save-button',check:'#check-button',close:'#close-save',open:'#open-save',status:'#save-status',back:'.back-link',return:'#item-r72 [data-view="detail"]',source:'a[href="#source-section"]'};
  await page.setViewportSize({width,height:width===1280?900:700});await page.goto(url); await page.locator('#reset-button').click();
  await page.locator(s.memo).focus();await page.keyboard.type(`root-${arm}-${width}`);
  await page.locator(s.save).focus();await page.keyboard.press('Enter');
  const initial=await page.locator(s.status).innerText();await page.waitForTimeout(1350);
  const unknown=await page.locator(s.status).innerText();const duplicate=await page.locator(s.save).isDisabled();
  await page.locator(s.close).click();await page.locator(s.open).focus();await page.keyboard.press('Enter');
  const unknownRestored={text:await page.locator(s.status).innerText(),draft:await page.locator(s.memo).inputValue()};
  await page.locator(s.check).focus();await page.keyboard.press('Enter');const pending=await page.locator(s.status).innerText();
  await page.locator(s.check).focus();await page.keyboard.press('Space');const success=await page.locator(s.status).innerText();
  await page.locator(s.close).click();await page.reload();
  if(await page.locator(s.open).isVisible())await page.locator(s.open).click();
  const restored={text:await page.locator(s.status).innerText(),draft:await page.locator(s.memo).inputValue()};
  await page.locator(s.source).click();const internal={url:page.url(),draft:await page.locator(s.memo).inputValue(),status:await page.locator(s.status).innerText(),focus:await page.evaluate(()=>document.activeElement.id)};
  await page.locator(s.back).first().click();const list=await page.locator('main').innerText();await page.locator(s.return).first().click();
  const returnState={url:page.url(),draft:await page.locator(s.memo).inputValue(),status:await page.locator(s.status).innerText()};
  const geometry=await page.evaluate(()=>({viewport:innerWidth,scrollWidth:document.documentElement.scrollWidth}));
  await page.screenshot({path:`/Users/jinhokim/dev/paul-skills/evals/design-beta-readiness-2026-10-14/evidence/wire-${arm}-${width}.png`,fullPage:true});
  results.push({arm,width,initial,unknown,duplicate,unknownRestored,pending,success,restored,internal,list,returnState,geometry,errors:errors.slice(start)});
 }
 return results;
}
