---
name: headver
description: "사용자가 HeadVer 적용을 명시적으로 요청했을 때 제품 버전과 관련 릴리스 흐름을 설계·구현·검토한다. 공개 라이브러리의 API 호환성 버저닝에는 기본 적용하지 않는다."
---

# HeadVer

## HeadVer란

HeadVer는 제품의 정확한 릴리스와 build를 찾기 위한 version 형식이다.

```text
{head}.{yearweek}.{build}
```

예를 들어 `6.2634.143`은 다음을 뜻한다.

- `6`: 사람이 정한 여섯 번째 릴리스 회차 또는 릴리스 라인
- `2634`: release timezone 기준 2026년 ISO 34주차
- `143`: build server가 발급한 Build 143

Head는 SemVer의 호환성 major가 아니다. YearWeek와 Build가 릴리스 시점과 정확한 artifact를 구분하므로, Head는 사람이 이해하기 쉬운 제품 릴리스 회차로만 사용한다.

HeadVer는 표시용 문자열이 아니라 artifact identity다. version을 source revision, image digest 또는 binary checksum과 함께 기록해야 `6.2634.143`이 어떤 build인지 다시 찾을 수 있다.

### 구성 요소 규칙

- **Head**: candidate를 만들기 전에 정하고 staging과 production 사이에서 바꾸지 않는다.
- **YearWeek**: ISO week-year의 마지막 두 자리와 ISO week number 두 자리다. 달력 연도가 아닌 ISO week-year를 사용한다.
- **Build**: artifact namespace 안에서 고유하고 단조 증가한다. 누락된 번호는 허용하며 artifact가 처음 게시되면 소비된다.
- 기존 artifact를 승격할 때는 Build를 증가시키지 않는다. 같은 source를 다시 build하면 새 Build와 새 artifact다.

## 실용적인 릴리스 방법

현재 production이 `5.2633.140`이라고 가정한다.

```text
v5.2633.140 production 성공
-> 같은 commit에 Head 종료 tag v5 생성
-> 설정의 Head를 6으로 변경
-> 6.2634.141 baseline artifact build·publish
-> 정확한 Git tag v6.2634.141 생성
-> staging 배포
```

Head만 변경한 baseline은 이전 production과 기능이 같아도 다음 릴리스 라인의 정상적인 첫 candidate다. Build를 소비하고 다른 candidate와 같은 방식으로 staging에서 검증한다. 다만 production 배포와 `v6` 종료 tag 생성은 자동으로 수행하지 않는다.

Head 6에서 변경사항이 쌓이면 새 Build를 계속 staging에 배포한다.

기본 workflow는 `main`에 반영된 commit마다 candidate artifact를 자동으로 build·publish하고 staging에 배포한다. production만 검증을 마친 exact tag를 선택해 별도로 실행한다.

```text
6.2634.142 build·publish -> v6.2634.142 -> staging
6.2635.147 build·publish -> v6.2635.147 -> staging
```

production에 올릴 때는 검증을 마친 정확한 tag를 선택한다.

```text
v6.2635.147 선택
-> 기록된 digest A를 production에 승격
-> source를 다시 build하지 않음
-> production 성공
-> 같은 commit에 Head 종료 tag v6 생성
-> GitHub Release는 정확한 tag v6.2635.147에 연결
-> Head를 7로 변경해 baseline candidate build·staging
```

`v6`는 Head 6의 production 확정 지점을 Git history에서 찾기 위한 immutable 표식이다. 배포 입력, latest pointer 또는 artifact identity로 사용하지 않는다. `v6`가 생성되면 Head 6은 닫히며 이후 hotfix도 새 Head를 사용한다.

## 반드시 지킬 것

1. version은 build 전에 한 번 확정한다.
2. version, source revision과 digest 또는 checksum을 함께 기록한다.
3. staging에서 검증한 바로 그 artifact를 production에 승격한다.
4. 승격하면서 다시 build하거나 version과 artifact를 덮어쓰지 않는다.
5. 같은 artifact에 서로 다른 두 HeadVer를 붙이지 않는다.
6. 환경 설정이나 flavor 때문에 binary가 달라지면 별도 artifact와 version으로 관리한다.
7. 같은 artifact와 배포 대상의 release는 직렬화한다.

같은 workflow run을 재실행하더라도 이미 게시된 HeadVer artifact를 다시 build하지 않는다. 안전한 resume을 증명할 수 없으면 새 run으로 새 Build를 발급한다.

## Repository에 적용할 때

다음 값을 먼저 확인한다.

```text
artifact와 독립 배포 단위
현재 Head와 기존 version/tag
release timezone
Build source와 기존 최대값
version 주입 지점
artifact identity와 staging→production 승격 방식
```

- 독립적으로 build·배포되는 프론트, 백엔드와 모바일 앱은 artifact별 HeadVer를 사용한다.
- Head 종료 tag가 이미 있으면 닫힌 Head의 재사용으로 보고 새 artifact 생성을 거부한다.
- 오류나 불확실한 외부 상태에서는 fail closed한다.
- tag·Release 생성, push, 스토어 업로드와 production 배포는 사용자가 명시적으로 요청한 범위에서만 수행한다.

앱·웹 서비스·백엔드 같은 제품 artifact에 사용한다. 공개 라이브러리처럼 version으로 API 호환성을 표현하는 패키지는 기존 SemVer 또는 생태계 정책을 우선한다.

GitHub Actions를 구현할 때 [워크플로우 예시](references/workflow-examples.md)에서 필요한 부분을 읽는다.

HeadVer 원본 명세: https://github.com/line/headver
