# S06 / gallery / r1: screen spec and first-impression check

**Inputs:** `BRIEF.md`, `index.html`, `capture.json` (route `index.html`, state `gallery`, r1, 1040×800) and `screen.png`. I didn't change any files.

## Screen spec

| Item | Content |
|---|---|
| Screen/state | S06 `gallery`. Per the brief, this is the only state built. |
| Purpose | Present the works and the ways into exploring them. |
| Intended first message | "ORBIT small exhibition 014: 불완전한 종이의 풍경, a digital collection of paper pieces." |
| Next action | Not applicable. This is a gallery, so it has no conversion CTA. The ways in are the "작품 목록" (works list) and "작가 소개" (artist) links. |
| Must keep | The paper collage, the 1° tilted yellow hero, the serif type, the yellow/brick/navy/kraft swatches, the asymmetric layout, and both links. |
| Content order | Exhibition label → title (h1) → one-line description → three-work strip in a thick border → two links |
| Mock boundary | `#works` and `#artist` have no matching section in the source. Since only this state was promised, I'm treating them as pending destinations, not broken links. |

## First-impression check (3 seconds)

- **Method:** I looked at the screenshot myself (an AI precheck, not timed). I already knew the intended message from the brief.
- **Fresh AI observation:** `not_run`.
- **Human 3-second test:** `not_run`. Neither browser nor extra participants were available.
- **What I predict a viewer sees:** the yellow hero and the large title stand out first, so the exhibition name and theme come across. The three swatches below read as "works." Both links are visible within the 800px-high first screen (at about y=670).
- **Result:** I found no mismatch with the intended message. The asymmetry and empty space are part of the approved direction, so I don't treat them as problems. **This is not a "3-second test passed" result.** It is a prediction.

## Suggested improvements (within the approved direction)

| Priority | Location | Evidence | Suggestion |
|---|---|---|---|
| Medium (not verified) | `index.html:2`, the h1's inline `font-size:64px` | An inline style overrides the `@media(max-width:600px){h1{font-size:30px}}` rule, so the title stays 64px on a narrow screen. The 26px hero padding plus 20px page margin may make the title overflow or wrap awkwardly at 320px. | Move the size into a class and use a smaller value under the existing media query. Keep the serif and the tilt. |
| Low | `index.html:2`, `nav` | The links sit below the strip and look like plain text links. They're visible, but they're the only ways in and they're visually weak. | Move them closer to the strip, or set them in the collage tone (e.g. a thick underline). Don't turn them into CTA buttons. |
| Note | The three swatch `div`s | They have no title or accessible name, so a screen reader can't tell which work each one is. Since they're placeholders, it's unclear whether this is in scope for this state. | When real images go in, add `alt` text and work titles. Hand this to the accessibility owner. |

## What I couldn't check

- **Rendering:** I only saw one 1040px screenshot. I haven't checked a narrow width, 320px, 200% zoom or RTL.
- **Interaction:** I haven't checked keyboard focus order, actual link movement or Back, because there was no browser.
- **Acceptance:** this is **rendered** only. Neither the behavior check nor user acceptance has been done.

**Still needs a decision:** whether the `#works`/`#artist` destination screens are in scope, and when the placeholder swatches get replaced with real works and titles.
