# Korean AI Skill Collection / 한국어 AI 스킬 컬렉션

한국 생활·업무에 활용할 기능을 목적별로 찾아보고, 필요한 스킬의 설치와 보관을 관리하는 모음집입니다.

**처음이라면:** 아래 분류에서 필요한 기능을 누르세요. 각 설명 페이지에서 할 수 있는 일, 준비사항, 원문을 확인할 수 있습니다. 목록을 읽는 것만으로 스킬이 설치되지는 않습니다.

이 저장소는 **기능 목록·한국어 해설·분류·원문 연결**과 별도로 작성한 **관리 도우미 두 개**를 제공합니다. 기능 125개를 모두 직접 개발했다는 의미는 아닙니다. 초기 목록은 공개 K-스킬 조사 자료를 바탕으로 구성했고, 개별 제작자와 실행 출처는 각 항목에서 확인할 수 있습니다.

## Browse by purpose / 목적별 찾기

| 분류 | 기능 수 |
| --- | ---: |
| [이동·여행](docs/categories/travel.md) | 18 |
| [주거·부동산](docs/categories/housing.md) | 8 |
| [리서치·공공정보](docs/categories/research.md) | 13 |
| [사업·창업·업무](docs/categories/business.md) | 21 |
| [금융·투자·통계](docs/categories/finance.md) | 7 |
| [생활·쇼핑·건강](docs/categories/daily.md) | 28 |
| [교육·문화·스포츠](docs/categories/culture.md) | 15 |
| [글쓰기·콘텐츠](docs/categories/writing.md) | 5 |
| [날씨·환경](docs/categories/environment.md) | 4 |
| [개발·문서·자동화](docs/categories/development.md) | 4 |
| [운세·작명](docs/categories/interpretation.md) | 2 |

총 125개 기능 후보와 관리 도우미 2개입니다. 기능 스킬은 설치하지 않은 상태이며, 문서 조사와 실행 검증을 구분합니다.

## Management skills / 관리 도우미

- [스킬 시작 도우미](skills/agent-skill-launcher/SKILL.md): 목록에서 기능 선택, 요구사항 점검, 검토한 스킬 추가.
- [스킬 보관·복원 도우미](skills/agent-skill-vault/SKILL.md): 보존·의존성 확인 후 보관, 티켓으로 상태 확인과 복원.
- [기계 읽기 목록](skills/agent-skill-launcher/references/collection-index.json): 125개 ID·분류·원문·설치 출처.

도우미 설치와 기능 125개 설치는 별개입니다. 목록을 읽었다고 자동으로 전체를 설치하지 않습니다. 도우미는 Python 3.10 이상 표준 라이브러리를 사용하며, 실제 실행 기능에는 개별 도구·플랫폼·인증이 필요할 수 있습니다.

## Install / 설치 방법

이 저장소의 `skills/agent-skill-launcher`, `skills/agent-skill-vault`를 Codex의 skill-installer로 선택 설치할 수 있습니다. 도우미를 설치한 뒤 원하는 기능을 말하면 원문 확인과 설치 범위를 먼저 정합니다.

가장 쉬운 방법은 Codex에 아래 문장을 보내는 것입니다.

```text
https://github.com/hackingan-finger6/ai-skill-collection 에서
skills/agent-skill-launcher 와 skills/agent-skill-vault 두 도우미만 설치해줘.
기능 스킬 125개는 아직 설치하지 마.
```

명령어를 사용하는 경우에는 관리 도우미 두 개만 선택해 설치합니다. Node.js와 npx가 필요합니다.

```bash
npx skills add hackingan-finger6/ai-skill-collection --skill agent-skill-launcher --skill agent-skill-vault --agent codex -g --copy
```

받아 보기만 하려면 **Code / 코드 → Download ZIP / 압축 파일 받기**를 선택하세요. ZIP 다운로드는 Codex 설치와 별개입니다.

## Use / 사용 예시

```text
스킬 시작 도우미로 한국어 글을 자연스럽게 다듬는 기능을 찾아줘.
아직 설치하지 말고 후보와 실행 조건만 보여줘.
```

기능 스킬을 설치할 때 해당 공급자의 코드와 라이선스 고지를 함께 보존합니다. 초기 목록에는 원 공급자의 CLI·프록시가 필요한 기능이 있습니다.

## Docs / 문서와 확인 범위

- [GitHub 구조 설명](docs/github-basics.md)
- [출처와 참고 프로젝트](SOURCES.md)
- [구성요소와 라이선스 표시](LICENSING.md)
- [검증 범위](docs/verification.md)
- [공유 방식 안내](docs/sharing.md)

## License / 사용 허가

이 저장소에서 작성한 문서와 관리 도우미는 [MIT License / MIT 사용 허가](LICENSE)로 공유합니다. 소개한 외부 기능의 권리와 라이선스는 각 원출처를 따릅니다.

`plugin.json`에는 도우미 두 개를 함께 배포할 수 있는 플러그인 묶음 정보를 넣었습니다. 공식 ChatGPT·Codex 공개 플러그인 디렉터리에 등록된 상태는 아닙니다.

작성·정리 기준일: 2026-10-07. API 응답, 사이트 동작, 계정 권한은 사용할 때 다시 확인합니다.
