async (page) => {
 const results=[];
 const measure=()=>{const target=document.querySelector('#target'),c=getComputedStyle(target);return {padding:c.padding,radius:c.borderRadius,border:c.borderWidth,background:c.backgroundColor,color:c.color,type:getComputedStyle(target.querySelector('h2')).fontSize,columns:getComputedStyle(target.querySelector('.tools')).gridTemplateColumns,rects:[...document.querySelectorAll('header,main>h1,#search,#target,#target h2,#note,.tools,#save,#clear,#error,#empty,#status,main>p>a')].map(e=>{let r=e.getBoundingClientRect();return {tag:e.tagName,id:e.id,x:r.x,y:r.y,w:r.width,h:r.height}}),scrollWidth:document.documentElement.scrollWidth,viewport:innerWidth};};
 for(const arm of ['original','paul'])for(const width of [1280,320]){
  await page.setViewportSize({width,height:width===1280?900:700});const base=`http://127.0.0.1:48914/runs/build-design-${arm}/`;
  await page.goto(base+'ref/index.html');const reference=await page.evaluate(measure);
  await page.goto(base+'app/');const actual=await page.evaluate(measure);
  await page.screenshot({path:`/Users/jinhokim/dev/paul-skills/evals/design-beta-readiness-2026-10-14/evidence/build-${arm}-${width}.png`,fullPage:true});
  const focus=[];for(let i=0;i<8;i++){await page.keyboard.press('Tab');focus.push(await page.evaluate(()=>({id:document.activeElement.id||document.activeElement.textContent.trim(),outline:getComputedStyle(document.activeElement).outlineStyle})));}
  await page.locator('#note').fill('root-build');await page.locator('#save').focus();await page.keyboard.press('Enter');const pending={text:await page.locator('#status').innerText(),disabled:await page.locator('#save').isDisabled()};await page.waitForTimeout(1100);const success=await page.locator('#status').innerText();
  await page.locator('#error').focus();await page.keyboard.press('Space');const error=await page.locator('#status').innerText();await page.locator('#empty').focus();await page.keyboard.press('Enter');const empty=await page.locator('#feedback').innerText();await page.locator('#clear').focus();await page.keyboard.press('Enter');const clear=await page.locator('#note').inputValue();
  results.push({arm,width,reference,actual,focus,pending,success,error,empty,clear});
 }
 return results;
}
