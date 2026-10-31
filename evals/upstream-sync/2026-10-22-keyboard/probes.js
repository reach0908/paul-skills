async (page) => {
  const results=[];
  for(const keys of [['ArrowDown','Enter'],['Space','ArrowDown','Enter'],['ArrowDown','ArrowDown','Enter'],['b','Enter'],['Alt+ArrowDown','ArrowDown','Enter']]) {
    await page.goto('about:blank');
    await page.setContent('<select aria-label="Choice"><option value="a">Alpha</option><option value="b">Bravo</option></select>');
    await page.evaluate(()=>{window.events=[];for(const type of ['keydown','input','change'])document.addEventListener(type,e=>window.events.push({type,key:e.key,value:e.target.value,prevented:e.defaultPrevented,trusted:e.isTrusted}));});
    await page.keyboard.press('Tab');
    for(const key of keys) await page.keyboard.press(key);
    results.push({keys,actual:await page.locator('select').inputValue(),events:await page.evaluate(()=>window.events)});
  }
  await page.goto('about:blank');
  await page.setContent('<select><option value="a">Alpha</option><option value="b">Bravo</option></select>');
  await page.keyboard.press('Tab');
  await page.keyboard.press('ArrowDown');
  await page.waitForTimeout(500);
  await page.keyboard.press('Enter');
  await page.waitForTimeout(500);
  results.push({keys:['ArrowDown','500ms','Enter','500ms'],actual:await page.locator('select').inputValue()});
  return {results,browser:page.context().browser().version()};
}
