# Codex CLI compatibility and wireframe CSS evidence follow-up

기본 Codex CLI를 0.146.0에서 0.162.1로 갱신한 뒤, 실제 글로벌 paul-skills 0.4.4로 네 사례의 실행과 대상 계약을 확인했다. CSS 짝 비교는 baseline/candidate 모두 4/4에서 올바른 적용값을 설명했다. 과거 30px 오류는 이번 새 실행에서 재현되지 않았으며, 정확도 개선을 입증했다고 주장하지 않는다. wireframe에는 CSS 적용값과 측정 여부를 구분하는 짧은 예방 문단을 추가했다.

## CLI repair and installed validation

`which -a codex`의 첫 경로는 `$HOME/.local/bin/codex`였고 0.146.0을 실행했다. 같은 설정으로 도구를 쓰지 않고 `COMPAT_OK`만 요청해도 `gpt-6-astra requires a newer version of Codex` 오류가 재현됐다. 공식 npm 배포의 0.162.1을 해당 user prefix에만 설치했다. [공식 CLI 문서](https://learn.chatgpt.com/docs/codex/cli), [실제 진단 receipt](cli-repair.json)

모델 설정을 대체하지 않았다. 갱신 후 같은 최소 입력은 `COMPAT_OK`로 완료됐다. 두 native transcript에서 실제 CLI 0.146.0/0.162.1, 동일 `gpt-6-astra`와 low effort를 확인했다. 기존 Codex config와 Claude settings는 byte 단위로 동일하고, 해당 prefix의 다른 npm 패키지도 동일하다. 다른 CLI 경로는 건드리지 않았다. 참고로 bun/Homebrew 대체 경로의 버전 조회는 exit 137, 앱 번들은 0.162.0-alpha.17.2를 보고했다. 이 관찰은 다른 설치의 정상 작동을 증명하지 않는다.

새 [설치 검사](installed/PROTOCOL.md)는 이전과 같은 네 prompt와 fixture bytes, 실제 0.4.4 설치, inherited model, 세션 한정 low effort를 사용했다. 전부 native 완료했고 입력 파일은 바뀌지 않았다.

| 사례 | 결과 | 실제 적용 근거 |
| --- | --- | --- |
| 브랜드 갤러리 | 대상 계약 통과 | 설치 본문 주입, layout/first-impression 전체 읽기, 승인된 브랜드·CTA 부재·부분 구현 범위 보존 |
| 경고 확인 화면 | 대상 계약 통과 | audit procedure 읽기, 여섯 담당 본문 전체가 모델에 전달된 뒤 첫 fixture 내용 열람 |
| wireframe + 요청된 3초 검토 | 대상 계약 통과 | layout owner와 참조 전체 읽기, inline 64px 우선 해석, 좁은 폭 위험을 확인 대기로 유지 |
| staged 회귀 리뷰 | 대상 계약 통과 | primary router만 읽고 `$paul-skills:interface-review staged` 전달. 도메인·artifact 검사는 없음 |

stdout에 명령이 실행됐다는 사실과 모델이 실제 받은 본문을 구분했다. warning의 첫 합본 출력은 일부 잘렸지만 이어진 재읽기로 여섯 본문 전체가 첫 artifact read 전에 전달됐다. [scoped receipts](installed/receipts), [응답](installed/responses), [수동 판정](manual-review.json)

## CSS reproduction and comparison

기존 [0.4.4 wireframe 응답](../design-first-impression-0.4.4-release-2026-10-15/responses/claude-wireframe-requested-check.md)은 600px 이하 제목을 30px로 서술했다. 제공 HTML에는 inline 64px가 있어 이 설명은 잘못됐다. 원본을 고치지 않고 Playwright CLI 0.1.22 / Chrome 152.0.7977.82의 독립 측정으로 확인했다. 좁은 데스크톱 viewport이며 실제 모바일 기기 관찰은 아니다.

| Fixture | 1040px 계산값 | 360px 계산값 | 목적 |
| --- | --- | --- | --- |
| 원본 inline 64px | 64px | 64px | 과거 응답과 실제 cascade 불일치 확인 |
| 모바일 30px `!important` | 64px | 30px | inline이 항상 이긴다는 오판 방지 |
| inline 제거 | 38px | 30px | 정상 media 적용을 미확인으로 과도하게 보류하는지 확인 |

측정은 각 정확한 fixture HTML을 `setContent`로 렌더링하고 `getComputedStyle(h1).fontSize`를 기대값과 비교했다. [계산값](css-oracle.json)과 실행 스크립트 hash를 보존한다. 이 oracle은 평가 agent에게 주지 않았다.

후보를 작성하기 전 같은 글로벌 Claude 0.4.4로 한 번 [재현](reproduction/PROTOCOL.md)했다. CSS 우선순위는 올바르게 설명해 과거 값 오류를 재현하지 못했다. 대신 측정하지 않은 320px 잘림 가능성에 HIGH/Block을 부여했다. 이 새 실패도 보존하며 짝 비교의 분모에는 넣지 않는다.

후보는 wireframe의 delivery 단계에 한 문단만 추가했다. 대상 요소/폭의 최종 적용 선언을 확인하고, 소스로 추론한 값과 브라우저 계산값을 구분하며, 미측정 잘림은 검증 메모로 남긴다. human docs와 patch Changeset도 함께 갱신했다. 기존 layout 위임, first-impression 절차와 다른 skill은 그대로다. router는 역할과 진입 경계가 바뀌지 않아 수정하지 않았다.

사전 동결한 [비교 프로토콜](comparison/PROTOCOL.md)에 따라 동일 prompt, fixture, Claude Code 2.1.300 / `claude-opus-5-5` / low로 네 쌍을 실행했다. 원본 두 반복, important 대조, stylesheet 대조이며 모든 8개 native attempt가 완료됐다. 두 arm의 source 경로, layout 호출과 참조 전체 읽기도 확인했다.

| 사전 판정 항목 | Baseline | Candidate |
| --- | --- | --- |
| 실제 적용되는 모바일 제목 값 | 4/4 정확 | 4/4 정확 |
| 소스 추론을 브라우저 실측으로 주장하지 않음 | 4/4 | 4/4 |
| 미측정 잘림을 차단 사유로 삼지 않음 | 4/4 | 4/4 |
| layout owner + first-impression 참조 적용 | 4/4 | 4/4 |
| 브랜드/부분 구현 범위, 사람·fresh AI 미실행 보존 | 4/4 | 4/4 |

원본 두 반복에서 baseline은 미확인 위험에 LOW/Medium 우선순위를 붙였고 candidate는 검증 메모로 남겼다. 이는 표현상의 관찰이며 사후 성공 기준으로 추가하지 않았다. 사전 판정은 동률이다. 기존 오류와 새 진단의 과도한 Block을 근거로 최소한의 예방적 명확화를 유지한다. 더 큰 표본에서 재발률이 감소했는지는 미검증이다. baseline 한 응답은 영어로 작성됐으며 원문을 그대로 보존했다.

Claude provider-reported list-price cost는 진단 USD 0.2164032, 짝 비교 USD 1.7451028, 합계 USD 1.961506이다. 실제 청구액이나 모델 간 효율 비교가 아니다. Codex 비용은 보고되지 않아 `null`이며 usage만 기록했다. 사람 대상 3초 검증은 모두 `not_run`이다.

## Preservation and delivery boundary

과거 실패·미실행·응답·freeze·verifier를 수정하지 않았다. 원래 개발 checkout의 HEAD/dirty 상태와 untracked 77개 파일을 보존했다. 두 호스트의 설치는 계속 0.4.4이며 각각 176개 manifest/promoted 파일이 태그와 일치한다. 수정 후보는 session-local bundle에서만 비교했으므로, 이 기록은 새 paul-skills 릴리스나 글로벌 후보 설치를 뜻하지 않는다. [보존 기록](preservation.json)

원시 세션 context, 전체 설정, npm 목록은 ignored scratch에 남긴다. 공개 결과는 synthetic fixture, 필요한 receipt, 최종 응답과 hash뿐이다. 독립 브라우저와 loopback 서버는 종료했다. 태스크 브랜치는 `codex/cli-compat-wireframe-css`이며 이전 릴리스 기록 브랜치와 원래 dirty checkout은 그대로다.

검증 명령:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 evals/design-cli-css-repair-2026-10-15/verify.py
npm run check
```

위 검증은 통과했다. `npm run check`에서 버전·56개 source record·44개 promoted 경로와 38개 테스트를 확인했다. 정적/receipt 검증은 실제 사람 이해도나 모든 모델 실행의 정확성을 대신하지 않는다. `collect.py` 재생성에는 비공개 native 기록이 필요하며, `cli_probe.py`와 frozen runner는 기존 label/실행 디렉터리를 덮어쓰지 않는다.
