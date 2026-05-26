# Gemini CLI 도구 매핑

스킬은 Claude Code 도구 이름을 사용한다. 스킬에서 아래 이름을 만나면 플랫폼의 대응 도구를 사용한다:

| 스킬 참조 | Gemini CLI 대응 |
| --- | --- |
| `Read`(파일 읽기) | `read_file` |
| `Write`(파일 생성) | `write_file` |
| `Edit`(파일 편집) | `replace` |
| `Bash`(명령 실행) | `run_shell_command` |
| `Grep`(파일 내용 검색) | `grep_search` |
| `Glob`(파일 이름 검색) | `glob` |
| `TodoWrite`(작업 추적) | `write_todos` |
| `Skill` tool(스킬 호출) | `activate_skill` |
| `WebSearch` | `google_web_search` |
| `WebFetch` | `web_fetch` |
| `Task` tool(서브에이전트 파견) | `@agent-name`([Subagent support](#subagent-support) 참고) |

## Subagent 지원

Gemini CLI는 `@` syntax를 통해 subagent를 native로 지원한다. 모든 작업을 파견할 때 built-in `@generalist` agent를 사용한다. 이 agent는 모든 tool에 접근할 수 있고 제공한 prompt를 따른다.

스킬이 named agent type 파견을 말하면, 스킬의 prompt template 전체를 채워 `@generalist`에 전달한다:

| 스킬 지시 | Gemini CLI 대응 |
| --- | --- |
| `Task tool (superpowers:implementer)` | 채운 `implementer-prompt.md` template으로 `@generalist` |
| `Task tool (superpowers:spec-reviewer)` | 채운 `spec-reviewer-prompt.md` template으로 `@generalist` |
| `Task tool (superpowers:code-reviewer)` | `@code-reviewer`(bundled agent) 또는 채운 review prompt로 `@generalist` |
| `Task tool (superpowers:code-quality-reviewer)` | 채운 `code-quality-reviewer-prompt.md` template으로 `@generalist` |
| inline prompt가 있는 `Task tool (general-purpose)` | inline prompt로 `@generalist` |

### Prompt 채우기

스킬은 `{WHAT_WAS_IMPLEMENTED}` 또는 `[작업 전체 텍스트]` 같은 placeholder가 있는 prompt template을 제공한다. 모든 placeholder를 채우고 완전한 prompt를 `@generalist` 메시지로 전달한다. prompt template 자체가 agent role, review criteria, expected output format을 포함하므로 `@generalist`가 따른다.

### 병렬 파견

Gemini CLI는 병렬 subagent dispatch를 지원한다. 스킬이 여러 독립 subagent task를 병렬로 파견하라고 하면, 해당 `@generalist` 또는 named subagent task들을 같은 prompt에서 함께 요청한다. 의존 작업은 순차로 유지하되, 기록을 단순하게 유지하려고 독립 subagent task를 직렬화하지 않는다.

## 추가 Gemini CLI 도구

Claude Code에는 대응 도구가 없는 Gemini CLI 도구:

| Tool | 용도 |
| --- | --- |
| `list_directory` | 파일과 하위 디렉터리 목록 |
| `save_memory` | GEMINI.md에 사실 저장 |
| `ask_user` | 사용자에게 structured input 요청 |
| `tracker_create_task` | rich task management(create, update, list, visualize) |
| `enter_plan_mode` / `exit_plan_mode` | 변경 전 read-only research mode 전환 |
