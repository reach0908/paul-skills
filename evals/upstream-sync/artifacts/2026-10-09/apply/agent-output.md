# 상류 검토 증거 개선 적용

- 검사 시각: 2026-10-09T06:02:30.616303+00:00
- 소스: `fixture`, `<fixture-root>/source`
- 비교 기준: `1fb5fee3e8685b51fe54fee7b8e96f33c7ce862c`
- 적용 대상: `aed5a773ac4ddd43fefd8526f713b520a4c3a6d2`
- 최종 로컬 digest: `sha256:82678f9b397f3817d724b55e57399ecb319dcdbd23be30f584d47a14c040c3fc`
- 범위: 격리 fixture 내부 파일 수정과 메타데이터 갱신. 커밋 및 게시 없음.
- 원격 조회와 fetch 없음. 제공된 고정 checkout의 스냅샷만 확인했으며 최신 원격 상태로 주장하지 않음.

## 결정과 적용

| 파일 | 결정 | 실제 변경 |
| --- | --- | --- |
| `skills/review/references/rules.md` | adopt | 각 지적에 테스트 명령과 관찰 결과를 보고하는 상류 문장을 그대로 추가 |
| `skills/review/SKILL.md` | adapt | 진입 문서에서 검토 규칙을 읽도록 상대 링크 추가 |
| `skills/review/SKILL.md` | keep-local | 한국어 출력과 사람의 게시 결정 문장을 그대로 보존 |

상류의 전체 변경 목록과 rename 정보를 검토했다. 변경은 `references/rules.md` 하나이며, 새 스킬, 삭제, 이름 변경, 다른 직접 소스 또는 미결정 항목은 없다. fixture에는 별도 문서, 라우터, 설치 manifest, 기존 검사 명령이 없다. 저장소 변경 기록은 `CHANGELOG.md`에 작성했다.

## 검증 증거

적용 직전 대상 HEAD가 위의 전체 commit ID와 같고 로컬 digest가 기존 registry와 동일한지 재확인했다. 적용 후 상류 규칙과 로컬 규칙이 완전히 일치하고, 두 로컬 정책 문장이 유지되며, 참조 링크가 유효하고, 진입 문서의 다른 부분이 바뀌지 않았음을 Python assertion으로 확인했다. 이 검사는 종료 코드 0이었다.

실제 동작 사례는 `verification/price.diff`의 합계 계산 회귀를 검토했다. 아래는 수정한 지침을 읽고 작성한 한국어 검토 결과다.

### 사례 검토 결과

**[P1] 수량을 곱하도록 합계 계산을 복구하세요.** `verification/price.py:2`에서 단가에 수량을 더하므로 단가 10, 수량 3의 합계가 30 대신 13이 됩니다. `return price * quantity`로 복구해야 합니다.

- 실행 명령: `PYTHONDONTWRITEBYTECODE=1 python3 verification/reproduce.py`
- 관찰 결과: `line_total(10, 3): expected=30, observed=13`, 이어서 `AssertionError: expected 30, observed 13`.
- 종료 코드: 1. 의도적으로 결함을 넣은 사례를 재현한 결과이며, 적용한 스킬 파일의 실패를 뜻하지 않습니다.
- 게시 여부: 사람의 결정을 기다리는 로컬 검토 결과입니다. 게시하지 않았습니다.

## 메타데이터와 제한

이 소스의 스킬 변경을 모두 결정하고 위 검증을 완료한 뒤 `reviewedRevision`과 최종 `localDigest`를 갱신했다. 기존 keep-local 결정과 불변 `importedRevision` 및 origin 경로를 보존했다. 저장소 전체 유지보수 검토를 별도로 완료했다고 주장하지 않으므로 `repositoryReview`는 기존 기준을 유지했다.

보류 항목은 없다. 다만 fixture에는 package 또는 CI 설정이 없어서 `npm run check`와 CI는 실행하지 않았다. 설치 검증과 모델 간 비교 시험도 하지 않았다. 단일 합성 사례는 명령과 관찰 결과를 포함하는 출력의 실행 예시이며 스킬 품질 향상이나 모델 우위를 입증하지 않는다. registry의 MIT 표기는 그대로 보존했으며 source에 라이선스 파일이 없어 독립적으로 확인하지 못했다. 원격 게시나 배포 권한으로 해석하지 않았다.
