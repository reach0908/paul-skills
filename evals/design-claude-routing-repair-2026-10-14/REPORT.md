# Claude 디자인 스킬 호출 경계 보완·회귀 검증

2026-10-14 KST. **최종 판단: 통과.** `better-interface`의 자동 진입과 `interface-review`의 사용자 명시 호출을 구분하도록 로컬 소스, 문서, 라우터와 출처 기록을 보완했다. 전역 설치는 0.4.0 그대로이며, 이번 수정은 세션 전용 후보로 검증했다. 패치 Changeset을 추가했고 새 버전 발행이나 전역 갱신은 수행하지 않았다.

## 결과

| 검사 | 결과 |
| --- | --- |
| 기존 34개 호출 과제 재검증 | 34/34 |
| 17개 디자인 스킬 명시 호출 | 17/17 |
| 자동 대상 12개 자연어 선택 | 12/12 |
| 최종 보완본 추가 검증 | 13/13 |
| 실제 새 Claude 프로세스 | 59개, 세션 ID 중복 없음 |
| 실제 자동 목록 / 명시 명령 목록 | 59/59에서 12개 / 17개 일치 |

17개를 전부 자동 실행하게 만든 것이 아니다. `interface-review`, `state-machine`, `break`, `explain-interface`, `variant`는 여전히 사용자 전용이고 자동 카탈로그에서 제외된다.

첫 후보의 전체 결과는 **42/43**이었다. 실제 전달 시험 1건에서 제한된 도구 허용 범위 때문에 실패가 남았다. 이 실패를 지우지 않고 최종 보완본 및 도구 계약을 공개한 후속 시험을 별도로 수행했다. 세부 결과는 [첫 행렬](evidence/summary.json)과 [후속 행렬](recovery/evidence/summary.json)을 따른다.

## 무엇을 바꿨나

- `better-interface` 설명에 미커밋, staged, branch, PR, 범위 기반 UI 회귀 요청도 자동 진입 대상임을 명시했다. 파일 탐색 전에 요청만으로 경로를 고른다.
- 변경 리뷰는 정확한 `/paul-skills:interface-review <target>` 명령과 호출 이유로 답한다. 대상이 없으면 임의로 만들지 않는다. 범위 해석은 명시 호출된 담당 스킬이 수행한다.
- `interface-review`는 사용자 전용 정책을 유지한다. 사용자가 호출한 뒤에는 `better-interface`와 여섯 전문 스킬로 계속 전달하며 같은 호출을 다시 요구하지 않는다.
- 일반 화면·흐름·저장소 인터페이스 감사는 `better-interface`의 자동 경로를 유지한다.
- 두 스킬의 문서, `ask-matt` 라우터와 문서, local provenance decision 및 digest, patch Changeset을 맞췄다. 원본 imported/reviewed revision은 바꾸지 않았다.

출처 규칙과 도메인 검토 기준을 새로 합치거나 사용자 전용 스킬을 자동 실행으로 바꾸지 않았다. 문서의 질문은 이번 관측 실패와 사용자의 호출 경계 요청에서 가져왔다.

## 17개 스킬별 정상 진입

| 스킬 | 자연어 / 정책 | 명시 호출 |
| --- | --- | --- |
| better-interface | [통과](recovery/evidence/followup-implicit-better-interface.json) | [통과](recovery/evidence/followup-explicit-better-interface.json) |
| better-accessibility | [통과](evidence/implicit-better-accessibility.json) | [통과](evidence/explicit-better-accessibility.json) |
| better-layout | [통과](evidence/implicit-better-layout.json) | [통과](evidence/explicit-better-layout.json) |
| better-writing | [통과](evidence/implicit-better-writing.json) | [통과](evidence/explicit-better-writing.json) |
| better-typography | [통과](evidence/implicit-better-typography.json) | [통과](evidence/explicit-better-typography.json) |
| better-colors | [통과](evidence/implicit-better-colors.json) | [통과](evidence/explicit-better-colors.json) |
| better-ui | [통과](evidence/implicit-better-ui.json) | [통과](evidence/explicit-better-ui.json) |
| design-browser | [통과](evidence/implicit-design-browser.json) | [통과](evidence/explicit-design-browser.json) |
| information-architecture | [통과](evidence/implicit-information-architecture.json) | [통과](evidence/explicit-information-architecture.json) |
| user-flow | [통과](evidence/implicit-user-flow.json) | [통과](evidence/explicit-user-flow.json) |
| wireframe | [통과](evidence/implicit-wireframe.json) | [통과](evidence/explicit-wireframe.json) |
| build-design | [통과](evidence/implicit-build-design.json) | [통과](evidence/explicit-build-design.json) |
| interface-review | 자동 비노출 유지 | [통과](recovery/evidence/followup-explicit-interface-review.json) |
| state-machine | 자동 비노출 유지 | [통과](evidence/explicit-state-machine.json) |
| break | 자동 비노출 유지 | [통과](evidence/explicit-break.json) |
| explain-interface | 자동 비노출 유지 | [통과](evidence/explicit-explain-interface.json) |
| variant | 자동 비노출 유지 | [통과](evidence/explicit-variant.json) |

첫 후보에서 17개 명시 호출과 12개 일반 자연어 호출을 모두 확인했다. 이후 최종 수정은 `better-interface`의 안내 응답 한 부분뿐이며 자동 설명은 같고 나머지 파일도 동일하다. 해당 스킬의 일반·명시·변경 진입 및 `interface-review` 전달은 최종 후보에서 다시 실행했다. 다른 정상 진입은 변경되지 않은 본문으로 검증한 첫 행렬의 증거를 사용한다. 이 두 버전의 증거를 하나의 동일 버전 59회 시험으로 표현하지 않는다.

## 기존 버전과의 비교

이전 [0.4.0 발견 검증](../design-claude-discovery-2026-10-14/REPORT.md)의 33/34와 실패 원문을 보존했다. 이번에도 같은 모델·호스트·프롬프트를 사용해 세 가지 요청을 실제 0.4.0 설치본과 후보에 각각 주었다.

| 요청 | 기존 0.4.0 | 첫 후보 |
| --- | --- | --- |
| 원래 실패한 빈 폴더의 미커밋 UI 리뷰 | 스킬 없이 파일 탐색, 올바른 호출 안내 없음 | 파일 탐색 없이 담당 스킬 로딩과 working 안내 |
| 실제 Git 변경이 있는 폴더의 같은 요청 | 파일을 읽은 뒤에야 담당 스킬 로딩 | 파일 읽기 전에 working 안내 |
| staged 변경 리뷰 | 정상 | 정상 |

기존 버전은 1/3, 첫 후보는 해당 세 요청에서 3/3이다. 세 쌍은 실패 재현과 수정 확인용이며 통계적인 성능 우월성이나 유일 원인 증명은 아니다.

최종 후보의 [8개 변경 안내](recovery/cases.json)는 빈 폴더, 실제 Git working, staged, branch, PR 482, 정확한 ref 범위, 대상 미지정, 명시 better-interface 요청을 다룬다. 정상 화면 감사도 두 표현으로 재검증했다.

## 실패와 재검증을 어떻게 처리했나

1. **첫 실제 전달 시험의 도구 차단.** [원문 증거](evidence/repair-authorized-handoff.json)에서 전체 Git diff와 base 내용은 읽었고 일곱 소유 스킬도 로드했다. 다만 참조 파일을 읽는 셸 조합, 상태 조회 조합, `git -C` 사용 중 세 번 거절됐다. 최종 리뷰가 유용하더라도 이 실행은 실패로 유지했다.
2. **부가 설명의 범위 혼동.** [첫 branch 응답](evidence/repair-branch.json)은 올바른 주 명령 뒤에 working을 대안으로 제시하는 부정확한 설명을 붙였다. 최종 소스는 명령과 호출 이유만 답하도록 줄였다. 첫 본문은 [스냅샷](diagnostics/candidate-1-better-interface.txt)으로 남겼다.
3. **채점기의 문자열 오탐.** 대상 미지정 답변의 선택 예시와 일반 감사 답변의 조건부 설명을 실제 대상 선택·경로 전환으로 오인한 두 판정을 고쳤다. [초기 판정과 수정 이유](diagnostics/grader-correction.md)를 보존했고, 프롬프트나 응답을 바꾸거나 모델을 재실행해 이 오탐을 없애지 않았다. 의미 판단은 [부모 에이전트 검토](manual-review.json)에 명시했다.

후속 시험의 [사전 조건](recovery/PROTOCOL.md)은 최종 소스 변경과 도구 계약을 분리한다. 실제 전달 요청에만 읽기 전용 Git 단독 명령과 파일 읽기 도구의 사용 범위를 알렸다. 권한 검사를 우회하지 않았고 전역 권한도 바꾸지 않았다.

## 실제 변경 리뷰 전달

[최종 실제 전달 기록](recovery/evidence/recovery-authorized-handoff.json)은 로컬 HTML의 `aria-label` 삭제를 이전 커밋과 비교한다. [원본](fixtures/before.html)과 [변경본](fixtures/after.html)은 공개 가능한 합성 자료이며 실제 제품 파일이 아니다.

확인할 항목은 명시 `interface-review` 본문, 자동 `better-interface`와 여섯 소유 스킬의 성공한 호출 및 전체 본문, 실제 Git before/after 근거, `Regression` 분류, 재호출 요구 없음, 입력 보존, 도구 거절 없음이다. 최종 의미 검토는 [후속 검토 기록](recovery/manual-review.json)에 남긴다. 화면 렌더링, 브라우저 접근성 트리, 스크린리더, 실제 키보드 동작은 별도 검증 대상으로 남는다.

실제로 이 항목들이 통과했고 읽기 전용 Git 조회 12개도 성공했다. 응답 첫 문장의 스크린리더 낭독 표현은 소스에서 예상한 설명이며 실측 근거로 사용하지 않았다. 응답의 Verification 역시 실제 낭독과 접근성 트리를 `Not verified`로 남겼다. 변경되지 않은 도메인의 `Clear` 표시는 정적 변경 범위의 판단이며 전체 렌더링 품질 통과를 의미하지 않는다.

## 증거와 재현

- Claude Code 2.1.296, 실제 모델 `claude-opus-5-5`, 관측 effort `xhigh`. 사용자 설정을 상속했고 모델을 임의로 낮추지 않았다.
- 새 프로세스마다 중립적인 `case_NNN` 폴더와 고유 세션 ID를 사용했다. 다른 시험의 결론이나 채점 기준은 전달하지 않았다.
- [최초 프로토콜](PROTOCOL.md), [46개 고정 요청](cases.json), [13개 후속 요청](recovery/cases.json).
- [첫 번들 해시](bundle-manifest.json), [최종 번들 해시](recovery/bundle-manifest.json). 표시 버전 0.4.0만으로 소스를 판정하지 않고 실제 경로와 전체 본문을 대조했다.
- 자동 선택은 성공한 Skill 호출과 실제 호스트 본문 주입이 모두 있어야 인정했다. 직접 명령의 네이티브 본문 주입은 별도로 검사했다.
- hooks는 프로세스마다 비활성화했고 외부 MCP와 브라우저는 사용하지 않았다. 전역 설정은 수정하지 않았다. 세션 전용 플러그인 로딩은 [공식 문서](https://code.claude.com/docs/en/plugins/create#load-a-plugin-for-one-session), 우선순위는 [로딩 규칙](https://code.claude.com/docs/en/plugins/loading#name-conflicts)을 참고하고 실제 경로로 재확인했다.
- 원본 호스트 기록은 로컬 비공개 `.scratch`에 보관했다. 공개 가능한 영수증에는 전체 응답, 관련 도구 입력, 본문·기록 해시와 필요한 실행 정보만 남겼다. 계정 정보와 원본 시스템 문맥을 복사하지 않았다.

이번 59회 실행의 호스트 보고 목록가 추정 합계는 **$18.621806**다. 첫 행렬 $14.361421, 후속 $4.260385. 실제 청구 금액은 확인하지 않았다. 이전 턴의 시험 비용은 이 합계에 포함하지 않는다.

로컬 검사는 [validation.json](validation.json)에 기록했다. 저장소 테스트 38개, 수집기 통제 시험 20개, strict plugin validation을 통과했다. 두 번들 복원 검사는 [prepare_bundles.py](prepare_bundles.py), 전체 영수증과 해시 검사는 [verify_evidence.py](verify_evidence.py)로 수행한다. [MANIFEST.json](MANIFEST.json)은 이 평가 폴더의 공개 파일을 고정한다.

## 적용 상태와 한계

Claude 전역 설치의 17개 본문과 17개 호출 정책 파일은 [0.4.0 설치 기록](installation-before.json)과 대조해 유지 여부를 확인했다. 이번 수정은 로컬 소스와 세션 전용 후보에만 있다. PR 게시, 병합, 패치 발행, 전역 갱신, 새 Codex 행동 검증은 수행하지 않았다.

이 결과는 시험한 프롬프트의 발견·호출 경계와 한 개의 정적 리뷰 전달을 뒷받침한다. 17개 스킬의 모든 디자인 산출물을 다시 평가하거나 원본 이상 품질, 실제 브라우저 QA, 임의의 프로젝트·모델·언어에 대한 완전성을 증명한 것은 아니다. 의미 검토자는 이 작업의 부모 에이전트이며 독립적인 인간 또는 블라인드 평가자가 아니다.

## 배포 후 기록 검증

0.4.1 패치 준비 과정에서 시험 당시 0.4.0 manifest를 `diagnostics/plugin-0.4.0.json`에 보존했다. bundle hash와 실행 receipt는 변경하지 않았다. 검증기는 이후 전역 설치를 갱신해도 과거 기록을 검사할 수 있도록 이전 설치 hash를 `paul-skills@0.4.0` 태그와 비교한다. 이 검사는 현재 활성 설치 상태를 뜻하지 않는다. 스킬 본문은 해당 시험 버전과 동일한 소스 checkout에서 검증한다.
