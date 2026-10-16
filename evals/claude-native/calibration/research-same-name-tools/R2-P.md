# skill-forge로 스킬 eval을 돌릴 수 있는가

- 조사일: 2026-10-16
- 범위: `sources/`의 H1~H3만 확인했다. 실행이나 네트워크 접속은 하지 않았다.

## 결론

이름이 같은 도구가 두 개라서 어느 쪽인지에 따라 답이 달라진다.

- Orbit Agents의 `skill-forge` 플러그인 2.x: 가능하다. `skill-forge eval`이 저장된 사례로 스킬을 실행하고 두 버전을 비교한다 [H1 `sources/H1-orbit-skill-forge.md` §Evaluate].
- Quill CLI의 내장 `skill-forge`: 불가능하다. 스킬 폴더 생성과 frontmatter 검증만 하고 평가나 벤치마크 명령이 없다 [H2 `sources/H2-quill-skill-forge.md` §What it does].

어느 호스트의 `skill-forge`를 말하는지 알려주면 그쪽 기준으로 정리할게.

## 근거

| 주장 | 자료 | 위치 |
| --- | --- | --- |
| Orbit 플러그인은 eval과 버전 비교 지원 | H1 (Orbit Agents) | §Evaluate |
| Quill 내장 스킬은 평가 명령 없음 | H2 (Quill CLI) | §What it does |

## 상충 자료

H3 포럼 글은 "skill-forge eval이 잘 된다"고 하지만 호스트와 버전을 밝히지 않는다. 어느 도구인지 알 수 없어서 근거로 쓰지 않았다.

## 한계

- 제공 자료 3개만 봤고 어떤 명령도 실행하지 않았다. 실제 eval 결과나 성능은 확인하지 않았다.

## 남은 질문

- 사용자가 쓰는 호스트가 Orbit Agents인지 Quill CLI인지.
