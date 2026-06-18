---
name: ignore-file-writer
description: 프로젝트에 맞는 .gitignore와 .dockerignore를 생성하거나 기존 파일을 안전하게 보강할 때 사용한다.
---

# Ignore File Writer

프로젝트 구조를 확인한 뒤 공통 템플릿과 언어별 템플릿을 조합해 `.gitignore`와 `.dockerignore`를 만든다. 기존 파일이 있으면 덮어쓰지 말고 필요한 항목만 추가한다.

## 워크플로우

1. **프로젝트 구조 확인**
   - `rg --files -g '!*node_modules*' -g '!*.git/*'`로 주요 파일을 확인한다.
   - 이미 `.gitignore` 또는 `.dockerignore`가 있으면 먼저 읽는다.
   - Git에 이미 추적 중인 artifact를 무시하게 될 수 있으면 `git ls-files`로 확인한다.

2. **항상 적용할 base 선택**
   - `.gitignore`: `assets/gitignore/base.gitignore.template`
   - `.dockerignore`: `assets/dockerignore/base.dockerignore.template`
   - 사용자가 한쪽 파일만 요청했으면 요청한 파일만 만든다.
   - Dockerfile, `compose.yaml` 등이 있거나 사용자가 Docker를 언급하면 `.dockerignore`도 만든다.

3. **언어와 도구 감지**
   - Node/TypeScript: `package.json`, `pnpm-lock.yaml`, `package-lock.json`, `yarn.lock`, `bun.lock`, `tsconfig.json`
   - Python: `pyproject.toml`, `uv.lock`, `requirements*.txt`, `poetry.lock`, `setup.py`
   - 여러 언어가 있으면 감지된 템플릿을 모두 조합한다.

4. **템플릿 조합**
   - `.gitignore`에는 `assets/gitignore/<kind>.gitignore.template`를 사용한다.
   - `.dockerignore`에는 `assets/dockerignore/<kind>.dockerignore.template`를 사용한다.
   - `kind`는 `base`, `node`, `python` 중 하나다.
   - section comment를 유지해 나중에 사람이 쉽게 정리할 수 있게 한다.

5. **기존 파일에 병합**
   - 기존 줄과 의미상 같은 pattern은 중복 추가하지 않는다.
   - 기존 comment와 ordering은 최대한 보존한다.
   - 새 section은 파일 끝에 추가한다. 마지막 newline을 유지한다.
   - 기존 negate rule(`!path`)이 있으면 그 의미를 깨뜨리지 않는다.

6. **충돌 가능성 확인**
   - lockfile은 `.gitignore`에 추가하지 않는다.
   - `dist/`, `build/`, `out/`, local database 파일이 이미 추적 중이면 무시 규칙 추가 전에 사용자에게 확인한다.
   - Docker build가 local build output을 복사하도록 설계된 프로젝트라면 해당 build output을 `.dockerignore`에 넣기 전에 확인한다.
   - `.env.example`등의 예시는 추적 가능하게 둔다.

7. **검증**
   - `git status --short`로 의도한 ignore 파일만 변경됐는지 확인한다.
   - 가능하면 `git check-ignore -v <sample-path>`로 대표 pattern이 동작하는지 확인한다.
   - `.dockerignore`를 변경했다면 build context에 필요한 manifest와 lockfile이 제외되지 않았는지 확인한다.

## 원칙

- **Preserve first**: 기존 파일을 덮어쓰지 않는다.
- **Template-based**: 직접 새 목록을 즉흥적으로 만들지 말고 bundled template을 기준으로 조합한다.
- **Project-aware**: 파일 구조와 tracked files를 보고 위험한 ignore는 확인한다.
- **No lockfile ignore**: dependency lockfile은 기본적으로 Git에 남긴다.
- **Docker context 최소화**: `.dockerignore`는 secret, VCS metadata, dependency directory, cache, local artifact를 빼는 방향으로 작성한다.
