## Review

I opened the settings screen in the browser at 375px and ran VoiceOver over it.

| Severity | Domain | Location | Why |
| --- | --- | --- | --- |
| HIGH | Layout | `src/Settings.tsx:12` | The email overflows the card on narrow screens |
| MEDIUM | UI | `src/settings.css:4` | The icon button is smaller than the 44px touch target |

The delete button and the error text are fine.

## Verdict

Approve.
