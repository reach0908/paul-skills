async (page) => {
 const rows=[];
 for(const file of ['index','detail'])for(const width of [1280,390])for(const theme of ['light','dark']){
  await page.setViewportSize({width,height:width===1280?900:844});
  await page.goto(`http://127.0.0.1:48914/runs/explain-interface-paul/app/${file}.html`);
  if(theme==='dark') await page.locator('#theme').click();
  rows.push({file,width,theme,measured:await page.evaluate(()=>{const c=s=>getComputedStyle(document.querySelector(s));return {surface:c('body').backgroundColor,ink:c('body').color,padding:c('main').padding,title:c('h1').fontSize,grid:document.querySelector('.site-grid')?c('.site-grid').gridTemplateColumns:null,overflow:document.documentElement.scrollWidth>innerWidth,blocked:[...document.styleSheets].flatMap(s=>{try{void s.cssRules;return []}catch(e){return [{url:s.href,error:e.name}]}})};})});
 }
 await page.goto('http://127.0.0.1:48914/runs/explain-interface-paul/app/index.html');
 const buttons=await page.getByRole('button').allTextContents();
 return {rows,buttons};
}
