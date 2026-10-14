async (page) => {
 const rows=[];
 for(const caseName of ['old','new']) for(const arm of ['original','paul']){
  const id=`break-${caseName}-${arm}`;
  await page.setViewportSize({width:1280,height:720});
  await page.goto(`http://127.0.0.1:48924/runs/${id}/app/stress/`);
  const selector=caseName==='old'?'.card':'.attachments';
  await page.locator(selector).first().waitFor();
  const cards=await page.locator(selector).evaluateAll(es=>es.map(e=>{
   const bounds=e.getBoundingClientRect();let parent=e.parentElement;
   while(parent && !parent.querySelector('h2,h3')?.textContent?.includes('·') && parent.tagName!=='MAIN')parent=parent.parentElement;
   const scenario=e.closest('[data-scenario]') || (e.parentElement.closest('section,article')) || parent;
   return {scenario:scenario?.getAttribute('data-scenario')||scenario?.querySelector('h2,h3')?.textContent,context:scenario?.innerText?.slice(0,300),width:bounds.width,wrap:e.classList.contains('wrap'),scrollWidth:e.scrollWidth,clientWidth:e.clientWidth,buttons:[...e.querySelectorAll('button')].map(b=>({name:b.textContent,length:[...b.textContent].length,right:b.getBoundingClientRect().right,parentRight:bounds.right,overflow:b.getBoundingClientRect().right>bounds.right+1,empty:!b.textContent.trim()}))};
  }));
  if(cards.length<8)throw new Error(`Incomplete rendered scenario page: ${id}/${cards.length}`);
  await page.screenshot({path:`/Users/jinhokim/dev/paul-skills/evals/design-beta-hardening-2026-10-14/evidence/${id}-full.png`,fullPage:true});
  rows.push({id,cards});
 }
 return rows;
}
