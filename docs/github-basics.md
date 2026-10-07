# GitHub 용어: 영어와 한국어

| 이름 | 의미 | 이번 작업의 예 |
| --- | --- | --- |
| Account / 계정 | 저장소를 소유하는 사용자 계정 | 현재 `hackingan-finger6` |
| Username / 사용자 이름 | 주소와 로그인에 쓰이는 계정 ID | 현재 `hackingan-finger6` |
| Display name / 표시 이름 | 프로필 화면에 보이는 이름 | 사용자 ID와 별도로 설정 |
| Repository / 저장소 | 프로젝트 파일과 변경 이력을 담는 공간 | 준비 중인 `ai-skill-collection` / AI 스킬 모음집 |
| Folder·Directory / 폴더·디렉터리 | 저장소 안에서 파일을 분류하는 공간 | `docs/` / 설명 문서, `skills/` / 관리 스킬 |
| README / 첫 화면 안내 문서 | 저장소를 열면 먼저 읽는 소개 | `README.md` |
| Private / 비공개 | 권한 있는 사용자만 볼 수 있는 상태 | 개인 작업이나 내부 프로젝트 |
| Public / 공개 | 누구나 열람할 수 있는 상태 | 콘텐츠에 공개 링크로 안내할 때 선택 |
| Commit / 변경 기록 | 파일 변경 내용을 하나의 이력으로 저장 | 수정 사항을 기록하는 단위 |
| Push / 업로드 | 로컬 변경 기록을 GitHub로 보내는 작업 | 내 컴퓨터 → GitHub |
| Remote / 원격 연결 | 로컬 Git 저장소에 연결한 GitHub 주소 | 저장소 주소를 가리키는 연결 |

프로젝트별로 별도 저장소를 만들 수 있습니다. 이번 모음집은 다른 서비스 코드와 나눠 관리할 수 있도록 전용 저장소로 구성합니다.

```text
hackingan-finger6/
  my-app/             App project / 서비스 프로젝트 예시
  my-website/         Website project / 웹사이트 프로젝트 예시
  ai-skill-collection/  AI skill collection / AI 스킬 모음집
    README.md         README / 첫 화면 안내
    docs/             Documents / 기능 설명 문서
    skills/           Skills / 관리 도우미
```

컴퓨터의 폴더가 GitHub 저장소와 자동으로 같은 것은 아닙니다. 로컬 Git 저장소에 원격 주소를 연결하고 커밋을 올리면 GitHub에 반영됩니다. 공개(Public) 저장소는 누구나 볼 수 있고 비공개(Private) 저장소는 권한 있는 계정만 볼 수 있습니다.

## 사용자 이름 변경 / Change username

사용자 이름을 변경해도 같은 계정의 저장소를 계속 사용할 수 있습니다. 다만 저장소 주소의 계정 부분이 달라집니다. 예를 들어 `github.com/이전ID/저장소`에서 `github.com/새ID/저장소`로 변경됩니다.

기존 저장소 주소에는 자동 연결이 제공되지만 원격 주소와 외부 링크를 새 주소로 갱신하는 것이 좋습니다. 이전 프로필 주소는 자동 연결되지 않습니다. 기존 이름을 다른 사람이 쓰기 시작할 수 있어 이전 주소에 계속 의존하지 않는 편이 좋습니다.

프로필의 표시 이름만 변경하는 경우에는 주소에 쓰는 사용자 이름을 바꾸지 않습니다. 주소를 바꾸고 싶은지, 화면에 보이는 이름만 바꾸고 싶은지 구분하면 됩니다.

메뉴 경로: **Settings / 설정 → Account / 계정 → Change username / 사용자 이름 변경**.

[GitHub 공식 설명 / Username changes](https://docs.github.com/en/account-and-profile/concepts/username-changes)
