# Community seed pickup brief
Revision: SEED-PM-8. Accepted synthetic product facts for this maintainer exercise.

Audience: neighborhood gardeners reserving one seed packet for Saturday collection. The scoped task is to find a seed, reserve it, and find the resulting pickup again. No sign-in, payment, email, stock administration or production backend is included.

Content:
- BEAN-2: 가을 강낭콩, season autumn, description 작은 화분에서도 기를 수 있는 키 작은 강낭콩 품종입니다.
- SUN-5: 해바라기, season summer, description 햇볕이 잘 드는 넓은 자리에서 자랍니다.
- Pickup: Saturday 10:00 to 12:00, North community garden desk.
- Initial catalogue selection: season=autumn. Initial My pickups is empty.

Existing routes are /seeds, /seeds/{seedId} and /my-pickups. Detail has one canonical seed ID regardless of search/filter entry. A local prototype may represent these routes with hashes if it documents the mapping. Global labels are Seeds and My pickups. There is no approved visual redesign; use the supplied neutral project tokens and semantic HTML.

Traceable requirements:
- I1, content identity: Preserve seed IDs, names and descriptions. One packet is selected for this task.
- I2, return context: Returning from a seed to Seeds keeps the season filter. Both destinations remain reachable at narrow width.
- I3, recoverable submission: A name is required. Validation keeps the selected seed and any typed name. Submit enters pending for 400 ms. Ignore repeated Submit while pending. The first mock attempt fails, retains seed/name and exposes Retry and Back. Retry confirms the reservation. This is explicitly simulated.
- I4, confirmed result: Only confirmation creates pickup SP-21. Show reference, name, seed, Saturday time and desk. My pickups changes from empty to the one record. Cancel/Back before success creates no record.
- I5, local boundary: No real accounts, sends, persistence or stock commitments. Provide Reset demo to restore autumn filter and empty pickups. Reload starts fresh. No localStorage.
- I6, usable screen hierarchy: At 1280x900 and 390x844, seed identity, pickup details, feedback and next action stay reachable with labelled controls, visible keyboard focus and sensible reading order.

The fixture author authorizes using each preceding stage's delivered artifact as the next stage's bounded reference in this evaluation only. This is not a claim of real user acceptance. If a prior stage omitted or contradicted one of these facts, preserve its output and identify that handoff problem rather than silently rewriting its source.
