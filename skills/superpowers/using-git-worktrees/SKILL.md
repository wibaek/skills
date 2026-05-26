---
name: using-git-worktrees
description: 현재 작업공간과 격리해야 하는 기능 작업을 시작하거나 구현 계획을 실행하기 전에 사용. 네이티브 도구 또는 git worktree 대체 경로로 격리된 작업공간이 있는지 보장한다.
---

# Git Worktree 사용

## 개요

작업이 격리된 작업공간에서 진행되도록 보장한다. 플랫폼의 네이티브 worktree 도구를 우선 사용한다. 네이티브 도구가 없을 때만 수동 git worktree로 대체한다.

**핵심 원칙:** 먼저 기존 격리를 감지한다. 그 다음 네이티브 도구를 사용한다. 그 다음 git으로 대체한다. 실행 환경과 싸우지 않는다.

**시작할 때 알림:** "격리된 작업공간을 설정하기 위해 using-git-worktrees 스킬을 사용합니다."

## 0단계: 기존 격리 감지

**무언가를 만들기 전에 이미 격리된 작업공간에 있는지 확인한다.**

```bash
GIT_DIR=$(cd "$(git rev-parse --git-dir)" 2>/dev/null && pwd -P)
GIT_COMMON=$(cd "$(git rev-parse --git-common-dir)" 2>/dev/null && pwd -P)
BRANCH=$(git branch --show-current)
```

**서브모듈 가드:** git 서브모듈 안에서도 `GIT_DIR != GIT_COMMON`이 참이다. "이미 worktree 안에 있다"고 결론 내리기 전에 서브모듈이 아닌지 확인한다:

```bash
# 경로가 반환되면 worktree가 아니라 서브모듈 안이다. 일반 repo로 취급한다.
git rev-parse --show-superproject-working-tree 2>/dev/null
```

**`GIT_DIR != GIT_COMMON`이고 서브모듈이 아니면:** 이미 연결된 worktree 안에 있다. 3단계(프로젝트 설정)로 건너뛴다. 또 다른 worktree를 만들지 않는다.

브랜치 상태와 함께 보고한다:

- 브랜치 위: "`<path>`의 격리된 작업공간에 이미 있고, 브랜치는 `<name>`입니다."
- Detached HEAD: "`<path>`의 격리된 작업공간에 이미 있습니다(detached HEAD, 외부에서 관리됨). 마무리 시점에 브랜치 생성이 필요합니다."

**`GIT_DIR == GIT_COMMON`이거나 서브모듈 안이면:** 일반 repo 체크아웃에 있다.

사용자가 이미 지시에서 worktree 선호를 밝혔다면 그대로 따른다. 그렇지 않다면 worktree를 만들기 전에 동의를 구한다:

> "격리된 worktree를 설정할까요? 현재 브랜치를 변경으로부터 보호할 수 있습니다."

이미 선언된 선호가 있으면 질문 없이 따른다. 사용자가 거절하면 현재 위치에서 작업하고 3단계로 건너뛴다.

## 1단계: 격리된 작업공간 만들기

**두 가지 메커니즘이 있다. 아래 순서로 시도한다.**

### 1a. 네이티브 Worktree 도구(선호)

사용자가 격리된 작업공간을 요청했다(0단계 동의). 이미 worktree를 만들 방법이 있는가? `EnterWorktree`, `WorktreeCreate`, `/worktree` 명령, `--worktree` 플래그 같은 도구일 수 있다. 있으면 그것을 사용하고 3단계로 건너뛴다.

네이티브 도구는 디렉터리 배치, 브랜치 생성, 정리를 자동 처리한다. 네이티브 도구가 있는데 `git worktree add`를 사용하면 실행 환경이 보거나 관리할 수 없는 유령 상태가 생긴다.

네이티브 worktree 도구가 없을 때만 1b단계로 진행한다.

### 1b. Git Worktree 대체 경로

**1a가 적용되지 않을 때만 사용한다.** 사용 가능한 네이티브 worktree 도구가 없을 때 수동으로 git worktree를 만든다.

#### 디렉터리 선택

다음 우선순위를 따른다. 명시적인 사용자 선호는 관찰된 파일시스템 상태보다 항상 우선한다.

1. **지시에서 선언된 worktree 디렉터리 선호를 확인한다.** 사용자가 이미 지정했다면 질문 없이 사용한다.

2. **프로젝트 로컬 worktree 디렉터리가 이미 있는지 확인한다:**

   ```bash
   ls -d .worktrees 2>/dev/null     # 선호(숨김)
   ls -d worktrees 2>/dev/null      # 대안
   ```

   발견되면 사용한다. 둘 다 있으면 `.worktrees`가 우선한다.

3. **기존 전역 디렉터리를 확인한다:**

   ```bash
   project=$(basename "$(git rev-parse --show-toplevel)")
   ls -d ~/.config/superpowers/worktrees/$project 2>/dev/null
   ```

   발견되면 사용한다. 예전 전역 경로와의 호환성을 위한 것이다.

4. **다른 지침이 없으면** 프로젝트 루트의 `.worktrees/`를 기본값으로 사용한다.

#### 안전 검증(프로젝트 로컬 디렉터리만)

**worktree를 만들기 전에 디렉터리가 ignore되는지 반드시 검증한다:**

```bash
git check-ignore -q .worktrees 2>/dev/null || git check-ignore -q worktrees 2>/dev/null
```

**ignore되지 않으면:** `.gitignore`에 추가하고 그 변경을 커밋한 뒤 진행한다.

**중요한 이유:** worktree 내용이 실수로 저장소에 커밋되는 일을 막는다.

전역 디렉터리(`~/.config/superpowers/worktrees/`)는 검증이 필요 없다.

#### Worktree 만들기

```bash
project=$(basename "$(git rev-parse --show-toplevel)")

# 선택한 위치에 따라 경로 결정
# 프로젝트 로컬: path="$LOCATION/$BRANCH_NAME"
# 전역: path="~/.config/superpowers/worktrees/$project/$BRANCH_NAME"

git worktree add "$path" -b "$BRANCH_NAME"
cd "$path"
```

**샌드박스 대체 경로:** 권한 오류(샌드박스 거부)로 `git worktree add`가 실패하면, 샌드박스가 worktree 생성을 막았고 현재 디렉터리에서 작업하겠다고 사용자에게 알린다. 그런 다음 현재 위치에서 설정과 기준 테스트를 실행한다.

## 3단계: 프로젝트 설정

적절한 설정을 자동 감지해 실행한다:

```bash
# Node.js
if [ -f package.json ]; then npm install; fi

# Rust
if [ -f Cargo.toml ]; then cargo build; fi

# Python
if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
if [ -f pyproject.toml ]; then poetry install; fi

# Go
if [ -f go.mod ]; then go mod download; fi
```

## 4단계: 깨끗한 기준선 검증

작업공간이 깨끗한 상태에서 시작하는지 확인하기 위해 테스트를 실행한다:

```bash
# 프로젝트에 맞는 명령 사용
npm test / cargo test / pytest / go test ./...
```

**테스트가 실패하면:** 실패를 보고하고, 계속 진행할지 조사할지 물어본다.

**테스트가 통과하면:** 준비 완료를 보고한다.

### 보고

```text
Worktree ready at <full-path>
Tests passing (<N> tests, 0 failures)
Ready to implement <feature-name>
```

## 빠른 참조

| 상황 | 행동 |
| --- | --- |
| 이미 연결된 worktree 안에 있음 | 생성 건너뜀(0단계) |
| 서브모듈 안에 있음 | 일반 repo로 취급(0단계 가드) |
| 네이티브 worktree 도구 사용 가능 | 사용(1a) |
| 네이티브 도구 없음 | Git worktree 대체 경로(1b) |
| `.worktrees/` 존재 | 사용(ignore 검증) |
| `worktrees/` 존재 | 사용(ignore 검증) |
| 둘 다 존재 | `.worktrees/` 사용 |
| 둘 다 없음 | 지시 파일 확인 후 `.worktrees/` 기본 사용 |
| 전역 경로 존재 | 사용(이전 호환성) |
| 디렉터리가 ignore되지 않음 | `.gitignore`에 추가하고 커밋 |
| 생성 중 권한 오류 | 샌드박스 대체 경로, 현재 위치에서 작업 |
| 기준 테스트 실패 | 실패 보고 후 질문 |
| `package.json`/`Cargo.toml` 없음 | 의존성 설치 건너뜀 |

## 흔한 실수

### 실행 환경과 싸우기

- **문제:** 플랫폼이 이미 격리를 제공하는데 `git worktree add`를 사용함
- **수정:** 0단계가 기존 격리를 감지한다. 1a단계는 네이티브 도구에 맡긴다.

### 감지 건너뛰기

- **문제:** 기존 worktree 안에 중첩 worktree를 만듦
- **수정:** 무언가를 만들기 전에 항상 0단계를 실행한다.

### ignore 검증 건너뛰기

- **문제:** worktree 내용이 추적되어 git status를 오염시킴
- **수정:** 프로젝트 로컬 worktree를 만들기 전에 항상 `git check-ignore`를 사용한다.

### 디렉터리 위치 가정

- **문제:** 불일치를 만들고 프로젝트 관례를 어김
- **수정:** 우선순위를 따른다. 기존 위치 > 전역 레거시 > 지시 파일 > 기본값.

### 실패한 테스트를 두고 진행

- **문제:** 새 버그와 기존 문제를 구분할 수 없음
- **수정:** 실패를 보고하고 계속 진행할 명시적 허락을 받는다.

## 위험 신호

**절대 하지 말 것:**

- 0단계가 기존 격리를 감지했는데 worktree 만들기
- 네이티브 worktree 도구(`EnterWorktree` 등)가 있는데 `git worktree add` 사용하기. 가장 큰 실수다. 있으면 사용한다.
- 1a단계를 건너뛰고 바로 1b의 git 명령으로 이동하기
- 프로젝트 로컬 worktree가 ignore되는지 검증하지 않고 만들기
- 기준 테스트 검증 건너뛰기
- 실패한 테스트를 두고 묻지 않고 진행하기

**항상 할 것:**

- 먼저 0단계 감지 실행
- git 대체 경로보다 네이티브 도구 선호
- 디렉터리 우선순위 준수: 기존 위치 > 전역 레거시 > 지시 파일 > 기본값
- 프로젝트 로컬은 디렉터리가 ignore되는지 검증
- 프로젝트 설정 자동 감지 및 실행
- 깨끗한 테스트 기준선 검증
