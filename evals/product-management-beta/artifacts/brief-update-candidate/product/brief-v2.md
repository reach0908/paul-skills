# Pocket Cards v2
Revision: v2-feedback-1
Status: product choices made by user; implementation pending
Supersedes: brief-v1.md
목적: 혼자 읽은 문장을 저장하고 돌아오는 무료 오프라인 경험.
사용자 결정 D1: 첫 버전은 카드 하나씩 직접 문장/출처를 입력한다. 자동 지도 생성은 제외. 이유: 작성과 회수 루프를 먼저 본다.
D2: 소유자만 편집/저장한다. 방문자는 읽기만 한다. 공개 여부는 매번 소유자가 선택한다. 이유: 의도 없는 공유 방지.
D3: 열기는 원문 보기, 선택은 이번 카드 후보, 저장은 저장 응답 확인 이후, 완료는 저장된 카드에서 별도 완료 액션을 선택한 경우다. 저장 실패면 완료할 수 없다. 이유: 보고 싶은 문장을 열었다고 학습 완료로 간주하지 않는다.
D4: 새로고침 뒤에도 카드/완료가 남는 저장을 의도한다.
D5: 사용자가 선택한 차분한 1열 구조와 색은 유지한다. 저장 버튼 위치는 하단, 문구는 저장으로 한다. 이유: 다음은 이동 버튼으로 보인다. 사용자 결정, 출처: reviews/feedback.md.
AI proposal P1: 완료를 자동 공유로 연결하기. 사용자 미선택.
Intended: D1-D5. Observed: evidence/local-walkthrough.md. Reported: notes/build-report.md.
Success: 의도한 입력→저장→재열기 루프를 혼자 수행, 수치 목표 미정.
Next: 디자인에서 D5의 저장 버튼 위치·문구 반영안 확인.

변경 기록 (v2-feedback-1): D5의 저장 버튼만 상단 → 하단, 다음 → 저장으로 변경. 사용자 결정, 이유와 출처: reviews/feedback.md의 이동 버튼으로 보인다는 피드백. D1-D4, 차분한 1열 구조와 색, 공개 선택 규칙은 유지한다. P1과 AI 메모의 자동 공유 아이디어는 사용자 미선택이다. 이 갱신은 제품 의도 변경이며 구현 반영 증거는 아니다.
