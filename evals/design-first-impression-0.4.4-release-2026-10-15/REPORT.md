# First-impression workflow 0.4.4 release and installation

사용자는 PR #26의 최종 검토, 문제 보완 후 병합, 릴리스와 설치 갱신을 승인했다. 기존 실패 기록과 관련 없는 변경은 보존했다. 이 기록은 릴리스와 실제 설치 검증이며 새 디자인 품질 비교나 사람 대상 3초 테스트가 아니다.

## Review and release

- [PR #26](https://github.com/reach0908/paul-skills/pull/26)은 최종 head `4df363da6efbbfd925d5d877d2943974608ccdc9`의 CI 성공 후 merge commit `ae85f6cd03ed55b6660f24f4a7d4f0762e0ae069`로 병합했다.
- 독립 Standards/Spec 검토 중 Standards에서 발견한 wireframe의 담당 스킬 우회 P2를 수정했다. 요청된 첫인상 검증은 `better-layout` Skill을 거치며 Skill 도구가 없으면 설치된 `SKILL.md`를 읽는다. 새 짝 비교에서 baseline은 참조만 읽었고 candidate는 담당 Skill 호출 후 참조 전체를 읽었다. 두 검토의 최종 차단 항목은 없었다. [최종 검토와 비교 근거](../design-first-impression-final-review-2026-10-15/REPORT.md)
- 자동 버전 PR 생성은 기존 Actions 권한으로 [실패](https://github.com/reach0908/paul-skills/actions/runs/38744721502)했다. 오류는 `GitHub Actions is not permitted to create or approve pull requests.`이다. 권한을 바꾸지 않고 생성된 버전 브랜치 그대로 maintainer가 [PR #27](https://github.com/reach0908/paul-skills/pull/27)을 열었다.
- 버전 diff는 Changeset 소비, changelog, package/lockfile/plugin version의 5개 파일뿐이었다. PR #27 CI 성공 후 `42b4d63cb5fb696fb5d0bba7c90fca6c8e874450`으로 병합했다.
- [Release 실행](https://github.com/reach0908/paul-skills/actions/runs/38745020351)이 성공했다. `paul-skills@0.4.4`의 원격 tag object는 `b6f900ebe63a2d422bbe25f563be58f0a5d5707c`, peeled commit은 위 버전 merge와 일치한다. 배포 단위는 immutable Git tag와 자체 marketplace이며 npm publish는 하지 않는다.

## Installed source and settings

| 확인 | Codex | Claude Code |
| --- | --- | --- |
| 실제 user-scope 설치 | 0.4.4, enabled | 0.4.4, enabled |
| 태그와 파일 비교 | promoted 파일 175개와 manifest 일치 | promoted 파일 175개와 manifest 일치 |
| 새 세션 발견 | promoted 44개, design 17개 | 각 native run에서 0.4.4 plugin path/version 확인 |
| 행동 검증 | 모델 호환 오류로 완료하지 못함 | 4건 완료, 아래 한계 포함 |

설치 갱신은 기존 marketplace/plugin에 호스트의 지원 CLI만 사용했다. Codex 설정 차이는 대상 marketplace의 `last_revision`, `last_updated`뿐이다. Claude settings는 byte 단위로 동일하다. 두 호스트의 다른 플러그인 version/scope/enabled는 바뀌지 않았다. [설치](installation.json), [발견](catalog.json), [설정 보존](settings-preservation.json)

현재 열린 대화의 카탈로그를 소급 갱신했다고 주장하지 않는다. Claude updater는 재시작 후 적용을 안내했다. 아래 검사는 실제 글로벌 설치를 사용하는 별도 새 세션이다.

## Fresh installed smoke

모델을 바꾸지 않고 각 호스트의 설정 모델과 세션 한정 low effort를 사용했다. Claude Code 2.1.300은 `claude-opus-5-5`에서 4건을 완료했다. Codex CLI는 0.146.0이었다. 총 native reported list-price cost는 USD 0.99526이며 실제 청구액이나 모델 간 우열을 뜻하지 않는다. 고정 입력, 240초 제한, 호스트당 실행 실패 2건 후 중단, 실패 재시도 금지를 사전 동결했다. [프로토콜](PROTOCOL.md), [동결](freeze.json), [수동 검토](manual-review.json)

| 사례 | Claude 결과 | 확인된 호출/근거 |
| --- | --- | --- |
| 승인된 브랜드 갤러리 | 대상 계약 통과 | 참조 전체 읽기, 승인된 콜라주/비대칭/CTA 부재 보존, 미구현 앵커를 현재 결함으로 판정하지 않음 |
| 모바일 확인 화면 | 대상 계약 통과 | audit procedure를 먼저 읽고 여섯 담당 Skill 성공 후 첫 artifact 열람, 경고/두 버튼/도움말 유지 |
| wireframe + 요청된 3초 검증 | 호출 계약 통과, 부수 오류 보존 | `better-layout` 성공 후 참조 전체 읽기. 다만 좁은 화면 제목을 30px로 서술한 것은 inline 64px 우선순위를 놓친 소스 해석 오류 |
| staged 변경 리뷰 | 대상 계약 통과 | 도구 호출 없이 `/paul-skills:interface-review staged` 전달 후 종료 |

네 응답 모두 읽고 hash에 결박해 검토했다. 전체 품질 4/4 통과라고 계산하지 않는다. wireframe의 반응형 설명은 정확한 화면 명세로 승인할 수 없다. warning의 명암비는 스스로 대략적인 머릿속 계산이라고 밝혔으며 재현 가능한 측정이 아니다. 브랜드의 낮은 심각도 조정 제안도 참가자 근거가 없는 주관적 제안이다. 이 오류와 한계는 응답 원문에 그대로 남았다. 이번 smoke는 설치 후 목표 계약 확인이며 새로운 품질 회귀 비교는 아니다.

Codex의 brand/warning은 native CLI가 `gpt-6-astra`에 대해 `requires a newer version of Codex`를 반환하여 모델 응답 전에 실패했다. 사전 중단 조건에 따라 나머지 2건은 `not_run`이다. 두 실패 세션의 host transcript에는 0.4.4 설치 경로와 정확한 선택 스킬 본문 주입이 확인되지만, 모델이 적용하거나 완료했다고 계산하지 않는다. 기존 모델 설정이나 별도 CLI 설치를 바꾸어 우회하지 않았다. Codex 행동 확인에는 호환되는 CLI 환경에서 별도 사전 동결 검사가 필요하다. [중단 기록](codex-stop.json), [실패 receipt](receipts/codex-brand.json)

사람 관찰과 fresh AI 관찰은 모두 `not_run`이다. 정적 이미지/소스에 대한 시간 제한 없는 자기 예측을 사람의 3초 이해 검증으로 승격하지 않았다. 모든 시작된 fixture의 파일 hash가 실행 전후 동일하다.

## Preservation and reproducibility

릴리스 태그와 PR #26 최종 head 사이의 모든 기존 eval 파일 2,737개와 skill 내용은 동일하다. 최초 실패, scope repair의 호출 순서 실패, entry-order 비교, 최종 검토 비교를 포함하는 first-impression 기존 241개 파일을 보존했다. 과거 source-sensitive verifier는 각 고정 revision에서 검증했으며 현재 버전 정보에 맞춰 과거 freeze를 고치지 않았다.

원래 개발 checkout은 HEAD `154c1a615fa973cefaf7a046fa074082417e91d5`, dirty 상태, untracked 77개 파일 내용이 모두 그대로다. 작업은 별도 clone에서 수행했다. [보존 근거](preservation.json)

공개 파일은 synthetic fixture, 최종 응답, 필요한 native receipt와 hash로 한정했다. 전체 설정, 다른 플러그인 정보, native session context는 ignored scratch에 남긴다. `collect_install_metadata.py`는 Python 3.11+가 필요하며, 처음 구형 Python에서 `tomllib` import가 실패한 뒤 설치된 Python 3.13으로 실행했다. 이는 모델 실행이나 재시도가 아니다.

```bash
python3 evals/design-first-impression-0.4.4-release-2026-10-15/verify.py
npm run check
```

위 두 검증은 성공했다. `npm run check`는 버전 일치, 56개 source record와 44개 promoted 경로, 38개 테스트를 통과했다. `verify.py`는 tag/source/receipt/수동 판정 hash의 일관성과 실패·미실행의 보존을 확인한다. 실제 사용자 검증이나 모델 응답의 완전한 정확성을 대신하지 않는다. 로컬 collector 재실행에는 비공개 원시 자료가 필요하다. frozen `run_smoke.py`를 다시 실행해 기존 시도를 덮어쓰면 안 된다.
