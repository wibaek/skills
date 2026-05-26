# 테스트 안티패턴

**이 reference를 로드할 때:** 테스트를 작성하거나 변경할 때, mock을 추가할 때, production code에 test-only method를 추가하고 싶은 유혹이 들 때.

## 개요

테스트는 mock 동작이 아니라 실제 동작을 검증해야 한다. mock은 격리를 위한 수단이지 테스트 대상이 아니다.

**핵심 원칙:** mock이 하는 일이 아니라 코드가 하는 일을 테스트한다.

**엄격한 TDD를 따르면 이런 안티패턴을 피할 수 있다.**

## 철칙

```text
1. mock 동작을 절대 테스트하지 않는다
2. production class에 test-only method를 절대 추가하지 않는다
3. dependency를 이해하지 않고 mock하지 않는다
```

## 안티패턴 1: Mock 동작 테스트

**위반:**

```typescript
// ❌ 나쁨: mock이 존재하는지 테스트
test('renders sidebar', () => {
  render(<Page />);
  expect(screen.getByTestId('sidebar-mock')).toBeInTheDocument();
});
```

**왜 틀렸는가:**

- 컴포넌트가 작동하는지 아니라 mock이 작동하는지 검증한다.
- mock이 있으면 통과하고 없으면 실패한다.
- 실제 동작에 대해 아무것도 알려주지 않는다.

**사람 파트너의 교정:** "우리가 mock의 동작을 테스트하고 있나요?"

**수정:**

```typescript
// ✅ 좋음: 실제 component를 테스트하거나 mock하지 않기
test('renders sidebar', () => {
  render(<Page />);  // sidebar를 mock하지 않기
  expect(screen.getByRole('navigation')).toBeInTheDocument();
});

// 또는 isolation을 위해 sidebar를 반드시 mock해야 한다면:
// mock에 assert하지 말고 sidebar가 있는 상태에서 Page의 동작을 테스트
```

### 게이트 함수

```text
mock element에 assert하기 전에:
  묻는다: "실제 component behavior를 테스트하는가, 아니면 mock 존재만 테스트하는가?"

  mock 존재를 테스트한다면:
    멈춘다. assertion을 삭제하거나 component mock을 해제한다.

  대신 실제 동작을 테스트한다.
```

## 안티패턴 2: Production에 Test-Only Method 추가

**위반:**

```typescript
// ❌ 나쁨: destroy()가 test에서만 사용됨
class Session {
  async destroy() {  // production API처럼 보임!
    await this._workspaceManager?.destroyWorkspace(this.id);
    // ... cleanup
  }
}

// test에서
afterEach(() => session.destroy());
```

**왜 틀렸는가:**

- Production class가 test-only code로 오염된다.
- production에서 실수로 호출되면 위험하다.
- YAGNI와 관심사 분리를 위반한다.
- object lifecycle과 entity lifecycle을 혼동하게 만든다.

**수정:**

```typescript
// ✅ 좋음: test utility가 test cleanup 처리
// Session에는 destroy() 없음 - production에서는 stateless

// test-utils/에서
export async function cleanupSession(session: Session) {
  const workspace = session.getWorkspaceInfo();
  if (workspace) {
    await workspaceManager.destroyWorkspace(workspace.id);
  }
}

// test에서
afterEach(() => cleanupSession(session));
```

### 게이트 함수

```text
production class에 method를 추가하기 전에:
  묻는다: "이것이 test에서만 사용되는가?"

  그렇다면:
    멈춘다. 추가하지 않는다.
    대신 test utility에 둔다.

  묻는다: "이 class가 이 resource의 lifecycle을 소유하는가?"

  아니라면:
    멈춘다. 이 method를 둘 class가 아니다.
```

## 안티패턴 3: 이해 없이 Mock하기

**위반:**

```typescript
// ❌ 나쁨: mock이 test logic을 깨뜨림
test('detects duplicate server', () => {
  // mock이 test가 의존하는 config write를 막음!
  vi.mock('ToolCatalog', () => ({
    discoverAndCacheTools: vi.fn().mockResolvedValue(undefined)
  }));

  await addServer(config);
  await addServer(config);  // throw해야 하지만 그러지 않음!
});
```

**왜 틀렸는가:**

- mock된 method가 test가 의존하는 side effect(config write)를 갖고 있었다.
- "안전하게" 하려고 과도하게 mock하면 실제 동작을 깨뜨린다.
- test가 잘못된 이유로 통과하거나 수수께끼처럼 실패한다.

**수정:**

```typescript
// ✅ 좋음: 올바른 level에서 mock
test('detects duplicate server', () => {
  // 느린 부분만 mock하고 test에 필요한 동작은 보존
  vi.mock('MCPServerManager'); // 느린 server startup만 mock

  await addServer(config);  // Config written
  await addServer(config);  // Duplicate detected ✓
});
```

### 게이트 함수

```text
어떤 method든 mock하기 전에:
  멈춘다. 아직 mock하지 않는다.

  1. 묻는다: "실제 method에는 어떤 side effect가 있는가?"
  2. 묻는다: "이 test가 그 side effect 중 하나에 의존하는가?"
  3. 묻는다: "이 test에 무엇이 필요한지 완전히 이해했는가?"

  side effect에 의존한다면:
    더 낮은 수준에서 mock한다(실제로 느리거나 외부인 operation).
    또는 필요한 동작을 보존하는 test double을 사용한다.
    test가 의존하는 high-level method를 mock하지 않는다.

  test가 무엇에 의존하는지 확실하지 않다면:
    먼저 실제 구현으로 test를 실행한다.
    실제로 무엇이 일어나야 하는지 관찰한다.
    그 다음 올바른 수준에서 최소한으로 mock한다.

  위험 신호:
    - "안전하게 이걸 mock하자"
    - "느릴 수 있으니 mock하는 게 낫다"
    - dependency chain 이해 없이 mock
```

## 안티패턴 4: 불완전한 Mock

**위반:**

```typescript
// ❌ 나쁨: partial mock - 필요하다고 생각한 field만 포함
const mockResponse = {
  status: 'success',
  data: { userId: '123', name: 'Alice' }
  // 누락: downstream code가 사용하는 metadata
};

// 나중에 code가 response.metadata.requestId에 접근하면 깨짐
```

**왜 틀렸는가:**

- **부분 mock은 구조적 가정을 숨긴다.** 알고 있는 field만 mock했다.
- **downstream code가 포함하지 않은 field에 의존할 수 있다.** 조용히 실패한다.
- **테스트는 통과하지만 integration은 실패한다.** mock은 불완전하고 실제 API는 완전하다.
- **거짓 신뢰**를 준다. 테스트는 실제 동작에 대해 아무것도 증명하지 않는다.

**철칙:** 즉시 test가 사용하는 field만이 아니라, 현실에 존재하는 COMPLETE data structure를 mock한다.

**수정:**

```typescript
// ✅ 좋음: 실제 API 완전성을 반영
const mockResponse = {
  status: 'success',
  data: { userId: '123', name: 'Alice' },
  metadata: { requestId: 'req-789', timestamp: 1234567890 }
  // 실제 API가 반환하는 모든 field
};
```

### 게이트 함수

```text
mock response를 만들기 전에:
  확인: "실제 API response는 어떤 field를 포함하는가?"

  행동:
    1. docs/examples의 실제 API response 확인
    2. system이 downstream에서 소비할 수 있는 모든 field 포함
    3. mock이 실제 response schema와 완전히 일치하는지 검증

  중요:
    mock을 만들고 있다면 전체 구조를 이해해야 한다.
    partial mock은 누락 field에 code가 의존할 때 조용히 실패한다.

  확실하지 않다면: 문서화된 모든 field를 포함한다.
```

## 안티패턴 5: 나중 생각으로 붙이는 Integration Test

**위반:**

```text
✅ 구현 완료
❌ No tests written
❌ 테스트 작성 안 됨
"테스트 준비 완료"
```

**왜 틀렸는가:**

- 테스트는 구현의 일부이지 선택적 follow-up이 아니다.
- TDD라면 이 문제를 잡았을 것이다.
- 테스트 없이 완료를 주장할 수 없다.

**수정:**

```text
TDD cycle:
1. 실패하는 테스트 작성
2. 통과하도록 구현
3. Refactor
4. 그 다음 완료 주장
```

## Mock이 너무 복잡해질 때

**경고 신호:**

- mock setup이 test logic보다 김
- test를 통과시키려고 모든 것을 mock함
- mock에 실제 component가 가진 method가 빠짐
- mock이 바뀌면 test가 깨짐

**사람 파트너의 질문:** "여기서 mock을 써야 하나요?"

**고려:** 실제 component를 사용하는 integration test가 복잡한 mock보다 단순한 경우가 많다.

## TDD가 이런 안티패턴을 막는 이유

**TDD가 돕는 방식:**

1. **테스트를 먼저 작성** -> 실제로 무엇을 테스트하는지 생각하게 한다.
2. **실패를 확인** -> test가 mock이 아니라 실제 동작을 테스트한다는 것을 확인한다.
3. **최소 구현** -> test-only method가 스며들지 않는다.
4. **실제 dependency** -> mock하기 전에 test에 실제로 무엇이 필요한지 보게 된다.

**mock 동작을 테스트하고 있다면 TDD를 위반한 것이다.** 실제 코드를 대상으로 test 실패를 보기 전에 mock을 추가한 것이다.

## 빠른 참조

| 안티패턴 | 수정 |
| --- | --- |
| mock element에 assert | 실제 component를 테스트하거나 mock 해제 |
| production의 test-only method | test utility로 이동 |
| 이해 없이 mock | 먼저 dependency 이해, 최소 mock |
| 불완전한 mock | 실제 API를 완전히 반영 |
| 나중 생각으로 붙이는 test | TDD - test first |
| 과도하게 복잡한 mock | integration test 고려 |

## 위험 신호

- assertion이 `*-mock` test ID를 확인함
- test file에서만 호출되는 method
- mock setup이 test의 50% 초과
- mock을 제거하면 test 실패
- mock이 왜 필요한지 설명할 수 없음
- "안전하게" mock하기

## 결론

**Mock은 격리 도구이지 테스트 대상이 아니다.**

TDD 중 mock 동작을 테스트하고 있음을 발견했다면 잘못된 방향이다.

수정: 실제 동작을 테스트하거나 애초에 왜 mock하는지 질문한다.
