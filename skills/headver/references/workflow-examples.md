# HeadVer workflow examples

실제 GitHub Actions workflow를 구현하거나 예시가 필요할 때만 읽는다. 아래 script 이름은 구조를 설명하는 placeholder다. repository의 기존 build, registry와 deploy 명령으로 교체한다.

## 공통 흐름

```text
version 확정
-> immutable artifact build·publish
-> version + source revision + artifact reference 기록
-> 정확한 HeadVer Git tag 생성
-> staging 배포
-> production에 같은 artifact 승격
-> Head 종료 Git tag 생성
```

- version과 artifact는 한 번만 만든다.
- build job은 version과 digest·checksum 같은 immutable reference를 이후 job에 전달한다.
- staging과 production에서는 source를 다시 build하지 않는다.
- 정확한 HeadVer tag는 staging candidate의 commit을 가리키며 이동시키지 않는다.
- production 성공 후 같은 commit에 Head 종료 tag를 추가한다.
- Head 종료 tag는 Git history 탐색용이며 배포나 artifact 조회에 사용하지 않는다.
- 같은 artifact의 release는 직렬화한다. 서로 독립된 artifact는 concurrency group을 분리한다.

Head 설정만 바뀐 commit도 다음 릴리스 라인의 baseline candidate로 build·publish하고 staging에 배포한다. Build와 정확한 HeadVer tag를 발급하되 production 배포와 Head 종료 tag 생성은 별도 승인 전까지 실행하지 않는다.

GitHub Actions의 `github.run_number`는 workflow별 counter이며 rerun에서는 바뀌지 않는다. workflow 교체·분리, 같은 artifact를 발행하는 다른 workflow와 외부 플랫폼의 기존 build number를 확인하고 충돌할 수 있으면 검증된 offset 또는 중앙 counter를 사용한다.

`Asia/Seoul`의 YearWeek은 `TZ=Asia/Seoul date +%g%V`처럼 계산한다. `%y%V`를 사용하지 않고 `2018-12-31 -> 1901`, `2019-12-31 -> 2001`, `2016-01-01 -> 1553` 경계값을 검증한다.

## GitHub Actions 예시

다음 예시는 특정 action이나 reusable workflow에 의존하지 않는다. 각 script가 repository에 맞는 artifact build·publish와 배포를 수행한다고 가정한다.

```yaml
name: HeadVer Release Candidate

on:
  workflow_dispatch:

concurrency:
  group: headver-release-${{ github.repository }}-my-app
  cancel-in-progress: false

permissions:
  contents: read

jobs:
  prepare:
    runs-on: ubuntu-latest
    outputs:
      head: ${{ steps.headver.outputs.head }}
      version: ${{ steps.headver.outputs.version }}
      build: ${{ steps.headver.outputs.build }}
    steps:
      - uses: actions/checkout@v6

      - name: Generate HeadVer
        id: headver
        run: ./scripts/generate-headver.sh "$GITHUB_OUTPUT"

      - name: Check version and tags
        env:
          HEAD: ${{ steps.headver.outputs.head }}
          VERSION: ${{ steps.headver.outputs.version }}
          BUILD: ${{ steps.headver.outputs.build }}
        run: ./scripts/assert-headver-available.sh "$HEAD" "$VERSION" "$BUILD"

  build:
    needs: prepare
    if: github.run_attempt == 1
    runs-on: ubuntu-latest
    outputs:
      artifact-reference: ${{ steps.publish.outputs.artifact-reference }}
      artifact-digest: ${{ steps.publish.outputs.artifact-digest }}
    steps:
      - uses: actions/checkout@v6

      - name: Build and publish artifact
        id: publish
        env:
          VERSION: ${{ needs.prepare.outputs.version }}
          BUILD: ${{ needs.prepare.outputs.build }}
          SOURCE_SHA: ${{ github.sha }}
        run: ./scripts/build-publish.sh "$GITHUB_OUTPUT"

  candidate-tag:
    needs: [prepare, build]
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
      - uses: actions/checkout@v6

      - name: Create exact HeadVer tag
        env:
          VERSION: ${{ needs.prepare.outputs.version }}
          ARTIFACT_REFERENCE: ${{ needs.build.outputs.artifact-reference }}
          ARTIFACT_DIGEST: ${{ needs.build.outputs.artifact-digest }}
          SOURCE_SHA: ${{ github.sha }}
        run: ./scripts/create-headver-tag.sh

  deploy-staging:
    needs: [build, candidate-tag]
    runs-on: ubuntu-latest
    environment: staging
    steps:
      - uses: actions/checkout@v6

      - name: Deploy existing artifact to staging
        env:
          ARTIFACT_REFERENCE: ${{ needs.build.outputs.artifact-reference }}
        run: ./scripts/deploy.sh staging "$ARTIFACT_REFERENCE"

  deploy-production:
    needs: [build, deploy-staging]
    runs-on: ubuntu-latest
    environment: production
    steps:
      - uses: actions/checkout@v6

      - name: Promote existing artifact to production
        env:
          ARTIFACT_REFERENCE: ${{ needs.build.outputs.artifact-reference }}
        run: ./scripts/deploy.sh production "$ARTIFACT_REFERENCE"

  close-head:
    needs: [prepare, build, deploy-production]
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
      - uses: actions/checkout@v6

      - name: Create Head closing tag and exact Release
        env:
          HEAD: ${{ needs.prepare.outputs.head }}
          VERSION: ${{ needs.prepare.outputs.version }}
          ARTIFACT_REFERENCE: ${{ needs.build.outputs.artifact-reference }}
          ARTIFACT_DIGEST: ${{ needs.build.outputs.artifact-digest }}
          SOURCE_SHA: ${{ github.sha }}
        run: ./scripts/close-head.sh
```

`artifact-reference`는 container digest, object URI와 checksum 또는 store build ID처럼 같은 artifact를 다시 지정할 수 있는 값이어야 한다.

build job이 성공하고 deploy만 실패했다면 **Re-run failed jobs**로 실패한 deploy만 다시 실행한다. build job 자체가 실패했다면 push 전후 상태를 안전하게 확인할 수 없는 한 재실행하지 않고 새 workflow run으로 새 Build를 발급한다.

## 정적 웹

`dist/`를 환경마다 다시 build하지 않는다.

```text
6.2634.143 생성
-> dist/ 한 번 build
-> web-6.2634.143.tar.gz / sha256:A 게시
-> staging이 sha256:A 사용
-> production이 같은 object 또는 checksum이 같은 복사본 사용
```

API URL이나 feature flag처럼 환경별 값이 build 결과에 포함되면 artifact가 달라진다. 가능한 경우 runtime config로 분리하고, 분리할 수 없으면 환경별 artifact namespace와 HeadVer를 사용한다.

## 컨테이너

mutable tag가 아니라 digest를 승격 기준으로 사용한다.

```text
registry.example.com/app:6.2634.143 -> sha256:A
staging image                         -> registry.example.com/app@sha256:A
production image                      -> registry.example.com/app@sha256:A
```

환경 설정은 secret, environment variable 또는 runtime configuration으로 주입하고 image layer에 포함하지 않는다.

## build와 deploy가 결합된 플랫폼

하나의 명령이 source build와 deploy를 함께 수행한다면 staging과 production에서 각각 실행할 때 서로 다른 artifact가 된다. 다음 중 운영 모델에 맞는 방식을 선택한다.

- 단일 환경에 한 번만 배포하고 해당 실행을 하나의 artifact로 기록한다.
- 환경마다 다른 build가 필요하면 artifact namespace와 HeadVer를 분리한다.
- 동일 artifact 승격이 필요하면 build·publish와 deploy-by-reference를 분리한다.

## 모바일 스토어

iOS와 Android는 각각 독립된 binary artifact다. 플랫폼별 archive와 store build identity를 기록한다.

Flutter build에는 다음 값을 주입한다.

```text
--build-name={HeadVer}
--build-number={build}
```

### iOS

```text
CFBundleShortVersionString={HeadVer}
CFBundleVersion={build}

archive 한 번 생성
-> TestFlight 업로드·검증
-> 같은 App Store Connect build를 production release에 선택
```

### Android

```text
versionName={HeadVer}
versionCode={build}

AAB 한 번 생성
-> internal 또는 closed track 업로드·검증
-> 같은 AAB와 versionCode를 production track으로 승격
```

flavor, signing 또는 환경 설정 때문에 binary가 달라지면 별도 artifact와 version으로 관리한다.
