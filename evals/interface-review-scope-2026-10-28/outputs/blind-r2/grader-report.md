# Blind grader report, main vs branch r2 (verbatim)

A fresh general-purpose subagent (claude-opus-5-5), separate from the r1 grader. It saw only R1.md to R6.md, diff.patch, context.txt and checklist.json in this folder, with no arm labels. IDs were shuffled with random.Random(202610282), and mapping.json was revealed after this report.

---

All six reports reach Block, and all six pass F1, F2, F3, V and X. They differ in their Pre-existing findings, their table formatting, and a few small factual slips. Line references I could check against diff.patch and context.txt are all correct (tokens.css:6, Button.css:10-11, CategoryChips.css:20-23, Home.css:2, Home.tsx:8/46/53). context.txt does not include Toolbar.tsx, Button.tsx, the `--color-text` value or `--space-3/4`, so claims resting on those cannot be checked.

**R1**
1. 
   - F1 pass (HIGH): one token-level row; white on button and pressed chip both 2.54:1.
   - F2 pass (HIGH): 880px against the 720px column, scroll at 320px.
   - F3 pass (LOW): own row, raw 12px should be `var(--space-3)`.
   - V pass: Block.
   - X pass.
2. No other change-attributed findings. Pre-existing: HIGH Accessibility, selected chip shown by color only (1.4.1).
3. Its Pre-existing row says the change "weakened the color difference". That is only half true. Selected border against unselected border drops from 4.17 to 2.05. Selected text against `#111827` text rises from 3.43 to 6.98.

**R2**
1. 
   - F1 pass (HIGH): split per consumer into two HIGH Regression rows (button, chip).
   - F2 pass (HIGH).
   - F3 pass (LOW): own row.
   - V pass: Block, counted as "3 HIGH" because F1 is split.
   - X pass.
2. No other change-attributed findings. Pre-existing:
   - HIGH Accessibility, chip state shown by color only (1.4.1).
   - LOW Accessibility, filter group is an unlabelled `div` (Toolbar.tsx:13). Cannot check, the file is not in context.
3. No verifiable errors. The claim that `Button`'s default variant is primary cannot be checked.

**R3**
1. 
   - F1 pass (HIGH): one token row.
   - F2 pass (HIGH).
   - F3 pass (LOW): own row.
   - V pass: Block.
   - X pass.
2. No other change-attributed findings. Pre-existing: HIGH Accessibility, chip state shown by color only (1.4.1).
3. Its `#111827`-against-accent ratios are slightly wrong. It gives 3.37 to 6.85; the correct values are 3.43 to 6.98.

**R4**
1. 
   - F1 pass (HIGH): one token row, both consumers spelled out.
   - F2 pass (HIGH): also gives the 688px content box.
   - F3 pass (LOW): own row.
   - V pass: Block.
   - X pass.
2. No other change-attributed findings. Pre-existing: HIGH Accessibility, chip state shown by color only (1.4.1).
3. It says horizontal scrolling starts below 880px. Because `.home` is centered with a 720px max-width and the grid overflows to the right, page scrolling starts below roughly 1008 to 1040px, not 880px. Minor.

**R5**
1. 
   - F1 pass (HIGH): one token row.
   - F2 pass (HIGH).
   - F3 pass (LOW): own row.
   - V pass: Block.
   - X pass.
2. No other change-attributed findings. Pre-existing: LOW Accessibility, the `role="status"` element mounts already holding its text (Home.tsx:53), so screen readers may miss the announcement. This is real and the line number is correct.
3. No factual errors. Format problem: in the F1 and F2 rows the "After" column holds the new code, and the recommended fix sits in "Why". It misses the color-only chip state (1.4.1) Pre-existing finding that R1 to R4 report.

**R6**
1. 
   - F1 pass (HIGH): one token row.
   - F2 pass (HIGH).
   - F3 pass (LOW): own row.
   - V pass: Block.
   - X pass.
2. No other change-attributed findings. Pre-existing: none, it explicitly says there are none.
3. 
   - Its contrast numbers are correct (3.43 and 6.98).
   - "State distinction did not weaken" ignores the border cue, which drops from 4.17 to 2.05 against the unselected `#e5e7eb` border.
   - It calls CategoryChips a sibling "in the same row". It is a separate block below the toolbar. Minor.
   - It misses the color-only chip state (1.4.1) Pre-existing finding.

**Cross-report note**
- **Change-attributed findings:** identical across all six. Each has F1 (HIGH Regression), F2 (HIGH Regression) and F3 (LOW Introduced, own row). The only structural difference is that R2 splits F1 into two per-consumer rows. No report has an extra change-attributed finding and none misses a real one.
- **Pre-existing findings:**
  - Color-only selected chip (1.4.1): R1 to R4 report it, R5 and R6 miss it. It is real, since the pressed state changes only `border-color` and `color`.
  - Unlabelled toolbar group: R2 only, cannot be checked from context.
  - `role="status"` mounted with its text: R5 only. It is real and the other five miss it.
- **Shared imprecision:** all six reports' handling of how the accent change affects the chip's state cue is incomplete. R3 and R6 look only at text against text (stronger). R1 and R4 look only at the weaker cue against white or the border.
