# Accepted map
Revision ML-IA-5.
| ID | Label | Route | Content |
| --- | --- | --- | --- |
| D-LOANS | Loans | /loans | Incoming or outgoing loan list, museum filter |
| D-LOAN | Loan details | /loans/{loanId} | Partner museum, dates, objects |
| D-OBJECT | Object details | /objects/{objectId} | Object identity, image description, current loan |
| D-PARTNERS | Partner museums | /partners | Museum directory |

Global navigation: Loans, Partner museums. List state lives in query parameters, for example /loans?direction=outgoing&museum=stone. Loan L-8 contains OBJ-21. A detail link carries the source loan and return query. OBJ-21 has one object destination even if it appears in loan history. At narrow widths the same destinations and filter remain available.
