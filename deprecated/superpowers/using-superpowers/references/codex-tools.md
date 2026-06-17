# Codex 도구 매핑

스킬은 Claude Code 도구 이름을 사용한다. 스킬에서 아래 이름을 만나면 플랫폼의 대응 도구를 사용한다:

| 스킬 참조 | Codex 대응 |
| --- | --- |
| `Task` tool(서브에이전트 파견) | `spawn_agent`([서브에이전트 파견에는 multi-agent 지원 필요](#서브에이전트-파견에는-multi-agent-지원-필요) 참고) |
| 여러 `Task` 호출(병렬) | 여러 `spawn_agent` 호출 |
| Task가 결과 반환 | `wait_agent` |
| Task가 자동 완료 | slot 해제를 위해 `close_agent` |
| `TodoWrite`(작업 추적) | `update_plan` |
| `Skill` tool(스킬 호출) | 스킬은 native로 로드된다. 지시를 따르면 된다. |
| `Read`, `Write`, `Edit`(파일) | 플랫폼의 native file tool 사용 |
| `Bash`(명령 실행) | 플랫폼의 native shell tool 사용 |

## 서브에이전트 파견에는 multi-agent 지원 필요

Codex config(`~/.codex/config.toml`)에 추가한다:

```toml
[features]
multi_agent = true
```

이 설정은 `dispatching-parallel-agents`, `subagent-driven-development` 같은 스킬에서 `spawn_agent`, `wait_agent`, `close_agent`를 사용할 수 있게 한다.

Legacy 참고: `rust-v0.115.0` 이전 Codex build는 spawned-agent waiting을 `wait`로 노출했다. 현재 Codex는 spawned agent에 `wait_agent`를 사용한다. `wait`라는 이름은 이제 code-mode `exec/wait`에 속하며, `cell_id`로 yielded exec cell을 resume한다. spawned-agent result tool이 아니다.

## 환경 감지

worktree를 만들거나 branch를 마무리하는 스킬은 진행 전에 read-only git 명령으로 환경을 감지해야 한다:

```bash
GIT_DIR=$(cd "$(git rev-parse --git-dir)" 2>/dev/null && pwd -P)
GIT_COMMON=$(cd "$(git rev-parse --git-common-dir)" 2>/dev/null && pwd -P)
BRANCH=$(git branch --show-current)
```

- `GIT_DIR != GIT_COMMON` -> 이미 linked worktree 안에 있음(생성 건너뜀)
- `BRANCH`가 비어 있음 -> detached HEAD(sandbox에서 branch/push/PR 불가)

각 스킬이 이 signal을 어떻게 사용하는지는 `using-git-worktrees` Step 0과 `finishing-a-development-branch` Step 1을 본다.

## Codex App 마무리

샌드박스가 branch/push operation을 막는 경우(externally managed worktree의 detached HEAD), agent는 모든 작업을 commit하고 사용자에게 App native control을 사용하라고 안내한다:

- **"Create branch"** - branch 이름 지정 후 App UI로 commit/push/PR
- **"Hand off to local"** - 작업을 사용자의 local checkout으로 transfer

agent는 여전히 test 실행, file staging, 추천 branch name, commit message, PR description 출력을 할 수 있다.
