async(page)=>{
 const rows=[];
 for(const arm of ['original','paul']){
  await page.goto('about:blank');await page.setViewportSize({width:320,height:450});await page.goto(`http://127.0.0.1:48914/runs/variant-${arm}/app/?__variant=compact`);
  for(let i=0;i<8;i++){await page.keyboard.press('Tab');if(await page.evaluate(()=>document.activeElement.id==='note'))break;}
  await page.evaluate(()=>new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve))));
  rows.push({arm,focus:await page.evaluate(()=>{const e=document.activeElement,r=e.getBoundingClientRect();return {id:e.id,top:r.top,bottom:r.bottom,viewport:innerHeight,scrollY}})});
  await page.screenshot({path:`/Users/jinhokim/dev/paul-skills/evals/design-beta-readiness-2026-10-14/evidence/variant-${arm}-compact-focus.png`});
 }
 return rows;
}
