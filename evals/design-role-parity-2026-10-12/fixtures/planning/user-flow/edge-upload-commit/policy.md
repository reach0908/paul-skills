# Expense upload policies
Revision EX-6, with unresolved COMMIT-2.
Actor: employee submitting one receipt image for an already saved expense draft.
Destinations: D-EXPENSES /expenses and D-EXPENSE /expenses/{expenseId}; the upload panel is in the expense detail. Expense EX-44 has amount 24000 KRW and memo 출장 기차표, both already saved. Keep the list filter status=draft on return.
Image constraints: JPEG or PNG, maximum 4 MiB. Invalid file gets actionable feedback without clearing saved amount or memo. A valid selected image and upload progress are local to this tab.
Upload begins when the employee presses Submit receipt. The server assigns an idempotency key on that attempt. Repeated Submit while pending is ignored. A transient network timeout does not prove success or failure; the user can query status and retry the same attempt with the same key. Status may report pending or a receipt ID. A definitive upload failure permits reselecting a file and a new attempt. Only a receipt ID confirms attachment.
COMMIT-2: whether leaving during pending cancels, continues, or warns has not been decided. The server behavior is also unconfirmed. Do not invent this transition or claim cancellation succeeds. You may name a proposed option but it must remain unapproved and unimplemented.
No payments, manager approval, multi-file queues or persistent offline uploads in this task. Drafts and confirmed success can return to Expenses; saved expense data and the original filter must remain.
