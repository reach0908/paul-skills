# 주장과 증거 연결

2026-10-14. 아래 원시 링크는 이 컴퓨터에 보존한 로컬 자료다. `.scratch`는 Git 배포 대상이 아니며, 과거 보고서 안의 상대 링크나 임시 서버 주소는 현재도 유효하다고 보장하지 않는다. SHA-256은 보존 이후 변동 확인에 사용하며 실행의 독립성이나 스킬 품질을 증명하지 않는다.

| ID | 확인한 주장 | 직접 증거 | 재검산·확인 방법 |
| --- | --- | --- | --- |
| E01 | 단계별 사용자 요청과 최종 응답 | [선별 대화](../../.scratch/design-field-review-20261014/thread-excerpts.json) | 관련 8턴의 사용자 요청·최종 메시지. 도구 로그와 내부 추론 제외 |
| E02 | 작업 상태와 원시 자료 보존 | [465개 파일 manifest](../../.scratch/design-field-review-20261014/source-manifest.json), [worktree 상태](../../.scratch/design-field-review-20261014/worktree-state.json) | 모든 파일 SHA-256 재계산, 복사 중 원본 안정성 검사 |
| E03 | 고정 번들 9스킬·23파일 로드 | [당시 로드 기록](../../.scratch/design-field-review-20261014/source/01-accessibility/evidence/skill-loads.md), [해시 결과](results.json) | 별도 원본·설치 경로 4행은 번들 23행에 중복 합산하지 않음. 보존 파일과 해시 대조 |
| E04 | 최초 15건 이름 불일치 해결 | [수정 전](../../.scratch/design-field-review-20261014/source/01-accessibility/evidence/labels-before.log), [수정 후](../../.scratch/design-field-review-20261014/source/01-accessibility/evidence/labels-after-final.log), [패치](../../.scratch/design-field-review-20261014/source/01-accessibility/evidence/implementation.diff) | `matchesVisibleAction` 0/15→15/15, 새 탭 안내 15/15 |
| E05 | 첫 변경의 화면 차이 0 | [당시 비교](../../.scratch/design-field-review-20261014/source/01-accessibility/evidence/visual-comparison.json), [재검산 코드](recheck_evidence.py) | 같은 폴더의 before/after 전체·카드 PNG 6쌍 크기 및 RGB 바이트 대조 |
| E06 | 환경 수정의 실체 | [환경 복구 보고서](../../.scratch/design-field-review-20261014/source/02-catalog-recovery/REPORT.md) | worktree 연결 변경, 정확한 이미지 허용 경로. 공유 DB 복구로 해석하지 않음 |
| E07 | 상세 5명과 가입 전 선택 흐름 | [2단계 개발](../../.scratch/design-field-review-20261014/source/02-catalog-recovery/evidence/flow-final.log), [2단계 빌드](../../.scratch/design-field-review-20261014/source/02-catalog-recovery/evidence/production-flow.log), [3단계 빌드](../../.scratch/design-field-review-20261014/source/03-integration/evidence/production-creator-onboarding.log), [4단계](../../.scratch/design-field-review-20261014/source/04-reading/creator-onboarding.log) | 각각 세 폭 × 5프로필, portraitLoaded, 5→4→reload4→5→review5, oauthSubmitted=false 확인 |
| E08 | 본문과 원본 카드의 통합 | [통합 보고서](../../.scratch/design-field-review-20261014/source/03-integration/REPORT.md) | 기존 작업 보존, 원본 이미지 복원, 8캡처/5인용/5카드쌍 기록 대조 |
| E09 | 본문 읽기 구조와 이름 링크 | [읽기 로그](../../.scratch/design-field-review-20261014/source/04-reading/reading-check.log), [새 링크 이동](../../.scratch/design-field-review-20261014/source/04-reading/mention-navigation.log) | viewport 객체 3개 추출. figures8/cards5/quotes5, H3·lists5/takeaways6, unlinkedMentions0 |
| E10 | 인용·캡처·기존 데이터 보존 | [4단계 보존](../../.scratch/design-field-review-20261014/source/04-reading/preservation.json), [5단계 보존](evidence/capture-content-preserved.json) | 보존 범위별 비교. 새 취재·대본 정확성 재검증과 구별 |
| E11 | 마지막 캡처 정렬 24건 통과 | [원시 브라우저 결과](../../.scratch/design-field-review-20261014/source/05-capture-card/after/browser.log), [전후 측정](evidence/capture-comparison.json), [QA 코드](../../.scratch/design-field-review-20261014/source/05-capture-card/verify-capture-layout.js) | 8×3 개수, aligned/linksInside/linksSeparate/imagesLoaded, overflow=false를 별도로 assert |
| E12 | 새 컴포넌트 키보드의 실제 범위 | [동일 QA 코드](../../.scratch/design-field-review-20261014/source/05-capture-card/verify-capture-layout.js), [동일 로그](../../.scratch/design-field-review-20261014/source/05-capture-card/after/browser.log) | 루프 종료 시 320px, 초기 `.focus()`, 이후 native Tab/Shift+Tab/Enter. 세 폭 모두 실행했다고 쓰지 않음 |
| E13 | 후속 전체 빌드 완료 | [2단계](../../.scratch/design-field-review-20261014/source/02-catalog-recovery/evidence/build-final.log), [3단계](../../.scratch/design-field-review-20261014/source/03-integration/evidence/build.log), [4단계](../../.scratch/design-field-review-20261014/source/04-reading/build.log), [5단계](../../.scratch/design-field-review-20261014/source/05-capture-card/build.log) | 각 521/521과 오류 문구 부재, 보고서와 대조. 이번 재조사에서 새 빌드를 실행하지 않음 |
| E14 | 전체 세션의 픽셀 동일성은 주장 불가 | [카드 비교](evidence/card-visual-comparison.json), [5단계 패치](../../.scratch/design-field-review-20261014/source/05-capture-card/change.patch) | 15개 카드 비동일, 10개 크기 차이. 사용자 요청에 따른 시각 변경 확인 |
| E15 | 구현 세션의 자체 리뷰 | [첫 리뷰](../../.scratch/design-field-review-20261014/source/01-accessibility/INTERFACE-REVIEW.md), [가독성 리뷰](../../.scratch/design-field-review-20261014/source/04-reading/INTERFACE-REVIEW.md), [최종 컴포넌트 보고서](../../.scratch/design-field-review-20261014/source/05-capture-card/REPORT.md) | 원 작성자의 Approve를 독립 심사 결과로 계산하지 않음 |
| E16 | 제품 채택과 릴리스 상태 | [사용자 요청 발췌](../../.scratch/design-field-review-20261014/thread-excerpts.json), [릴리스 확인](RELEASE-STATUS.md) | 배포 요청, PR 생성, CI, 병합, Ready, 운영 검증을 분리 |

후속 QA 보완의 새 브라우저 결과, 결함 주입 기록과 변경 코드 해시는 [QA-REPAIR.md](QA-REPAIR.md)에 연결했다. 이전 원시 증거를 덮어쓰지 않았다.

전체 재검산 결과는 [results.json](results.json)에 있다. 모델·비용과 미검증 분기는 임의의 0이나 PASS로 채우지 않았다. 최초 조사와 이후 스킬·검증 코드 보완의 증거를 구별한다.
