async (page) => {
  const mutation = null;
  const results = [];
  const assert = (value, message) => { if (!value) throw new Error(message); };
  const cases = [['state-machine', 'state', '__state', 30, 'Data 2:'], ['variant', 'variant', '__variant', 3, 'Density 2:']];
  const errors = [];
  page.on('pageerror', error => errors.push(String(error)));
  for (const [skill, prefix, param, count, label] of cases) {
    for (const [width, height] of [[1280, 800], [390, 844], [320, 450], [640, 400]]) {
      const record = {skill, width, height, focusPath: []}; results.push(record);
      try {
        await page.setViewportSize({width, height});
        await page.goto(`http://127.0.0.1:8973/${skill}.html`);
        // Each negative control mutates one case, independently of assertions.
        if (mutation && skill === 'state-machine' && width === 390) {
          await page.evaluate(kind => {
            if (kind === 'missing-option') document.querySelector('option').remove();
            if (kind === 'no-tab') document.querySelector('select').tabIndex = -1;
            if (kind === 'blocked-keys') document.querySelector('select').addEventListener('keydown', e => { if (e.key !== 'Tab' && e.key !== 'Shift') e.preventDefault(); });
            if (kind === 'overflow') document.querySelector('[class$="-stage"]').style.minWidth = '1500px';
          }, mutation);
        }
        const buttons = page.locator(`[data-${prefix}]`);
        const select = page.locator('select');
        const wide = width === 1280;
        assert(await buttons.count() === count, 'wrong button count');
        assert(await page.locator('option').count() === count, 'wrong option count');
        assert(await page.locator('optgroup').count() === (count === 30 ? 3 : 1), 'wrong group count');
        assert(await page.locator('nav').isVisible() === wide, 'wrong list visibility');
        assert(await select.isVisible() !== wide, 'wrong select visibility');
        record.initialFocus = await page.evaluate(() => document.activeElement.tagName);
        assert(record.initialFocus === 'BODY', 'navigation restored old focus');
        const focus = async () => {
          const value = await page.evaluate(() => ({tag:document.activeElement.tagName,id:document.activeElement.id,data:document.activeElement.dataset,outline:getComputedStyle(document.activeElement).outlineStyle}));
          record.focusPath.push(value); return value;
        };
        await page.keyboard.press('Tab');
        let current = await focus();
        assert(current.tag === (wide ? 'BUTTON' : 'SELECT'), 'not naturally keyboard reachable');
        assert(current.outline !== 'none', 'missing focus indicator');
        await page.keyboard.press('Tab');
        current = await focus();
        assert(wide ? current.data[prefix] === 'choice-1' : current.id === 'draft', 'wrong forward Tab order');
        await page.keyboard.press('Shift+Tab');
        current = await focus();
        assert(wide ? current.data[prefix] === 'choice-0' : current.tag === 'SELECT', 'wrong reverse Tab order');
        if (wide) {
          await page.keyboard.press('Tab');
          await page.keyboard.press('Enter');
          record.activation = 'Tab to second list button, Enter';
        } else {
          await page.evaluate(() => {
            window.nativeEvents = [];
            for (const type of ['input', 'change']) document.querySelector('select').addEventListener(type, e => window.nativeEvents.push({type,value:e.target.value,trusted:e.isTrusted}));
          });
          await page.keyboard.type(label);
          await page.keyboard.press('Enter');
          await page.keyboard.press('Escape');
          record.activation = `native type-ahead ${label}, Enter, Escape`;
          record.nativeEvents = await page.evaluate(() => window.nativeEvents);
          assert(record.nativeEvents.some(e => e.type === 'change' && e.value === 'choice-1' && e.trusted), 'native keyboard change missing');
        }
        assert(await select.inputValue() === 'choice-1', 'keyboard did not select next choice');
        assert(new URL(page.url()).searchParams.get(param) === 'choice-1', 'keyboard selection missing from URL');
        // Reach the product input with real Tab, without programmatic focus.
        let steps = 0;
        while (await page.evaluate(() => document.activeElement.id) !== 'draft' && steps++ < count + 2) await page.keyboard.press('Tab');
        assert(await page.evaluate(() => document.activeElement.id) === 'draft', 'product input unreachable');
        await page.locator('#draft').fill('preserved draft');
        await page.keyboard.press('ArrowDown');
        await page.keyboard.press('h');
        assert(await select.inputValue() === 'choice-1', 'shortcut stole input key');
        assert(await page.locator(wide ? 'nav' : 'select').isVisible(), 'input H hid controls');
        await page.locator('#draft').fill('preserved draft');
        await page.keyboard.press('Tab');
        assert((await focus()).id === 'save', 'save button unreachable');
        await page.keyboard.press('Enter');
        assert(await page.locator('#feedback').innerText() === 'Saved: preserved draft', 'keyboard save failed');
        await page.keyboard.press('h');
        assert(!await page.locator('nav').isVisible() && !await select.isVisible(), 'hide failed');
        await page.keyboard.press('h');
        assert(await page.locator(wide ? 'nav' : 'select').isVisible(), 'restore failed');
        for (const [key, expected] of [['ArrowDown',2], ['ArrowUp',1], ['ArrowRight',2], ['ArrowLeft',1]]) {
          await page.keyboard.press(key);
          assert(await select.inputValue() === `choice-${expected}`, `global ${key} failed`);
        }
        await page.keyboard.press('Control+ArrowDown');
        assert(await select.inputValue() === 'choice-1', 'shortcut stole modified key');
        record.visited = [];
        for (let i=0;i<count;i++) {
          await page.keyboard.press('ArrowDown');
          const expected = `choice-${(i+2)%count}`;
          assert(await select.inputValue() === expected, 'list-order traversal failed');
          assert(await page.locator('#active').innerText() === expected, 'component selection disagrees');
          assert(await page.locator(`[data-${prefix}="${expected}"]`).getAttribute('aria-pressed') === 'true', 'pressed state disagrees');
          record.visited.push(expected);
        }
        assert(new Set(record.visited).size === count, 'incomplete state coverage');
        assert(await page.locator('#draft').inputValue() === 'preserved draft', 'lost draft');
        assert(await page.locator('#feedback').innerText() === 'Saved: preserved draft', 'lost task feedback');
        const before = await select.inputValue();
        await page.setViewportSize({width:wide?390:1280,height});
        assert(await select.inputValue() === before, 'resize lost selection');
        assert(await page.locator('#draft').inputValue() === 'preserved draft', 'resize lost draft');
        await page.setViewportSize({width,height});
        record.geometry = await page.evaluate(() => ({scroll:document.documentElement.scrollWidth,client:document.documentElement.clientWidth,stage:document.querySelector('[class$="-stage"]').getBoundingClientRect().toJSON()}));
        assert(record.geometry.scroll <= record.geometry.client + 1, 'horizontal page overflow');
        assert(record.geometry.stage.x >= -1 && record.geometry.stage.right <= width+1, 'stage outside viewport');
        if (wide) {
          await buttons.last().click();
          assert(await select.inputValue() === `choice-${count-1}`, 'pointer selection failed');
          record.listScroll = await page.locator('nav').evaluate(el => el.scrollTop);
          if (count === 30) assert(record.listScroll > 0, 'long list did not scroll');
        }
        record.selected = await select.inputValue();
        assert(new URL(page.url()).searchParams.get(param) === record.selected, 'URL disagrees');
        const saved = page.url();
        await page.goto(saved);
        assert(await select.inputValue() === record.selected, 'shared URL did not restore selection');
        assert(errors.length === 0, 'browser runtime error');
        record.status = 'passed';
        if (!mutation && (width === 1280 || width === 320)) await page.screenshot({path:`/private/tmp/paul-keyboard-20261022/browser/${skill}-${width}.png`});
      } catch (error) {
        record.status = 'failed'; record.error = String(error);
      }
    }
  }
  assert(results.length === 8, 'incomplete case matrix');
  return {status:results.every(r=>r.status==='passed')?'passed':'failed',mutation,results,errors,browser:page.context().browser().version(),observedAt:new Date().toISOString(),limit:'Extracted HTML/CSS and authored interaction adapter; desktop Chrome, no independent agent, human, physical-device or browser-zoom trial'};
}
