# 디자인 리뷰 스킬 9개 정식 승격

2026-10-14 KST. 사용자가 직전의 9개 승격 권고에 대해 “추천하는 방향으로 모두 진행하자”라고 승인했다. 이 기록은 그 승인에 따른 정식 편입과 배포 검증을 다룬다.

## 승격 범위

| 호출 방식 | 스킬 |
| --- | --- |
| 사용자 직접 호출 | `interface-review` |
| 자동 또는 직접 호출 | `better-interface`, `better-accessibility`, `better-layout`, `better-writing`, `better-typography`, `better-colors`, `better-ui`, `design-browser` |

플러그인의 정식 스킬은 27개에서 36개로 늘어난다. 후보의 파일 61개를 `skills/in-progress/`에서 `skills/design/`으로 옮겼다. 60개는 [직전 검증](../design-routing-repair-2026-10-14/REPORT.md)과 바이트가 같다. 독립 규칙 검토에서 나온 Aside 조사 참조 파일 1개의 호출 표현만 보완했으며, [승인본 해시](approved-files.json)와 [검토 후 변경](reviewed-adjustments.json)을 별도로 보존했다. 직접 원본 8개는 Jakub의 고정된 소스에서 적응한 스킬이고 `design-browser`는 직접 작성한 실행 역할이다. 원본 revision과 출처별 digest를 승격 때문에 다시 찍거나 원본 검토 이력을 진전시키지 않았다.

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
- 전체 신규 파일을 포함한 공백 검사에서 고정 평가 자료 28개에 43개 경고가 나왔다. 패치의 문법상 공백과 기록된 파일 끝 개행을 보존하도록 해당 경로만 `.gitattributes`에 지정했다. 실제 스킬과 구현 파일의 검사는 유지했다.
- 승인본 파일 60개 해시 일치, 검토 후 수정 파일 1개는 이전·이후 해시로 검증.
- 인증 정보 패턴 검사에서 발견된 실제 키나 토큰 없음. 모델 원시 로그와 임시 인증 연결은 공개 패키지에 포함하지 않는다.

## 독립 검토

### Standards

문서화된 규칙 위반 1건: `design-browser/references/aside.md`가 `research` 의존성을 명시적인 Skill 도구 호출로 표현하지 않았다. 해당 도구가 있으면 호출하고, 없을 때만 설치된 파일을 읽고 절차를 따르도록 고쳤다. 도구 없는 호스트의 기존 경로는 유지된다. 단어 수준의 패키지 검토이며 실제 Aside 모델 실행을 새로 했다는 뜻은 아니다.

선택적 개선 1건: 기존 `prototype`과 `design-browser`의 도구 정책에 일부 중복이 있다. 현재 동작이 일치하며 승인된 프로토타입 흐름을 이 승격에서 다시 바꾸지 않았다. 추후 통합 대상으로 남긴다.

### Spec

요구사항 누락, 요청 밖 변경, 잘못된 구현을 발견하지 못했다. 검토 당시 61개 후보 파일이 이전 최종 시험 패키지와 같았음을 별도로 대조했다. 그 뒤의 규칙 보완 1개는 위 조정 목록에 기록한다.

## 릴리스와 설치

**Paul Skills 0.3.0 정식 발행과 두 호스트의 전역 설치 갱신을 완료했다.** [승격 PR #11](https://github.com/reach0908/paul-skills/pull/11)과 [버전 PR #12](https://github.com/reach0908/paul-skills/pull/12)는 병합됐고 각각 저장소 CI를 통과했다.

- 태그: `paul-skills@0.3.0`
- 태그가 가리키는 커밋: `0fd300cfa675dbaac149d416294fd6454df58474`
- 태그 객체: `3b6338382786b76c4c06388f2104ceefd914d10b`
- 해당 커밋의 Release와 Validate skills 워크플로 모두 성공. [원격 실행 영수증](evidence/release.json).

자동 버전 PR 생성은 GitHub Actions의 PR 생성 권한 제한으로 한 번 실패했다. [실패 실행](https://github.com/reach0908/paul-skills/actions/runs/38501395583)의 원문은 `GitHub Actions is not permitted to create or approve pull requests.`다. 유지관리 문서에 따라 자동 생성된 `8ebaefb` 브랜치를 그대로 현재 유지관리 계정으로 PR #12에 올렸다. 토큰 권한은 변경하지 않았다. 그 뒤 태그 발행은 [정상 완료](https://github.com/reach0908/paul-skills/actions/runs/38501575475)했다.

| 확인 대상 | 결과 |
| --- | --- |
| Codex 사용자 범위 플러그인 | 0.3.0, 활성, 정식 스킬 36개 |
| Claude Code 사용자 범위 플러그인 | 0.3.0, 활성, 정식 스킬 36개 |
| 각 설치본 파일 대조 | 정식 스킬 파일 143개 모두 릴리스와 해시 일치 |
| manifest 대조 | 두 설치본 모두 릴리스 manifest와 동일 |
| 새 Codex app-server 카탈로그 | 36개 모두 설치·활성 상태로 발견 |

[설치 영수증과 파일별 해시](evidence/installation.json). 설치 방법은 [공식 OpenAI 플러그인 문서](https://developers.openai.com/plugins/build/plugins)와 설치된 CLI 도움말로 확인했다. Codex에서는 marketplace upgrade 후 plugin add를 사용했고, Claude에서는 marketplace update 후 사용자 범위 plugin update를 사용했다.

## 설치 후 새 세션 검증

실제 전역 설치본을 사용해 대화 이력이 없는 Codex CLI 세션 3개를 실행했다. 모델은 앞선 검증과 같은 `gpt-5.6-sol`, 추론 설정은 `xhigh`다. 정상 전역 메모리와 다른 설치 기능은 유지했으므로 격리·맹검 품질 비교가 아니라 설치 후 호출 점검이다.

| 사례 | 확인 결과 |
| --- | --- |
| 이름 없는 미커밋 변경 요청 | `interface-review working` 안내로 종료. 변경 diff와 화면 소스를 검토하거나 판정을 내리지 않음 |
| 일반 화면 리뷰 | `better-interface`와 6개 도메인 로딩. 키보드·가로 넘침·중복 상세 내용·기본 글꼴 설정의 4개 유효 발견 유지 |
| 명시한 `interface-review working` | 사용자 직접 호출이 실제 스킬 본문으로 주입됨. 정확한 작업 트리 범위를 검토하고 키보드 회귀와 기존 가로 넘침 문제를 분리 |

세 세션의 자동 선택 목록에는 디자인 역할 8개가 있었고 사용자 전용 `interface-review`는 없었다. 명시 호출에서는 설치된 파일과 일치하는 전체 본문이 제공됐다. 세 입력 화면은 전후 해시가 같으며 브라우저를 실행하거나 수정하지 않았다. [3/3 요약](evidence/smoke-summary.json), [일반 변경 요청](evidence/implicit-diff-a.json), [화면 리뷰](evidence/implicit-review.json), [명시 변경 리뷰](evidence/explicit-review.json).

첫 수집 결과는 2/3이었다. 수집기가 성공한 스킬 읽기 뒤의 검색 결과 없음(exit 1)을 명령 전체 실패로 취급했고, 호스트가 직접 주입한 스킬 본문도 누락했다. 전체 주입 본문을 실제 설치 파일과 대조하는 수집 보완 후, 같은 로그에서 3/3으로 재산정했다. 모델 재실행이나 실패 표본 제외는 없었다. [수집 보완 기록](evidence/collector-correction.json)과 [수집 코드](collect_smoke.py)를 남긴다. 원시 실행 로그는 로컬 `.scratch/design-promotion-20261014/`에 보존한다.

이 검증은 새 브라우저 QA나 전체 원본 비교의 재실행이 아니다. Claude Code 모델 실행과 기존에 열려 있던 데스크톱 대화의 목록 갱신도 확인하지 않았다. 새 채팅에서 정식 스킬을 사용하고, 기존 대화가 이미 받은 목록과 새 설치본을 구분한다. 나머지 8개 디자인 후보는 정식 플러그인 밖의 베타로 유지한다.
