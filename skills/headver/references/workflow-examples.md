# HeadVer workflow examples

이 문서는 실제 release workflow를 설계하거나 예시를 요청받았을 때만 읽는다. 아래 명령은 구조를 보여주는 placeholder이므로 repository의 기존 build, registry, deploy 명령으로 교체한다. 사용하지 않는 플랫폼의 예시는 적용하지 않는다.

## 공통 구조

환경별 job을 나누더라도 version과 artifact는 build job에서 한 번만 만든다.

```text
version 확정
-> immutable artifact build·publish
-> version + source revision + digest 기록
-> 정확한 HeadVer Git tag 생성
-> staging에 digest 배포
-> 검증 또는 승인
-> production에 같은 digest 배포
-> Head 종료 Git tag + Release metadata 기록
```

다음 조건을 유지한다.

- 같은 artifact의 release를 직렬화하고 진행 중인 release를 새 실행이 취소하지 않게 한다. 서로 독립된 artifact는 concurrency group을 분리한다.
- build job의 output으로 version과 digest를 이후 job에 전달한다.
- staging과 production job은 deploy manifest를 읽기 위해 source를 checkout할 수 있지만 애플리케이션 artifact를 다시 build하지 않는다.
- rerun 시 artifact가 없으면 같은 Build로 최초 게시할 수 있다.
- rerun 시 artifact가 있으면 source revision을 검증하고 기존 digest를 재사용한다.
- artifact 상태를 확인할 수 없거나 같은 version이 다른 revision을 가리키면 실패한다.
- 정확한 HeadVer tag는 staging candidate의 commit을 가리키며 이동시키지 않는다.
- production 성공 후 Head 종료 tag 하나를 같은 commit에 추가한다. 이 tag는 Git history 탐색용 metadata이며 배포나 artifact 조회에 사용하지 않는다.
- Head 종료 tag가 이미 있으면 해당 Head는 닫힌 것으로 보고 새 candidate 생성을 거부한다.
- tag·Release만 실패했다면 기존 version, source revision과 digest를 검증하고 누락된 metadata만 복구한다.

Head 설정만 바뀐 commit도 다음 릴리스 라인의 baseline candidate로 build·publish하고 staging에 배포한다. 이 경우에도 Build와 정확한 HeadVer tag를 발급하고 다른 candidate와 같은 불변조건을 적용하되, production 배포와 Head 종료 tag 생성은 별도 승인 전까지 실행하지 않는다.

## `wibaek/gha` 적용

[`wibaek/gha`](https://github.com/wibaek/gha)는 reusable workflow를 `jobs.<job_id>.uses`로 호출한다. `steps` 안에서 호출하지 않고 `@v1.0`처럼 release tag로 고정한다. 기본 권한은 `contents: read`로 두고 GHCR build에는 `packages: write`, deploy에는 `packages: read`처럼 job별 최소 권한만 추가한다.

`wibaek/gha`의 HeadVer 문서는 구현 참고 자료이며 이 스킬의 정책보다 우선하지 않는다. Head-only 변경으로 만드는 baseline candidate에도 다른 candidate와 같은 artifact 불변조건을 적용한다.

### GHCR와 VPS staging→production

`docker-build-ghcr-push.yaml@v1.0`은 image를 한 번 build·push하고 다음 output을 제공한다.

```text
image-reference = ghcr.io/owner/app@sha256:...
image-digest    = sha256:...
```

`ssh-compose-vps-deploy.yaml@v1.0`은 `image-reference`를 입력으로 받으므로 staging과 production job에 같은 output을 전달한다. HeadVer image tag와 build image tag를 함께 발행하면 full version과 `artifact + build` 중복을 각각 검사할 근거가 생긴다.

현재 GHCR reusable workflow는 실행될 때마다 build·push하며 기존 artifact를 조회해 resume하는 기능은 제공하지 않는다. 따라서 아래 호환 예시는 caller의 `prepare`와 `docker` job에서 `github.run_attempt != 1`인 artifact publish를 차단한다. 게시 전 실패한 rerun을 같은 Build로 허용하려면 reusable workflow 앞에 registry lookup·claim adapter를 추가하거나 `wibaek/gha`에 resume output을 구현해야 한다.

Docker job이 성공하고 deploy 또는 metadata job만 실패했다면 GitHub Actions의 **Re-run failed jobs**로 실패한 downstream job만 다시 실행해 기존 `image-reference`와 digest를 사용한다. **Re-run all jobs**는 사용하지 않는다. Docker job 자체가 실패했다면 push 전후 상태를 안전하게 판별할 수 없으므로 이 예시에서는 재실행하지 않고 새 workflow run으로 새 Build를 발급한다.

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
    permissions:
      contents: read
      packages: read
    outputs:
      head: ${{ steps.headver.outputs.head }}
      version: ${{ steps.headver.outputs.version }}
      build: ${{ steps.headver.outputs.build }}
    steps:
      - name: Block artifact publish on rerun
        if: github.run_attempt != 1
        run: |
          echo "::error title=Full workflow rerun blocked::If Docker succeeded and only a downstream job failed, use Re-run failed jobs. If Docker failed, start a new workflow run."
          exit 1

      - name: Checkout
        uses: actions/checkout@v6

      - name: Generate HeadVer outputs
        id: headver
        run: ./scripts/generate-headver.sh "$GITHUB_OUTPUT"

      - name: Check immutable tags before publish
        env:
          GH_TOKEN: ${{ github.token }}
          HEAD: ${{ steps.headver.outputs.head }}
          VERSION: ${{ steps.headver.outputs.version }}
          BUILD: ${{ steps.headver.outputs.build }}
        run: ./scripts/assert-headver-tags-available.sh "$HEAD" "$VERSION" "$BUILD"

  docker:
    needs: prepare
    if: github.run_attempt == 1
    uses: wibaek/gha/.github/workflows/docker-build-ghcr-push.yaml@v1.0
    permissions:
      contents: read
      packages: write
    with:
      image-name: auto
      context: .
      dockerfile: ./Dockerfile
      platform: linux/amd64
      tags: |
        type=raw,value=${{ needs.prepare.outputs.version }}
        type=raw,value=build-${{ needs.prepare.outputs.build }}

  candidate-metadata:
    needs: [prepare, docker]
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
      - name: Checkout artifact source revision
        uses: actions/checkout@v6

      - name: Create immutable HeadVer candidate tag
        env:
          VERSION: ${{ needs.prepare.outputs.version }}
          DIGEST: ${{ needs.docker.outputs.image-digest }}
          IMAGE_REFERENCE: ${{ needs.docker.outputs.image-reference }}
          SOURCE_SHA: ${{ github.sha }}
        run: ./scripts/ensure-headver-candidate-tag.sh

  deploy-staging:
    needs: [docker, candidate-metadata]
    uses: wibaek/gha/.github/workflows/ssh-compose-vps-deploy.yaml@v1.0
    permissions:
      contents: read
      packages: read
    with:
      app-name: my-app
      service-name: app
      remote-dir: /srv/my-app-staging
      compose-file: deploy/compose.yaml
      image-reference: ${{ needs.docker.outputs.image-reference }}
    secrets:
      VPS_HOST: ${{ secrets.STAGING_VPS_HOST }}
      VPS_USER: ${{ secrets.STAGING_VPS_USER }}
      VPS_SSH_KEY: ${{ secrets.STAGING_VPS_SSH_KEY }}
      VPS_SSH_KNOWN_HOSTS: ${{ secrets.STAGING_VPS_SSH_KNOWN_HOSTS }}
      RUNTIME_ENV: ${{ secrets.STAGING_APP_ENV }}

  approve-production:
    needs: deploy-staging
    runs-on: ubuntu-latest
    environment: production
    steps:
      - name: Record approval
        run: echo "Production deployment approved"

  deploy-production:
    needs: [docker, approve-production]
    uses: wibaek/gha/.github/workflows/ssh-compose-vps-deploy.yaml@v1.0
    permissions:
      contents: read
      packages: read
    with:
      app-name: my-app
      service-name: app
      remote-dir: /srv/my-app
      compose-file: deploy/compose.yaml
      image-reference: ${{ needs.docker.outputs.image-reference }}
    secrets:
      VPS_HOST: ${{ secrets.PRODUCTION_VPS_HOST }}
      VPS_USER: ${{ secrets.PRODUCTION_VPS_USER }}
      VPS_SSH_KEY: ${{ secrets.PRODUCTION_VPS_SSH_KEY }}
      VPS_SSH_KNOWN_HOSTS: ${{ secrets.PRODUCTION_VPS_SSH_KNOWN_HOSTS }}
      RUNTIME_ENV: ${{ secrets.PRODUCTION_APP_ENV }}

  close-head:
    needs: [prepare, docker, deploy-production]
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
      - name: Checkout artifact source revision
        uses: actions/checkout@v6

      - name: Create immutable Head closing tag and exact Release
        env:
          HEAD: ${{ needs.prepare.outputs.head }}
          VERSION: ${{ needs.prepare.outputs.version }}
          DIGEST: ${{ needs.docker.outputs.image-digest }}
          IMAGE_REFERENCE: ${{ needs.docker.outputs.image-reference }}
          SOURCE_SHA: ${{ github.sha }}
        run: ./scripts/ensure-headver-production-metadata.sh
```

`candidate-metadata`는 예를 들어 정확한 Git tag `v5.2634.143`을 staging 전에 생성한다. production은 이 tag와 함께 기록된 기존 digest를 승격하며 tag에서 source를 다시 build하지 않는다. `close-head`는 production 성공 후 같은 commit에 `v5` 같은 Head 종료 tag 하나만 추가하고 GitHub Release는 정확한 `v5.2634.143` tag에 연결한다. 종료 tag는 사람이 Git history에서 해당 Head의 production 확정 지점을 찾기 위한 표식이며 workflow input이나 registry image tag로 사용하지 않는다. 종료 tag가 이미 같은 commit을 가리키면 성공으로 처리하고, 다른 commit을 가리키면 force update하지 않고 실패한다.

현재 `v1.0`의 VPS deploy workflow에는 `environment`와 `concurrency-group` input이 없다. 따라서 예시는 caller의 `approve-production` job에 `production` GitHub Environment를 연결하고 workflow-level concurrency로 `my-app` release 전체를 직렬화한다. GitHub Actions는 같은 concurrency group에 실행 중인 run 하나와 대기 중인 run 하나만 유지하므로, 여러 artifact가 있는 repository에서는 artifact마다 group suffix를 다르게 지정한다. `main`에만 있는 신규 input을 `@v1.0` 호출에 넘기지 않는다. 해당 input이 새 release tag에 포함되면 called workflow의 environment와 concurrency를 직접 사용할 수 있다.

`production` GitHub Environment에 required reviewer를 설정하면 승인 대기 중에도 image digest는 바뀌지 않는다. runtime secret은 image build argument로 넣지 않고 각 deploy job의 `RUNTIME_ENV`로 전달한다.

`wibaek/gha/.github/workflows/release.yaml@v1.0`은 release-please와 SemVer release PR을 위한 workflow다. HeadVer candidate tag, Head 종료 tag·GitHub Release 생성이나 부분 실패 복구에 그대로 사용하지 않는다. `candidate-metadata`와 `close-head`는 artifact manifest의 version, source SHA와 digest만 사용하며 build·deploy를 호출하지 않는 별도 script 또는 metadata-only workflow로 구현한다.

rollback이나 단순 redeploy는 `docker` job을 거치지 않고 기록된 digest reference를 `ssh-compose-vps-deploy.yaml` 또는 `ssh-compose-image-load-deploy.yaml`의 `image-reference`로 직접 넘긴다.

### Cloudflare Pages와 Workers 경계

현재 `cloudflare-pages-deploy.yaml@v1.0`과 `cloudflare-workers-deploy.yaml@v1.0`은 source checkout, dependency 설치, build와 deploy를 한 job에서 수행한다. 같은 source로 staging과 production workflow를 각각 호출하면 별도 build가 되므로 HeadVer의 동일 artifact 승격 예시로 사용하지 않는다.

다음 중 실제 운영 모델에 맞는 방식을 선택한다.

- 단일 환경에 한 번만 배포한다면 기존 reusable workflow를 그대로 사용하고 해당 실행을 하나의 artifact로 기록한다.
- staging과 production에 서로 다른 build가 필요하다면 artifact namespace와 HeadVer를 분리한다.
- 동일 artifact 승격이 필요하다면 build/publish와 deploy-by-reference를 분리한 reusable workflow를 추가한 뒤, 같은 deployment reference 또는 checksum을 두 환경에 전달한다.

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
