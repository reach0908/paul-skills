async (page) => {
  const url = 'http://127.0.0.1:48827/';
  const session = 'saved-materials-prestarted';
  const viewportHeight = 900;
  const viewportWidths = [1440, 390, 320];
  const maxTabPresses = 6;
  const expectedMaterials = [
    {
      id: 'one',
      buttonName: '첫 기능 정하기 열기',
      detail: '해결할 불편 하나에서 시작해요.',
    },
    {
      id: 'two',
      buttonName: '변경 이력 남기기 열기',
      detail: '다시 돌아갈 수 있도록 기록해요.',
    },
    {
      id: 'three',
      buttonName: '완성한 화면 확인하기 열기',
      detail: '다양한 화면과 조작 방법으로 확인해요.',
    },
  ];

  const describeFocus = async () =>
    page.evaluate(() => {
      const element = document.activeElement;
      if (!(element instanceof HTMLElement)) return null;
      const style = getComputedStyle(element);
      const rect = element.getBoundingClientRect();
      return {
        tag: element.tagName,
        text:
          element.tagName === 'BODY'
            ? '<body>'
            : (element.innerText || element.getAttribute('aria-label') || '')
                .trim()
                .replace(/\s+/g, ' ')
                .slice(0, 80),
        dataId: element.getAttribute('data-id'),
        tabIndex: element.tabIndex,
        focusVisiblePseudo: element.matches(':focus-visible'),
        outlineStyle: style.outlineStyle,
        outlineWidth: style.outlineWidth,
        outlineColor: style.outlineColor,
      };
    });

  const hasVisibleFocus = (focus) =>
    Boolean(
      focus &&
        focus.focusVisiblePseudo &&
        focus.outlineStyle !== 'none' &&
        Number.parseFloat(focus.outlineWidth) > 0,
    );

  const settle = async () => {
    await page.waitForLoadState('networkidle');
    await page.evaluate(
      () => new Promise((resolve) => requestAnimationFrame(() => requestAnimationFrame(resolve))),
    );
  };

  const measureLayout = async () =>
    page.evaluate(() => {
      const root = document.documentElement;
      const cards = document.querySelector('.cards');
      const articles = [...document.querySelectorAll('article')];
      const viewportWidth = root.clientWidth;
      const rectFor = (element) => {
        const rect = element.getBoundingClientRect();
        return {
          left: Number(rect.left.toFixed(2)),
          right: Number(rect.right.toFixed(2)),
          width: Number(rect.width.toFixed(2)),
        };
      };
      const visibleOverflowingElements = [...document.querySelectorAll('body *')]
        .filter((element) => {
          const style = getComputedStyle(element);
          const rect = element.getBoundingClientRect();
          return (
            style.display !== 'none' &&
            style.visibility !== 'hidden' &&
            rect.width > 0 &&
            (rect.left < 0 || rect.right > viewportWidth)
          );
        })
        .map((element) => ({
          tag: element.tagName,
          className: element.className || null,
          rect: rectFor(element),
        }));

      return {
        documentClientWidth: viewportWidth,
        documentScrollWidth: root.scrollWidth,
        bodyScrollWidth: document.body.scrollWidth,
        cards: rectFor(cards),
        articles: articles.map(rectFor),
        visibleOverflowingElements,
      };
    });

  const report = {
    metadata: {
      url,
      session,
      observedAt: new Date().toISOString(),
      requestedViewports: viewportWidths.map((width) => ({ width, height: viewportHeight })),
      expectedMaterialCount: expectedMaterials.length,
      maxTabPresses,
      browserVersion: await page.context().browser().version(),
      userAgent: await page.evaluate(() => navigator.userAgent),
    },
    keyboardCases: [],
    horizontalOverflowCases: [],
  };

  for (const width of viewportWidths) {
    for (let materialIndex = 0; materialIndex < expectedMaterials.length; materialIndex += 1) {
      const material = expectedMaterials[materialIndex];
      const result = {
        case: `keyboard-${width}-${material.id}`,
        requestedViewport: { width, height: viewportHeight },
        targetId: material.id,
        buttonName: material.buttonName,
        status: 'fail',
        focusPath: [],
        assertions: [],
      };

      try {
        await page.setViewportSize({ width, height: viewportHeight });
        await page.goto(url, { waitUntil: 'domcontentloaded' });
        await settle();
        result.actualViewport = page.viewportSize();
        result.initialFocus = await describeFocus();

        const materialCount = await page.locator('[data-id]').count();
        result.materialCount = materialCount;
        if (materialCount !== expectedMaterials.length) {
          throw new Error(
            `Expected ${expectedMaterials.length} materials, found ${materialCount}`,
          );
        }
        result.assertions.push('material count is exactly 3');

        let targetFocus = null;
        for (let step = 1; step <= maxTabPresses; step += 1) {
          await page.keyboard.press('Tab');
          const focus = await describeFocus();
          result.focusPath.push({ step, ...focus });
          if (focus && focus.dataId === material.id) {
            targetFocus = focus;
            break;
          }
        }
        if (!targetFocus) {
          throw new Error(
            `Target ${material.id} was not reached within ${maxTabPresses} real Tab presses`,
          );
        }
        result.assertions.push('target is reachable with real Tab presses');

        if (!hasVisibleFocus(targetFocus)) {
          throw new Error(`Target ${material.id} lacks a visible keyboard focus indicator`);
        }
        result.assertions.push('target has a visible focus indicator');

        if (materialIndex > 0) {
          await page.keyboard.press('Shift+Tab');
          result.shiftTabFocus = await describeFocus();
          const expectedPreviousId = expectedMaterials[materialIndex - 1].id;
          if (result.shiftTabFocus.dataId !== expectedPreviousId) {
            throw new Error(
              `Shift+Tab from ${material.id} expected ${expectedPreviousId} but reached ${result.shiftTabFocus.dataId || result.shiftTabFocus.tag}`,
            );
          }
          await page.keyboard.press('Tab');
          result.restoredTargetFocus = await describeFocus();
          if (result.restoredTargetFocus.dataId !== material.id) {
            throw new Error(`Tab did not restore focus to ${material.id}`);
          }
          result.assertions.push('Shift+Tab and Tab preserve the expected material order');
        } else {
          result.shiftTabCheck = 'not applicable: first scoped material has no previous scoped material';
        }

        await page.keyboard.press('Enter');
        const dialog = page.locator('dialog');
        result.openState = {
          open: await dialog.evaluate((element) => element.open),
          title: await dialog.locator('#detail-title').textContent(),
          detail: await dialog.locator('#detail-content').textContent(),
          focus: await describeFocus(),
          layout: await page.evaluate(() => ({
            documentClientWidth: document.documentElement.clientWidth,
            documentScrollWidth: document.documentElement.scrollWidth,
          })),
        };
        if (!result.openState.open) {
          throw new Error(`Enter on ${material.id} did not open the detail dialog`);
        }
        if (result.openState.detail !== material.detail) {
          throw new Error(
            `Detail mismatch for ${material.id}: ${JSON.stringify(result.openState.detail)}`,
          );
        }
        result.assertions.push('Enter opens the matching detail dialog');

        let closeFocus = result.openState.focus;
        const closeFocusPath = [];
        for (let step = 1; closeFocus?.text !== '닫기' && step <= 3; step += 1) {
          await page.keyboard.press('Tab');
          closeFocus = await describeFocus();
          closeFocusPath.push({ step, ...closeFocus });
        }
        if (closeFocusPath.length > 0) result.closeFocusPath = closeFocusPath;
        if (closeFocus?.text !== '닫기' || !hasVisibleFocus(closeFocus)) {
          throw new Error('Dialog close control was not keyboard reachable with visible focus');
        }

        await page.keyboard.press('Enter');
        result.closedState = {
          open: await dialog.evaluate((element) => element.open),
          focus: await describeFocus(),
        };
        if (result.closedState.open) {
          throw new Error('Enter on the close control did not close the dialog');
        }
        if (result.closedState.focus.dataId !== material.id) {
          throw new Error(`Focus was not restored to opener ${material.id}`);
        }
        result.assertions.push('Enter closes the dialog and restores focus to its opener');
        result.status = 'pass';
      } catch (error) {
        result.error = error instanceof Error ? error.message : String(error);
      }

      report.keyboardCases.push(result);
    }

    const overflowResult = {
      case: `horizontal-overflow-${width}`,
      requestedViewport: { width, height: viewportHeight },
      status: 'fail',
      assertions: [],
    };
    try {
      await page.setViewportSize({ width, height: viewportHeight });
      await page.goto(url, { waitUntil: 'domcontentloaded' });
      await settle();
      overflowResult.actualViewport = page.viewportSize();
      overflowResult.materialCount = await page.locator('[data-id]').count();
      if (overflowResult.materialCount !== expectedMaterials.length) {
        throw new Error(
          `Expected ${expectedMaterials.length} materials, found ${overflowResult.materialCount}`,
        );
      }
      overflowResult.assertions.push('material count is exactly 3 before measurement');
      overflowResult.measurements = await measureLayout();
      const measurements = overflowResult.measurements;
      if (measurements.documentScrollWidth > measurements.documentClientWidth) {
        throw new Error(
          `Document scroll width ${measurements.documentScrollWidth}px exceeds client width ${measurements.documentClientWidth}px`,
        );
      }
      if (
        measurements.cards.left < 0 ||
        measurements.cards.right > measurements.documentClientWidth
      ) {
        throw new Error(
          `Cards bounds [${measurements.cards.left}, ${measurements.cards.right}] exceed viewport [0, ${measurements.documentClientWidth}]`,
        );
      }
      if (measurements.visibleOverflowingElements.length > 0) {
        throw new Error(
          `${measurements.visibleOverflowingElements.length} visible element(s) exceed the viewport`,
        );
      }
      overflowResult.assertions.push('document, list, cards, and visible descendants fit viewport');
      overflowResult.status = 'pass';
    } catch (error) {
      overflowResult.error = error instanceof Error ? error.message : String(error);
    }
    report.horizontalOverflowCases.push(overflowResult);
  }

  const allCases = [...report.keyboardCases, ...report.horizontalOverflowCases];
  report.summary = {
    expectedCaseCount: viewportWidths.length * (expectedMaterials.length + 1),
    completedCaseCount: allCases.length,
    passed: allCases.filter((result) => result.status === 'pass').length,
    failed: allCases.filter((result) => result.status === 'fail').length,
    failedCases: allCases
      .filter((result) => result.status === 'fail')
      .map((result) => ({ case: result.case, error: result.error })),
  };

  if (report.summary.completedCaseCount !== report.summary.expectedCaseCount) {
    throw new Error(`CASE_MATRIX_INCOMPLETE\n${JSON.stringify(report, null, 2)}`);
  }
  if (report.summary.failed > 0) {
    throw new Error(`QA_ASSERTION_FAILURE\n${JSON.stringify(report, null, 2)}`);
  }

  return report;
}
