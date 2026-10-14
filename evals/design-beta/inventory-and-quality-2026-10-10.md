# 디자인 스킬 전체 정리와 품질 확인

2026-10-10 기준. 이번 작업은 현재 로컬 스킬과 등록된 원본 리비전을 비교한다. 원격 저장소의 최신 HEAD와 같다는 뜻은 아니다.

후속 수정과 실제 재비교는 [품질 보완 결과](improvement-2026-10-10.md)를 본다. 이 문서의 첫 비교 누락과 정적 위험 기록은 수정 전 상태를 보존하며, 현재 코드의 판정은 후속 기록이 우선한다.

현재 `skills/design/`에 정식 승격된 스킬은 **0개**다. 디자인 후보 **17개**는 모두 `skills/in-progress/`에 있다. 이 중 **13개는 Jakub 원본을 수정한 adaptation**, **4개는 직접 작성한 original**이다. 기존 engineering의 `prototype`은 별도로 함께 사용한다. 사용자 검증과 명시적 승격 승인이 있기 전에는 베타 상태를 유지한다.

제1 품질 기준은 **참고하거나 가져온 원본의 해당 역할보다 결과가 나빠지지 않는 것**이다. [품질 기준](quality-floor.md)은 이를 통과 조건으로 기록한다. 현재 이 기준은 요구사항이며, 17개 전체가 이미 충족했다는 선언이 아니다.

## 단계별 목록

표의 자동은 에이전트와 사용자 모두 호출 가능, 직접은 사용자가 명시적으로 호출하는 정책을 뜻한다. 각 원본의 호출 정책은 유지했다.

| 단계 | 스킬 | 맡는 한 가지 역할 | 호출 | 출처 및 원본과의 관계 |
| --- | --- | --- | --- | --- |
| 구조 | [information-architecture](../../skills/in-progress/information-architecture/SKILL.md) | 콘텐츠의 목적지, 분류, 탐색 구조 결정 | 자동 | 직접 작성. Impeccable `shape` 참고. 대응하는 IA 스킬의 복사본은 아님 |
| 흐름 | [user-flow](../../skills/in-progress/user-flow/SKILL.md) | 사용자 행동, 상태 전환, 복구 경로 명세 | 자동 | 직접 작성. Impeccable `shape`, `onboard`, `harden` 참고 |
| 와이어프레임 | [wireframe](../../skills/in-progress/wireframe/SKILL.md) | 흐름을 조작 가능한 저충실도 화면으로 구성 | 자동 | 직접 작성. Impeccable `new-work`와 기존 prototype 인터페이스 참고 |
| 구현 | [build-design](../../skills/in-progress/build-design/SKILL.md) | 제공된 시안을 기존 토큰과 컴포넌트로 구현 | 자동 | Jakub 동명 스킬 수정. 브라우저/Markdown 입력, 상태 보존, 비교 근거 추가 |
| 접근성 | [better-accessibility](../../skills/design/better-accessibility/SKILL.md) | 키보드, 포커스, 의미 구조와 접근성 검토 | 자동 | Jakub 동명 스킬. 브라우저 경로, 삭제 후 포커스와 비동기 반복 제출 검증 보강 |
| 색상 | [better-colors](../../skills/design/better-colors/SKILL.md) | 색상 토큰, 사용 의미, 대비 측정 | 자동 | Jakub 동명 스킬. 공통 운영 변경, 비텍스트 대비의 측정 범위 명확화 |
| 레이아웃 | [better-layout](../../skills/design/better-layout/SKILL.md) | 그룹, 간격, 정렬, 반응형 구조 검토 | 자동 | Jakub 동명 스킬. 글자 체계별 읽기 폭 판단 보완 |
| 타이포그래피 | [better-typography](../../skills/design/better-typography/SKILL.md) | 글꼴, 크기, 줄바꿈과 가독성 검토 | 자동 | Jakub 동명 스킬. 한국어/혼합 문자열 참고 자료와 분기 추가 |
| 문구 | [better-writing](../../skills/design/better-writing/SKILL.md) | 행동, 오류, 상태를 설명하는 UI 문구 검토 | 자동 | Jakub 동명 스킬. 자연스러운 한국어 행동 이름과 문법 보완 |
| 시각적 디테일 | [better-ui](../../skills/design/better-ui/SKILL.md) | 표면, 아이콘, 모션의 세부 품질 검토 | 자동 | Jakub 동명 스킬. 도메인 지침 유지, 공통 운영 변경 |
| 종합 검토 | [better-interface](../../skills/design/better-interface/SKILL.md) | 위 6개 도메인의 근거를 모아 우선순위 판정 | 자동 | Jakub 동명 스킬. 도메인 호출, 미검토 범위와 판정 조건 명확화 |
| 변경 검토 | [interface-review](../../skills/design/interface-review/SKILL.md) | 변경분에서 새 문제와 기존 문제를 구분 | 직접 | Jakub 동명 스킬. 코드 리뷰와 디자인 리뷰의 범위 및 결과 분리 |
| 대안 탐색 | [variant](../../skills/in-progress/variant/SKILL.md) | 하나의 컴포넌트에 대한 대안 비교 화면 생성 | 직접 | Jakub 동명 스킬. 기존 prototype과의 역할 경계 및 브라우저 경로 추가 |
| 구현 상태 탐색 | [state-machine](../../skills/in-progress/state-machine/SKILL.md) | 이미 구현된 컴포넌트의 상태를 전환하며 표시 | 직접 | Jakub 동명 스킬. 공통 운영 변경. 기획 단계 user-flow와 구분 |
| 스트레스 검사 | [break](../../skills/in-progress/break/SKILL.md) | 긴 내용 등 극단 조건에서 컴포넌트를 점검 | 직접 | Jakub 동명 스킬. 한 번의 제한된 검사 범위를 유지하며 브라우저 경로 변경 |
| 레퍼런스 해석 | [explain-interface](../../skills/in-progress/explain-interface/SKILL.md) | 화면이나 효과의 구현 원리를 설명 | 직접 | Jakub 동명 스킬. 특정 DevTools MCP 추천을 공통 브라우저 정책으로 변경 |
| 브라우저 실행 | [design-browser](../../skills/design/design-browser/SKILL.md) | 목적에 맞는 도구로 관찰 근거 수집 | 자동 | 직접 작성. Microsoft CLI 문서, Aside 도움말, 사용자 정책 참고 |

`better-interface`의 역할은 검토 조정이다. 접근성이나 색상 규칙을 자체적으로 다시 정의하지 않는다. `design-browser`는 동작과 관찰을 반환하며, 분석 에이전트가 심각도와 판정을 결정한다.

기존 [prototype](../../skills/engineering/prototype/SKILL.md)은 [Matt Pocock 원본](https://github.com/mattpocock/skills/tree/b0618bc436ad893b3c5e84e55fba86586d34a404/skills/engineering/prototype)의 수정본이다. 더 넓은 UI/로직 질문에 대한 일회성 프로토타입을 만들며, 17개 신규 후보에는 포함하지 않는다. 사용자가 인정한 것은 앞선 비교 프로토타입의 유용성으로, 모든 디자인 결과나 원본 대비 품질을 승인한 것은 아니다.

## 원본과 정확히 같은가

**13개 모두 완전히 동일한 복사본은 아니다.** 공통적으로 Paul 출처 정보, 스킬별 MIT 고지, 목적별 브라우저 실행 지침이 추가됐다. 일부는 한국어와 입력 방식, 리뷰 범위를 보완했다.

직접 원본은 [Jakub skills의 `d574cc8a576dc24256ad38268b8d03d86724a1b3`](https://github.com/jakubkrehel/skills/tree/d574cc8a576dc24256ad38268b8d03d86724a1b3/skills)이며, 각 행은 그 저장소의 같은 이름 스킬에 대응한다. 스킬별 정확한 원본 파일 링크와 다른 참고 자료의 핀은 [출처 지도](source-map.md)에 있다.

수정 전 독립 소스 감사에서 확인한 내용:

- 원본 매니페스트의 Git 객체 해시 **65/65 일치**.
- 당시 13개 adaptation의 폴더 digest가 등록값과 **13/13 일치**.
- 원본 파일 삭제 **0개**, 호출 정책 유지 **13/13**, MIT 고지 보존 **13/13**.
- 변경된 파일의 실제 내용과 원본 참고 파일도 비교했다. 모든 참고 파일이 무수정인 것은 아니다.

당시 원본 스킬 파일 64개는 48개 동일, 16개 수정, 0개 삭제였다. 보조 참조 38개는 36개 동일, 2개 수정이었다. [수정 전 소스 감사 JSON](source-audit-2026-10-10.json)과 [독립 상세 보고서](../../.scratch/design-quality-20261010/audit/report.ko.md)에 그 시점의 차이를 기록했다.

후속 수정 후에는 원본 파일 64개 중 **46개 동일, 18개 수정, 삭제 0개**다. 원본 해시 65/65, 등록 digest 13/13, 호출 정책과 MIT 고지 13/13은 다시 확인했다. [수정 후 소스 감사 JSON](source-audit-2026-10-10-repair.json)에 현재 차이를 별도로 기록했다. 원본 import/review 리비전은 그대로다.

이 결과는 출처와 변경 관리의 무결성을 보여준다. 에이전트가 원본과 같은 품질의 결과를 낸다는 증거는 별도의 실행 비교가 필요하다.

## 조사했지만 아직 가져오지 않은 영역

UI UX Pro Max, Emil Kowalski, ibelick, React Doctor, Raphael Salaja, gstack와 추가 하네스 사례는 조사 대상이다. 현재 13개 adaptation의 직접 원본이 이 저장소들로 바뀐 것은 아니다. pstack은 조사한 후보의 정체가 사용자 의도와 일치하는지도 아직 확인되지 않았다.

전용 모션 설계, 디자인 시스템 구축, 성능 QA, React 정적 분석은 현재 17개만으로 독립된 전용 스킬까지 완성된 상태가 아니다. 관련 기초 규칙 또는 브라우저 수집 절차는 있으나, 이 범위의 결과 품질을 검증했다고 표현하지 않는다.

## 가벼운 비교 예제

합성 한국어 ‘갈피’ 읽기 목록을 만들었다. 글 저장, 실패, 삭제, 빈 상태를 로컬 메모리와 타이머로 제공한다. 서비스 계정이나 실제 INFLFEED 데이터는 사용하지 않는다. [예제 소스](cases/reading-list/index.html)는 리뷰를 위한 결함을 포함하며 제품 구현 템플릿이 아니다.

원본과 Paul 묶음에 동일한 요청을 주고 서로의 결과를 읽지 않는 새 에이전트에서 실행했다. 두 조건 모두 Playwright CLI를 사용한다. 비교 대상은 `better-interface`와 6개 도메인 스킬의 리뷰 결과다. Paul의 `design-browser`는 브라우저 실행 의존성으로 포함된다. 구현, variant, state-machine 등을 이 시험으로 검증하지 않는다.

실행 결과와 최종 판정은 [비교 결과](comparison-2026-10-10.md)에 기록한다. 한 번의 합성 예제는 전체 역할의 동등성을 입증하지 않는다. 반복 실행, 독립 과제, 실제 화면 구현의 사람 평가가 남는다.

실행 결과, 핵심 8개 항목은 양쪽 모두 발견했다. 원본만 보고한 동적 숫자의 고정 폭 지침 LOW 항목 1개를 Paul이 빠뜨렸다. 해당 지침은 Paul에도 보존돼 있으며, 이번 결과만으로 반복적 열세나 원인은 확정할 수 없다. **전체 원본 동등 이상 판정은 보류한다.**

## 추가로 확인한 지침 위험

아래는 첫 감사 당시의 위험이다. 이후 본문·참고 지침을 수정했고, 실행 결과와 남은 한계는 [후속 기록](improvement-2026-10-10.md)에 분리했다.

- `build-design`은 Markdown 입력을 허용하지만 비교 단계에는 디자인 스크린샷과 Figma 응답을 전제하는 문구가 남아 있다. Markdown-only 입력의 완료 조건을 실제로 확인해야 한다.
- `better-writing`은 한국어 어순을 허용하면서 일부 하위 표에는 영어의 verb plus object 표현을 유지한다. 한국어 파괴적 행동 문구에서도 자연스러운 결과가 유지되는지 미검증이다.
- `better-typography`는 문장부호를 제품 정책에 따르는 선택으로 바꾸었지만 참고 표에는 일괄 치환으로 읽힐 표현이 남아 있다.

이는 원본과 현행 지침에서 찾은 정적 위험이다. 이번 실행에서는 이 세 문제가 실제 실패를 만들었다고 주장하지 않는다. 감사 중 스킬 본문을 변경하지 않았으며, 범위가 맞는 후속 사례로 확인할 항목으로 남겼다.

## 다음 검증의 우선순위

1. 이번 비교에서 원본보다 부족한 결과가 확인되면 해당 변경부터 수정하고 재검증한다.
2. 변경 폭이 큰 `build-design`을 원본도 지원하는 공통 입력으로 비교하고, Paul에 추가된 브라우저/Markdown 입력은 별도 과제로 검증한다.
3. 명시 호출 스킬 5개는 각각의 실제 산출물과 종료 범위를 확인한다.
4. IA, user-flow, wireframe은 기존 합성 실행을 넘어 다른 PM 입력과 유지가 정답인 기존 화면에서도 연결을 확인한다.
5. 통과한 역할부터 사용자에게 실제 사용 결과를 확인받는다. 품질 기준과 승격 승인은 별개로 기록한다.
