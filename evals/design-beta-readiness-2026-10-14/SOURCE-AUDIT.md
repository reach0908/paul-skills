# 남은 디자인 베타 8개: 출처·기존 증거·승격 경계 독립 감사

감사일: 2026-10-14, 범위: 현재 `skills/in-progress/`의 아래 8개. 이 문서는 읽기 전용 소스 감사이며 새 모델 실행이나 새 브라우저 실행의 결과가 아니다. 루트 실행자의 새 비교 결과가 나오면 해당 결과를 추가해 최종 판정해야 한다. 스킬·출처 등록·전역 설치는 변경하지 않았다.

## 결론

기존 최종 평가에서 8개 모두 대표 과제의 객관적 계약을 충족했다. 이번에 현재 폴더 전체 digest를 다시 계산하니 8/8이 당시 최종 식별자와 일치했다. 따라서 기존 평가가 다른 스킬 버전의 평가가 되어버린 문제는 없다. 다만 런타임 의존성인 `design-browser`, 관련 종합/변경 리뷰의 현재 digest는 달라졌다. **현재 전체 묶음에서의 동작, 새 세션 호출 경계, 디자인 결과의 사용자 수용까지 포함한 승격 판정은 아직 별도다.** [기존 최종 결과](/Users/jinhokim/dev/paul-skills/evals/design-role-parity-2026-10-12/RESULTS.md), [당시 식별자](/Users/jinhokim/dev/paul-skills/evals/design-role-parity-2026-10-12/evidence/candidate-identities-current.json), [품질 기준](/Users/jinhokim/dev/paul-skills/evals/design-beta/quality-floor.md:19).

원본 직접 adaptation은 5개다. IA·user-flow·wireframe은 직접 작성했으므로 '원본 이상 합격'으로 셀 수 없다. 이 세 역할의 기준은 요구 계약과 무스킬 대조이며 기존 대조군도 잘했으므로 스킬 사용의 우위는 미입증이다. [출처 표](/Users/jinhokim/dev/paul-skills/evals/design-beta/source-map.md), [원본 없는 역할 기준](/Users/jinhokim/dev/paul-skills/evals/design-beta/quality-floor.md:9).

## 이번에 직접 확인한 식별자

고정 원본: `jakubkrehel/skills`의 `d574cc8a576dc24256ad38268b8d03d86724a1b3`, MIT. `prepare.py`의 원본 경로 `/tmp/paul-design-research-20261009/jakubkrehel-skills`는 폴더가 남아 있지만 Git HEAD/config 등 메타데이터가 없어 `git show`가 현재 실패한다. 원본 복원 대신 과거 실행에서 동결한 아래 묶음을 읽었고, canonical `upstream-manifest.json`의 **65/65 파일 SHA-256**과 일치했다. LICENSE는 각 역할에 복사된 파일 중 `skills/build-design/LICENSE`로 검증했다. 이는 원본 파일 내용의 식별을 복구한 것이며 원본 저장소 Git 객체 복구를 주장하지 않는다.

`/Users/jinhokim/dev/paul-skills/.scratch/design-role-parity-20261012/runs/build-design-original-r1/.agents`

[준비 도구의 원본 경로](/Users/jinhokim/dev/paul-skills/evals/design-role-parity-2026-10-12/prepare.py:17), [고정 원본 manifest](/Users/jinhokim/dev/paul-skills/evals/design-beta/upstream-manifest.json).

| 역할 | 직접 원본 | 현재 전체 폴더 digest | 과거 최종과 일치 |
| --- | --- | --- | --- |
| information-architecture | 없음, Impeccable shape의 개념적 영향 | `f3812ec0cf05cb9063593ebe0f3eb3b520c6d5c38e886321978bfa557ea41343` | 예 |
| user-flow | 없음, Impeccable shape/onboard/harden의 개념적 영향 | `88ed20779e0334a5fdf0adc6f69f2be871fe0673241ae5128881e3656f3226a1` | 예 |
| wireframe | 없음, Impeccable new-work와 기존 prototype의 개념적 영향 | `ab88c42bcc7c41134e37adcb29430cc60c05cedcb537431eacd77d3e36287f81` | 예 |
| state-machine | Jakub 같은 이름의 스킬 | `9e56a5fb4d3977145b0b7ab8c8aa4a682c433990ac8e709fbabf0281a3b81bcf` | 예 |
| break | Jakub 같은 이름의 스킬 | `26c4cce857f6287944c8d4f3cf9f9d9c2112dabb9036c6d57c8a5287240ec1fc` | 예 |
| explain-interface | Jakub 같은 이름의 스킬 | `ed0f68018cd2e768255e2b6e98cdec69667c8d5f504d8c638a1e37e609b2a069` | 예 |
| variant | Jakub 같은 이름의 스킬 | `7195dd0b375c96108466d7869acc098cad989bccf40063c115ba7eddc39ad832` | 예 |
| build-design | Jakub 같은 이름의 스킬 | `ec61958d20891ff8c386b5742755392f72884659ae94245b726986dd5135b131` | 예 |

Digest는 기존 provenance 도구의 `local_tree`와 `digest` 알고리즘을 사용했다. 출처 등록의 5개 `localDigest`도 일치한다. 3개 original은 해당 출처 필드가 없으므로 과거 평가 식별자와 비교했다. [계산 규칙](/Users/jinhokim/dev/paul-skills/skills/in-progress/upstream-sync/scripts/compare.py:37), [출처 등록](/Users/jinhokim/dev/paul-skills/skill-sources.json).

5개 adaptation의 과거 원본 묶음 23개 파일 중 현재 **17개 바이트 동일, 6개 수정, 누락 0개**. 수정은 각 SKILL.md 5개와 build-design의 openai.yaml 1개이며, `build-design/browser-and-spec.md` 1개가 추가되었다. 원본 지원 문서와 라이선스는 유지됐다. 이 집계는 평가 준비 단계에서 복사한 LICENSE도 포함한다.

- state-machine: 출처 frontmatter와 공통 브라우저 위임만 추가. switcher·상태 발견·실제 컴포넌트·데이터 경계·정리 계약은 원본 유지.
- break: 위 추가에 더해 task-owned CLI 세션을 허용. 원본의 한 번 관찰, 소스 미수정, 장시간 브라우저 설치/디버깅 금지와 시나리오 단위 시각 보고를 유지.
- explain-interface: 원본의 chrome-devtools 예시를 공통 브라우저 도구 정책으로 교체. 효과/사이트/이미지/무브라우저 경로와 지원 문서 모두 유지.
- variant: prototype과의 범위 구분, 시각 전환 때 작업 상태 보존, 짧은 화면의 고정 컨트롤 초점 확인을 추가. 뒤의 두 개는 실제 과거 실패를 보완했다.
- build-design: 브라우저·Markdown 경로 추가, 승인된 결정 재사용, 누락된 상태·접근성·기존 사용자 작업 보존 강화. 원본이 시안과 충돌할 때도 그대로 구현하도록 한 부분을 사용성 보존+편차 기록으로 변경했다. Figma 지원 파일은 그대로 있지만 사용자의 로컬 작업 범위에서는 검증 대상이 아니다.

## 역할별로 이미 있는 근거와 다음 확인

| 역할 | 이미 입증된 범위 | 남은 핵심 확인 | 근거 |
| --- | --- | --- | --- |
| information-architecture | PM/어휘/객체·목적지·필터 구분, 권한 미정 표시, 조회/복귀 문맥, 기존 지도 보존. 대조군도 충족 | 새 문맥에서 skill 명칭 없이 구조 설계 요청을 발견하는지. PM 결정을 다시 인터뷰하거나 구현·화면 구성까지 넘겨잡지 않는지 | [r2](/Users/jinhokim/dev/paul-skills/evals/design-role-parity-2026-10-12/evidence/information-architecture-r2-assessment.json) |
| user-flow | 상태/이벤트/guard/데이터 보존, pending와 확정 성공 분리, Retry/취소, 미정 서버 정책 보류, 기존 전이 유지. 대조군도 충족 | IA와 기존 coded state-machine의 경계. timeout 뒤 반복 질의가 실제로 요구되는 새 계약에서만 해당 전이를 확인 | [r2](/Users/jinhokim/dev/paul-skills/evals/design-role-parity-2026-10-12/evidence/user-flow-r2-assessment.json) |
| wireframe | 작동 HTML+명세, 넓고 좁은 화면, 실패/Retry/receipt/reset, 화면 안 링크의 route·입력·pending 보존 수정 | 현재 design-browser와의 연결, 수정 후 새로운 단계 연결에서 동일 링크 회귀가 다시 생기지 않는지 | [r3](/Users/jinhokim/dev/paul-skills/evals/design-role-parity-2026-10-12/evidence/wireframe-r3-navigation-assessment.json) |
| state-machine | 실제 컴포넌트 import, 코드 유래 8/12상태, 80상태/폭 방문, URL/reload, 원본 보존, 정확한 삭제 | 명시 호출 경계, 입력 중 단축키 무시/수정키/기존 preventDefault, 현재 브라우저 위임의 동일 범위 유지 | [r2](/Users/jinhokim/dev/paul-skills/evals/design-role-parity-2026-10-12/evidence/state-machine-r2-assessment.json), [switcher 계약](/Users/jinhokim/dev/paul-skills/skills/in-progress/state-machine/switcher.md:11) |
| break | 적절한 props 축, 실제 컴포넌트, 반복 가능한 overflow/clipping, 화면에 관찰 주석, 제품 소스 보존 | 현재 design-browser QA 경로를 만나도 한 번 관찰이라는 한정 범위를 유지하는지. 무결함 대조 화면에 취향성 지적을 추가하지 않는지 | [r2](/Users/jinhokim/dev/paul-skills/evals/design-role-parity-2026-10-12/evidence/break-r2-assessment.json), [범위 계약](/Users/jinhokim/dev/paul-skills/skills/in-progress/break/SKILL.md:17) |
| explain-interface | 복합 blur/paint stack, WAAPI 시간 도출, reduced motion, 이미지 가설과 측정 구분, 페이지 지시 무시 | **명시적으로 제공하는 '사이트 전체 시스템 설명' 경로는 아직 실행하지 않음.** 다른 width/theme, CSS 접근 불가, 실제 style 승자와 token/stack 추정을 구분하는 새 비교가 효율적 | [r2](/Users/jinhokim/dev/paul-skills/evals/design-role-parity-2026-10-12/evidence/explain-interface-r2-assessment.json), [site 계약](/Users/jinhokim/dev/paul-skills/skills/in-progress/explain-interface/read-the-system.md:195) |
| variant | 한 축/실제 페이지/선택안 반영·정리. 두 차례 실패 수정 후 입력·선택·disabled·feedback 유지, 짧은 화면/실제200%확대 표본 통과 | 현재 의존성에서 상태 보존/초점 재확인. **기존 결과의 사용자 시각 수용 미완료**. prototype 자동 경로와 중복 harness를 만들지 않는지 | [r4](/Users/jinhokim/dev/paul-skills/evals/design-role-parity-2026-10-12/evidence/variant-r4-state-repair-assessment.json) |
| build-design | 로컬 이미지/디자인 데이터/명세, 토큰·상태·키보드 보존. image 최대1.390625 CSSpx 차이는 사전2px 허용 안, export/preserve geometry 동일 | **사용자 시각 수용 미완료**. 현재 browser/spec 연결에서 특정 route/state/revision 별 비교와 미정 값의 편차 표시, 동작 상태 보존 | [r2](/Users/jinhokim/dev/paul-skills/evals/design-role-parity-2026-10-12/evidence/build-r2-assessment.json), [명세 경로](/Users/jinhokim/dev/paul-skills/skills/in-progress/build-design/browser-and-spec.md) |

전체 각 역할의 기본 과제는 3사례×2조건×2반복이다. 같은 실행의 세 사례는 문맥을 공유하므로 독립 통계 표본 3개가 아니다. wireframe/variant의 수정 재시험은 노출 사례와 새 사례를 함께 포함한다. 해당 수를 새 숨김 과제라고 다시 세지 않는다. [검증 범위](/Users/jinhokim/dev/paul-skills/evals/design-role-parity-2026-10-12/branch-coverage.md).

## 관찰된 실패, 검증 공백, 단순 제안을 구분

**관찰됐고 수정 재시험까지 된 실패:** variant의 외관 선택이 선택 해제 상태를 초기화한 회귀, 짧은 viewport의 picker 가림; wireframe의 skip link가 hash route를 바꾸던 문제. 이 실패들은 현재 후보의 미해결 결함으로 세지 않는다. 다만 새로운 의존성에서의 검증은 별도다. [실패와 수정 기록](/Users/jinhokim/dev/paul-skills/evals/design-role-parity-2026-10-12/repairs.md).

**이번 감사에서 관찰된 재현성 문제:** 오래된 원본 임시 clone에서 `git show` 실패. 동결 trial bundle 65개 파일이 manifest와 일치해 원본 입력은 대체할 수 있다. 이는 출력 품질 결함과 구분한다.

**검증 공백:** 최신 design-browser와 후보 8개의 연결, 실제 호스트의 자동/명시 호출, explain-interface 사이트 전체 경로, variant/build의 사용자 시각 수용. 과거 결과는 이를 통과했다고 주장하지 않는다.

**추가 검증 제안:** state-machine의 단축키 guard, break의 단일 pass와 현재 evidence 절차 간 우선순위, IA→flow→wireframe→build의 현재 수정본 연결. 지침에 범위가 명확히 있거나 기존 평가가 통과한 것만으로 새 실행의 실패라고 판정하지 않는다.

## 우선순위와 종료 기준

P0는 새 기능 추가가 아니라 승격 판정 전에 반드시 충족할 증거 조건, P1은 현재 역할의 핵심 미검증 가지를 적은 비용으로 보완하는 작업, P2는 지금 승격 범위를 늘리지 않고 유지할 확장 검증이다.

### P0: 승격 결정을 내리기 위한 조건

1. **현재 묶음으로 회귀가 없는지 확인.** 현재 후보 digest와 현재 design-browser를 묶은 새 독립 입력에서 5개 adaptation은 원본, 3개 original은 과제 계약+대조군과 비교한다. 원본의 유효한 필수 결과를 잃지 않고, 지원되지 않는 완료/관찰을 주장하지 않아야 한다. 루트가 준비하는 새 8쌍은 이 조건을 보완하되 과거 반복 증거와 함께 해석한다. 새 실패가 있으면 실제 원인만 최소 수정하고 실패 사례+별도 사례를 재시험한다.
2. **실제 호출 정책 확인.** IA/user-flow/wireframe/build-design 4개는 자동+명시 도달, state-machine/break/explain-interface/variant 4개는 명시 전용이다. 새 세션에서 8개 모두 자동 호출되어야 한다는 기준은 잘못이다. 임시 설치 목록, 자동 선택의 4개, 명시 전용 4개의 긍정 호출 및 이웃 요청에서의 무단 호출 방지를 확인한다. user-flow의 계획 상태와 state-machine의 구현 상태, variant와 prototype, build-design과 원치 않는 재디자인을 구분한다.
3. **variant/build의 사용자 수용.** 동일 원본/후보 revision·viewport·state로 작동하는 비교를 보여주고 '업무에 사용할 수준'인지 사용자 판단을 기록한다. 특정 안을 좋아한다는 답변과 스킬의 비교 품질이 수용된다는 답변을 구분한다. 현재 기하·동작 통과만으로 외관 승인을 대신하지 않는다.
4. **정식 승격 명시 승인 및 패키징.** 이 요청은 검증·보완점 정리 권한이다. 새 8개 전체의 승격 승인으로 해석하지 않는다. 승인 뒤 해당 bucket/README/docs/router/plugin/provenance/Changeset을 맞추고 설치 검증을 수행한다. 현재 베타가 정식 plugin에 없다는 사실은 결함이 아니다. [정책](/Users/jinhokim/dev/paul-skills/AGENTS.md).

### P1: 지금 우선 보완할 가지와 증거 유지

1. **explain-interface의 whole-site 경로를 한 번 독립 비교.** CSS token/theme override, 두 폭, 실제 focus, 근거가 약한 framework fingerprint, 읽지 못한 stylesheet를 포함한 작고 알려진 로컬 site를 사용한다. 종료 기준은 실제 값/도출/추정/미관찰 구분, 중요한 스타일 sheet를 조용히 생략하지 않음, 단일 효과로 범위를 축소하지 않음이다. recipe 결과만으로 현재 cascade의 승자를 확정하지 않아야 한다.
2. **workbench guard와 관찰 예산.** state-machine은 input 안의 H/숫자/화살표가 상태를 바꾸지 않는지, 직접 URL과 reload/resize가 상태를 유지하는지 확인한다. break는 원본 컴포넌트/제품 CSS를 보존하고 단일 페이지의 지원되는 축만 표시하며 미관찰 실패를 보고하지 않는지 확인한다. 현재 QA 절차가 장시간 도구 setup이나 다중 전체 페이지 QA를 강제하지 않는지 관찰하고 실제 실패가 있을 때만 문구를 보완한다.
3. **수정된 단계 연결 한 건.** 이전 5단계 조합은 예전 wireframe 산출물이었고 수정된 미리보기/수정시험은 별도였다. 현재 IA→flow→wireframe→build에서 이전 ID·pending·return·화면 내부 link가 유지되는지 확인한다. 단계를 모두 새로 비교하는 비싼 평가가 아니라 실제 전달 파일의 digest와 정책/동작 보존을 확인하는 연결 검사로 한정한다.
4. **평가 재현 자료의 안정 경로.** 새 report에 현재 source/candidate/dependency/input/output hash와 실행 실패를 기록하고 원본은 manifest로 검증한 동결 bundle 또는 재확보한 pinned clone을 사용한다. 임시 loopback URL만 남기지 말고 정적 파일 위치/재실행 절차도 남긴다. 오래된 report의 '17개 전부 beta' 상태는 역사 기록으로 유지하고 현재 inventory와 혼동하지 않도록 새 report에서 시점을 명시한다.

### P2: 현재 범위 밖으로 기록할 확장

실제 사용자 tree test, 전체 locale/문자 조합, 모든 프레임워크·서버 streaming/동시성, 실제 VoiceOver/NVDA·터치기기, 모든 canvas/WebGL 내부 구현, 모든 시각 축과 디자인 시스템은 이번 승격의 보편 인증 요건으로 만들지 않는다. 프로젝트가 해당 기능을 사용하게 될 때 그 입력에 맞는 검증을 추가한다. Figma는 사용자가 명시적으로 사용하지 않으므로 로컬 경로 승격의 필수 작업에 넣지 않는다. 시간/토큰/비용 비교는 기록이 없으면 미측정으로 유지한다.

## 권장 결정 순서

현재 감사만으로 새 8개를 승격하지 않는다. 새 current-bundle 비교와 호출 검증을 먼저 끝낸다. 실패가 없다면 IA·user-flow·state-machine·break는 기능 검증 정리가 빠른 축이고, wireframe은 현재 단계 연결, explain-interface는 whole-site 경로를 추가로 확인하는 순서가 합리적이다. variant/build-design은 기능 검사와 별도로 사용자 시각 수용을 확보한다. 전체 8개를 한 번에 통과시키려는 목표 때문에 앞 여섯 개의 근거와 뒤 두 개의 미결 수용을 섞지 않는다.

이 문서는 어떤 입력에서도 항상 원본보다 우월하다는 주장을 하지 않는다. 선언한 역할의 대표 과제에서 원본의 유효한 결과를 보존했다는 증거와, 실제 미결 조건을 분리해서 사용자 결정을 돕는다.
