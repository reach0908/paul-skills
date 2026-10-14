# 기록 UI conventions

This is a synthetic Korean export-history UI. It simulates success/failure with a timer and updates the completed job count. It does not create actual files, persist data or enforce real server permissions. Reload resets the counter. A filename containing fail, or a blank filename, gives a mock failure.

Keep plain HTML/CSS/JS, the system font, existing tokens, and a flat style. Korean sentences use 해요체. Action labels use natural Korean object/action order. Literal straight quotes and three periods are intentional product punctuation, including UI messages. Keep filenames and code identifiers intact. A typography review should assess the rendered interface without replacing those deliberate choices.

The full-record action is visibly unavailable to this ordinary-member fixture. Its button must not initiate work by pointer or keyboard. There is no framework, test runner or screen-reader harness. Inspect at 1280x900, 390x844 and 320x844.
