# 에이전트 기술 표준 스킬

AI 코딩 에이전트가 재사용할 수 있는 기술 표준 스킬 모음이다. 각 스킬은 특정 표준이나 설계 지침을 일관되게 적용하기 위한 절차와 참고 자료를 담는다.

스킬은 Agent Skills 형식을 따른다.

## 설치

```bash
npx skills add wibaek/skills
```

## 사용 방식

설치 후 에이전트가 요청 내용을 보고 관련 스킬을 자동으로 선택한다. 필요한 경우 사용자가 스킬 이름을 직접 언급해서 호출할 수도 있다.

예시:

- "REST API 설계 리뷰해줘"
- "API 에러 응답 표준화해줘"
- "OAuth2 flow 설계 검토해줘"

## 스킬 목록

| 스킬 | 용도 |
| --- | --- |
| `api-error-standard` | RFC 9457/7807 Problem Details 기반 API 에러 응답 표준화 |
| `headver` | HeadVer 기반 제품 버전과 build-once/promote-many 릴리스 흐름 설계 |
| `oauth2-standard` | RFC 6749 기반 OAuth 2.0 flow, endpoint, token/error response 검토 |
| `rest-api-guidelines` | HTTP+JSON REST API의 resource 설계, method, status code, pagination, 호환성 규칙 정리 |

## 구조

```text
skills/
  api-error-standard/
  headver/
  oauth2-standard/
  rest-api-guidelines/
```

각 스킬은 필요에 따라 다음 파일과 디렉터리를 포함한다.

| 경로 | 설명 |
| --- | --- |
| `SKILL.md` | 에이전트가 따를 스킬 지침 |
| `assets/` | template file과 configuration 예시 |
| `references/` | 보조 문서와 참고 자료 |
| `scripts/` | 자동화를 위한 helper script |
