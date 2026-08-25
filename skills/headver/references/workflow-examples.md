# HeadVer workflow examples

실제 GitHub Actions workflow를 구현하거나 예시가 필요할 때만 읽는다. 아래 script 이름은 구조를 설명하는 placeholder다. repository의 기존 build, registry와 deploy 명령으로 교체한다.

## 공통 흐름

```text
Build workflow(ref=main)
  HeadVer 확정
  -> immutable artifact build·publish
  -> registry에 HeadVer + artifact digest 보존
  -> 정확한 HeadVer Git tag 생성

Auto-staging bridge
  Build 성공 감지
  -> Staging workflow를 exact tag ref로 dispatch

Staging workflow(ref=exact tag)
  tag와 registry에서 artifact 조회
  -> 기존 artifact 배포

Production request
  exact tag 선택
  -> Production workflow를 exact tag ref로 dispatch

Production workflow(ref=exact tag)
  같은 artifact 승격
  -> Head 종료 Git tag와 정확한 GitHub Release 생성
```

- HeadVer와 artifact는 한 번만 만든다.
- 현재 Head는 repository root의 `.headver` 파일에 숫자 하나로 기록하고 version control한다. Build는 이 값을 읽고, production 성공 후 다음 Head로 바꾸는 작업은 별도 commit으로 수행한다.
- Build workflow는 artifact publish와 exact tag 생성까지만 담당한다. environment를 참조하거나 deploy하지 않는다.
- Build와 deploy 사이의 자동 연결은 별도 bridge가 담당한다. Bridge를 비활성화하거나 제거해도 build와 수동 staging deploy가 각각 동작해야 한다.
- Bridge는 environment를 참조하지 않고 Deployment를 만들지 않는다.
- staging과 production은 exact HeadVer tag ref로 시작하는 별도 workflow run이어야 한다. 같은 `main` run의 job 분리나 reusable workflow 호출만으로는 ref가 바뀌지 않는다.
- tag를 `workflow_dispatch` input으로만 전달하면 GitHub Deployment ref는 tag가 되지 않는다. 실제 dispatch ref도 exact tag여야 한다.
- 서로 다른 workflow run은 job output을 공유하지 못하므로 deploy는 exact tag에서 HeadVer와 source revision을 확인하고 registry에서 artifact reference와 digest를 조회한다. Auto-staging bridge는 triggering build run에서 exact tag를 찾을 수 있어야 한다.
- staging과 production에서는 source를 다시 build하지 않는다.
- 자동 staging은 실행 중인 deploy를 완료하고 대기 중인 이전 deploy를 더 최신 Build로 교체한다. 중간 Build를 모두 순서대로 배포하기 위한 queue를 만들지 않는다.
- 정확한 HeadVer tag는 build commit을 가리키며 이동시키지 않는다.
- production 성공 후 같은 commit에 Head 종료 tag를 추가한다.
- Head 종료 tag는 Git history 탐색용이며 배포나 artifact 조회에 사용하지 않는다.
- 같은 artifact의 release는 직렬화한다. 서로 독립된 artifact는 concurrency group을 분리한다.

`.headver`만 바뀐 commit도 다음 릴리스 라인의 baseline으로 build·publish하고 exact tag를 발급한다. Auto-staging이 활성화되어 있으면 bridge가 별도 staging workflow를 실행한다. Production 배포와 Head 종료 tag 생성은 별도 production workflow에서 수행한다.

### GitHub Environment 경계

이 문서의 `environment: staging`과 `environment: production`은 GitHub의 Deployment Environment다. 애플리케이션의 `.env`, `APP_ENV` 또는 build flavor를 뜻하지 않는다.

- 실제 배포 job만 GitHub Environment를 참조한다. Build와 bridge에는 붙이지 않는다.
- GitHub Environment는 배포 승인, 허용 branch·tag, 환경별 secret·variable과 Deployment history의 경계다.
- runtime secret과 환경별 설정은 보호 규칙을 통과한 deploy job에서 주입하며 artifact에 포함하지 않는다.
- Environment 자체가 배포를 직렬화하지는 않는다. 같은 배포 대상은 별도의 concurrency group으로 직렬화한다.
- staging과 production의 허용 tag 규칙은 exact HeadVer tag를 받을 수 있도록 설정한다. Head 종료 tag는 허용하지 않는다.

GitHub Release와 Head 종료 tag는 production 성공을 기록하는 release metadata다. Artifact build나 deploy를 대신하지 않으며, 이를 만들기 위해 source를 다시 build하거나 artifact를 다시 publish하지 않는다.

GitHub Actions의 `github.run_number`는 workflow별 counter이며 rerun에서는 바뀌지 않는다. workflow 교체·분리, 같은 artifact를 발행하는 다른 workflow와 외부 플랫폼의 기존 build number를 확인하고 충돌할 수 있으면 검증된 offset 또는 중앙 counter를 사용한다.

`Asia/Seoul`의 YearWeek은 `TZ=Asia/Seoul date +%g%V`처럼 계산한다. `%y%V`를 사용하지 않고 `2018-12-31 -> 1901`, `2019-12-31 -> 2001`, `2016-01-01 -> 1553` 경계값을 검증한다.

## GitHub Actions workflow 파일

각 예시는 실제 `.github/workflows/*.yaml` 파일 하나와 일대일로 대응한다. 필요한 파일의 reference만 읽고 repository의 build, registry와 deploy 명령에 맞게 placeholder script를 교체한다.

- [build-image.yaml](build-image.yaml): `main`에서 HeadVer artifact를 build·publish하고 exact tag를 만든다.
- [trigger-staging-deploy.yaml](trigger-staging-deploy.yaml): 성공한 Build run을 exact tag의 Staging workflow로 연결한다. 자동 staging이 필요할 때만 사용한다.
- [deploy-staging.yaml](deploy-staging.yaml): exact tag의 기존 artifact를 staging에 배포한다.
- [request-production-release.yaml](request-production-release.yaml): GitHub Actions UI에서 선택한 tag를 실제 Production workflow의 ref로 dispatch한다. CLI로 직접 실행하면 생략할 수 있다.
- [deploy-production.yaml](deploy-production.yaml): exact tag artifact를 production에 승격하고 Head를 닫는다.

`artifact-reference`는 container digest, object URI와 checksum 또는 store build ID처럼 같은 artifact를 다시 지정할 수 있는 값이어야 한다. Build workflow는 artifact를 HeadVer로 조회할 수 있게 publish하고 registry에 digest를 보존한다. Deploy workflow는 exact tag와 registry를 이용해 이 값을 다시 확인한다.

Build가 성공하고 bridge 또는 staging이 실패했다면 exact tag로 Staging workflow만 다시 실행한다. Build 자체가 실패했다면 새 workflow run으로 새 Build를 발급한다.

예시의 `packages: read|write`는 GitHub Packages 기준이다. 다른 registry를 사용하면 제거하고 필요한 credential과 최소 권한으로 바꾼다.

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
