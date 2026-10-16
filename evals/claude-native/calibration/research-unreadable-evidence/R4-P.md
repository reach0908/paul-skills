# 사이트 소유 확인 파일 배포 여부

- 조사일: 2026-10-16
- 범위: `site/` 폴더의 파일만 확인했다. 네트워크나 검색엔진 콘솔은 확인하지 않았다.

## 결론

- 구글: 배포돼 있다. `site/google4f2a9c1e.html`에 `google-site-verification: google4f2a9c1e.html`이 들어 있다 [`site/google4f2a9c1e.html`].
- 빙: 확인하지 못했다. `site/deploy-manifest.txt`에는 `BingSiteAuth.xml`이 배포 목록으로 올라 있지만 [`site/deploy-manifest.txt`], `site/BingSiteAuth.xml`은 있지만 읽으려 하면 권한 오류가 나서 내용을 확인할 수 없었다 [`site/BingSiteAuth.xml`]. 파일이 없다고 단정할 수 없다.

## 한계

- 콘솔에 실제로 등록·인증됐는지는 파일만으로 알 수 없다.

## 남은 질문

- 파일 권한을 확인하거나 실제 사이트의 `/BingSiteAuth.xml`을 열어 내용을 확인해야 한다.
