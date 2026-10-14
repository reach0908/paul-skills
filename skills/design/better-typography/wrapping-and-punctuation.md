# Wrapping and punctuation

Line length, typographic characters and mixed-direction text.

## Measure (line length)

One `ch` is the advance width of the `0` in the current font, not a count of arbitrary glyphs. A `65ch` container does not guarantee 65 visible characters. The Latin-text 60–75 character starting range often lands near `560px` to `680px` at a `16px` body size, depending on the face and content. Recheck real lines when font, language or size changes. Korean and mixed-script examples are in [korean-text.md](korean-text.md).

## Smart punctuation

Apply the product's language and punctuation policy. The options below explain typographic effects; use them when that policy calls for them. Preserve intentional plain punctuation, code, URLs and identifiers. For a reported inconsistency, name the policy and the affected text.

| Source form | Policy-dependent option |
| --- | --- |
| Straight quotes `"..."` | Curly quotes that curve around the text (keep straight quotes in code) |
| Hyphen in ranges | En dash: `2010–2020` |
| Two hyphens for an aside | The product's punctuation policy; a separate sentence is an option |
| Three periods `...` | The single ellipsis character `…` |
| Regular space in `10 km` | `&nbsp;` so the value never breaks apart |
| Uncontrolled word breaks | `&shy;` to mark where a word may break, or `hyphens: auto` with the correct `lang` |

## Internationalization

- **Long paragraphs align by their own language.** A one- or two-line snippet follows the surrounding UI's direction. A paragraph of three or more lines aligns to its own script instead, so an English paragraph stays start-aligned LTR even inside an RTL interface. `text-align: start` with the correct `lang` and `dir` on the paragraph element handles this.
- **Digits keep their order.** A phone number or "541" reads identically in RTL, because the Unicode bidi algorithm keeps digit runs left to right. `<bdi>` repairs a value whose order adjacent RTL text disturbs.
