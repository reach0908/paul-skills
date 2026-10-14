# Field repair brief
Revision: FR-12; product scope accepted except ACCESS-4 below.
Current labels and routes: Today (/today), Jobs (/jobs), Manuals (/manuals). A job detail is /jobs/{jobId}. These routes are shared in dispatch messages. Search by job code must resolve the same detail as the list. A manual may be associated with several device models and jobs but has one manual ID and one canonical detail.
Audience: employee technicians and occasional subcontractors. Employees see their assigned job details, private notes and device manuals. Assignments include upcoming and completed jobs. Jobs have customer contact information, device model, service address and status. Notes are text attached to one job, with a last-saved time. Manuals include title, model compatibility, revision and offline availability.
Retrieval tasks:
- T1: From a dispatch link, identify today's service address and return to Today.
- T2: From a job, read the latest compatible manual and return to that job.
- T3: Find my saved note on a completed job by job code.
Offline: cached job and manual content is readable. Some records may not be cached; unavailable locally does not mean forbidden. Do not design syncing behavior here.
ACCESS-4 is unresolved: may subcontractors see customer contact information and old notes? Dispatch is deciding. Do not assume either access or denial. Their safe public manual path is settled.
No dispatcher admin, billing, route planning or authoring tools. A compact layout must retain job lookup and the manual-to-job context. Existing routes work; distinguish a findability change from visual navigation.
