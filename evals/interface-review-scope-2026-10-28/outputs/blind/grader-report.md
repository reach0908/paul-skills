# Blind grader report (verbatim)

Fresh general-purpose subagent, claude-opus-5-5. It saw only R1.md to R6.md, diff.patch, context.txt and checklist.json in this folder, with no arm labels; mapping.json was revealed after this report.

---

Scoring summary: all six reports pass F1, F2, V and X. All six report the same set of change-caused findings. They differ only in how they package F1 and F3, in which pre-existing issue they list, and in a few small factual slips.

I checked the numbers against the diff and context. Contrast is 5.17:1 for white on #2563eb and 2.54:1 for white on #60a5fa. The grid is 5×160 + 4×12 = 848px, or 880px with 32px of padding. The usable column is 720 − 32 = 688px, and 288px at a 320px viewport. --space-3 and --space-4 are not shown in the diff, so 12px and 16px are taken from the reports.

**R1**
1. Grades:
   - F1 pass (HIGH): one token-level Regression covering the primary button and the pressed chip, 2.54:1.
   - F2 pass (HIGH): Regression, 848/880px against the 720px column (688px usable); notes horizontal scroll at 320px.
   - F3 pass (LOW): Introduced, raw 12px replaces the token; suggests --space-3.
   - V pass: Block.
   - X pass.
2. Other change-attributed findings: none. Pre-existing: HIGH, Accessibility, selected chip shown by color only (1.4.1, CategoryChips.css:20-23).
3. Factual errors: none. Minor: the F2 "After" cell holds the proposed fix, not the changed code.

**R2**
1. Grades:
   - F1 pass (HIGH, split per consumer): Colors Regression for the primary button, plus an Accessibility Regression for the pressed chip's text and border.
   - F2 pass (HIGH): Regression, 848/880px against 720px; scrolling at 320px.
   - F3 pass (LOW): Introduced.
   - V pass: Block.
   - X pass.
2. Other change-attributed findings: none (the chip Accessibility row is F1 per consumer). Pre-existing: HIGH, Accessibility, chip state by color only (1.4.1).
3. Factual errors:
   - It says fixed 160px tracks make long or translated labels "clipped". Button.css has no nowrap, so labels would wrap, not clip.
   - "Button's default variant is primary" cannot be verified, since Button.tsx is not in context.
   - In the F2 row, the Before cell shows the new code and the After cell shows the fix (mislabelled columns).

**R3**
1. Grades:
   - F1 pass (HIGH): one token-level Regression covering both consumers.
   - F2 pass (HIGH): Regression, 880px against 720px ("overflows by 160px", which is correct); 1.4.10 failure at 320px.
   - F3 pass (LOW): Introduced.
   - V pass: Block.
   - X pass.
2. Other change-attributed findings: none. Pre-existing: LOW, Accessibility, `role="status"` is rendered with its text already in place, so the announcement may be missed (Home.tsx:53; the line number is correct).
3. Factual errors: none.

**R4**
1. Grades:
   - F1 pass (HIGH): one token-level Regression.
   - F2 pass (HIGH): Regression, 848/880px against 720px; scrolling at 320px.
   - F3 pass (LOW): Introduced.
   - V pass: Block.
   - X pass.
2. Other change-attributed findings: none. Pre-existing: HIGH, Accessibility, chip state by color only (1.4.1). It notes the new accent actually separates the chip more from the text color.
3. Factual errors: it gives the contrast of #111827 against the old and new accent as 3.37 → 6.85. Computed, it is 3.43 → 6.98. The value of --color-text is not in the diff or context, so this assumes #111827. The direction of the claim is right, and it does not affect any graded item.

**R5**
1. Grades:
   - F1 pass (HIGH): one token-level Regression.
   - F2 pass (HIGH): Regression, 848px against 688px usable (288px at 320px).
   - F3 pass (severity: folded into F2, HIGH): the raw 12px bypassing --space-3 is mentioned inside F2's "Why", not as a separate finding. F3 allows any severity and is optional.
   - V pass: Block.
   - X pass.
2. Other change-attributed findings: none. Pre-existing: HIGH, Accessibility, chip state by color only (1.4.1).
3. Factual errors: none.

**R6**
1. Grades:
   - F1 pass (HIGH, split per consumer): two Colors Regressions, one for the primary button and one for the pressed chip's text and border.
   - F2 pass (HIGH): Regression, 880px against 720px; 1.4.10 failure at 320px.
   - F3 pass (LOW): Introduced.
   - V pass: Block.
   - X pass.
2. Other change-attributed findings: none (the second Colors row is F1 per consumer). Pre-existing: HIGH, Accessibility, chip state by color only (1.4.1).
3. Factual errors: none.

**Cross-report note**
- **Change-attributed findings:** none goes beyond F1 to F3, and no report misses a real change-caused issue that another found. The only differences are packaging:
  - R2 and R6 split F1 into two HIGH rows.
  - R1, R3, R4 and R5 report F1 as one token-level row.
  - R5 folds F3 into F2 instead of giving it its own row.
  - Every report also flags the pressed-chip border at 2.54:1 against the 3:1 threshold (1.4.11), as part of F1.
- **Pre-existing findings:** R1, R2, R4, R5 and R6 all report the chip state shown only by color (1.4.1). The CSS backs this up: only the border and text color change. R3 omits it and instead reports a LOW `role="status"` live-region issue that no other report has. That issue is plausible but cannot be confirmed from source alone. Neither difference affects the verdict, since both issues pre-date the change.
