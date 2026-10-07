# 보관함 작업 안내

`vault.py`는 Python 3.10+ 표준 라이브러리로 실행한다. 영구 삭제 옵션은 없다. 실제 helper의 절대 경로를 사용한다.

## 1. 목록과 의존성 조사

```text
python vault.py catalog --root 설치루트
```

목록을 파일에 저장할 때 기존 파일을 덮어쓰지 않는다. `revision`은 현재 보이는 스킬들의 이름·내용·보호 상태를 묶은 해시다. 각 항목의 `digest`는 파일 경로·크기·내용 해시와 빈 폴더를 포함한다. `.system` 등 숨김 관리 영역은 `protected`로 기록한다. 자동 내용 수집 대상은 `SKILL.md`가 있는 일반 스킬 폴더다.

참조를 조사한 후 다음 구조로 별도 JSON을 작성한다.

```json
{
  "root": "설치루트의 절대 경로",
  "revision": "catalog의 revision",
  "scope": "조사한 설치 영역, 프로젝트 설정과 문서 경로; 조사하지 못한 부분",
  "references": {
    "example-search": [],
    "example-report": ["example-search"]
  },
  "retain": ["example-report"]
}
```

`references`에는 catalog의 모든 항목을 넣는다. 키는 참조하는 스킬의 폴더명, 값은 의존하는 폴더명 배열이다. 숨김·보호 영역의 참조도 조사표에 포함한다. 스킬 밖의 프로젝트가 요구하는 항목은 `retain`에 넣는다. 배열이 비어 있다는 사실은 조사 후 의존성이 없다고 기록한 것이어야 한다. helper는 조사표와 목록의 일치 및 명시된 의존 관계를 검사하며 조사 자체의 완전성을 보장하지 않는다.

## 2. 보관

```text
python vault.py park --root 설치루트 --name example-search --expected 내용digest --audit 조사표.json --vault 외부보관함
```

다른 남은 항목이 참조하거나 `retain`에 있는 대상은 거부한다. 여러 의존 항목을 함께 정리하려면 호출하는 쪽부터 하나씩 보관하고 매번 남은 목록의 조사표를 갱신한다. 시스템·관리 스킬과 링크/junction/Git/특수 파일을 포함한 항목도 거부한다.

보관함은 기존 디렉터리여야 하며 설치 루트와 서로 포함 관계가 없어야 한다. helper는 이번에 지정한 루트와만 경로를 비교하므로 다른 에이전트의 검색 범위 밖인지도 에이전트가 확인한다.

한 티켓에는 `receipt.json`과 이동한 `payload` 폴더가 있다. 인수증은 이동 전에 생성하고 상태를 계속 수정하지 않는다. 둘 중 어떤 위치에 폴더가 있는지로 상태를 판별한다. `park`가 실패하면 오류에 표시된 티켓을 확인한다. 자동 재시도하지 않는다.

## 3. 상태 확인과 복원

```text
python vault.py status --root 원래설치루트 --vault 외부보관함 --ticket 티켓ID
python vault.py restore --root 원래설치루트 --vault 외부보관함 --ticket 티켓ID
```

`state`는 `parked`(보관 위치만 존재), `at_origin`(원래 위치만 존재), `conflict`(둘 다 존재), `missing`(둘 다 없음), `changed`(내용 변경) 중 하나다. `at_origin`은 이동 전 중단과 복원 완료를 구별하지 않으므로 실제 실행 결과와 함께 해석한다. 보관 위치의 내용이 변했거나 원래 위치에 무언가 있으면 복원하지 않는다. 원래 위치에 같은 내용만 있고 보관 위치가 비어 있으면 재복원 요청은 `already_at_origin`으로 끝난다.

중단된 티켓은 폴더를 삭제해 해결하지 않는다. 실제 내용과 경로를 먼저 확인한다. helper는 적대적인 다른 프로세스와의 경로 변경 경쟁을 막는 잠금 장치가 아니며 대상 폴더를 다른 프로그램이 수정하지 않는 조건에서 사용한다.
