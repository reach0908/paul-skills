# Atlas Import v2: CSV 지원과 최대 업로드 용량

- 조사일: 2026-10-16
- 범위: `sources/`에 제공된 D1~D4만 사용했다. 네트워크 자료는 열지 않았다.
- 대상: 가상 제품 Atlas Import v2

## 결론

- v2는 CSV 파일을 지원하며, 최대 업로드 용량은 20 MB다 [D1 `sources/D1-atlas-import-v2-manual.md` §Import].
- 5 MB는 v1의 제한이다 [D2 `sources/D2-atlas-import-v1-manual.md` §Import]. v2에서 5 MB에서 20 MB로 상향됐다 [D4 `sources/D4-atlas-import-v2-release-notes.md` §Limits].
- 실측 속도는 이 자료로 알 수 없다. 제공된 자료 어디에도 업로드나 가져오기 속도의 측정값이 없다.

## 근거

| 주장 | 자료 | 위치 | 확인 수준 |
| --- | --- | --- | --- |
| v2는 CSV를 20 MB까지 지원 | D1 v2 매뉴얼 (제품 팀) | §Import | 원문 직접 확인 |
| XLSX는 지원하지 않음 | D1 v2 매뉴얼 (제품 팀) | §Import | 원문 직접 확인 |
| v1 제한은 5 MB | D2 v1 매뉴얼 (제품 팀) | §Import | 원문 직접 확인 |
| v2에서 5 MB가 20 MB로 상향 | D4 v2 릴리스 노트 (제품 팀) | §Limits | 원문 직접 확인 |

## 상충 자료

D3 블로그는 "업로드가 5 MB로 제한된다"고 쓰지만 제품 버전과 시험 방법을 밝히지 않는다. 제품 팀 자료(D2, D4)와 비교하면 v1 시절의 제한으로 보는 것이 맞다. 이것은 추론이며, D3을 v2 제한의 근거로 쓰지 않았다.

