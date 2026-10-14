# Paul Skills 0.4.1 release and global host verification

2026-10-14. 정식 패치 발행과 Codex·Claude 사용자 전역 설치 갱신을 완료했다. 두 호스트의 설치 파일은 릴리스 태그와 일치한다. 새 세션의 본문 로딩과 카탈로그는 확인됐지만, 행동 기준 전체 통과는 Claude 6/6, Codex 5/6이다. Codex의 자동 staged 리뷰 한 건은 라우터를 읽기 전에 저장소를 살펴보고 도메인 스킬을 읽어 실패했다. 따라서 양쪽 호출 경계가 완전히 해결됐다고 판정하지 않는다.

## Release and installation

| 항목 | 확인 결과 |
| --- | --- |
| 정식 버전 | `0.4.1` |
| 태그 | [`paul-skills@0.4.1`](https://github.com/reach0908/paul-skills/tree/paul-skills%400.4.1) |
| 릴리스 커밋 | `f90ae4f68b00a2f0e3bfa63eb867267053e14453` |
| 수정 PR | [#17](https://github.com/reach0908/paul-skills/pull/17), 병합 완료 |
| 버전 PR | [#18](https://github.com/reach0908/paul-skills/pull/18), 병합 완료 |
| 태그 발행 | [Release 38542421422](https://github.com/reach0908/paul-skills/actions/runs/38542421422), 성공 |
| Codex 전역 | 사용자 범위, 활성, 0.4.1 |
| Claude 전역 | 사용자 범위, 활성, 0.4.1 |
| 내용 대조 | 각 호스트의 정식 스킬 파일 173개 및 plugin manifest 1개가 태그와 바이트 단위 일치 |
| 새 Codex 카탈로그 | 정식 44개 활성, 디자인 17개 직접 발견 가능 |

자동 버전 PR 생성은 [Release 38542132082](https://github.com/reach0908/paul-skills/actions/runs/38542132082)에서 GitHub Actions의 PR 생성 권한 제한으로 실패했다. 저장소 유지보수 규칙대로 자동 생성된 동일 브랜치를 승인된 maintainer PR로 올렸다. 권한 설정을 확대하지 않았다. npm 패키지를 발행하는 저장소가 아니며, 이번 발행도 namespaced Git 태그다.

수정은 자동 리뷰 진입점인 `better-interface`가 파일 검사 전에 화면 감사와 변경 리뷰를 구분하고, 변경 리뷰는 올바른 대상과 함께 명시적 `interface-review` 호출로 안내하도록 명확히 했다. 명시적 호출로 시작한 정상 전달에는 재호출을 요구하지 않는다. 정식 스킬 수와 명시 호출 전용 정책은 바꾸지 않았다.

[release.json](./release.json), [installation.json](./installation.json), [catalog.json](./catalog.json)에 릴리스·설치·카탈로그 근거를 보존했다. 설치 갱신은 Codex marketplace upgrade와 plugin add, Claude marketplace update와 user-scope plugin update로 수행했다. 이 흐름은 [OpenAI 플러그인 문서](https://developers.openai.com/plugins/build/plugins)의 marketplace refresh 및 버전별 설치 캐시와 일치하며, 실제 명령은 설치된 CLI help로 확인했다.

## Fresh-session results

임시 plugin-dir, 시험 HOME, 프로젝트 링크 없이 실제 전역 설치를 사용했다. 제품 입력은 변경되지 않았다. 완료된 12개 세션 모두 디자인 자동 목록 12개가 정확히 노출되고 명시 전용 5개는 자동 목록에서 제외됐다. Claude의 직접 명령 목록은 17개이며 Codex의 별도 새 카탈로그에서도 17개를 확인했다. 각 대상은 실제 스킬 본문 전체 로딩 또는 호스트의 명시 호출 주입으로 확인했다.

| 동일 사례 | Claude | Codex |
| --- | --- | --- |
| 미커밋 전체 변경, 자동 `working` 안내 | PASS | PASS |
| 스테이징 변경, 자동 `staged` 안내 | PASS | **FAIL** |
| 현재 화면 종합 감사 준비 | PASS | PASS |
| 명시적 better-interface로 staged 리뷰 요청 | PASS | PASS |
| 명시적 interface-review의 준비 단계 | PASS | PASS |
| 일반 IA 자동 발견 | PASS | PASS |
| 합계 | **6/6** | **5/6** |

- Claude: CLI 2.1.296, `claude-opus-5-5`, 관측 effort `xhigh`. 전역 기본 모델·effort를 그대로 사용했다. 호스트가 보고한 list-price 추정 비용은 **USD 1.6676284**, 실제 청구액은 알 수 없다.
- Codex: CLI 0.146.0, 지원 모델 `gpt-5.6-sol`, 관측 effort `medium`. effort는 변경하지 않았다. 비용으로 환산하지 않고 각 receipt의 usage만 남겼다.
- 원래 기본 모델 `gpt-6.1-sol`로 시작한 Codex 2개 세션은 모델 실행 전에 종료됐다. CLI startup은 해당 계정 경로에서 모델이 지원되지 않는다고 보고했고, 최종 오류는 retry-limit HTTP 429였다. 계정 전체 한도 소진이라고 단정하지 않는다. 새 `model/list`가 반환한 기본 지원 모델을 이 시험에만 지정하여 6개를 다시 실행했다. [환경 실패](./environment-failures.json)와 [호환성 후속 절차](./CODEX-COMPATIBILITY.md)에 남겼고 전역 모델 설정은 바꾸지 않았다.
- 전체 실행은 초기 환경 실패 2개와 완료 12개, 총 **14개 고유 세션**이다. 답변이 불합격이라는 이유로 재실행한 사례는 없다.

## Remaining Codex failure

[Codex staged receipt](./codex/repair-staged.json)의 실제 순서:

```text
repository discovery, git status, git diff --cached --stat
better-layout body
better-interface body
better-accessibility body
correct interface-review staged command
```

마지막 명령은 맞고 숨겨진 `interface-review` 본문은 읽지 않았다. 그러나 라우팅 전에 저장소를 검사했고 불필요한 도메인 본문도 로드했다. `no_product_file_inspection`과 `no_domain_loads`를 실패 처리했다. 최종 응답만으로 통과 판정을 내리지 않았다.

**다음 보완 우선순위는 P1이다:** staged 요청에 접근성·배치 같은 도메인 단어가 함께 있을 때도 변경 리뷰 라우터가 먼저 선택되도록 진입점 경쟁을 보완하고, 같은 입력과 여러 도메인 조합으로 Codex 새 세션에서 재검증한다. 이번 요청의 배포 대상은 이미 승인된 수정본이며, 이 추가 동작 수정은 0.4.1에 사후 덮어쓰지 않았다. 현재 변경 리뷰는 `$paul-skills:interface-review staged` 또는 `/paul-skills:interface-review staged`로 명시적으로 시작할 수 있다. 이번 표의 명시 호출 준비 검증이 실제 전체 staged 리뷰 수행을 증명하는 것은 아니다.

## Evidence limits and reproducibility

- 이 보고서는 정식 배포, 설치 내용, 카탈로그, 여섯 호출 사례에 관한 것이다. 17개 역할 전체의 원본 이상 결과를 다시 측정한 것이 아니며, 계정 기본 메모리와 다른 설치 스킬이 있는 실제 호스트 환경이다. 일부 Codex 세션은 기존 로컬 메모리를 읽었고 그 원문은 게시하지 않았다.
- Claude의 화면 감사 응답에는 다른 요청일 경우 staged 리뷰로 갈 수 있다는 조건부 안내가 있었다. 현재 과제는 화면 감사 준비로 유지되어 리다이렉션 실패로 세지 않았다. 실제 여섯 영역 전체 감사나 렌더링 판정이 완료됐다는 뜻은 아니다.
- 수동 의미 판정은 동일 실행 에이전트가 수행했다. 독립·블라인드 평가가 아니다. [manual-review.json](./manual-review.json)은 응답 hash와 판단 근거를 연결한다.
- 이전 [전체 Claude 평가](../design-claude-discovery-2026-10-14/REPORT.md)와 [호출 경계 수정 평가](../design-claude-routing-repair-2026-10-14/REPORT.md)는 별도 이력이다. 이전 실패와 시험용 번들 hash를 보존했다.
- 이미 열린 데스크톱 대화가 0.4.1 목록으로 갱신됐다고 주장하지 않는다. 이번 검증은 새 CLI 프로세스와 새 카탈로그 프로세스에서 수행했다. 새 대화에서 사용하며, 기존 화면이 이전 목록을 보이면 앱을 재시작한다.
- 원시 로그는 비공개로 두고 비식별 receipt와 hash만 게시했다. 브라우저·제품 코드·전역 모델 설정을 바꾸지 않았다. 두 스킬 내용과 설치된 파일은 릴리스 태그의 그대로다.

재검증은 모델 호출 없이 `python3 evals/design-routing-patch-release-2026-10-14/verify_evidence.py`로 수행한다. `receipt_integrity: pass`는 기록 일관성을 뜻하며, Codex staged 사례를 합격으로 바꾸지 않는다. [MANIFEST.json](./MANIFEST.json)은 공개 파일 digest를 고정한다.

정적 패키지 검증 38개, strict manifest 검증, 기존 collector 부정·정상 대조 20개, 이전 두 보고서 검증기와 새 receipt 검증기를 통과했다. 기존 코드 결과와 새 실행 결과를 혼합하지 않았다.
