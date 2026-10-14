# Claude Code 디자인 스킬 17개 발견·호출 검증

2026-10-14 KST. 실제 사용자 범위 Paul Skills 0.4.0 설치본으로 새 Claude Code 프로세스를 실행했다. **확정 시험 34개 중 33개 통과, 1개 실패다.** 설치와 명시 호출은 정상이며, 일반적인 UI 변경 리뷰 요청의 자동 연결에서 보완점이 발견됐다.

## 결과

후속: [호출 경계 보완·회귀 검증](../design-claude-routing-repair-2026-10-14/REPORT.md)에서 로컬 수정 후보로 기존 34개 과제를 모두 통과했고, 최종 보완본의 13개 추가 시험도 통과했다. 아래의 0.4.0 설치본 33/34 결과와 실패 원문은 변경하지 않았다. 후속 수정은 아직 전역 설치에 배포하지 않았다.

| 항목 | 결과 |
| --- | --- |
| 실제 자동 목록과 직접 호출 목록 | 새 문맥 34/34에서 자동 12개, 직접 17개 일치 |
| 자연어에서 담당 스킬 선택·본문 로딩 | 12/12 |
| 명시 호출·설치 본문 일치 | 17/17 |
| 사용자 전용 경계 및 올바른 안내 | 4/5 |
| 자연어 17개에서 사용자 전용 본문 읽기·호출 시도 | 0회 |
| 입력 파일 변경 / 실행 오류 / 권한 거절 | 0 / 0 / 0 |

자동 대상 12개와 사용자 전용 5개는 서로 다른 정책이다. 17개 모두를 자동 실행해야 한다는 뜻이 아니다. Claude의 `init.skills`에는 사용자 전용 이름도 들어가므로 이를 자동 목록으로 세지 않았다. 실제 모델에 전달된 `skill_listing`과 직접 호출 목록 `slash_commands`를 별도로 확인했다.

| 스킬 | 자동 정책 | 자연어 선택 | 명시 호출 |
| --- | --- | --- | --- |
| better-interface | 자동 가능 | [통과](evidence/implicit-better-interface.json) | [통과](evidence/explicit-better-interface.json) |
| better-accessibility | 자동 가능 | [통과](evidence/implicit-better-accessibility.json) | [통과](evidence/explicit-better-accessibility.json) |
| better-layout | 자동 가능 | [통과](evidence/implicit-better-layout.json) | [통과](evidence/explicit-better-layout.json) |
| better-writing | 자동 가능 | [통과](evidence/implicit-better-writing.json) | [통과](evidence/explicit-better-writing.json) |
| better-typography | 자동 가능 | [통과](evidence/implicit-better-typography.json) | [통과](evidence/explicit-better-typography.json) |
| better-colors | 자동 가능 | [통과](evidence/implicit-better-colors.json) | [통과](evidence/explicit-better-colors.json) |
| better-ui | 자동 가능 | [통과](evidence/implicit-better-ui.json) | [통과](evidence/explicit-better-ui.json) |
| design-browser | 자동 가능 | [통과](evidence/implicit-design-browser.json) | [통과](evidence/explicit-design-browser.json) |
| information-architecture | 자동 가능 | [통과](evidence/implicit-information-architecture.json) | [통과](evidence/explicit-information-architecture.json) |
| user-flow | 자동 가능 | [통과](evidence/implicit-user-flow.json) | [통과](evidence/explicit-user-flow.json) |
| wireframe | 자동 가능 | [통과](evidence/implicit-wireframe.json) | [통과](evidence/explicit-wireframe.json) |
| build-design | 자동 가능 | [통과](evidence/implicit-build-design.json) | [통과](evidence/explicit-build-design.json) |
| interface-review | 자동 비노출 | 해당 없음 | [통과](evidence/explicit-interface-review.json) |
| state-machine | 자동 비노출 | 해당 없음 | [통과](evidence/explicit-state-machine.json) |
| break | 자동 비노출 | 해당 없음 | [통과](evidence/explicit-break.json) |
| explain-interface | 자동 비노출 | 해당 없음 | [통과](evidence/explicit-explain-interface.json) |
| variant | 자동 비노출 | 해당 없음 | [통과](evidence/explicit-variant.json) |

`better-interface`의 일반 화면 검토 자동 선택은 통과했지만, 아래의 변경 리뷰 경계 사례는 실패했다.

명시 호출은 `/paul-skills:<이름>`으로 시작했다. 실제 호스트 대화에 주입된 전체 본문을 설치본과 대조했다. 자연어 선택은 성공한 `Skill` 호출과 같은 본문의 실제 로딩이 함께 있어야 통과한다. 응답에서 이름을 언급한 것만으로 통과시키지 않았다. 본문 비교에서는 frontmatter를 제외하고, SKILL.md 전체 파일 해시와 호출 정책 파일 해시는 별도로 보존했다.

[전체 결과와 설치 해시](evidence/summary.json), [고정 과제 34개](cases.json). 설치본의 17개 SKILL.md 및 17개 agents/openai.yaml은 릴리스 `paul-skills@0.4.0`, 커밋 `b6e460adadc5ea438fc740f86fe07c2f2f43fe89`와 일치했다.

## 발견한 보완점: 변경 리뷰의 자동 연결

`boundary-interface-review`는 “커밋하지 않은 UI 변경 전체를 리뷰하고 회귀를 찾아 달라”는 요청이다. 이번 응답은 준비까지만이며, 빈 로컬 작업 폴더에서 실행했다.

- 기대: `better-interface`를 자동으로 읽고, 파일을 살피기 전에 사용자에게 `/paul-skills:interface-review working`을 직접 호출하도록 안내한다.
- 관측: 스킬을 하나도 호출하지 않고 일반 파일과 숨김 파일을 찾는 `Glob`을 두 번 실행했다. 이후 `better-interface` 자체를 명시적으로 호출해야 한다고 잘못 안내했다. 올바른 `interface-review working` 안내는 없었다.
- 영향: 사용자 전용 스킬이 무단 실행되지는 않았다. 다만 자연어 변경 리뷰 요청에서 의도한 진입점 안내를 보장하지 못했다. diff 검토나 제품 변경은 실제로 일어나지 않았다.

[실패 응답과 도구 기록](evidence/boundary-interface-review.json). 정해 둔 소유 스킬 선택, 명시 호출 안내, 선행 파일 조사 금지 검사 3개가 한 사례에서 실패했다. 빈 폴더의 파일 탐색과 실제 diff 내용 검토를 구분한다. 이 실패를 숨기거나 통과 기준을 낮추거나 응답이 좋아질 때까지 다시 실행하지 않았다.

우선순위 1은 `better-interface`의 자동 진입 설명에서 “변경 리뷰 요청에도 이 스킬을 먼저 선택한다”와 “사용자가 직접 호출할 대상은 interface-review다”를 더 명확히 구분하는 것이다. 현재 관측은 잘못된 안내를 증명하지만, 설명 문구가 유일한 원인인지는 확정하지 못한다. 수정 후보는 빈 폴더와 실제 Git 변경이 있는 로컬 fixture, 여러 한국어 표현에서 기존 버전과 비교해야 한다. 이 요청에서는 스킬 본문이나 설치본을 수정하지 않았다.

당장 변경 리뷰의 진입은 `/paul-skills:interface-review working`을 직접 지정할 수 있다. 이 명시 경로의 본문 주입과 준비 응답은 [통과 기록](evidence/explicit-interface-review.json)이 있다. 실제 변경 분석과 구현 결과까지 이번 시험에서 검증한 것은 아니다.

## 사용자 전용 경계와 역할 확인

| 사용자 전용 역할 | 자연어 경계 과제 | 관측 |
| --- | --- | --- |
| [interface-review](evidence/boundary-interface-review.json) | 커밋하지 않은 UI 변경 리뷰 | 실패: 사용자 전용 실행은 없었으나 올바른 직접 호출 안내 누락 |
| [state-machine](evidence/boundary-state-machine.json) | 저장 작업의 행동·전이·이탈·복귀 계획 | 통과: user-flow 호출, state-machine 본문 접근 없음 |
| [break](evidence/boundary-break.json) | 단일 카드의 좁은 폭·긴 제목 점검 준비 | 통과: break 본문 접근 없음 |
| [explain-interface](evidence/boundary-explain-interface.json) | flex와 gap의 짧은 개념 설명 | 통과: explain-interface 본문 접근 없음 |
| [variant](evidence/boundary-variant.json) | 기존 카드 radius의 작은 보정 | 통과: variant 본문 접근 없음 |

`state-machine`의 명시 응답은 실제 컴포넌트와 기존 데이터 연결을 유지하고 코드에 없는 상태를 새로 만들지 않는 작업대로 설명했다. 자연어 작업 흐름은 `user-flow`가 담당했다. `break`는 극단 조건의 점검 페이지, `variant`는 현재안을 유지한 비교 작업대, `explain-interface`는 구현 메커니즘 설명으로 진입했다. [중요 경계의 응답 검토](evidence/manual-review.json)를 보존한다. 이는 준비 응답의 역할 확인이며 실제 작업대를 구축한 결과가 아니다.

## 시험 조건과 방법 보완

Claude Code 2.1.296, 실제 해석된 모델 `claude-opus-5-5`, 관측된 추론 수준 `xhigh`다. 사용자 설정의 `opus`를 그대로 사용했고 모델이나 시스템 프롬프트를 바꾸지 않았다. 다른 전역 스킬도 보이는 환경이다. 테스트용 plugin-dir이나 프로젝트 스킬 복사로 전역 설치를 대신하지 않았다.

임시 작업 폴더와 새 session ID를 사용하고 각 요청은 준비 또는 짧은 명세로 한정했다. 도구는 Skill, Read, Glob, Grep이며 일반 권한 검사와 비대화형 거절을 사용했다. 선택적 훅은 이 프로세스에서만 끄고 관련 없는 MCP 서버는 제외했다. 제품 파일 수정, 브라우저 실행, 성능 측정, 실제 서비스 접근은 이 모델 시험의 범위 밖이다.

예비 실행 1회로 기록 형식을 확인했다. 이어진 첫 자연어 12회는 폴더 이름에 기대 스킬명이 들어가는 방법상의 문제가 발견됐다. 모델의 환경 정보에 힌트가 될 수 있으므로 모두 최종 점수에서 제외하고, 같은 요청을 `case_018` 같은 중립적인 번호 폴더에서 다시 실행했다. 명시 17회와 경계 5회도 중립 폴더를 사용했다. 변경한 조건과 기존 기록을 [프로토콜 1](PROTOCOL.md), [프로토콜 2](PROTOCOL-2.md), [제외한 실행](exploratory-evidence/summary.json)에 보존한다.

| 실행 구분 | 새 문맥 수 | 호스트 정가 추정 비용 |
| --- | --- | --- |
| 예비 수집 확인 | 1 | USD 0.132472 |
| 폴더명 힌트가 있어 제외한 탐색 | 12 | USD 4.985641 |
| 중립 폴더의 확정 시험 | 34 | USD 11.983469 |
| 전체 | 47 | USD 17.101582 |

비용은 호스트가 제공한 정가 기준 추정치다. 실제 청구액은 확인하지 못해 `null`로 둔다. 입력·출력·캐시·추론 토큰과 실행 시간은 사례별 JSON에 있다. 최대 동시 실행은 2개, 회당 240초와 추정 USD 0.80 한도다. 방법 보완을 반영한 전체 실행 중단 기준은 USD 20이었다. 모델 응답을 보고 유리한 결과로 바꾸려는 재시도는 없었다.

## 검증 코드와 보관

- [실행 코드](run_trials.py), [증거 수집](collect.py), [공개 증거 검증](verify_evidence.py).
- 판정 코드의 [13개 통제 시험](test_collector.py): 이름만 언급, 잘린 본문, 거절된 호출, 본문 없는 호출, 사용자 전용 본문 우회 읽기, 설치 목록과 자동 목록 혼동, 미완료 프로세스 등을 검사한다.
- 저장소 `npm run check`: 출처 기록 56개, 정식 경로 44개, 기존 테스트 38개 통과. [검사 기록](evidence/validation.json).
- 원시 로그는 `.scratch/design-claude-discovery-20261014/`와 `.scratch/design-claude-discovery-20261014-v2/`에 보관했다. 공개 기록에는 원시 대화와 출력의 해시, 관련 스킬 로딩, 도구 호출, 시험 응답과 측정값만 남긴다. 인증, 전체 시스템 프롬프트와 개인 설정은 포함하지 않는다.
- JSON 응답의 em dash는 같은 문자로 복원되는 JSON escape로 보관한다. 모델 응답의 의미나 판정 근거를 바꾸지 않는다.

로컬 원시 기록 재수집은 `python3 evals/design-claude-discovery-2026-10-14/collect.py`, 모델 실행 없는 공개 자료 검증은 `python3 evals/design-claude-discovery-2026-10-14/verify_evidence.py`다. [MANIFEST.json](MANIFEST.json)은 보고서·과제·코드·공개 증거의 파일별 해시를 고정한다. 새 유료 실행은 기존 기록을 덮어쓰지 말고 별도의 프로토콜과 경로에서 진행한다.

## 판단 범위

이 결과는 해당 입력에서의 Claude Code 발견·진입·호출 경계다. 역할당 자연어 1회는 일반적인 호출 성공률이나 모든 문구에 대한 보장이 아니다. 실제 제품 저장소의 지침이 섞인 문맥, 장기 대화, 이미 열린 Claude 터미널이나 Desktop UI의 목록 갱신은 별도다. 디자인 산출물 품질, 17개 역할의 원본 이상 동등성, 접근성 인증, 시각적 일치나 실제 QA 실행의 새 증거로 사용하지 않는다.

이전 승격 보고서의 “Claude 모델 실행 미검증” 상태는 이 후속 기록으로 갱신한다. 다만 변경 리뷰의 자동 연결 실패가 남아 있으므로 Claude의 모든 호출 경계가 완전히 통과했다고 판단하지 않는다.

## 근거 문서

- [Claude Code의 스킬 호출 정책](https://code.claude.com/docs/en/skills#control-who-invokes-a-skill): 자동 및 직접 호출, 본문 로딩.
- [프로그램 실행](https://code.claude.com/docs/en/headless): 새 CLI 프로세스와 구조화된 출력.
- [프로세스별 훅 설정](https://code.claude.com/docs/en/hooks#disable-or-remove-hooks): 시험 범위 한정.
- [앞선 승격·설치 보고서](../design-final-promotion-2026-10-14/REPORT.md): Codex와 패키지 검증의 기존 기록.
