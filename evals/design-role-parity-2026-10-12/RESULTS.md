# 17개 디자인 역할 검증 결과

17개 역할의 기본 비교와 관찰된 결함의 수정 재시험을 마쳤다. 원본을 직접 가져온 13개는 이번 대표 과제에서 원본의 유효한 결과를 유지했다. 직접 작성한 4개는 요구 계약과 무스킬 조건으로 확인했다. 이는 모든 입력에서 무조건 원본 이상이라는 보증이 아니다. `variant`와 `build-design`의 주관적 외관 수용은 사용자 확인을 기다린다.

**현재 배치: 디자인 후보 17개 모두 `skills/in-progress/`, 승격된 디자인 스킬 0개.** Figma는 사용자 범위 밖이며 로컬 이미지·Markdown·브라우저 화면을 사용했다.

## 실행과 판정

| 구분 | 실제 실행 | 해석 |
| --- | ---: | --- |
| 기본 비교 | 68개 문맥, 204개 사례 수행 | 17역할 × 3사례 × 2조건 × 2반복 |
| 수정 재시험 | 16개 문맥, 46개 사례 수행 | 노출 사례와 새 사례, 이전 실패 보존 |
| 성능 보완 | 2개 문맥, 각 3회 브라우저 표본 | 2개 과제, 6측정 표본. INP/제품 우위 아님 |
| 단계 연결 | 5개 새 문맥 | IA → 흐름 → 와이어프레임 → 구현 → 리뷰 |

역할 실행은 총 86개 문맥에서 252개 사례를 수행했다. 연결 5단계와 평가자의 재현은 별도로 센다. 한 문맥의 사례 3개는 독립 통계 표본이 아니다. 같은 노출 과제의 재시험은 숨겨진 검증으로 취급하지 않는다.

## 역할별 결론

각 adaptation의 원본은 Jakub 저장소의 같은 이름 폴더다. 정확한 파일 링크와 다른 참고 레포의 관계는 [출처 표](../design-beta/source-map.md), 전체 현재 digest와 당시 실행 입력은 [현재 식별자](evidence/candidate-identities-current.json)와 [실행 기록](evidence/execution-receipts.json)에 있다. 아래 합격은 대표 과제의 객관적 결과에 한정한다.

| 역할 | 직접 원본 | 기본/추가 문맥 | 확인한 결과와 판정 |
| --- | --- | ---: | --- |
| [interface-review](../../skills/design/interface-review/SKILL.md) | Jakub / interface-review | 4/2 | 변경 원인·삭제 신호·동등 대체·공유 소비자 범위·변경 없음. [대표 결과 충족](evidence/interface-review-r5-repair-assessment.json) |
| [variant](../../skills/in-progress/variant/SKILL.md) | Jakub / variant | 4/4 | 실제 컴포넌트 비교·선택안 이관·정리·초점·작업 상태 유지. [대표 결과 충족, 외관 수용 대기](evidence/variant-r4-state-repair-assessment.json) |
| [state-machine](../../skills/in-progress/state-machine/SKILL.md) | Jakub / state-machine | 4/0 | 소스 상태 8개 및 경계 12개, URL·reload·정리. [대표 결과 충족](evidence/state-machine-r2-assessment.json) |
| [break](../../skills/in-progress/break/SKILL.md) | Jakub / break | 4/0 | 실제 컴포넌트의 내용·수량·폭 경계, 재현 가능한 결함, 제품 소스 보존. [대표 결과 충족](evidence/break-r2-assessment.json) |
| [explain-interface](../../skills/in-progress/explain-interface/SKILL.md) | Jakub / explain-interface | 4/0 | 효과 계층·복합 blur·시간 도출·WAAPI·이미지 가설 구분. [대표 결과 충족](evidence/explain-interface-r2-assessment.json) |
| [better-accessibility](../../skills/design/better-accessibility/SKILL.md) | Jakub / better-accessibility | 4/0 | 이름·폼·중복 제출·키보드·모달·제거 뒤 초점. 새 닫힘 초점 경쟁도 별도 재현. [대표 결과 충족](evidence/better-accessibility-r2-assessment.json) |
| [better-colors](../../skills/design/better-colors/SKILL.md) | Jakub / better-colors | 4/0 | 실제 렌더링 대비·CSS 우선순위·밝음/어두움. 잘못된 초기 검사 기준 보정. [대표 결과 충족](evidence/better-colors-r2-assessment.json) |
| [better-layout](../../skills/design/better-layout/SKILL.md) | Jakub / better-layout | 4/0 | 좁은 폭·LTR/RTL·실제 200% 확대에서 본문과 행동 접근. [대표 결과 충족](evidence/better-layout-r2-assessment.json) |
| [better-typography](../../skills/design/better-typography/SKILL.md) | Jakub / better-typography | 4/0 | 계층·숫자·긴 URL 원문 복원과 선택·모바일 16px·글자 확대. [대표 결과 충족](evidence/better-typography-r2-assessment.json) |
| [better-writing](../../skills/design/better-writing/SKILL.md) | Jakub / better-writing | 4/2 | 용어·행동·확인·회복 문구 및 삭제/권한 상실 뒤 빈 상태. [대표 결과 충족](evidence/better-writing-r3-repair-assessment.json) |
| [better-ui](../../skills/design/better-ui/SKILL.md) | Jakub / better-ui | 4/2 | 반전 가능한 모션·reduce·스크롤·테마와 선택 테두리 geometry. [대표 결과 충족](evidence/better-ui-r3-repair-assessment.json) |
| [better-interface](../../skills/design/better-interface/SKILL.md) | Jakub / better-interface | 4/2 | 6분야 원인별 검토·낮은 심각도·중복 통합·읽기 전용. [대표 결과 충족](evidence/better-interface-r4-dependency-assessment.json) |
| [build-design](../../skills/in-progress/build-design/SKILL.md) | Jakub / build-design | 4/0 | 로컬 이미지·디자인 데이터·Markdown/브라우저 참조, 토큰/동작 보존, 좌표·상태 비교. [대표 결과 충족, 외관 수용 대기](evidence/build-r2-assessment.json) |
| [information-architecture](../../skills/in-progress/information-architecture/SKILL.md) | 직접 작성, 원본 동등성 N/A | 4/0 | 기존 PM·객체·권한 미결·목적지와 필터·return 보존. [대표 결과 충족](evidence/information-architecture-r2-assessment.json) |
| [user-flow](../../skills/in-progress/user-flow/SKILL.md) | 직접 작성, 원본 동등성 N/A | 4/0 | 확인된 결과·중복 방지·회복·취소·미정 서버 정책과 기존 전이 보존. [대표 결과 충족](evidence/user-flow-r2-assessment.json) |
| [wireframe](../../skills/in-progress/wireframe/SKILL.md) | 직접 작성, 원본 동등성 N/A | 4/2 | 실제 조작 HTML·화면 명세·오류·Retry·receipt·reset. [대표 결과 충족](evidence/wireframe-r3-navigation-assessment.json) |
| [design-browser](../../skills/design/design-browser/SKILL.md) | 직접 작성, 원본 동등성 N/A | 4/4 | 전체 페이지·키보드·모션·source-only 증거 경계·User Timing/long task·로딩 전후와 정상 대조. [대표 결과 충족](evidence/design-browser-r4-transition-assessment.json) |

6개 역할의 지침을 보완했다. `interface-review`의 공유 소비자 총수, `variant`의 초점 가림과 작업 상태, `better-writing`의 데이터·접근 상실 후 회복 안내, `better-ui`의 선택 테두리 이동, `design-browser`의 전환 전후 관찰, `wireframe`의 화면 내 링크와 라우팅 구분이다. 수정 코드의 존재만으로 통과시키지 않고 실제 출력과 별도 재현을 확인했다. [실패·수정 기록](repairs.md).

## 원본과 얼마나 같은가

Jakub 원본은 MIT 라이선스의 `d574cc8a576dc24256ad38268b8d03d86724a1b3`에 고정했다. 원본 해시 65/65와 등록된 adaptation digest 13/13을 확인했다. 대응하는 스킬 파일 64개는 46개 바이트 동일, 18개 수정, 누락 0개다. 따라서 13개 폴더를 수정 없는 클론이라고 부르지 않는다. 도구 경로, 한국어와 로컬 구현, 관찰된 결함의 보완을 포함한 adaptation이다. [현재 출처 감사](evidence/provenance-current.json).

IA·흐름·와이어프레임·브라우저 절차는 직접 작성한 역할이다. Impeccable과 Playwright 문서의 영향은 출처 표에 구분돼 있다. 무스킬 조건도 좋은 결과를 냈으므로 네 역할의 우수성이나 효율 우위를 주장하지 않는다.

## 연결 검증에서 배운 점

실제 앞 단계 파일을 다음 단계에 넘기고 해시를 고정했다. 씨앗 ID, 계절 복귀, 필수 이름, 첫 실패·Retry, SP-21 내역, 모의 경계가 유지됐다. 두 폭에서 원본 화면과 구현을 재생했고 확정 화면의 위치와 PNG가 일치했다. [단계별 판정](evidence/composition-stage-assessments.json), [독립 동작 확인](evidence/composition-root-checks.json).

마지막 리뷰는 상세의 본문 링크가 목록으로 이동하는 결함을 찾았다. 와이어프레임에서 발생해 구현에 상속된 문제다. 실행자의 제한된 Approve를 전체 합격으로 사용하지 않았고, 원래 다섯 단계와 실패 기록을 보존했다. 별도 와이어프레임 재시험과 수정 미리보기의 동작 확인으로 후속 수정 근거를 남겼다. [연결 수정 판정](evidence/composition-repair-assessment.json).

[원래 연결 실행](http://127.0.0.1:48812/composition/app/)과 [수정 미리보기](http://127.0.0.1:48812/composition-repaired/app/)는 이 세션의 로컬 서버에서 볼 수 있다. 실서비스 예약이나 디자인 승인 결과는 아니다.

## 남아 있는 경계

- `variant`와 `build-design`의 [외관 비교 화면](http://127.0.0.1:48812/visual-review/)은 아직 사용자 수용 답변이 없다. A/B 표시는 가렸지만 URL에서 조건을 알 수 있어 완전한 blind 평가가 아니다.
- [역할별 검증 범위](branch-coverage.md) 밖의 입력, 실제 VoiceOver/NVDA·터치 기기·모든 브라우저·모든 디자인 시스템은 인증하지 않았다. 지연 목록의 시작·결과 관찰과 짧은 중간 로딩 상태 포착도 구분한다.
- Playwright 성능 보완은 로컬 150ms 작업의 User Timing과 long task다. 양쪽 모두 0→120개를 관찰했지만 대기·paint·INP나 도구 비용 우위의 증거가 아니다.
- 대략 240초인 연결 단계 예산을 일부 실행이 넘겼다. 실제 소요를 보존하고 엄격한 시간 제한 통과로 표현하지 않았다. 모델·토큰·비용 비교도 미측정이다.
- 명시 호출을 시험했다. 자동 발견·자동 선택은 별도이며 설치 링크 준비만으로 통과하지 않는다.
- 최종 패키지 검사와 품질 판정은 다르다. 모든 후보는 beta에 유지하며 사용자 검증과 명시적 승인 전에는 승격하지 않는다.

## 근거와 재현

[프로토콜](PROTOCOL.md), [전체 기계 판독 결과](results.json), [입력 쌍 감사](evidence/paired-input-audit-current.json), [산출물 무결성](evidence/integrity-final.json), [패키지 검사](evidence/package-check-current.json), [증거 파일 해시](evidence/manifest.json)를 함께 읽는다. 공개 구조화 결과와 원래 동결한 기준을 저장했다. 많은 원시 CLI 로그·스크린샷은 로컬 `.scratch/design-role-parity-20261012/`에 남으며 해시만으로 외부에서 열 수 있는 것은 아니다.

새 비교는 README의 준비 도구로 별도 디렉터리에서 실행한다. 고정된 과거 입력을 덮어쓰거나 원본의 오류를 최소 품질 기준으로 받아들이지 않는다.
