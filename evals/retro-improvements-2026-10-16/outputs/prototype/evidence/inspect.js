async (page) => {
 const results=[];
 const assert=(v,m)=>{if(!v)throw Error(m)};
 for(const width of [320,390]){
  await page.setViewportSize({width,height:844});
  for(const variant of ['A','B','C']){
   await page.goto('http://127.0.0.1:8769/?variant='+variant);
   assert(await page.locator('template').count()===3,'three variants');
   assert(await page.locator('#page a').getAttribute('href')==='#start','CTA destination');
   assert(await page.locator('#page a').innerText()==='Start reading','CTA text');
   assert((await page.locator('#page [role=status]').innerText()).includes('device'),'offline status');
   const measure=await page.evaluate(()=>({width:innerWidth,document:document.documentElement.scrollWidth,variant:document.documentElement.dataset.variant,headings:[...document.querySelectorAll('#page h1,#page h2')].map(x=>x.textContent)}));
   assert(measure.document<=width,'horizontal overflow');
   await page.screenshot({path:'evidence/'+variant+'-'+width+'.png',fullPage:true});
   const focus=[];
   for(let i=0;i<3;i++){await page.keyboard.press('Tab');focus.push(await page.evaluate(()=>document.activeElement.getAttribute('aria-label')||document.activeElement.textContent));}
   assert(focus[0]==='Start reading'&&focus[1]==='Previous variant'&&focus[2]==='Next variant','tab order');
   const next={A:'B',B:'C',C:'A'}[variant];
   await page.keyboard.press('Enter');
   assert(await page.locator('html').getAttribute('data-variant')===next,'Enter next');
   await page.keyboard.press('ArrowLeft');
   assert(await page.locator('html').getAttribute('data-variant')===variant,'arrow previous');
   await page.getByRole('button',{name:'Previous variant',exact:true}).click();
   const previous={A:'C',B:'A',C:'B'}[variant];
   await page.reload();
   assert(await page.locator('html').getAttribute('data-variant')===previous,'reload stable');
   results.push({...measure,focus,next,previous,reloadStable:true});
  }
 }
 assert(results.length===6,'matrix count');
 await page.goto('http://127.0.0.1:8769/?variant=C');
 await page.getByRole('link',{name:'Start reading'}).click();
 assert(page.url().endsWith('#start'),'CTA anchor');
 return {observedAt:new Date().toISOString(),browser:page.context().browser().version(),viewportKind:'desktop browser resized, not touch emulation',cases:results,ctaAnchor:true};
}
