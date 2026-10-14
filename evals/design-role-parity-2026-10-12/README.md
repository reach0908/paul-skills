# 디자인 스킬 역할별 비교

2026-10-12 사용자가 승인한 전체 역할 검증이다. [이전 사례 비교](../design-beta/improvement-2026-10-10.md)를 확장하며, [사전 프로토콜](PROTOCOL.md)에 따라 실행 결과와 판정을 분리한다.

17개 역할의 51개 기본 과제와 추가 수정·성능·연결 과제를 사용한다. 실행과 품질 판정은 [최종 결과](RESULTS.md), 역할별 미검증 범위는 [범위 표](branch-coverage.md), 입력과 관찰 근거는 [증거 색인](evidence/manifest.json)에 기록한다. 파일 수나 실행 완료 수 자체가 합격 수는 아니다.

| 묶음 | 역할 수 | 과제 수 | 실행 입력 |
| --- | --- | --- | --- |
| 명시 호출 | 5 | 15 | [목록](fixtures/explicit/cases.json) |
| 도메인과 종합 검토 | 7 | 21 | [목록](fixtures/domains/cases.json) |
| 로컬 시안 구현 | 1 | 3 | [목록](fixtures/build/cases.json) |
| 직접 작성한 계획·브라우저 역할 | 4 | 12 | [목록](fixtures/planning/cases.json) |

원본·Paul 비교는 13개 adaptation에 적용한다. 직접 작성한 4개는 요구사항과 무스킬 조건으로 검증하며 원본 동등성은 해당 없음으로 남긴다. 사용자는 Figma를 사용하지 않고 항상 로컬 기반으로 작업한다고 명시했다. 로컬 이미지, Markdown, 브라우저 산출물이 대상이며 라이브 Figma 통합은 범위 밖이다.

## 재현

`prepare.py ROLE CONDITION REPEAT`는 고정 원본 또는 현재 Paul 파일과 과제를 새 임시 디렉터리에 복사한다. `CONDITION`은 `original`, `paul`, `control`이다. 원본은 등록된 Git 객체의 SHA-256까지 확인한다. 기존 실행 디렉터리를 덮어쓰지 않는다. 실행마다 `PROMPT.md`와 `trial.json`의 입력 해시를 보존한다.

실행자는 자기 디렉터리의 세 과제만 해결한다. 조건과 반복 사이에는 새 문맥을 사용하고, 한 역할 실행 안의 세 과제는 문맥을 공유한다. 필요한 브라우저 작업은 Playwright CLI로 수행한다. 공개 테스트 데이터에는 실제 계정이나 서비스 변경이 없다. `collect.py RUN_ID`는 산출물 해시와 입력 변경을 수집하며 품질 판정을 대신하지 않는다.

별도 [연결 과제](fixtures/planning/composition.json)는 IA부터 리뷰까지 같은 요구사항과 식별자가 보존되는지 확인한다. `prepare_composition.py DESTINATION`은 기존 Git 저장소 밖의 새 임시 디렉터리에 연결 과제를 준비하며 이전 결과를 덮어쓰지 않는다. 단계마다 실제 이전 산출물과 해시를 인계한다.

[성능 관찰 보완 과제](fixtures/supplements/performance/TASK.md)는 같은 로컬 동작의 User Timing과 지원되는 long-task 관찰을 수집한다. `prepare_performance.py control|paul`로 별도 두 실행을 준비한다. 세 번의 브라우저 표본은 측정 수단의 확인이며 실사용 성능, INP 또는 모델 우위의 증거가 아니다.

주관적 시각 수용, 실제 사용자 검증, 플러그인 승격은 별개의 결정이다. 후보는 계속 `in-progress/`에 둔다.

[전환 관찰 재시험](fixtures/supplements/transitions/catalog-scroll/TASK.md)은 기존 anchor 과제, 새 지연 로딩 목록, 이미 로딩된 대조 화면을 사용한다. `prepare_transitions.py control|paul --suffix NAME`으로 새 실행을 준비하며 기존 실행은 덮어쓰지 않는다. 정확한 과거 prompt와 입력은 각 실행 해시에 고정돼 있다.

`prepare_wire_navigation.py control|paul --suffix NAME`은 연결 과제에서 발견한 본문 링크 수정과 새 화면의 내부 이동을 시험한다. 수정된 연결 화면은 [로컬 예제](examples/composition-repaired/REPAIR.md)로도 보존했다. 예제 폴더에서 정적 서버를 실행해 `app/`과 `design/`을 열 수 있다.
