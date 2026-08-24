---
name: headver
description: "사용자가 HeadVer 적용을 명시적으로 요청했을 때 제품 버전과 관련 릴리스 흐름을 설계·구현·검토한다. 공개 라이브러리의 API 호환성 버저닝에는 기본 적용하지 않는다."
---

# HeadVer

제품 artifact에 `{head}.{yearweek}.{build}` 형식의 고유하고 추적 가능한 version을 적용한다. version은 표시용 문자열이 아니라 source revision과 실제 build 결과를 연결하는 artifact identity다.

## 적용 범위

- 앱, 웹 서비스, 백엔드처럼 최종 사용자에게 배포되는 제품 artifact에 사용한다.
- 공개 라이브러리처럼 소비자가 version으로 API 호환성을 판단하는 패키지는 기존 SemVer 또는 생태계 정책을 우선한다.
- 독립적으로 build·배포되는 프론트, 백엔드, 모바일 앱은 artifact별 HeadVer를 사용한다.
- tag·Release 생성, push, 스토어 업로드와 production 배포는 사용자가 명시적으로 요청한 범위에서만 수행한다.

## 먼저 결정할 값

repository의 version 주입 지점, 기존 tag·build number, 배포 환경과 artifact 승격 방식을 확인하고 구현 전에 다음 값을 정리한다.

```text
artifact:
head:
timezone:
build source:
build offset 또는 시작값:
version format:
tag format:
artifact identity:
promotion 방식:
```

## 버전 형식

```text
{head}.{yearweek}.{build}
```

예: `6.2634.143`

### Head

- 사람이 정하는 0 이상의 릴리스 회차 또는 릴리스 라인이다.
- candidate를 만들기 전에 확정하며 staging과 production 사이에서 바꾸지 않는다.
- production 성공 후 다음 Head로 변경한 commit은 다음 라인의 baseline candidate를 build·publish하고 staging에 배포한다.
- baseline candidate도 Build와 정확한 HeadVer tag를 갖는 일반 artifact다. production 배포와 Head 종료 tag 생성은 자동으로 수행하지 않는다.
- production 성공 후 Head 종료 tag를 만들면 해당 Head는 닫힌다. 이후 hotfix는 새 Head를 사용한다.

### YearWeek

- release timezone 기준 ISO week-year의 마지막 두 자리와 ISO week number 두 자리를 결합한다.
- 항상 네 자리이며 달력 연도가 아닌 ISO week-year를 사용한다.

```bash
TZ=Asia/Seoul date +%g%V
```

`%y%V`를 사용하지 않는다. 경계값은 `2018-12-31 -> 1901`, `2019-12-31 -> 2001`, `2016-01-01 -> 1553`이다.

### Build

- artifact namespace 안에서 고유하고 단조 증가하는 정수다.
- immutable artifact가 처음 게시되면 소비되며 누락된 번호를 허용한다.
- 기존 artifact를 승격할 때는 증가시키지 않는다.
- 같은 source라도 다시 build하면 새 Build와 새 artifact로 취급한다.
- 같은 workflow run을 재실행하더라도 기존 HeadVer artifact를 다시 build하거나 덮어쓰지 않는다. 안전한 resume을 증명할 수 없으면 새 run으로 새 Build를 발급한다.

## Artifact 불변조건

1. version은 artifact build 전에 한 번 확정한다.
2. version, source revision과 digest 또는 동등한 식별자를 함께 기록한다.
3. staging에서 검증한 바로 그 artifact를 production에 승격한다.
4. 승격 중에 다시 build하거나 version과 artifact를 덮어쓰지 않는다.
5. 같은 artifact에 서로 다른 두 HeadVer를 붙이지 않는다.
6. 환경 설정이나 flavor 때문에 binary가 달라지면 별도 artifact와 version으로 관리한다.

```text
6.2634.143 / digest A build
-> staging에 digest A 배포
-> production에 digest A 승격
```

production 직전에 Head를 변경해 새 artifact를 build하거나, 하나의 artifact에 이전·새 HeadVer를 함께 붙이는 흐름은 금지한다.

## Git tag와 릴리스 흐름

Git tag에 `v` prefix를 사용하는 프로젝트의 기본 흐름은 다음과 같다.

1. HeadVer 생성
2. artifact build·publish와 source revision·digest 기록
3. 정확한 HeadVer Git tag 생성: `v5.2634.143`
4. staging 배포와 검증
5. production에 같은 artifact 승격
6. production 성공 후 같은 commit에 Head 종료 tag `v5` 하나 생성
7. 정확한 tag에 GitHub Release와 배포 metadata 기록
8. 다음 Head의 baseline candidate 생성과 staging 배포

정확한 HeadVer tag는 candidate를 식별하는 immutable tag다. Head 종료 tag는 production 확정 지점을 Git history에서 찾기 위한 immutable 표식이며 배포 입력, latest pointer 또는 artifact identity로 사용하지 않는다.

두 tag는 같은 commit을 가리켜야 한다. 이미 같은 commit을 가리키는 tag는 idempotent success로 처리하고, 다른 commit을 가리키면 이동시키지 않고 실패한다. tag·Release 생성만 실패했다면 artifact를 다시 build하지 않고 누락된 metadata만 복구한다.

같은 artifact와 배포 대상의 release는 직렬화하고, 새 실행이 진행 중인 release를 취소하지 않게 한다.

## 구현과 검증

- `head`, Build와 offset은 0 이상의 정수로, `yearweek`는 정확히 네 자리로 검증한다.
- timezone, 기존 tag·Release와 외부 build 최대값을 확인하고 오류나 불확실한 외부 상태에서는 fail closed한다.
- Head 종료 tag가 이미 있으면 닫힌 Head의 재사용으로 보고 새 artifact 생성을 거부한다.
- 모든 release 진입점이 같은 HeadVer를 주입하고 version, source revision과 digest를 기록하는지 확인한다.
- production이 staging에서 검증한 artifact를 그대로 사용하는지 검증한다.

CI/CD 구현, rerun·부분 실패 복구 또는 플랫폼별 version 주입을 설계할 때만 [워크플로우 예시](references/workflow-examples.md)에서 해당 부분을 읽고 repository의 기존 명령과 배포 구조에 맞게 적용한다.

HeadVer 원본 명세: https://github.com/line/headver
