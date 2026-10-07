# 시작 도구 사용

Python 3.10+ 표준 라이브러리만 필요하다. `launcher.py`의 절대 경로로 실행한다.

## 요구사항 점검

선택한 스킬의 실제 문서에서 확인한 조건만 JSON으로 작성한다.

```json
{
  "skill": "example-search",
  "commands": ["python", "uv"],
  "environment": ["EXAMPLE_API_KEY"],
  "systems": ["Windows", "Linux"],
  "machines": [],
  "evidence": "확인한 문서 URL 또는 로컬 파일과 버전"
}
```

```text
python launcher.py probe --requirements 요구사항.json
```

`commands`는 PATH에서 찾는 실행 파일 이름이며 인수나 경로를 넣지 않는다. 실행하지 않으므로 버전·패키지 호환성은 별도로 확인해야 한다. `systems`는 `platform.system()` 값, `machines`는 `platform.machine()` 값이다. 빈 배열은 제한 조건을 확인하지 않았다는 뜻이다. 환경변수는 현재 Python 프로세스의 비어 있지 않은 값의 존재만 확인한다. `.env`나 vault를 읽지 않는다.

결과의 `local_check`는 `blocked`, `platform_mismatch`, `conditions_present` 중 하나다. `conditions_present`는 명시한 조건이 현재 보인다는 뜻이며 기능 성공을 보장하지 않는다. 명시하지 않은 요구사항은 검사하지 않는다.

## 로컬 묶음 검토와 설치

```text
python launcher.py review --source 검토할스킬폴더
python launcher.py add --source 검토할스킬폴더 --root 설치루트 --name example-search --reviewed-digest 검토결과digest
```

`review`가 반환하는 파일 목록을 확인하여 스크립트·인증 처리·외부 호출·재배포 조건을 검토한다. frontmatter 이름과 설치 이름이 다르면 문서와 호출 방식에 영향을 주는지 확인한다. `add`는 확인된 로컬 파일을 추가하는 기능이다. GitHub 다운로드와 의존 프로그램 설치는 포함하지 않는다. 공급자별 설치 방식이 필요한 경우 해당 도구를 직접 사용하되 대상 범위를 유지한다.

루트는 이미 존재하는 실제 디렉터리여야 한다. 이름은 소문자 영문·숫자·하이픈으로 1~64자다. 원본은 `SKILL.md`를 포함해야 한다. `.git`, 링크, junction, 특수 파일이 있으면 거부한다. 같은 루트에 기존 이름이 있으면 중단한다. 다른 프로그램이 원본이나 설치 루트를 변경하는 동안 실행하지 않는다.

설치 전후 해시가 다르거나 중간에 오류가 발생하면 출력의 `staging` 경로를 확인한다. 남겨진 임시 폴더는 실패 증거이며 설치 완료 폴더가 아니다. 자동으로 재시도하거나 임시 폴더를 정식 이름으로 변경하지 않는다.
