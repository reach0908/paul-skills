# 디자인 리뷰 스킬 9개 정식 승격

2026-10-14 KST. 사용자가 직전의 9개 승격 권고에 대해 “추천하는 방향으로 모두 진행하자”라고 승인했다. 이 기록은 그 승인에 따른 정식 편입과 배포 검증을 다룬다.

## 승격 범위

| 호출 방식 | 스킬 |
| --- | --- |
| 사용자 직접 호출 | `interface-review` |
| 자동 또는 직접 호출 | `better-interface`, `better-accessibility`, `better-layout`, `better-writing`, `better-typography`, `better-colors`, `better-ui`, `design-browser` |

플러그인의 정식 스킬은 27개에서 36개로 늘어난다. 후보의 파일 61개는 [직전 검증](../design-routing-repair-2026-10-14/REPORT.md)과 바이트가 같다. 폴더만 `skills/in-progress/`에서 `skills/design/`으로 옮겼다. 직접 원본 8개는 Jakub의 고정된 소스에서 적응한 스킬이고 `design-browser`는 직접 작성한 실행 역할이다. 원본 revision과 출처별 digest를 승격 때문에 다시 찍거나 원본 검토 이력을 진전시키지 않았다.

나머지 8개인 `information-architecture`, `user-flow`, `wireframe`, `state-machine`, `break`, `explain-interface`, `variant`, `build-design`은 베타로 남는다. 공개 저장소의 베타 소스와 정식 플러그인 포함 여부를 구분한다. 별도 PM 스킬 PR #10은 이번 작업의 대상이 아니다.

## 연결한 문서와 도구

- 루트와 디자인·베타 목록, 플러그인 manifest, 출처 경로를 맞췄다.
- 정식 디자인 docs 페이지 9개와 `ask-matt`의 화면·변경·도메인·브라우저 경로를 추가했다.
- 문서 질문은 이 대화의 원본 디자인 보존, 원자적 역할, 명시 호출, 전체 페이지, 로컬 작업과 QA 범위 요구를 근거로 작성했다. 관련 공개 GitHub 이슈 검색은 결과가 없었고 지정된 개인 위키·사전 폴더도 없었다. 사전 용어 목록은 공개 원본에서 확인했다.
- 새 평가 준비 도구는 `skill-sources.json`의 현재 경로를 따라간다. 승격 뒤 누락된 스킬로 빈 비교를 만들지 않도록 이동과 모호한 등록에 대한 회귀 테스트를 추가했다.
- 과거 보고서의 탐색 링크는 현재 경로로 연결했지만 실제 실행 입력·결과·해시는 고정했다. 과거 `collect.py`는 당시 설치와 환경을 재확인하는 도구다. 현재 릴리스 검증을 대신하지 않는다.
- 중간 개발 Changeset 7개는 최종 배포 상태를 설명하는 하나의 minor Changeset으로 합쳤다.

## 승격의 근거

[대표 원본 비교](../design-role-parity-2026-10-12/RESULTS.md), [실제품 QA 보완](../design-field-trial-2026-10-14/QA-REPAIR.md), [설치·발견 검증](../design-install-discovery-2026-10-14/REPORT.md), [호출 경계 보완](../design-routing-repair-2026-10-14/REPORT.md)을 함께 근거로 삼았다. 마지막 수정본의 새 문맥 7/7 통과와 일반 화면 리뷰 2회의 유효 발견 4개 유지도 포함한다.

이는 검증한 로컬 반응형 웹 범위의 출시 판단이다. 모든 입력·모델·플랫폼에서 원본 이상이라는 보증이나 실제 보조기술 전체에 대한 인증은 아니다. 첫 수정본의 문구 누락과 실행별 심각도 차이도 원래 보고서에 남아 있다.

## 패키지 검증

- 저장소 검사: 56개 출처 기록, 36개 정식 경로, 38개 테스트 통과.
- 두 manifest의 엄격한 검증 통과.
- 승격 전후의 파일 61개 해시 일치.
- 인증 정보 패턴 검사에서 발견된 실제 키나 토큰 없음. 모델 원시 로그와 임시 인증 연결은 공개 패키지에 포함하지 않는다.

## 릴리스와 설치

릴리스와 전역 설치 갱신은 아직 진행 중이다. PR, 태그, 워크플로와 설치 캐시를 각각 확인한 뒤 완료 기록을 추가한다. 설치 방법은 [공식 OpenAI 플러그인 문서](https://developers.openai.com/plugins/build/plugins)와 실제 설치된 CLI 도움말로 확인했다. 기존 열린 대화의 자동 목록이 새 설치본으로 바뀌었다고 가정하지 않는다.
