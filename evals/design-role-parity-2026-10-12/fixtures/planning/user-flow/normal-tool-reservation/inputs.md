# Accepted inputs
PM revision TL-PM-9; destination map revision TL-IA-2.
Actor: signed-in library member reserving one drill for pickup.
Destinations: D-TOOLS /tools, D-TOOL /tools/{id}, D-MY-RESERVATIONS /reservations. An inline form at D-TOOL collects pickup date and a short note; it is not a separate route. Entry context is /tools?category=drills.
Success means a reservation receipt with reservation ID, tool, date and pickup address returned by the server. Clicking Reserve is not success.
Policy:
- Pickup date is required and must be one of the visible available dates.
- Empty date receives inline feedback; note stays intact.
- While a request is pending, repeated Reserve input creates no additional request.
- This fixture has one transient failure before a retry succeeds. On failure retain date and note, expose Retry and Edit.
- If the server instead reports date-unavailable, keep note, clear the unavailable selection, show alternatives and let the member choose another date.
- Back before submission or after an error returns to the drill list with category intact; returning to the form during the session preserves draft date and note except invalidated dates.
- During pending, Cancel stops waiting and returns to editing. The server contract guarantees cancellation before commitment; no later reservation is created for the cancelled attempt.
- On confirmed success provide My reservations and return to Tools. Do not submit payments or send notifications.
Walk successful, missing-date, transient-failure/retry, date-unavailable and pending/cancel paths. These are author walkthroughs, not observations of a running system.
