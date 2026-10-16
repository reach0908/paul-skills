async (page) => {
  const results = [];
  for (const width of [390, 1280]) {
    await page.setViewportSize({width, height: 844});
    await page.goto('http://127.0.0.1:53825/?page=library');
    await page.screenshot({path:`evidence/library-before-${width}.png`, fullPage:true});
    results.push(await page.evaluate(() => ({route:location.search, width:innerWidth, cards:[...document.querySelectorAll('#topics .card')].map(el=>{ const s=getComputedStyle(el); return {text:el.textContent, tag:el.tagName, href:el.getAttribute('href'), padding:s.padding, radius:s.borderRadius, font:s.font, color:s.color, margin:s.margin}; }), recommended:document.querySelector('#recommendations').outerHTML})));
    await page.goto('http://127.0.0.1:53825/?page=collection');
    await page.screenshot({path:`evidence/collection-before-${width}.png`, fullPage:true});
  }
  return {browser:page.context().browser().version(), observedAt:new Date().toISOString(), results};
}
