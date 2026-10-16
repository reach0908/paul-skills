async (page) => {
  const results=[];
  for(const width of [390,1280]) {
    await page.setViewportSize({width,height:844});
    await page.goto('http://127.0.0.1:53825/?page=collection');
    await page.screenshot({path:`evidence/collection-default-after-${width}.png`,fullPage:true});
    results.push({width,height:844,route:page.url(),focus:await page.evaluate(()=>document.activeElement.tagName)});
  }
  return results;
}
