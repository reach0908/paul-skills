async (page) => {
  const results = [];
  const assert = (condition, message) => {if (!condition) throw new Error(message);};
  const styles = {};
  for (const width of [390, 1280]) {
    for (const route of ['library', 'collection']) {
      await page.setViewportSize({width, height:844});
      await page.goto(`http://127.0.0.1:53825/?page=${route}`);
      const section = route === 'library' ? '#topics' : '#related';
      assert(await page.locator(`${section} a.card`).count() === 2, `${route} expected 2 topic anchors`);
      const measured = await page.locator(`${section} a.card`).evaluateAll(elements=>elements.map(el=>{const s=getComputedStyle(el), r=el.getBoundingClientRect(); return {text:el.textContent, href:el.getAttribute('href'), padding:s.padding, radius:s.borderRadius, font:s.font, color:s.color, margin:s.margin, left:r.left, right:r.right, width:r.width};}));
      const overflow = await page.evaluate(()=>({scroll:document.documentElement.scrollWidth, client:document.documentElement.clientWidth}));
      assert(overflow.scroll<=overflow.client, `${route} horizontal overflow at ${width}`);
      measured.forEach(card=>assert(card.left>=0 && card.right<=width, 'Card exceeds viewport'));
      assert(measured[0].href==='?page=topic&id=design' && measured[1].href==='?page=topic&id=science', 'Wrong topic destinations');
      const visual = measured.map(({left,right,width,...rest})=>rest);
      if (route==='library') styles[width]=visual;
      else assert(JSON.stringify(styles[width])===JSON.stringify(visual), `Source/target mismatch at ${width}`);
      const focusPath=[];
      const initialFocus=await page.evaluate(()=>document.activeElement.tagName);
      for(let i=0;i<6;i++) {
        await page.keyboard.press('Tab');
        const focused=await page.evaluate(()=>({tag:document.activeElement.tagName,text:document.activeElement.textContent,href:document.activeElement.getAttribute('href')}));
        focusPath.push(focused);
        if(focused.href==='?page=topic&id=design') break;
      }
      assert(focusPath.at(-1).href==='?page=topic&id=design','Design unreachable with Tab');
      const focusStyle=await page.evaluate(()=>{const s=getComputedStyle(document.activeElement);return {outline:s.outline,offset:s.outlineOffset,visible:document.activeElement.matches(':focus-visible')};});
      assert(focusStyle.visible && focusStyle.outline.includes('3px'), 'Missing focus treatment');
      await page.keyboard.press('Tab');
      assert(await page.evaluate(()=>document.activeElement.getAttribute('href'))==='?page=topic&id=science','Science not next tab stop');
      await page.keyboard.press('Shift+Tab');
      assert(await page.evaluate(()=>document.activeElement.getAttribute('href'))==='?page=topic&id=design','Reverse order incorrect');
      await page.screenshot({path:`evidence/${route}-after-${width}.png`,fullPage:true});
      await page.keyboard.press('Enter');
      await page.waitForURL('**/?page=topic&id=design');
      assert(await page.locator('h1').innerText()==='Topic','Topic screen not reached');
      const designDestination=page.url();
      await page.goto(`http://127.0.0.1:53825/?page=${route}`);
      for(let i=0;i<6;i++) {await page.keyboard.press('Tab');if(await page.evaluate(()=>document.activeElement.getAttribute('href'))==='?page=topic&id=science') break;}
      assert(await page.evaluate(()=>document.activeElement.getAttribute('href'))==='?page=topic&id=science','Science unreachable');
      await page.keyboard.press('Enter');
      await page.waitForURL('**/?page=topic&id=science');
      results.push({route,width,height:844,measured,overflow,initialFocus,focusPath,focusStyle,designDestination,scienceDestination:page.url()});
    }
    await page.goto('http://127.0.0.1:53825/?page=library');
    assert(await page.locator('#recommendations button').count()===1,'Recommendation missing');
    await page.locator('#recommendations button').click();
    assert(await page.locator('#recommendations button').innerText()==='Profile: Morgan','Recommendation action changed');
  }
  assert(results.length===4,'Missing matrix case');
  return {observedAt:new Date().toISOString(),browser:page.context().browser().version(),completedCases:results.length,recommendationAction:'Profile: Morgan at both widths',results};
}
