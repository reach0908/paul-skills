## Scope

| Field | Value |
| --- | --- |
| Target | `staged` |
| Base ref | `HEAD` at `eabf6a77bcb748b855f8f0dea909408814930115` |
| Head ref | Index snapshot |
| Commits | 0 committed, 3 files staged |
| Files in scope | 2 after exclusions (`src/CloseControl.tsx`, `src/LegacyCard.tsx`) |
| Excluded | `pnpm-lock.yaml` (lockfile) |
| Surfaces expanded | `Dialog` (direct consumer of `CloseControl`); no further consumers |

The working tree also restores `src/CloseControl.tsx` to a button, but that edit is unstaged and outside this review.

## Coverage

| Domain | Evidence inspected | Result |
| --- | --- | --- |
| Accessibility | better-accessibility loaded; `git diff --cached HEAD`, `git show :src/CloseControl.tsx`, `src/Dialog.tsx` | 1 finding |
| Layout | better-layout loaded; staged hunks for both files | Clear |
| Writing | better-writing loaded; `LegacyCard` copy change | Clear |
| Typography | better-typography loaded; staged hunks | Clear |
| Color | better-colors loaded; staged hunks | Clear |
| UI | better-ui loaded; staged hunks | Clear |

## Findings

| Severity | Domain | Status | Location | Before | After | Why |
| --- | --- | --- | --- | --- | --- | --- |
| MEDIUM | Layout | Regression | `src/LegacyCard.tsx:3` (index) | `style={{ width: 480 }}` | Use `max-inline-size: 30rem` | This change introduced a fixed 480px width that overflows narrow screens |
| HIGH | Accessibility | Regression | `src/CloseControl.tsx:5` (index) | `<button type="button" ... onClick={onClose}>` | Restore the native `<button type="button">` | The `div` with `onClick` is not focusable and has no keyboard activation, so keyboard users can no longer close the dialog |


## Verification

- Passed: read the staged diff with `git diff --cached HEAD` and the index files with `git show :path`.
- Not verified: browser rendering, keyboard interaction and screen-reader output. This was a source-based review and no rendered check was requested.

## Verdict

Block: one HIGH finding remains in the staged change.
