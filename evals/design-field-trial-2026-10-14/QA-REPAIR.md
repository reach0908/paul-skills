# 발견한 QA 빈틈 보완과 재검증

2026-10-14 KST. [최초 재분석](REPORT.md)에서 발견한 검사 누락을 스킬 지침과 INFLFEED 회귀 코드에 반영했다. 이번에는 저장 로그 재검산에 더해 **새로운 Playwright CLI 브라우저 실행**을 수행했다. 제품 화면·콘텐츠·데이터는 수정하지 않았다.

## 판정

**캡처 개수·가로 넘침 assertion과 키보드 검증 범위의 두 빈틈은 이번 로컬 재검증 범위에서 해결됐다.** 1440/390/320px에서 각각 캡처 8개, 자연스러운 키보드 경로 8개가 통과했다. 의도적으로 주입한 결함 18개는 모두 해당 검사에서 거부됐다. 이 결과를 새로운 원본 대비 스킬 동등성 실험으로 세지는 않는다.

| 검사 | 이전 | 보완 후 실제 결과 |
| --- | --- | --- |
| 캡처 개수 | DOM에서 발견한 만큼만 반복. 개수 assertion 없음 | 데이터 fixture의 8개와 DOM 개수, 순서별 저자·원문 URL을 검사. 0/7/9개는 세 폭 모두 실패 |
| 가로 넘침 | `overflow` 값을 출력 | lazy 이미지 로드 뒤 `scrollWidth <= clientWidth` assertion. 세 폭 모두 같은 폭으로 통과, 강제 넘침은 세 폭 모두 실패 |
| 컴포넌트 영역 | 이미지·캡션과 링크 일부 좌표 확인 | 기존 정렬·로드·링크 간격에 프레임 viewport 범위, 캡션 내부 넘침, 링크 상하 경계를 추가 |
| 키보드 시작 | 320px에서 첫 저자 링크에 `focus()` | 각 폭의 8개 캡처마다 새 문서의 BODY에서 native Tab으로 진입. 초기 hash 없음, 포커스 강제 지정 없음 |
| 키보드 순서·행동 | 첫 캡처의 Tab/Shift+Tab/Enter | 24개 캡처의 저자·원문 포커스와 정방향·역방향 순서. 실제 Enter로 저자 상세 24회·원문 24회 이동 |
| 검증 자체의 실패 경로 | 실제 실패 전파 테스트 없음 | 18개 DOM 결함 거부, 프로세스 종료·부분 증거 보존·CLI 오류·정리 실패 처리 테스트 3개 통과 |

## 스킬 반영

- [design-browser](../../skills/design/design-browser/SKILL.md): QA와 회귀 코드 작성 시 [executable QA evidence](../../skills/design/design-browser/references/qa-evidence.md)를 읽도록 연결했다. 예상 개수의 독립 기준, 측정값 assertion, viewport/state별 실행, 자연스러운 Tab 진입, 결함 주입 검증, 실패 증거·종료 코드 보존을 한곳에 둔다.
- [better-accessibility의 focus-and-keyboard](../../skills/design/better-accessibility/focus-and-keyboard.md): 자연스러운 진입과 프로그램으로 지정한 포커스를 구분하고, 보고서에서 주장하는 모든 폭·상태의 키보드 검증을 요구한다.
- `skill-sources.json`에는 기존 Jakub import/review revision을 유지하고 Paul 보완 결정과 local digest를 기록했다. [Changeset](../../.changeset/design-qa-evidence.md)을 추가했다. 17개 스킬의 역할과 라우팅, 베타 상태, 글로벌 설치는 변경하지 않았다. frozen trial bundle과 과거 로드 해시도 보존했다.

`writing-for-agents`의 단일 기준 문서와 조건부 참조 원칙을 적용했다. 공통 실행 절차를 접근성·레이아웃 스킬마다 복사하지 않았다. 승격 스킬의 동작이나 라우팅을 바꾸지 않아 별도 공개 docs 페이지와 promoted router 항목을 추가하지 않았다.

## 제품 검증 코드

INFLFEED의 격리 브랜치 `codex/article-capture-qa-20261014`에서 작성했다. [PR #272](https://github.com/reach0908/signal-feed/pull/272)의 범위는 다음 6개 파일이다.

| 파일 | 역할 |
| --- | --- |
| `scripts/verify-article-captures.mjs` | 실제 로컬 아티클의 배치·개수·키보드·목적지 검증, 실패 시 부분 결과 저장 |
| `scripts/verify-article-capture-qa.mjs` | 별도 세션에 결함을 넣고 같은 검사와 host validator가 이를 거부하는지 검증 |
| `scripts/verify-article-captures.test.mjs` | 브라우저 없이 CLI 프로세스 실패·부분 기록·정리 오류 경계를 확인하는 3개 단위 테스트 |
| `package.json` | 두 로컬 검증 실행 명령 |
| `product/evidence/2026-10-14-capture-qa/README.md` | 실행 조건, 범위와 한계 |
| `product/evidence/2026-10-14-capture-qa/results-summary.json` | 소스 해시와 폭별 실측 결과 |

제품 전용 코드는 제품 저장소가 소유한다. 과거 `verify-capture-layout.js`는 이전 증거의 일부이므로 수정하지 않았다. 유지보수할 새 검사로 대체하며, 원시 기록과 새 결과를 구별한다.

```sh
npm run test:article-captures -- http://127.0.0.1:8884 .local/article-capture-qa
npm run test:article-capture-qa -- http://127.0.0.1:8884 .local/article-capture-negative
node --test scripts/verify-article-captures.test.mjs
```

기존 로컬 빌드 미리보기의 제품 revision은 `d9e32693aedc3302686d52a2d983841d434e2784`다. 검사 코드는 별도 QA 브랜치에서 실행했다. 제품 runtime 변경이 없어 미리보기 재빌드를 검사 코드 검증으로 오인하지 않는다. Playwright CLI 0.1.22, Chrome 152, viewport 높이 1000px, reduced-motion, 폰트 준비·지연 이미지 decode 이후 측정했다.

## 폭별 증거

| 폭 | 개수·배치 | document scroll/client | native Tab 진입 | 저자/원문 Enter | 결함 주입 거부 |
| --- | --- | --- | --- | --- | --- |
| 1440 | 8/8 | 1440/1440 | 8/8 | 8/8 각각 | 6/6 |
| 390 | 8/8 | 390/390 | 8/8 | 8/8 각각 | 6/6 |
| 320 | 8/8 | 320/320 | 8/8 | 8/8 각각 | 6/6 |

각 캡처 저자까지의 실제 Tab 횟수는 세 폭 모두 `4, 9, 17, 24, 26, 33, 35, 42`였다. 탐색 상한 160을 넘으면 실패하며, 경로 전체를 원시 JSON에 저장했다. 컴포넌트 좌표의 허용 오차는 1 CSS px이고 문서 가로 넘침에는 허용 오차를 두지 않았다. 뷰포트 너비 대신 document client width를 써 스크롤바를 넘침으로 오판하지 않는다.

- [결과·소스·스킬 해시](qa-repair/results-summary.json)
- [새 원시 증거 manifest](qa-repair/evidence-manifest.json), [최종 정상 결과](../../.scratch/design-field-review-20261014/qa-repair/final-positive/results.json), [최종 결함 주입 결과](../../.scratch/design-field-review-20261014/qa-repair/final-negative/results.json)
- [1440px 포커스](qa-repair/keyboard-0-1440.png), [390px 긴 이름 포커스](qa-repair/keyboard-3-390.png), [320px 긴 이름 포커스](qa-repair/keyboard-3-320.png)
- [Paul 최종 저장소 검사](../../.scratch/design-field-review-20261014/qa-final-repo-check.log): 36개 테스트 통과. `claude plugin validate . --strict` 통과. 제품 변경 파일 Biome, 단위 테스트 3개와 diff 검사 통과.

브라우저 세션은 양성/결함 주입별로 분리했다. 각각 자신의 세션을 닫은 기록을 보존했고, 사용자 미리보기와 서버는 유지했다. 계정 상태 변경이나 OAuth 제출을 하지 않았다.

## 실패 기록과 한계

첫 실행은 1440px의 여섯 번째 캡처에서 YouTube가 `t=392`를 `t=392s`로 바꿔 실패했다. 같은 정수 초의 접미사만 정규화하고 영상 ID·전체 목적지·시각 비교는 유지했다. [최초 실패](../../.scratch/design-field-review-20261014/qa-repair/positive/result-1440.json)를 보존했으며, 수정 이후 전체 정상 검사와 결함 주입 검사를 다시 실행했다. 포맷 검사에서 드러난 finally의 오류 전파도 고친 뒤 최종 소스로 재검증했다.

로컬의 Vercel Analytics/Speed Insights 스크립트 404는 초기 콘솔에서 관찰했다. 이번 캡처·키보드 검사로 해당 서비스의 로컬 지원이나 전체 콘솔 무오류를 주장하지 않는다.

포커스 검사는 실제 `:focus-visible`, 양의 outline 폭, 뷰포트 내부 위치를 확인한다. 모든 가림·색상 대비 기준을 검증한 것은 아니다. 실기기 터치, 실제 스크린리더, 200% 브라우저 확대, Safari/Firefox, 외부 영상 재생과 사용자 성과는 별도다. 구현·검토는 같은 주 세션에서 수행했으며 독립 스킬 비교 실험은 추가하지 않았다.

## 전달 상태

QA 변경 커밋 `36d3b420e8490692eed5c6c4154e8f8ec26d91be`는 [PR #272](https://github.com/reach0908/signal-feed/pull/272)의 전체 CI와 GitGuardian 통과 후 **2026-10-14 01:58:08 KST**에 병합됐다. 메인 SHA는 `10128dcba86d6b38f54c3f1e40bab0aef4e824c0`이다. [GitHub 확인 응답](qa-repair/merge-receipt.json), [필수 CI](https://github.com/reach0908/signal-feed/actions/runs/38434060649/job/115423368671).

INFLFEED 기본 작업 폴더를 fast-forward했고, 메인의 검증 코드 3개가 테스트한 파일 해시와 같은지 확인했다. 이번 QA worktree는 소스·CLI 증거 67개를 별도로 보존한 후 정리했다. 정리 시 미커밋 증거 부족으로 자동 승인 검사가 한 차례 거절했으나, staged/unstaged/untracked/ignored 항목이 모두 없는 것을 다시 확인한 뒤 같은 정리 작업이 허용됐다. 다른 작업 폴더와 미리보기 서버는 유지했다.

Paul Skills 쪽은 스킬·출처·Changeset·평가 문서를 기존 작업 위에 보존했다. 이 변경은 로컬 베타 수정이며 글로벌 설치·승격·Paul Skills 릴리스를 수행한 것은 아니다. QA PR의 병합으로 새 운영 UI 배포를 검증했다고 주장하지 않는다.
