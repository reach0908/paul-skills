# Approved change
Revision RP-CHANGE-2.
After R5_BOOKED, the carrier may report pickup-failed with reason No access. Present that reason, preserve the return, address and old booking reference, and allow choosing a new pickup date. The old date must not remain selected because it is in the past. The shopper can also return to open returns without rescheduling.
On reschedule confirmation, create a new scheduling attempt referring to the old booking. While pending, repeated confirm must not duplicate it. A scheduling error keeps the new date for retry. On success show the new booking reference; retain the old reference in history. Reuse the established scheduling path if its contract can express those data distinctions. Do not alter the return eligibility policy or add an automatic refund.
