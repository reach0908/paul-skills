async (page) => {
  await page.goto('about:blank');
  await page.setContent('<select aria-label="Choice"><option value="a">Alpha</option><option value="b">Bravo</option></select>');
  await page.keyboard.press('Tab');
  const focus = await page.evaluate(() => document.activeElement.tagName);
  await page.keyboard.press('ArrowDown');
  await page.keyboard.press('Enter');
  const actual = await page.locator('select').inputValue();
  return {focus,expected:'b',actual,status:actual==='b'?'passed':'failed',browser:page.context().browser().version()};
}
