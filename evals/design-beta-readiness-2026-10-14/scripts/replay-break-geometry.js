async (page) => {
 const result=[];
 for(const arm of ['original','paul']) {
  await page.setViewportSize({width:1280,height:720}); await page.goto(`http://127.0.0.1:48914/runs/break-${arm}/app/stress/`);
  if(await page.locator('.card').count()!==15)throw new Error('Expected 15 real cards');
  const geometry=await page.locator('.card').evaluateAll(es=>es.map(e=>({scenario:(e.parentElement.closest('section')||e.parentElement).innerText.slice(0,150),width:e.getBoundingClientRect().width,scrollWidth:e.scrollWidth,clientWidth:e.clientWidth,buttons:[...e.querySelectorAll('.queue-label')].map(b=>({text:b.textContent,right:b.getBoundingClientRect().right,parentRight:e.getBoundingClientRect().right,overflow:b.getBoundingClientRect().right>e.getBoundingClientRect().right+1}))})));
  result.push({arm,geometry});
 }
 return result;
}
