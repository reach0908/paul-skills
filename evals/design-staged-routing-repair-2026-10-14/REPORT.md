# Codex staged 호출 순서 보완과 Claude 회귀 검증

2026-10-14. **로컬 보완과 새 세션 검증을 수행했지만, Codex 자동 staged 경로의 완전 해결 판정은 보류한다.** 실패한 응답과 중간 후보를 모두 보존했다. 일상 Codex·Claude 설치는 정식 0.4.1 그대로이며 이 후보를 배포하거나 전역 설치하지 않았다.

## 변경 범위

- `better-interface`를 변경 리뷰의 첫 진입점으로 명시했다. 본문 읽기를 Git status/diff, 저장소 탐색, 도메인 본문 읽기와 한 호출에 묶지 않도록 설명과 첫 단계를 보완했다.
- 접근성·배치·문구·글꼴·색상·UI 디테일 6개 스킬의 설명을 현재 화면 검토, 요청된 수정, 승인된 도메인 전달로 한정했다. 변경 원인 검토는 먼저 라우터로 보낸다.
- 일반 화면 검토와 직접 수정은 각 도메인으로 계속 진입하며, 명시적으로 실행한 `interface-review`의 전달은 재호출 없이 계속한다.
- `ask-matt`, 관련 문서 8개, Changeset과 출처 기록을 맞췄다. 정식 스킬 수 44개, 디자인 17개, 자동 디자인 12개와 명시 전용 5개의 정책은 그대로다.
- 6개 도메인의 기존 규칙 본문은 새 진입 문단을 제외하면 0.4.1과 동일하다. 참고 파일과 원본 저장소의 고정 revision을 바꾸지 않았다. [출처 검증](./source-validation.json)

## 시험 설계와 실제 환경

[첫 프로토콜](./PROTOCOL.md), [두 번째 후보](./round2/PROTOCOL.md), [최종 후보](./round3/PROTOCOL.md)에 각 실행 전 입력과 소스를 고정했다. 실패 뒤 수정한 별도 후보이며, 같은 답을 재생성해 좋은 응답만 선택한 시험이 아니다. 마지막 후보의 실패도 유지한다.

Codex는 같은 사용자 설정·메모리·다른 스킬의 스냅샷으로 복제한 임시 CODEX_HOME에서 실제 플러그인으로 설치했다. 기존 Paul 플러그인은 복제 설정에서만 비활성화했다. 모델은 앞선 릴리스 시험과 동일한 지원 모델 `gpt-5.6-sol`, 관측 effort는 `medium`이다. Claude는 실제 사용자 설정과 `--plugin-dir` 후보를 사용했고 모델·effort를 바꾸지 않았다. 관측값은 `claude-opus-5-5`, `xhigh`다. 이 결과는 일상 전역 설치의 새 버전 검증이나 Codex의 다른 기본 모델 검증이 아니다.

각 사례는 새 세션과 중립 이름의 작업 디렉터리를 사용했다. 전체 후보 플러그인 174개 파일의 hash, 실제 카탈로그, 본문 전체 로딩, 도구 순서, 입력 보존과 응답을 연결했다. 기존 릴리스 3회는 원래 실패 요청의 비교 기준이며, 다른 모든 사례에 동시 baseline을 둔 것은 아니다.

각 호스트의 최종 21개 사례:

- 원래 접근성·배치 staged 요청 3회
- 글꼴·색상 staged 요청 3회, 문구·모션 staged 요청 1회
- working와 branch 자동 경로 각 1회
- 일반 도메인 6개, 현재 화면 종합 감사, IA 각 1회
- 명시 owner 준비, 명시 router, 명시 domain 각 1회
- 실제 Git 변경을 읽고 6개 도메인에 전달하는 리뷰 1회

화면 작업은 준비 또는 짧은 명세까지만 요청했다. 실제 리뷰의 합성 fixture는 버튼의 `aria-label` 하나가 삭제된 HTML이다. 브라우저, 제품 변경, 외부 서비스 동작은 실행하지 않았다. 수동 의미 판정은 동일 실행 에이전트가 했으며 독립·블라인드 판정이 아니다.

## 결과

최종 집계는 [RESULTS.json](./RESULTS.json), [Codex summary](./round3/codex/summary.json), [Claude summary](./round3/claude/summary.json)에 기록했다. Claude는 최종 21/21을 통과했다. Codex는 18/21이며 별도 기본 읽기 대조는 1/1 통과다.

| 소스 | Codex | Claude | 판정 근거 |
| --- | --- | --- | --- |
| 정식 0.4.1 비교 기준 | 2/3 | 이번 비교 기준 실행 없음 | 원래 staged 요청 반복 |
| 후보 1 | 2/3 | 3/3 | Codex가 라우터와 도메인을 함께 읽어 확장 중단 |
| 후보 2 | 16/19 | 18/19 | Codex 순서·범위 문제, Claude 실제 리뷰 비용 한도 종료 포함 |
| 후보 3 | 18/21 | 21/21 | 최종 소스, 다른 후보 결과와 합산하지 않음 |

최종 후보의 일반 도메인 6개, 현재 화면 감사, IA 준비는 양쪽 모두 **8/8 PASS**다. 변경 리뷰 자동 경로는 Codex **8/9**, Claude **9/9**이며, 명시 router/domain 경로는 양쪽 **2/2**다. 명시 owner 준비는 Codex **0/1**, Claude **1/1**이고, 공통 제약의 실제 리뷰는 Codex **0/1**, Claude **1/1**이다. 이 합계는 호출 및 제한된 산출물 기준이지 전체 UI 품질 점수가 아니다.

전체 기록은 행동 시험 **90개**와 모델 응답 전 네트워크 실패 **2개**, 총 **92개 고유 세션**이다. Claude가 보고한 모든 후보의 list-price 추정 합계는 **USD 14.7807262**이며 실제 청구액은 알 수 없다. Codex는 receipt의 토큰 사용량만 기록하고 비용으로 임의 환산하지 않았다. 비용 한도에 걸린 후보 2도 합계에 포함했다.

## 보존한 실패와 진단

**최종 후보의 Codex staged-1은 실패다.** 하나의 도구 호출에서 `pwd`, 개인 메모리 검색, 라우터, 접근성, 배치 본문을 함께 읽었다. 마지막에는 `$paul-skills:interface-review`만 반환하고 `staged`를 빠뜨렸다. 응답은 Git index의 스테이징을 배포 staging처럼 해석했다. 메모리 검색이 함께 있었다는 것은 관찰이며, 메모리가 원인이라는 인과 증거는 없다. [실제 호출 기록](./round3/codex/staged-1.json)

후보 2의 글꼴·색상 사례도 올바른 최종 명령을 반환했지만 라우터 읽기에 Git status와 diff 조회를 묶었다. 전체 본문 출력도 잘려 있었으므로 성공으로 인정하지 않았다. 후보 2의 명시 owner 준비 응답은 `working`의 비교 기준으로 기본 브랜치를 요구하는 부정확한 안내를 해 실패 처리했다. `working` 기준은 HEAD다. [순서 실패](./round2/codex/staged-type-color.json), [범위 안내 실패](./round2/codex/explicit-owner.json)

후보 2의 Codex 실제 리뷰는 모든 owner를 읽고 회귀를 찾았으나 없는 `origin/HEAD` 조회가 비정상 종료되어 엄격한 명령 성공 기준을 통과하지 못했다. Claude 실제 리뷰는 모든 owner를 읽었지만 USD 1.60의 호스트 표시 비용 한도에서 최종 보고서 전에 끝났다. 최종 후보의 Claude 실행 전에만 한도를 실제 리뷰 USD 3, 준비 USD 1, 배치 USD 15로 조정하고 [별도 프로토콜](./round3/CLAUDE-PROTOCOL.md)에 고정했다. 이전 미완료를 성공으로 덮어쓰지 않았다.

최종 후보의 최초 Codex 시작 2개는 제한된 실행 환경에서 DNS/네트워크 연결에 실패했고 모델 응답이 없었다. 원본 로그 hash와 세션을 [환경 진단](./round3/network-diagnostic.json)에 보존한 뒤, 동일 입력·모델·소스를 네트워크 가능한 실행으로 다시 시작했다. 행동 실패와 별도 집계한다.

## 호스트별 읽기 도구 대조

공통 실제 리뷰 프롬프트는 Claude의 `Read/Glob/Grep`으로 파일을 읽고 셸은 Git 명령만 쓰도록 제한했다. Codex에는 해당 이름의 파일 도구가 없어 Git diff로 본문을 읽었고, Git grep 시도에서 오류가 발생했다. 따라서 이 실패 하나를 스킬 자체 회귀라고 단정할 수 없다.

[Codex 기본 읽기 대조](./native-read-control/PROTOCOL.md)는 최종 후보의 소스를 그대로 유지하고 이 도구 제약만 Codex 기본 읽기에 맞춘 새 세션 1개다. 원래 21개 집계와 분리하며 기존 실패를 대체하지 않는다. 결과는 **1/1 PASS**다. 명시 owner, 라우터, 6개 도메인 전체 본문을 읽고 HEAD 기준을 정확히 사용했으며, 도구 오류 없이 삭제된 접근 가능한 이름을 HIGH Regression으로 보고했다. [별도 receipt](./native-read-control/codex/authorized-handoff-native-read.json)에 기록한다.

## 검증 코드 보완

- 라우터 경로 문자열이 명령에 있다는 이유로 뒤에 연결된 Git 조회를 허용하지 않는다.
- 상대 경로 `SKILL.md` 읽기는 원시 도구 입력의 정확한 작업 디렉터리와 전체 본문 일치를 함께 확인한다.
- `git diff --no-index /dev/null`로 읽은 스킬은 추가 줄 접두사를 제거한 전체 본문이 고정 파일과 정확히 일치할 때만 로딩으로 인정한다. Git의 정상적인 차이 표시 종료 코드 1과 실제 조회 오류를 구분한다.
- 부분 본문, 잘못된 작업 디렉터리, 메모리 읽기에 숨긴 Git 조회를 통과시키지 않는 13개 대조 시험을 추가했다.
- 수정 전 판정은 [grader-before.json](./round2/grader-before.json)에 보존했다. 모델을 다시 실행하지 않고 증거 해석 오류만 수정했으며, 실제 조기 Git 조회와 최종 staged 실패는 계속 실패다.

## 판단과 후속 우선순위

**P1: 자동 staged 진입은 미해결이며 정식 패치 배포를 보류한다.** 세 번의 지시문 후보에서도 동일 요청의 호출 순서 실패가 재현됐다. 같은 소스를 성공할 때까지 반복해 해결이라고 보고하지 않는다. 후속 작업은 본문 문장을 더 늘리는 것보다 도구 실행 전에 순서를 검사할 수 있는 호스트 제어의 적용 가능성을 따로 확인하는 것이 적절하다. 이는 아직 구현하거나 검증한 기능이 아니다.

당장은 변경 리뷰를 `$paul-skills:interface-review staged` 또는 `/paul-skills:interface-review staged`로 명시적으로 시작하는 경로가 가장 분명하다. 이번 실제 전달 fixture의 대상은 `working`이므로 전체 staged 실행까지 이 시험으로 증명했다고 주장하지 않는다.

최종 Codex의 명시 owner 준비도 `working`에 기본 브랜치·merge-base를 요구해 실패했다. 실제 리뷰는 HEAD를 정확히 사용하고 모든 도메인을 읽어 회귀를 찾았지만, 스킬을 읽으려던 `git grep --no-index` 오류를 다른 읽기로 복구하는 과정이 있어 엄격한 도구 오류 기준으로 실패했다. 두 항목을 자동 staged 순서 실패와 구분한다. [준비 응답](./round3/codex/explicit-owner.json), [실제 전달](./round3/codex/authorized-handoff.json)

Claude 실제 리뷰도 불필요하게 기본 브랜치를 해석했지만, 이 fixture에서는 `main = HEAD`이고 실제 비교는 `git diff HEAD`여서 해당 사례의 범위와 회귀 결과는 맞았다. 기본 브랜치와 HEAD가 갈라진 실제 저장소에서도 올바르다는 근거로 확대하지 않는다.

**P2: scope 안내와 실행 비용의 안정성은 별도 회귀 대상으로 유지한다.** 정상 호출에 성공해도 준비 답변의 범위 설명이나 실제 리뷰 완료가 항상 정확하다는 뜻은 아니다. 도메인의 기존 규칙을 보존한 것 역시 원본 이상의 전체 디자인 결과를 재입증한 것은 아니다.

## 기록 범위와 재검증

원시 대화, 계정 설정, 인증 정보와 개인 메모리는 공개 증거에 넣지 않았다. 비식별 receipt, 응답과 source hash만 이 디렉터리에 남겼다. [전체 파일 목록](./MANIFEST.json), [최종 카탈로그](./round3/catalog.json), [전역 설치 전](./global-before.json)·[후](./global-after.json)를 대조할 수 있다. 정식 전역 0.4.1의 174개 파일은 두 호스트 모두 변경되지 않았다.

```bash
python3 evals/design-staged-routing-repair-2026-10-14/verify_evidence.py
python3 evals/design-staged-routing-repair-2026-10-14/round3/test_order_grader.py
npm run check
claude plugin validate . --strict
```

정적 패키지 검사와 단위 시험 **38개**, strict manifest 검사, 판정 코드 대조 **13개**, 이전 릴리스 기록 검증기를 통과했다. `receipt_integrity: pass`는 기록 일관성이다. 모델 행동 실패를 합격으로 바꾸지 않는다. 이 보고서는 17개 디자인 역할 전체 품질, 새 모델 우위, 브라우저 런타임, 접근성 적합성, 제품 배포를 검증한 보고서가 아니다.

## Follow-up source freeze

The subsequent [native scope repair](../design-review-scope-repair-2026-10-14/REPORT.md) preserves candidate 3 under `candidate3-sources/`. The historical verifier now uses that frozen snapshot instead of the evolving repository. No previous outcome or receipt was changed.
