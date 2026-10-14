async(page)=>{
 const results=[];
 for(const arm of ['original','paul'])for(const width of [1280,320])for(const variant of ['airy','balanced','compact']){
  await page.goto('about:blank');await page.setViewportSize({width,height:width===1280?900:450});
  await page.goto(`http://127.0.0.1:48914/runs/variant-${arm}/app/?__variant=${variant}`);
  const initial=await page.evaluate(()=>({scrollY,active:document.activeElement.tagName}));const path=[],seen=new Set();
  for(let i=0;i<18&&seen.size<12;i++){
   await page.keyboard.press('Tab');
   const row=await page.evaluate(()=>{const e=document.activeElement,r=e.getBoundingClientRect(),p=document.querySelector('.variant-picker'),q=p.getBoundingClientRect(),interactive=e.matches('a[href],button,input,textarea,select');return {id:e.id||e.dataset.variant||(interactive?e.textContent.trim():e.tagName),interactive,overlap:interactive&&!p.contains(e)&&r.left<q.right&&r.right>q.left&&r.top<q.bottom&&r.bottom>q.top,visible:r.left>=0&&r.right<=innerWidth+1&&r.top>=0&&r.bottom<=innerHeight+1,outline:getComputedStyle(e).outlineStyle,rect:{top:r.top,bottom:r.bottom,left:r.left,right:r.right},scrollY};});
   path.push(row);if(row.interactive)seen.add(row.id);
  }
  results.push({arm,width,variant,initial,path,uniqueControls:seen.size});
 }
 return results;
}
