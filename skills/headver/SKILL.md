---
name: headver
description: "사용자가 HeadVer 적용을 명시적으로 요청했을 때 제품 버전과 관련 릴리스 흐름을 설계·구현·검토한다. 공개 라이브러리의 API 호환성 버저닝에는 기본 적용하지 않는다."
---

# HeadVer

최종 사용자에게 전달되는 제품 artifact에 `{head}.{yearweek}.{build}` 형식의 고유하고 추적 가능한 버전을 적용한다.

단순히 버전 문자열을 계산하는 데 그치지 않고, 버전이 artifact identity로 유지되도록 릴리스 정책·CI/CD 구현·기존 workflow를 함께 검토한다.

## 적용 경계

HeadVer는 앱, 웹 서비스, 내부 백엔드처럼 배포 artifact의 시점과 정확한 빌드를 식별해야 하는 제품에 사용한다.

공개 라이브러리나 외부 소비자가 버전으로 API 호환성을 판단하는 패키지에는 자동 적용하지 않는다. 이 경우 기존 SemVer 또는 해당 생태계의 버저닝 정책을 우선 확인한다.

프론트, 백엔드, 모바일 앱이 독립적으로 빌드·배포된다면 artifact별로 독립된 HeadVer를 사용한다. 하나의 버전을 공유하려면 같은 소스 revision에서 하나의 릴리스 단위로 생성·승격되는지 먼저 확인한다.

버전 정책 설계, repository 구현, 실제 외부 릴리스 실행을 구분한다. tag·Release 생성, push, 스토어 업로드, production 배포는 사용자가 명시적으로 요청한 범위에서만 수행한다.

## 먼저 확인할 것

변경 전에 repository의 실제 릴리스 구조를 확인한다.

- 독립적으로 배포되는 artifact와 대상 환경
- version을 읽거나 주입하는 모든 빌드 진입점
- staging과 production이 동일 artifact를 승격하는지, 환경별로 다시 빌드하는지
- 현재 Git tag, package manifest, 앱 스토어 build number, 이미지 tag 정책
- CI의 build counter 범위와 초기화 가능성
- release timezone과 기존 environment naming
- rerun, 동시 실행, 부분 실패 복구 정책

확정한 artifact별로 다음 값을 구현 전에 보여준다.

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

예:

```text
6.2634.143
```

### Head

- 사람이 결정하는 0 이상의 정수다.
- 사용자에게 전달할 릴리스 회차 또는 릴리스 라인을 나타낸다.
- 배포 환경이나 workflow 실행 횟수를 나타내지 않는다.
- CI가 기능 변경, commit message 또는 배포 성공만 보고 임의로 증가시키지 않는다.
- 기존 제품에 처음 적용할 때는 현재 제품 버전, 예정된 릴리스 라인과 사용자의 선택을 기준으로 초기값을 정한다.

다음 릴리스 후보를 만들기 전에 사용할 Head가 이미 확정되어 있어야 한다. staging에서 검증한 artifact를 production에 승격하는 순간 Head를 바꾸지 않는다.

production 성공 후 다음 Head를 설정 파일이나 PR로 준비할 수 있다. 이 Head-only 변경은 다음 릴리스 라인을 예약할 뿐이며, 기본적으로 artifact build·publish·staging deploy를 발생시키지 않아야 한다. Head만 바꾼 commit이 `main` build를 자동 실행한다면 다음 중 repository에 맞는 방식을 적용한다.

- version 설정만 변경된 실행은 artifact 생성 단계를 건너뛴다.
- artifact-producing workflow를 명시적 release-candidate trigger로 분리한다.
- path 또는 change guard로 Head-only 변경을 식별한다.

프로젝트가 기능 변경 없는 baseline artifact를 의도적으로 원한다면 예외로 허용할 수 있다. 이 경우 build number 소비, staging 배포와 artifact 보관 비용을 정책에 명시한다.

### YearWeek

- ISO week-year의 마지막 두 자리와 ISO week number 두 자리를 결합한다.
- 항상 네 자리 숫자여야 한다.
- 달력 연도가 아니라 ISO week-year를 사용한다.
- 릴리스 시간대를 명시하고 모든 생성 경로에서 동일하게 적용한다.

`Asia/Seoul`을 사용하는 shell 예시는 다음과 같다.

```bash
TZ=Asia/Seoul date +%g%V
```

`%y%V`를 사용하지 않는다. 연말·연초 경계에서 ISO 연도와 달력 연도가 달라질 수 있다.

최소한 다음 경계값을 검증한다.

```text
2018-12-31 -> 1901
2019-12-31 -> 2001
2016-01-01 -> 1553
```

### Build

- build server가 자동 발급하는 증가형 정수다.
- 같은 artifact namespace 안에서 고유하고 단조 증가해야 한다.
- 누락된 번호는 허용한다. immutable artifact가 최초 게시된 순간 해당 Build가 소비되며, production에 도달하지 않았더라도 다시 사용하지 않는다.
- artifact 게시 전에 실패하여 해당 HeadVer의 artifact가 존재하지 않는다면 같은 workflow run의 rerun은 같은 Build로 최초 게시를 완료할 수 있다.
- source build 없이 기존 artifact를 승격하는 배포에서는 증가시키지 않는다.
- 이미 게시된 artifact를 다시 빌드한다면 코드가 같더라도 새 Build와 새 artifact로 취급한다.

GitHub Actions의 `github.run_number`는 특정 workflow별 카운터이며 rerun에서는 바뀌지 않는다. 사용하기 전에 다음을 확인한다.

- workflow 교체·이름 변경·분리로 카운터 namespace가 달라지는지
- 여러 workflow가 같은 artifact를 발행하는지
- 외부 앱 스토어 또는 registry에 이미 더 큰 build가 있는지
- 일반 CI나 Head-only commit이 불필요하게 번호를 소비하는지

기존 build와 충돌할 수 있으면 검증된 offset 또는 중앙 counter를 사용한다. offset은 외부 시스템의 실제 최대값을 확인한 뒤 정하며, 오류를 감추기 위한 임의의 큰 값으로 선택하지 않는다.

workflow rerun은 동일한 `github.run_number`를 사용한다. artifact 상태에 따라 다음처럼 처리한다.

- artifact가 아직 게시되지 않았다면 같은 Build로 최초 게시를 완료할 수 있다.
- 기존 immutable artifact가 있다면 그 artifact를 이어서 게시하는 idempotent resume만 허용한다.
- artifact의 존재 여부나 identity를 확인할 수 없다면 실패시키고 새 workflow run으로 새 Build를 발급한다.

동일 HeadVer로 artifact를 다시 빌드하거나 덮어쓰지 않는다.

## Artifact 불변조건

HeadVer는 build 결과물의 불변 identity다. 다음 원칙을 지킨다.

1. version은 artifact를 만드는 workflow에서 build 전에 한 번 확정한다.
2. artifact에 version, source revision과 digest 또는 동등한 식별자를 기록한다.
3. staging에서 검증한 바로 그 artifact를 production에 승격한다.
4. 승격 과정에서 source build, version 재생성, artifact overwrite를 하지 않는다.
5. 같은 artifact에 서로 다른 두 HeadVer를 붙이지 않는다.
6. production 직전에 Head를 바꾸기 위해 재빌드하지 않는다.

예:

```text
Head 6 확정
-> 6.2634.143 / digest A 빌드
-> staging에 digest A 배포
-> 검증 성공
-> production에 digest A 그대로 승격
```

다음 흐름은 금지한다.

```text
5.2634.143 / digest A를 staging에서 검증
-> production 직전에 Head를 6으로 변경
-> 6.2634.144 / digest B를 새로 빌드해 배포
```

digest B는 검증되지 않은 별도 artifact다. digest A에 `5.2634.143`과 `6.2634.143`을 동시에 붙이는 것도 version과 artifact identity를 불일치시킨다.

컨테이너 이미지가 환경별 설정을 build 시점에 포함하거나 모바일 flavor가 서로 다른 바이너리를 만든다면 동일 artifact 승격으로 간주하지 않는다. artifact를 환경별로 분리하고 각각의 version과 검증 경로를 정의한다.

## 릴리스 수명주기

일반적인 build-once/promote-many 흐름은 다음과 같다.

1. 설정과 외부 build 최대값 검증
2. HeadVer 한 번 생성
3. artifact build·publish
4. version, commit SHA, digest 기록
5. staging에 동일 artifact 배포
6. 검증 후 production에 동일 artifact 승격
7. 정책에 따라 Git tag, GitHub Release와 배포 메타데이터 기록
8. 다음 Head 준비하되 Head-only 변경에서는 build 생략

실제 CI/CD를 설계하거나 예시를 제시할 때는 [워크플로우 예시](references/workflow-examples.md)에서 해당 artifact 유형만 읽고 repository의 기존 명령과 배포 구조에 맞게 적용한다.

tag·Release 생성 시점은 플랫폼의 복구 가능성을 고려해 정한다. production 성공 후 tag·Release가 실패해도 새 Build를 발급하거나 artifact를 다시 빌드하지 않는다. 이미 배포된 version, commit SHA와 digest를 확인해 누락된 tag·Release만 복구한다. 복구를 수동으로 할지 자동화할지는 프로젝트가 선택하며, 별도 복구 workflow를 반드시 두도록 강제하지 않는다.

같은 artifact와 배포 대상의 release는 직렬화하고 진행 중인 release를 새 실행이 취소하지 않게 한다. 실제 concurrency key는 artifact, 환경과 branch 구조에 맞춘다.

hotfix는 기존 Head를 유지하고 새 Build를 발급하거나 새 Head를 사용할 수 있다. 기존 Head를 유지한다면 대상 release branch·tag 또는 production release metadata에 기록된 Head를 사용하고, `main`에 예약된 다음 Head를 자동으로 읽지 않는다. 어느 쪽이든 hotfix artifact를 만들기 전에 선택하고, 이미 존재하는 artifact를 다른 version으로 다시 이름 붙이지 않는다.

## 설정과 검증

프로젝트 설정은 기존 관례가 없을 때만 별도 파일을 제안한다. 예:

```yaml
schema_version: 1
artifact: app

versioning:
  scheme: headver
  head: 6
  timezone: Asia/Seoul
  build:
    source: github-run-number
    offset: 100
```

설정은 fail-closed 방식으로 처리한다.

- `schema_version`과 `versioning.scheme`을 검증한다.
- `artifact`가 비어 있지 않은지 확인한다.
- `head`, offset과 build가 0 이상의 정수인지 엄격하게 확인한다.
- `10abc`, `abc`, 빈 문자열과 `null`을 숫자로 묵시 변환하지 않는다.
- timezone이 유효하지 않으면 실패한다.
- `yearweek`가 정확히 네 자리인지 확인한다.
- 최종 version이 숫자로 된 세 구간인지 확인한다.
- 기존 tag, Release, registry와 외부 스토어 build 중복을 게시 전에 확인한다.

오류가 있으면 추정값이나 기본값으로 배포를 계속하지 않는다.

## 플랫폼 매핑

### Flutter

```text
--build-name={HeadVer}
--build-number={build}
```

`pubspec.yaml`의 정적 version을 release source of truth로 사용할 필요는 없지만, 모든 로컬·CI release 명령이 같은 값을 명시적으로 주입하는지 확인한다.

### iOS

```text
CFBundleShortVersionString={HeadVer}
CFBundleVersion={build}
```

App Store Connect의 기존 최대 build보다 커야 한다. TestFlight에서 검증한 build를 App Store로 승격한다면 동일 archive/build를 사용한다.

### Android

```text
versionName={HeadVer}
versionCode={build}
```

일반 Gradle 또는 Flutter build 명령이 HeadVer 주입을 우회하지 않는지 확인한다. Google Play의 기존 `versionCode`보다 커야 한다.

### 웹과 백엔드

version을 container image tag 하나에만 남기지 말고 digest, source revision, 배포 메타데이터와 연결한다. 애플리케이션 build 정보와 관측 도구에서도 같은 artifact를 찾을 수 있어야 한다.

Sentry 등 관측 도구가 commit SHA 기반 release 이름을 이미 사용한다면 강제로 HeadVer로 바꾸지 않는다. HeadVer와 SHA를 metadata로 상호 연결한다.

## 구현 검토

구현 또는 리뷰 시 다음을 확인한다.

- ISO week-year와 release timezone이 정확한가
- Head-only 변경이 의미 없는 baseline artifact를 자동 생성하는가
- Head가 staging과 production 사이에서 바뀌지 않는가
- 동일 digest 또는 binary가 환경 간 승격되는가
- build counter가 artifact 전체에서 고유하고 외부 최대값보다 큰가
- workflow 교체나 rerun이 build identity를 충돌시키는가
- 모든 release 진입점이 HeadVer를 주입하는가
- 설정 오류가 fail-closed로 처리되는가
- 동시 release가 직렬화되는가
- tag, Release, artifact 또는 외부 배포 중 일부만 성공했을 때 복구 가능한가
- 배포 도구와 dependency가 lockfile 또는 동등한 방식으로 고정되는가
- 문서, 설정과 실제 workflow가 같은 정책을 설명하는가

구현 후에는 다음 결과를 구분해 보고한다.

- 로컬 version 생성 검증
- CI artifact build 검증
- staging 배포와 artifact identity 검증
- production 승격 검증
- Git tag와 Release 생성
- 실제로 확인하지 못한 외부 상태

CI 성공만으로 외부 스토어 업로드나 production 배포까지 성공했다고 표현하지 않는다.

## 참고

- HeadVer 공식 명세: https://github.com/line/headver
- GitHub Actions contexts: https://docs.github.com/en/actions/reference/workflows-and-actions/contexts
