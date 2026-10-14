# 실제 호출 경계 검증

Codex CLI 0.146.0의 새 문맥에서 실제 호출을 실행했다. 프로젝트 전용 `.agents/skills` 복사본 18개를 사용했다. 전역 설치나 정식 플러그인에 베타를 추가하지 않았다. `skills/list`의 발견 가능성과 실행 중 본문 전달을 구분한다.

## 명시 호출

`$스킬이름`으로 8개 각각을 호출했으며, 경계 설명만 요청해 모의 작업을 무단으로 진행하지 않는지 확인했다. 호스트가 삽입한 `<skill>` 본문을 해당 로컬 파일과 대조했다. 이름을 언급하거나 파일 목록에 등장한 것만으로 호출 성공을 세지 않았다.

| 스킬 | 본문 전달 | 경계 설명 산출물 |
| --- | --- | --- |
| information-architecture | 일치 | [scope](artifacts/explicit-information-architecture/output/scope.md) |
| user-flow | 일치, 경계 보완 후 추가 1회도 일치 | [최신 scope](artifacts/explicit-user-flow-r2/output/scope.md) |
| wireframe | 일치 | [scope](artifacts/explicit-wireframe/output/scope.md) |
| state-machine | 일치 | [scope](artifacts/explicit-state-machine/output/scope.md) |
| break | 일치 | [scope](artifacts/explicit-break/output/scope.md) |
| explain-interface | 일치 | [scope](artifacts/explicit-explain-interface/output/scope.md) |
| variant | 일치 | [scope](artifacts/explicit-variant/output/scope.md) |
| build-design | 일치 | [scope](artifacts/explicit-build-design/output/scope.md) |

이는 실제 호스트의 명시 도달 검사다. 각 역할의 구현 품질 비교를 대신하지 않으며, 이전 16개 역할 비교와 이번 8개 재비교를 함께 읽어야 한다.

## 이웃 요청과 실패 보존

| 자연어 요청 | 읽힌 관련 본문 | 판정 |
| --- | --- | --- |
| 응답 없는 저장의 행동·복구 경로, 초기 실행 | user-flow, state-machine | **실패.** 작업대 적용을 중단했어도 명시 요청 없는 본문 읽기가 발생 |
| 같은 입력, 경계 보완 후 새 문맥 | user-flow | 통과 |
| 별도 업로드 작업의 시작 전·완료 후 닫기와 복귀 | user-flow | 통과 |
| 긴 파일명을 줄바꿈하는 최소 CSS | better-typography | break를 읽지 않음 |
| 일반적인 blur와 backdrop-filter의 차이 설명 | better-writing | explain-interface를 읽지 않음 |
| 지정된 카드 패딩 한 값만 수정하는 CSS | build-design | variant를 읽지 않음 |

첫 실패에서는 모델이 `.agents/skills` 디렉터리를 열거하고, user-flow와 state-machine을 함께 읽었다. 호스트의 자동 목록은 state-machine을 올바르게 숨기고 있었다. 숨겨진 스킬이 파일시스템에서 접근 불가능하다는 뜻은 아니므로, 목록 정책만으로 행동 경계를 인증하지 않는다. [초기 명령 기록](artifacts/negative-state-machine/commands.json), [같은 요청 재시험](artifacts/negative-state-machine-r2/commands.json), [새 요청 재시험](artifacts/negative-state-machine-r3/commands.json).

user-flow의 설명과 첫 문단에 이 요청을 직접 담당한다는 점과 별도 작업대의 명시 호출 경계를 추가했다. 첫 실패는 그대로 보존하고 후속 두 문맥에서 금지된 네 스킬의 본문을 읽지 않은 것을 확인했다. 두 번 성공으로 모든 표현에서의 비호출을 보장하지 않는다.

## 자동 선택과 한계

스킬 이름을 쓰지 않는 실제 단계 과제를 통해 IA, 흐름, 화면 설계, 승인 명세 구현의 자동 선택을 확인한다. 단순 카탈로그 노출을 자동 선택의 증거로 삼지 않는다. 완성된 연결 결과는 최종 보고서와 실행 무결성 기록에서 확인한다.

Claude Code는 frontmatter와 manifest의 정적 일관성만 검사했다. 이번 행동 기록은 Codex에서 생성됐으며 Claude 런타임의 동일 동작을 주장하지 않는다. 일반 전역 스킬의 메타데이터도 호스트에 나타날 수 있어 완전한 보안 격리나 순수 토큰 비용 비교가 아니다.
