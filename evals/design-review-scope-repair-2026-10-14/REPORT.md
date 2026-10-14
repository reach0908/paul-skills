# Codex 호출 순서와 로컬 변경 범위 재검증

판정: **정식 배포 보류**. 새 세션 50개에서 Codex 23/25, Claude 25/25가 통과했다. `working` 기준 설명과 실제 HEAD/index 비교는 양쪽에서 통과했지만 Codex에 두 실패가 남았다. Codex 글꼴·색상 staged 사례에서 진입 문서와 두 분야 문서를 한 호출에 읽는 문제가 관찰되었다. 올바른 최종 명령만으로 이 실패를 상쇄하지 않는다.

## 변경

- `better-interface`의 짧은 진입 문서와 `audit-procedure.md`의 실행 절차를 분리했다. 실행 절차의 기존 규칙과 여섯 분야의 본문 규칙은 보존했다.
- `working`은 HEAD 대비 현재 추적 파일의 순변경과 untracked 파일, `staged`는 HEAD 대비 Git index snapshot으로 명시했다. 두 범위에 이전 브랜치 커밋은 들어가지 않는다.
- 준비 답변에도 같은 기준을 적용하고, 명시한 로컬 범위에는 기본 브랜치와 merge-base 탐색을 요구하지 않도록 했다. 빈 로컬 범위를 이전 커밋으로 넓히지 않는다.
- `staged`의 소비자 탐색과 내용 읽기도 index를 기준으로 지정했다.
- Codex는 자신의 읽기 전용 셸 도구를 사용한다. Claude의 Read/Glob/Grep 제약을 Codex에 주입하던 시험 조건을 제거했다. Claude는 해당 호스트의 네이티브 도구와 읽기 전용 Git 허용 목록을 유지한다.
- 문서, Changeset, 출처 기록의 local digest를 동기화했다. 원본 revision과 원본 검토 완료 지점은 바꾸지 않았다.

## 시험 경계

[PROTOCOL.md](PROTOCOL.md)와 [cases.json](cases.json)을 실행 전에 고정했다. 호스트별 25개 새 세션으로 이전 21개 사례, working 준비 답변 2회 추가, 서로 다른 index/working 상태의 실제 리뷰 2개를 실행했다. 각 호스트의 첫 6건은 초기 확인이며 뒤의 사례와 같은 소스를 사용한다.

Codex는 해당 CLI에서 지원되는 `gpt-5.6-sol`, medium으로 실행하며, Claude는 기본 `claude-opus-5-5`, xhigh를 사용한다. 다른 Codex 데스크톱 모델의 결과로 일반화하지 않는다. Codex의 개인 호스트 설정과 메모리 스냅샷은 기존 비교 조건을 유지하고, 인증 자료와 원시 호스트 문맥은 공개 보고서에 담지 않는다. Claude의 시작 문맥에 Git 상태가 포함될 수 있으므로, 모델이 먼저 조회했는지는 도구 기록으로 판정한다. Codex의 기존 메모리 조회는 허용하며, 진입 문서와 메모리 조회를 묶은 사례 자체는 실패로 계산하지 않는다. 저장소·분야 문서·실행 절차를 먼저 읽거나 함께 읽는지를 판정한다.

이 시험은 호출과 범위 판정의 회귀 검증이다. 준비 답변은 17개 역할의 전체 품질이나 원본 대비 우월성 증거가 아니다. 작성 에이전트가 응답과 도구 기록을 검토했으며 독립적인 블라인드 판정이 아니다. 이미 실패를 보고 수리한 개발 사례이므로 독립 표본 신뢰도 추정에도 쓰지 않는다.

## 실제 Git 상태

| 상태 | Panel의 접근 가능한 이름 | 추가 파일 |
| --- | --- | --- |
| 기본 브랜치 main | 없음 | 없음 |
| 현재 HEAD | 있음 | 없음 |
| Git index | 없음 | 없음 |
| divergent 작업 트리 | 복구됨 | 이름 없는 버튼이 있는 untracked `src/New.html` |

같은 파일이라도 staged 리뷰는 Panel의 `Regression`, working 리뷰는 New의 `Introduced`만 변경 원인으로 다뤄야 한다. main을 기준으로 삼거나 작업 파일을 index 대신 읽으면 이 결론을 얻을 수 없다. 생성 시 Git 상태를 확인하는 assertion과 실제 조회 명령, 최종 보고서의 SHA·범위를 함께 검증한다.

## 확인된 결과

| 검사군 | Codex | Claude |
| --- | --- | --- |
| 자동·명시 진입 경계 | 10/11 | 11/11 |
| 여섯 분야·현재 화면·IA 정상 호출 | 7/8 (호출 자체는 8/8, 색상 읽기 오류 1건) | 8/8 |
| 명시 `working` 준비 설명 반복 | 3/3 | 3/3 |
| 실제 HEAD/index/working 분리 리뷰 | 3/3 | 3/3 |

Claude는 25/25가 통과해 이번 범위에서 정상 호출과 명시 호출의 회귀가 관찰되지 않았다. 자동 디자인 목록 12개와 명시 호출 목록 17개도 유지됐다. Codex의 25개 새 세션은 23개 통과다. 원래 staged 문장 3회는 모두 통과했고, 글꼴·색상 변형은 3회 중 2회 통과했다. `working` 준비 설명 3회와 실제 변경 범위 리뷰 3건은 모두 정확했다.

- [글꼴·색상 staged 실패](codex/staged-type-color.json): 첫 호출에 진입, 타이포그래피, 색상 SKILL.md를 함께 읽었다. 최종 `interface-review staged` 명령은 맞았고 제품 저장소를 읽지는 않았지만, 분야 문서를 미리 읽지 않는 기준을 위반했다.
- [색상 정상 호출의 실행 오류](codex/normal-better-colors.json): 필요한 스킬은 정확히 로드했으나 다섯 참조 읽기에서 셸 인자 전달 오류가 발생했다. 올바른 개별 읽기로 복구하고 준비 답변을 완성했지만 무오류 실행 기준에는 실패다. 이 명령은 시험 스크립트가 제공한 명령이 아니라 모델이 구성한 것이다. 스킬 변경이 이 오류의 원인이라는 인과 주장은 하지 않는다.
- [실제 working 리뷰](codex/authorized-handoff.json), [index 비교](codex/staged-divergent.json), [상쇄된 tracked 변경과 untracked 구분](codex/working-divergent.json)은 HEAD/index 기준과 최종 분류가 모두 맞았다. 기본 브랜치 조회 없이 6개 분야와 실행 절차를 로드해 보고서를 완료했다.

증거 수집기는 [GRADER-NOTES.md](GRADER-NOTES.md)의 실제 로그 형식 보정을 적용했다. 원본 호출 ID·경로·전문 일치를 확인하고, 검색 결과 없음과 읽기 실패를 구분한다. 후보 소스나 응답을 바꾸거나 실패 사례를 재추출하지 않았다.

정적 검증은 `npm run check` 38개, 호출/증거 판정기 제어 시험 19개, `claude plugin validate . --strict`, `git diff --check`가 통과했다. 56개 출처 레코드, 44개 정식 스킬, 17개 디자인 스킬과 기존 호출 정책을 유지한다. 후보 패키지는 175개 파일이며, 현재 전역 0.4.1의 174개 파일은 두 호스트 모두 그대로다.

## 남은 제한과 배포 판단

Codex의 특정 분야 이름이 포함된 요청에서 도메인 문서를 미리 읽는 문제는 자동 선택 단계에서 발생한다. 진입 본문을 짧게 분리하는 수정만으로 해결되었다고 주장할 수 없다. 통과한 답변만 선택하거나 도메인 선행 읽기를 허용하도록 합격선을 낮추지 않는다.

우선순위는 다음과 같다.

1. **P0: Codex 자동 진입 순서.** 분야 설명의 선택 조건과 진입 단계의 실제 분리를 재검토해야 한다. 동일한 실패 문장의 반복뿐 아니라 접근성·배치, 글꼴·색상, 문구·모션 변형 모두에서 분야 선행 로드를 차단해야 한다. 이번 구조 변경만으로 해결됐다고 볼 수 없다.
2. **P1: Codex 참조 읽기 안정성.** 정상 도메인 진입은 성공했으므로 스킬 미발견 문제와 분리한다. 중첩 셸과 위치 인자 없이 해당 호스트의 직접 파일 읽기로 참조를 완독하는지 검증해야 한다. 복구된 명령 오류를 숨기지 않는다.
3. **유지 조건:** 수정이 끝난 동일 소스로 Claude의 정상 호출, 명시 호출, 실제 HEAD/index 비교를 함께 통과해야 한다. 이번 결과만으로 전체 17개 역할의 원본 이상 품질을 새로 선언하지 않는다.

현재 전역 설치와 버전은 0.4.1로 유지한다. 이 작업은 후보 수정과 재검증이며 PR, 병합, 태그, 공개 릴리스 또는 일상용 설치 갱신을 수행하지 않는다.

이전 92개 세션과 실패는 [앞선 보고서](../design-staged-routing-repair-2026-10-14/REPORT.md)에 보존되어 있다. 후보 3 소스를 별도 스냅샷으로 고정해 현재 파일이 바뀌어도 과거 증거 검증이 유지된다.

## 증거와 비용

- [RESULTS.json](RESULTS.json): 50개 고유 세션, 호스트별 합격 수와 배포 보류 판정
- [Codex 요약](codex/summary.json), [Claude 요약](claude/summary.json): 실패 조건과 실행 호스트
- [manual-review.json](manual-review.json): 최종 응답 해시에 묶인 의미 검토 기록
- [fixture-facts.json](fixture-facts.json): 실제 main/HEAD/index/working 상태
- [candidate-manifest.json](candidate-manifest.json), `candidate-sources/`: 175개 후보 파일의 고정 해시와 변경 파일 스냅샷
- [validation.json](validation.json): 패키지·판정기·호스트 검증 결과
- [MANIFEST.json](MANIFEST.json): 공개 증거 파일 무결성 목록

Claude의 호스트 보고 정가 추정 합계는 USD 12.2893662다. 실제 청구액은 알 수 없고, Codex의 달러 비용도 제공되지 않아 null로 남겼다. 이번 50개 실행은 모두 종료되었고 답변 재시도나 실패 삭제는 없었다.

재검증 명령: `python3 evals/design-review-scope-repair-2026-10-14/verify_evidence.py --live-source --live-install`. 기록만 검증할 때 두 옵션을 빼면 후보 스냅샷을 사용한다. 원시 세션은 공개 산출물에 포함하지 않으며 공개 영수증에는 원시 로그 해시만 남긴다.

모델 세션 자체를 재실행하려면 private 호스트 스냅샷과 해당 호스트 인증이 필요하다. 공개 무결성 검증은 이 자료 없이 저장소의 0.4.1 태그와 보존된 후보 스냅샷으로 수행할 수 있다.

## Follow-up

The [domain discovery and reference-reading repair](../design-domain-entry-repair-v4-2026-10-14/REPORT.md) records new frozen candidates and fresh host sessions. This report keeps its original 23/25 Codex and 25/25 Claude outcomes; the later result does not rewrite these failures.
