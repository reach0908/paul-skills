# Accepted repair desk contract
Sources RD-PM-2, RD-IA-4, RD-FLOW-3, accepted for this prototype.
Destinations: D-QUEUE /queue, D-CHECKIN /check-in. Queue contains ticket Q-31 for Mina, item Desk lamp, status Waiting.
Entry is the queue. A Check in item action opens the form. Required customer name and item description, optional contact note. Use the sample long item description: Vintage adjustable desk lamp with a flickering warm light and a loose brass switch near the base.
| State | Event | Next | Required behavior |
| --- | --- | --- | --- |
| S-QUEUE | Check in item | S-EDIT | Empty form |
| S-EDIT | Submit empty required field | S-INVALID | Identify missing fields, keep all typed data |
| S-INVALID | Correct fields | S-EDIT | Editable retained form |
| S-EDIT | Submit valid form | S-PENDING | Progress, no duplicate submit |
| S-PENDING | Mock confirmation after 500 ms | S-DONE | Show ticket Q-32, name, item and Waiting status |
| S-EDIT or S-INVALID | Cancel | S-QUEUE | Discard only unsaved check-in |
| S-DONE | Back to queue | S-QUEUE | Q-32 is now present alongside Q-31 |

Local memory resets on page reload. No actual SMS, payment or repair triage. Provide a visible reset control. At narrow widths the ticket/item/status and the next action are primary; staff notes are secondary. Use labelled native fields, focus visibility and sensible focus after errors or completion. The prototype behavior is agreed; the screen design is still a draft.
