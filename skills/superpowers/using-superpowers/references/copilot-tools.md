# Copilot CLI 도구 매핑

스킬은 Claude Code 도구 이름을 사용한다. 스킬에서 아래 이름을 만나면 플랫폼의 대응 도구를 사용한다:

| 스킬 참조 | Copilot CLI 대응 |
| --- | --- |
| `Read`(파일 읽기) | `view` |
| `Write`(파일 생성) | `create` |
| `Edit`(파일 편집) | `edit` |
| `Bash`(명령 실행) | `bash` |
| `Grep`(파일 내용 검색) | `grep` |
| `Glob`(파일 이름 검색) | `glob` |
| `Skill` tool(스킬 호출) | `skill` |
| `WebFetch` | `web_fetch` |
| `Task` tool(서브에이전트 파견) | `agent_type: "general-purpose"` 또는 `"explore"`가 있는 `task` |
| 여러 `Task` 호출(병렬) | 여러 `task` 호출 |
| Task status/output | `read_agent`, `list_agents` |
| `TodoWrite`(작업 추적) | built-in `todos` table이 있는 `sql` |
| `WebSearch` | 대응 없음. search engine URL과 `web_fetch` 사용 |
| `EnterPlanMode` / `ExitPlanMode` | 대응 없음. main session에 머문다. |

## Async shell session

Copilot CLI는 persistent async shell session을 지원하며, Claude Code에는 직접 대응되는 기능이 없다:

| Tool | 용도 |
| --- | --- |
| `bash` with `async: true` | long-running command를 background에서 시작 |
| `write_bash` | 실행 중인 async session에 input 전송 |
| `read_bash` | async session output 읽기 |
| `stop_bash` | async session 종료 |
| `list_bash` | 활성 shell session 목록 |

## 추가 Copilot CLI 도구

| Tool | 용도 |
| --- | --- |
| `store_memory` | 향후 session을 위해 codebase 사실 저장 |
| `report_intent` | 현재 intent로 UI status line 업데이트 |
| `sql` | session SQLite database(todos, metadata) query |
| `fetch_copilot_cli_documentation` | Copilot CLI 문서 조회 |
| GitHub MCP tools(`github-mcp-server-*`) | Native GitHub API access(issues, PRs, code search) |
