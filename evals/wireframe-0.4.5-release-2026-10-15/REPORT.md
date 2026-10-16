# Wireframe responsive evidence 0.4.5 release

사용자가 PR #29의 최종 검토, 문제없을 때 머지, 릴리스와 설치 갱신을 승인했다. PR #29와 버전 PR #30을 머지했고, `paul-skills@0.4.5` 태그와 두 호스트의 글로벌 설치를 확인했다. 새 wireframe 설치 검사는 Codex와 Claude Code 각각 1/1 완료했다. 이전 4/4 대 4/4 비교의 동률과 실패 기록은 그대로다.

## Review and release

- [PR #29](https://github.com/reach0908/paul-skills/pull/29)의 정확한 head `4e7a8ca47810ec5c04dac2418fa5bec61d28c6be`를 최종 검토했다. Standards 0건, Spec 0건으로 머지 차단 사항이 없었다. 앞선 전체 검토와 13개 native receipt 재계산을 재사용하고, 이후 보고서 문단만 추가된 것을 확인했다. 로컬 38개 테스트, 두 strict manifest 검사, 평가 무결성 검사와 PR CI가 통과했다.
- Source merge는 `f42de07afe7870e358feb213c54065460f429a01`이다. [버전 자동화](https://github.com/reach0908/paul-skills/actions/runs/38753655750)는 버전 브랜치를 생성했지만 GitHub Actions의 PR 생성 권한 제한으로 실패했다. 권한을 바꾸지 않고 같은 생성 브랜치로 [PR #30](https://github.com/reach0908/paul-skills/pull/30)을 제출했다. 버전 메타데이터, changelog, Changeset 소비 외 변경은 없었다.
- 버전 PR도 로컬 검사와 CI 통과 후 머지했다. [Release 실행](https://github.com/reach0908/paul-skills/actions/runs/38754063299)이 성공했고, [0.4.5 태그](https://github.com/reach0908/paul-skills/tree/paul-skills%400.4.5)의 peeled commit `f817160249b7a3ac5a139f5d72a82863ceca4351`은 버전 merge 및 workflow head와 일치한다. tag object는 `7a3bc20ffd6fa10b7d138dbecad5eead64e58c26`이다. 배포는 namespaced Git tag와 자체 marketplace이며 npm publish는 없다. [릴리스 receipt](release.json)

## Installed sources and fresh sessions

두 호스트의 지원 명령으로 기존 `paul-skills` marketplace만 갱신했다. Codex는 `plugin marketplace upgrade paul-skills` 후 `plugin add paul-skills@paul-skills`, Claude Code는 `plugin marketplace update paul-skills` 후 user-scope `plugin update`를 사용했다. 두 설치 모두 0.4.5로 enabled이며, 각각 manifest와 promoted 파일 176개가 태그와 byte 단위로 일치했다. 새 Codex app-server의 `skills/list`에서도 44개 promoted skill과 그중 17개 design skill을 확인했다. [설치](installation.json), [발견](catalog.json)

사전 동결한 [프로토콜](installed/PROTOCOL.md)에 따라 기존 갤러리 fixture와 wireframe prompt를 각각 한 번 실행했다. 실제 글로벌 설치를 사용하고, 새 중립 폴더와 inherited model, 세션 한정 low effort 요청을 유지했다. 브라우저와 추가 참가자는 사용하지 않았다. 재시도는 없고 입력 파일도 동일하다.

| Host | Native 결과 | 적용 근거 | 화면 명세 결과 |
| --- | --- | --- | --- |
| Codex CLI 0.162.1 / gpt-6-astra | 완료, 61.703초 | 0.4.5 wireframe 전체 본문 주입, layout owner 전체 본문과 first-impression 참조 전달 | inline 64px 우선, 소스와 실측 구분, 미측정 잘림은 확인 대기 |
| Claude Code 2.1.300 / claude-opus-5-5 | 완료, 41.004초 | 0.4.5 plugin path/version, 명시 command 확장, layout Skill 실행과 참조 전체 읽기 | inline 64px 우선, 320px 측정 후 판단, 승인된 브랜드·부분 구현 범위 보존 |

Claude stream은 command 확장 receipt를 제공하지만 확장된 primary 본문 전체를 노출하지 않는다. Codex는 native 입력에서 설치된 primary 본문과의 정확한 일치를 확인했다. 이 증명 범위를 서로 같다고 취급하지 않는다. [Scoped receipts](installed/receipts), [응답](installed/responses), [수동 판정](manual-review.json)

Codex의 `Approve`는 정적 레이아웃 범위로 제한됐다. Claude의 placeholder 접근성 제안은 구현 의도 확인을 전제로 하며, 실측된 사용성 결함으로 채택하지 않는다. 사람 대상 3초 관찰과 독립 fresh-AI 관찰은 두 응답 모두 `not_run`이다. 두 설치 검사는 정확도 향상이나 모든 디자인 판단의 정당성을 증명하지 않는다. 기존 [CSS 비교](../design-cli-css-repair-2026-10-15/REPORT.md)의 4/4 대 4/4 동률과 과거 오류 비재현 결론을 바꾸지 않는다.

Claude provider-reported list-price cost는 USD 0.2361584이며 실제 청구액이 아니다. Codex 비용은 미보고 `null`이고 usage만 보존한다. 이미 열린 대화가 새 지침으로 소급 교체됐다고 주장하지 않으며, 새 호스트 세션에서 활성화를 확인했다.

## Preservation and verification

PR #29 head에 있던 평가 파일 2,849개를 그대로 보존했다. 과거 CLI 실패, CSS 오류 응답, 미실행과 별도 진단의 과도한 Block 모두 포함한다. 원래 개발 checkout의 HEAD `154c1a6`, dirty 상태와 untracked 77개 파일도 동일하다. 두 호스트의 다른 plugin version/scope/enabled는 동일하고, Codex config와 Claude settings의 bytes도 바뀌지 않았다. 전체 설정과 native context는 ignored scratch에만 남긴다. [보존](preservation.json), [설정](settings-preservation.json)

```bash
PYTHONDONTWRITEBYTECODE=1 python3.13 evals/wireframe-0.4.5-release-2026-10-15/verify.py
```

Metadata collector는 `tomllib`을 위해 Python 3.11 이상이 필요하다. 기본 Python 3.9 실행의 import 오류 뒤 설치돼 있던 3.13으로 실행했으며 시스템 Python을 변경하지 않았다. `collect.py`의 재생성에는 비공개 scratch 기록이 필요하고, `verify.py`는 공개 receipt와 고정 Git 소스로 검증한다. 원시 모델 응답은 문체까지 원문 그대로 보존한다.
