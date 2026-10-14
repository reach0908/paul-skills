async (page) => {
 const results=[];
 for(const arm of ['original','paul'])for(const width of [1280,320])for(const variant of ['airy','balanced','compact']){
  await page.setViewportSize({width,height:width===1280?900:450});await page.goto(`http://127.0.0.1:48914/runs/variant-${arm}/app/?__variant=${variant}`);
  const buttons=await page.locator('.variant-picker button').count();
  await page.locator('#search').fill('probe-query');await page.locator('#note').fill('probe-note');
  const other=variant==='compact'?'airy':'compact';await page.locator(`.variant-picker [data-variant="${other}"]`).click();
  const retained={query:await page.locator('#search').inputValue(),note:await page.locator('#note').inputValue(),url:page.url()};
  await page.locator('#clear').click();await page.locator(`.variant-picker [data-variant="${variant}"]`).click();const cleared=await page.locator('#note').inputValue();
  await page.locator('#note').fill('saved-probe');await page.locator('#save').focus();await page.keyboard.press('Enter');
  const pending={text:await page.locator('#status').innerText(),disabled:await page.locator('#save').isDisabled()};
  await page.locator(`.variant-picker [data-variant="${other}"]`).click();const switched={text:await page.locator('#status').innerText(),disabled:await page.locator('#save').isDisabled()};
  await page.waitForTimeout(1100);await page.locator(`.variant-picker [data-variant="${variant}"]`).click();
  const success={text:await page.locator('#status').innerText(),note:await page.locator('#note').inputValue(),query:await page.locator('#search').inputValue()};
  await page.goto(`http://127.0.0.1:48914/runs/variant-${arm}/app/?__variant=${variant}`);
  const focus=[];
  for(let i=0;i<12;i++){
   await page.keyboard.press('Tab');
   focus.push(await page.evaluate(()=>{const e=document.activeElement,r=e.getBoundingClientRect(),p=document.querySelector('.variant-picker'),q=p.getBoundingClientRect();return {id:e.id||e.dataset.variant||e.textContent.trim(),rect:{left:r.left,right:r.right,top:r.top,bottom:r.bottom},overlap:!p.contains(e)&&r.left<q.right&&r.right>q.left&&r.top<q.bottom&&r.bottom>q.top,visible:r.left>=0&&r.right<=innerWidth+1&&r.top>=0&&r.bottom<=innerHeight+1,outline:getComputedStyle(e).outlineStyle};}));
  }
  const geometry=await page.evaluate(()=>({width:innerWidth,scrollWidth:document.documentElement.scrollWidth,padding:getComputedStyle(document.querySelector('#target')).padding}));
  await page.screenshot({path:`/Users/jinhokim/dev/paul-skills/evals/design-beta-readiness-2026-10-14/evidence/variant-${arm}-${variant}-${width}.png`,fullPage:true});
  results.push({arm,width,variant,buttons,retained,cleared,pending,switched,success,focus,geometry});
 }
 return results;
}
