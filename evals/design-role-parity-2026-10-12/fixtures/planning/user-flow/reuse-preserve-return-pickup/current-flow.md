# Current accepted return flow
Revision RP-FLOW-4. Actor: shopper with return R-10; D-RETURNS /returns?status=open and D-RETURN /returns/R-10.
| From | Action/event | Guard | Feedback | To | Data |
| --- | --- | --- | --- | --- | --- |
| R1_READY | Open schedule | Return eligible | Available pickup dates | R2_DRAFT | Existing address stays |
| R2_DRAFT | Choose date | Date available | Selected date | R2_DRAFT | Date retained |
| R2_DRAFT | Back | Always | Return overview | R1_READY | Date retained for session |
| R2_DRAFT | Confirm | Date chosen | Scheduling progress | R3_PENDING | Address/date retained |
| R3_PENDING | Confirm again | Pending | Existing progress | R3_PENDING | No extra request |
| R3_PENDING | Scheduling error | Server rejects | Error and Retry | R4_ERROR | Date retained |
| R4_ERROR | Retry | Still eligible | Scheduling progress | R3_PENDING | Same selection |
| R3_PENDING | Server confirms | Booking ID returned | Pickup receipt | R5_BOOKED | Booking ID stored |
| R5_BOOKED | Back to returns | Always | Open returns | EXIT | status=open retained |

No date clearing on Back or error. R3_PENDING cannot be cancelled in this established release. All form/progress/error states share D-RETURN. Changing address and refund payout are out of scope.
