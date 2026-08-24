# HeadVer workflow examples

이 문서는 실제 release workflow를 설계하거나 예시를 요청받았을 때만 읽는다. 아래 명령은 구조를 보여주는 placeholder이므로 repository의 기존 build, registry, deploy 명령으로 교체한다. 사용하지 않는 플랫폼의 예시는 적용하지 않는다.

## 공통 구조

환경별 job을 나누더라도 version과 artifact는 build job에서 한 번만 만든다.

```text
version 확정
-> immutable artifact build·publish
-> version + source revision + digest 기록
-> staging에 digest 배포
-> 검증 또는 승인
-> production에 같은 digest 배포
-> tag·Release metadata 기록
```

다음 조건을 유지한다.

- release를 직렬화하고 진행 중인 release를 새 실행이 취소하지 않게 한다.
- build job의 output으로 version과 digest를 이후 job에 전달한다.
- staging과 production job에서는 source checkout이나 build 명령을 실행하지 않는다.
- rerun 시 artifact가 없으면 같은 Build로 최초 게시할 수 있다.
- rerun 시 artifact가 있으면 source revision을 검증하고 기존 digest를 재사용한다.
- artifact 상태를 확인할 수 없거나 같은 version이 다른 revision을 가리키면 실패한다.
- production 이후 tag·Release만 실패했다면 기존 metadata만 복구한다.

## GitHub Actions 골격

checkout과 인증 단계는 생략했다. dependency 설치는 repository가 이미 사용하는 고정된 action 또는 script를 따른다. 아래 예시는 job 간 identity 전달과 재빌드 방지 구조에 집중한다.

```yaml
name: release

on:
  workflow_dispatch:

concurrency:
  group: release-${{ github.ref_name }}
  cancel-in-progress: false

jobs:
  build:
    runs-on: ubuntu-latest
    outputs:
      version: ${{ steps.version.outputs.version }}
      digest: ${{ steps.artifact.outputs.digest }}
    steps:
      - name: Install dependencies after checkout
        run: ./scripts/prepare-release

      - name: Generate HeadVer
        id: version
        run: |
          set -euo pipefail
          version="$(./scripts/headver-version "$GITHUB_RUN_NUMBER")"
          printf 'version=%s\n' "$version" >> "$GITHUB_OUTPUT"

      - name: Publish or resume immutable artifact
        id: artifact
        env:
          VERSION: ${{ steps.version.outputs.version }}
        run: |
          set -euo pipefail
          if ./scripts/artifact-exists "$VERSION"; then
            ./scripts/verify-artifact "$VERSION" "$GITHUB_SHA"
          else
            ./scripts/build-artifact "$VERSION"
            ./scripts/publish-artifact "$VERSION" "$GITHUB_SHA"
          fi
          digest="$(./scripts/artifact-digest "$VERSION")"
          printf 'digest=%s\n' "$digest" >> "$GITHUB_OUTPUT"

  deploy-staging:
    needs: build
    runs-on: ubuntu-latest
    environment: staging
    steps:
      - name: Deploy immutable artifact
        env:
          VERSION: ${{ needs.build.outputs.version }}
          DIGEST: ${{ needs.build.outputs.digest }}
        run: ./scripts/deploy-artifact staging "$VERSION" "$DIGEST"

  deploy-production:
    needs: [build, deploy-staging]
    runs-on: ubuntu-latest
    environment: production
    steps:
      - name: Promote the staging artifact
        env:
          VERSION: ${{ needs.build.outputs.version }}
          DIGEST: ${{ needs.build.outputs.digest }}
        run: ./scripts/deploy-artifact production "$VERSION" "$DIGEST"

  release-metadata:
    needs: [build, deploy-production]
    runs-on: ubuntu-latest
    steps:
      - name: Create missing tag and Release metadata
        env:
          VERSION: ${{ needs.build.outputs.version }}
          DIGEST: ${{ needs.build.outputs.digest }}
        run: ./scripts/ensure-release-metadata "$VERSION" "$GITHUB_SHA" "$DIGEST"
```

`production` environment에 승인이 설정되어 있다면 승인 대기 중에도 build artifact가 바뀌지 않는다. `release-metadata` 복구가 필요할 때는 build와 deploy를 다시 실행하지 않고 이미 배포된 version, revision과 digest를 입력으로 사용한다.

Head 설정만 바뀐 commit에서 artifact가 생성되는 것을 피하려면 release workflow를 `workflow_dispatch` 같은 명시적 candidate trigger로 분리하는 방식을 우선 고려한다. `push` trigger를 유지한다면 변경 파일이 Head 설정뿐일 때에만 build job을 건너뛰고, 코드 변경까지 함께 있는 commit을 잘못 제외하지 않게 한다.

## 정적 웹 artifact

정적 웹은 `dist/`를 환경마다 다시 빌드하지 않는다.

```text
6.2634.143 생성
-> dist/ 한 번 build
-> web-6.2634.143.tar.gz / sha256:A 게시
-> staging이 sha256:A를 사용
-> production이 동일 object 또는 checksum이 같은 복사본을 사용
```

API URL이나 feature flag처럼 환경별 값이 build 결과에 포함되면 staging과 production artifact가 달라진다. 가능한 경우 runtime config로 분리한다. 분리할 수 없다면 환경별 artifact namespace와 HeadVer를 따로 두고 동일 artifact 승격이라고 표현하지 않는다.

정적 호스팅이 object promotion을 지원하지 않으면 다음을 검증한다.

- production 업로드 입력이 staging에서 검증한 object인지
- 업로드 전후 checksum이 같은지
- deploy manifest에 HeadVer, source revision과 checksum이 함께 기록되는지

## 컨테이너 기반 웹·백엔드

컨테이너는 mutable tag가 아니라 digest를 승격 기준으로 사용한다.

```text
registry.example.com/app:6.2634.143 -> sha256:A
staging deployment image             -> registry.example.com/app@sha256:A
production deployment image          -> registry.example.com/app@sha256:A
```

환경 이름을 붙인 tag를 새 image처럼 다시 build하지 않는다. 같은 image digest를 가리키는 편의용 tag를 허용하더라도 HeadVer identity와 배포 기록의 기준은 digest로 유지한다. 환경 설정은 secret, environment variable 또는 runtime configuration으로 주입하고 image layer에 포함하지 않는다.

registry에 같은 HeadVer tag가 이미 있다면 다음처럼 처리한다.

- 기록된 source revision이 현재 revision과 같으면 기존 digest로 resume한다.
- revision 또는 digest가 다르면 tag를 덮어쓰지 않고 실패한다.
- 존재 여부를 확인할 권한이 없거나 registry 응답이 불확실하면 새 image를 밀지 않는다.

## 모바일 스토어 승격

iOS와 Android는 각각 독립된 binary artifact로 취급한다. 하나의 릴리스 단위로 관리하더라도 플랫폼별 archive와 store build identity를 기록한다.

### iOS

```text
HeadVer와 CFBundleVersion 확정
-> archive 한 번 생성
-> TestFlight 업로드
-> 해당 build 검증
-> 같은 App Store Connect build를 production release에 선택
```

App Store 제출 직전에 archive를 다시 만들지 않는다. 인증서나 export 단계가 binary를 바꾼다면 어떤 산출물을 staging에서 검증하고 production에 제출하는지 별도로 정의한다.

### Android

```text
HeadVer와 versionCode 확정
-> AAB 한 번 생성
-> internal 또는 closed track 업로드
-> 해당 release 검증
-> 같은 AAB와 versionCode를 production track으로 승격
```

production용으로 `flutter build appbundle` 또는 Gradle build를 다시 실행하지 않는다. Play Console의 track promotion을 사용하거나, 동일한 AAB를 다시 제출해야 한다면 checksum을 확인한다.

flavor, signing 또는 환경 설정 때문에 서로 다른 binary가 만들어진다면 별도 artifact로 버전과 검증 경로를 관리한다.
