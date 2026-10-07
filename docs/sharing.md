# Share skills / 스킬 공유 방법

## 1. Public repository / 공개 저장소

GitHub 저장소를 공개(Public)로 두고 첫 화면 안내(README), 스킬 폴더, 설치 방법, 사용 예시, 출처와 사용 허가(License)를 함께 제공합니다. 콘텐츠에서는 저장소 링크 하나로 안내할 수 있습니다.

이 모음집에서 실제 설치 가능한 스킬은 관리 도우미 두 개입니다. 125개 기능 문서는 안내 목록이며, 기능 구현은 원출처에서 선택 설치합니다.

## 2. Skill folder / 개별 스킬 폴더

각 도우미는 `skills/스킬이름/SKILL.md` 구조입니다. 필요한 실행 코드(Scripts), 참고 문서(References), 표시 정보(agents/openai.yaml)를 같은 폴더에 넣어 따로 받아도 사용할 수 있게 구성합니다.

Codex에 설치를 부탁하거나 README의 선택 설치 명령을 사용할 수 있습니다. 전체 기능을 자동 설치하는 명령을 기본 안내로 제공하지 않습니다.

## 3. Plugin package / 설치 묶음

여러 스킬을 한 번에 배포할 때는 `plugin.json`과 `skills/`를 묶은 플러그인 형태를 사용할 수 있습니다. 이 저장소에는 버전 `0.1.0`의 portable plugin / 공통 형식 플러그인 정보를 작성했습니다.

GitHub 공개 저장소에 올리는 것과 공식 플러그인 디렉터리에 등록하는 것은 다릅니다. 공식 디렉터리 등록에는 별도 제출·심사 절차가 있습니다. 현재는 GitHub를 통한 공유와 스킬 폴더 설치 방법을 제공합니다. 실제 플러그인 UI 설치는 시험하지 않았습니다.

## 참고한 공식 안내 / Official references

- [OpenAI — Build skills / 스킬 구조와 설치](https://learn.chatgpt.com/docs/build-skills)
- [OpenAI — Package your plugin / 플러그인 배포 묶음](https://developers.openai.com/plugins/build/plugins)
- [Vercel — skills CLI / GitHub에서 스킬 선택 설치](https://github.com/vercel-labs/skills)
- [GitHub — About repositories / 공개·비공개 저장소](https://docs.github.com/en/repositories/creating-and-managing-repositories/about-repositories)
