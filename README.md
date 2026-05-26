# 에이전트 스킬

AI 코딩 에이전트의 작업 방식을 확장하기 위한 개인 스킬 모음이다. 각 스킬은 에이전트가 특정 상황에서 따라야 할 지침, 참고 자료, 자동화 스크립트를 함께 담는다.

스킬은 Agent Skills 형식을 따른다.

## 설치

```bash
npx skills add wibaek/skills
```

## 사용 방식

설치 후 에이전트가 요청 내용을 보고 관련 스킬을 자동으로 선택한다. 필요한 경우 사용자가 스킬 이름을 직접 언급해서 호출할 수도 있다.

예시:

- "Python 프로젝트 시작해줘"
- "FastAPI 프로젝트 만들어줘"
- "TS lint/format/test 설정해줘"
- "REST API 설계 리뷰해줘"
- "커밋 해줘"
- "PR 본문 작성해줘"

## 스킬 목록

### 개인 워크플로우

| 스킬 | 용도 |
| --- | --- |
| `python-starter` | Python 프로젝트의 formatter, linter, 기본 개발 도구 설정 |
| `ts-starter` | 기존 Node 또는 frontend 프로젝트의 TypeScript, Biome, Vitest 설정 |
| `git-commit-writer` | 실제 git diff를 바탕으로 Conventional Commit 메시지 작성과 commit workflow 수행 |
| `github-pr-writer` | branch history, diff, 검증 결과를 바탕으로 GitHub PR 제목과 본문 작성 |
| `benchmark-prd-scout` | 명시적으로 호출됐을 때만 제품/서비스 벤치마킹 결과를 PRD, 기능 목록, 백로그로 정리 |

### 기술 표준

| 스킬 | 용도 |
| --- | --- |
| `api-error-standard` | RFC 9457/7807 Problem Details 기반 API 에러 응답 표준화 |
| `oauth2-standard` | RFC 6749 기반 OAuth 2.0 flow, endpoint, token/error response 검토 |
| `rest-api-guidelines` | HTTP+JSON REST API의 resource 설계, method, status code, pagination, 호환성 규칙 정리 |

### 슈퍼파워 워크플로우

| 스킬 | 용도 |
| --- | --- |
| `using-superpowers` | 대화 시작 시 적용할 스킬을 찾고 우선순위를 정하는 기본 규칙 |
| `brainstorming` | 기능 생성, 동작 변경, 설계 작업 전에 의도와 요구사항 정리 |
| `using-git-worktrees` | 현재 작업공간과 격리된 기능 작업 환경 구성 |
| `writing-plans` | 여러 단계 작업을 실행 가능한 계획으로 분해 |
| `executing-plans` | 리뷰 체크포인트가 있는 구현 계획 실행 |
| `subagent-driven-development` | 독립 작업으로 나뉜 구현 계획을 서브에이전트 흐름으로 진행 |
| `dispatching-parallel-agents` | 공유 상태나 순차 의존성이 없는 작업을 병렬 처리 |
| `test-driven-development` | 기능/버그 수정 전에 실패 테스트부터 작성 |
| `systematic-debugging` | 버그, 테스트 실패, 예상치 못한 동작의 원인을 먼저 추적 |
| `requesting-code-review` | 작업 완료 후 요구사항 충족 여부를 코드 리뷰로 검증 |
| `receiving-code-review` | 코드 리뷰 피드백을 기술적으로 검토하고 필요한 수정 수행 |
| `verification-before-completion` | 완료나 통과를 말하기 전에 실제 검증 명령 실행 |
| `finishing-a-development-branch` | 구현 완료 후 merge, PR, 정리 방식 결정 |

슈퍼파워 스킬의 권장 사용 순서와 상세 색인은 [skills/superpowers/README.md](skills/superpowers/README.md)에 정리되어 있다.

## 구조

```text
skills/
  personal/      개인 workflow와 project setup 선호
  general/       재사용 가능한 기술 표준과 guideline
  superpowers/   process 중심 workflow skill
```

각 스킬은 필요에 따라 다음 파일과 디렉터리를 포함한다.

| 경로 | 설명 |
| --- | --- |
| `SKILL.md` | 에이전트가 따를 스킬 지침 |
| `assets/` | template file과 configuration 예시 |
| `references/` | 보조 문서와 참고 자료 |
| `scripts/` | 자동화를 위한 helper script |
