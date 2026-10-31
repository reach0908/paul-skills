async (page) => {
  const results = [];
  const assert = (value, message) => { if (!value) throw new Error(message); };
  const cases = [['state-machine', 'state', '__state', 30], ['variant', 'variant', '__variant', 3]];
  for (const [skill, prefix, param, count] of cases) {
    for (const [width, height] of [[1280, 800], [390, 844], [320, 450], [640, 400]]) {
      const record = {skill, width, height}; results.push(record);
      try {
        await page.setViewportSize({width, height});
        await page.goto(`http://127.0.0.1:8973/${skill}.html`);
        const buttons = page.locator(`[data-${prefix}]`);
        assert(await buttons.count() === count, 'wrong button count');
        assert(await page.locator('option').count() === count, 'wrong option count');
        const wide = width === 1280;
        assert(await page.locator('nav').isVisible() === wide, 'wrong list visibility');
        assert(await page.locator('select').isVisible() !== wide, 'wrong select visibility');
        await page.keyboard.press('Tab');
        record.firstFocus = await page.evaluate(() => document.activeElement.tagName);
        assert(record.firstFocus === (wide ? 'BUTTON' : 'SELECT'), 'not naturally keyboard reachable');
        record.focusOutline = await page.evaluate(() => getComputedStyle(document.activeElement).outlineStyle);
        assert(record.focusOutline !== 'none', 'missing focus indicator');
        await page.keyboard.press('ArrowDown');
        if (!wide) await page.keyboard.press('Enter');
        assert(await page.locator('select').inputValue() === 'choice-1', 'arrow did not select next choice');
        if (wide && count === 30) {
          for (let i=0;i<10;i++) await page.keyboard.press('ArrowDown');
          assert(await page.locator('select').inputValue() === 'choice-11', 'group crossing failed');
        }
        await page.locator('#draft').fill('preserved draft');
        await page.locator('#save').click();
        await page.keyboard.press('h');
        assert(!await page.locator('nav').isVisible() && !await page.locator('select').isVisible(), 'hide failed');
        await page.keyboard.press('h');
        if (wide) await buttons.last().click();
        else await page.locator('select').selectOption(`choice-${count-1}`);
        assert(await page.locator('#draft').inputValue() === 'preserved draft', 'lost draft');
        assert(await page.locator('#feedback').innerText() === 'Saved: preserved draft', 'lost task feedback');
        assert(new URL(page.url()).searchParams.get(param) === `choice-${count-1}`, 'URL disagrees');
        await page.setViewportSize({width: wide ? 390 : 1280, height});
        assert(await page.locator('select').inputValue() === `choice-${count-1}`, 'resize lost selection');
        await page.setViewportSize({width, height});
        record.geometry = await page.evaluate(() => ({scroll: document.documentElement.scrollWidth, client: document.documentElement.clientWidth, stage: document.querySelector('[class$="-stage"]').getBoundingClientRect().toJSON()}));
        assert(record.geometry.scroll <= record.geometry.client + 1, 'horizontal page overflow');
        assert(record.geometry.stage.x >= -1 && record.geometry.stage.right <= width+1, 'stage outside viewport');
        record.selected = await page.locator('select').inputValue();
        record.status = 'passed';
        if (width === 1280 || width === 320) await page.screenshot({path:`/private/tmp/paul-upstream-sync-20261022/browser/${skill}-${width}.png`});
      } catch (error) {
        record.status = 'failed'; record.error = String(error);
        return {status:'failed',results,browser:page.context().browser().version()};
      }
    }
  }
  assert(results.length === 8, 'incomplete case matrix');
  return {status:'passed',results,browser:page.context().browser().version(),limit:'CSS/HTML reference and authored interaction adapter only; no independent agent or human trial'};
}
