# GreeumMCP 튜토리얼

이 튜토리얼에서는 GreeumMCP를 사용하여 Claude Desktop, Cursor IDE 등과 통합하는 방법을 단계별로 설명합니다.

## 목차

1. [시작하기](#시작하기)
2. [Claude Desktop과 함께 사용하기](#claude-desktop과-함께-사용하기)
3. [Cursor IDE와 통합하기](#cursor-ide와-통합하기)
4. [MCP 도구 사용하기](#mcp-도구-사용하기)
5. [Python API 활용](#python-api-활용)
6. [고급 설정](#고급-설정)

## 시작하기

### 설치 및 실행

```bash
# 설치
pip install greeummcp

# 실행 (기본 설정)
greeummcp

# 커스텀 데이터 디렉토리
greeummcp ~/my-memories
```

### 첫 번째 메모리 저장

Claude Desktop이나 Cursor에서 GreeumMCP가 활성화되면 다음과 같이 사용할 수 있습니다:

```
"이것을 기억해줘: 프로젝트 X의 데드라인은 12월 15일이고, 주요 담당자는 김철수 과장이다."
```

GreeumMCP가 자동으로 이 정보를 장기 메모리에 저장합니다.

## Claude Desktop과 함께 사용하기

### 1. 설정 파일 생성

가장 간단한 설정:

```json
{
  "mcpServers": {
    "greeum_mcp": {
      "command": "greeummcp"
    }
  }
}
```

커스텀 데이터 디렉토리 사용:

```json
{
  "mcpServers": {
    "greeum_mcp": {
      "command": "greeummcp",
      "args": ["/path/to/memories"]
    }
  }
}
```

### 2. Claude Desktop에서 사용 예시

#### 메모리 저장
```
나: "새로운 프로젝트 아이디어를 기억해줘: AI 기반 코드 리뷰 도구를 개발하자. 
    주요 기능은 자동 버그 탐지, 코드 스타일 검사, 성능 최적화 제안이다."

Claude: add_memory 도구를 사용하여 프로젝트 아이디어를 저장했습니다.
```

#### 메모리 검색
```
나: "내가 저장한 프로젝트 아이디어들을 보여줘"

Claude: query_memory 도구로 검색한 결과, 다음 프로젝트 아이디어들을 찾았습니다:
1. AI 기반 코드 리뷰 도구 - 자동 버그 탐지, 코드 스타일 검사, 성능 최적화
2. ...
```

#### 시간 기반 검색
```
나: "어제 논의한 내용이 뭐였지?"

Claude: search_time 도구로 어제의 기록을 검색한 결과:
- 클라이언트 미팅에서 UI 개선 요청
- 데이터베이스 스키마 변경 계획
- ...
```

## Cursor IDE와 통합하기

### 1. 프로젝트별 설정

`.cursor/mcp.json` 파일 생성:

```json
{
  "greeum_mcp": {
    "command": "greeummcp",
    "args": ["${workspaceFolder}/memories"]
  }
}
```

### 2. 개발 중 활용 예시

#### 코드 관련 메모 저장
```
"TODO 기억: UserService 클래스의 인증 로직을 리팩토링해야 함. 
현재 코드가 너무 복잡하고 테스트하기 어려움."
```

#### 버그 추적
```
"버그 발견: 사용자가 로그아웃 후 다시 로그인하면 세션이 제대로 초기화되지 않음. 
재현 조건: Chrome 브라우저, 쿠키 활성화 상태"
```

#### 진행 상황 기록
```
"진행 상황: 인증 모듈 구현 완료 (80%), 
남은 작업: OAuth2 통합, 테스트 케이스 작성"
```

## MCP 도구 사용하기

### 메모리 관리 도구

#### add_memory - 장기 메모리 추가
```python
# MCP 도구로 호출되는 예시
result = add_memory(
    content="중요한 회의 결정사항: 프로젝트 범위를 모바일 앱으로 확장",
    keywords=["회의", "결정", "모바일"],
    tags=["important", "project-scope"],
    importance=0.9
)
```

#### query_memory - 의미 기반 검색
```python
# 관련된 메모리 찾기
results = query_memory(
    query="모바일 앱 개발 관련 결정사항",
    limit=5
)
```

#### search_time - 시간 기반 검색
```python
# 특정 시간대의 메모리 검색
results = search_time(
    query="지난주 회의",
    language="ko"
)
```

### 단기 메모리 도구

#### add_stm - 임시 정보 저장
```python
# 짧은 시간 동안만 기억할 정보
stm_id = add_stm(
    content="임시 비밀번호: temp123!@#",
    ttl_type="short"  # 1시간 후 자동 삭제
)
```

#### get_stm_memories - 단기 메모리 조회
```python
# 현재 활성화된 단기 메모리들
active_memories = get_stm_memories(limit=10)
```

### 유틸리티 도구

#### generate_prompt - 메모리 기반 프롬프트 생성
```python
# 관련 메모리를 포함한 프롬프트 생성
enhanced_prompt = generate_prompt(
    user_input="프로젝트 진행 상황 요약해줘",
    max_blocks=5,
    max_stm=3
)
```

## Python API 활용

### 직접 서버 실행

```python
from greeummcp import run_server

# 커스텀 설정으로 서버 실행
run_server(
    data_dir="./project_memories",
    transport="stdio",
    greeum_config={
        "ttl_short": 3600,      # 1시간
        "ttl_medium": 86400,    # 1일
        "ttl_long": 604800,     # 1주일
        "cache_capacity": 20,    # 캐시 크기
        "default_language": "ko" # 기본 언어
    }
)
```

### 프로그래밍 방식으로 통합

```python
from greeummcp.server import GreeumMCPServer
from greeummcp.adapters.greeum_adapter import GreeumAdapter

# 서버 인스턴스 생성
server = GreeumMCPServer(
    data_dir="./memories",
    transport="stdio"
)

# 어댑터를 통한 직접 접근
adapter = server.adapter

# 메모리 추가
block = adapter.block_manager.add_block(
    context="프로그래밍 방식으로 추가한 메모리",
    keywords=["test", "api"],
    importance=0.7
)

# 메모리 검색
results = adapter.block_manager.search_blocks_by_keyword(
    keywords=["test"],
    limit=5
)
```

## 고급 설정

### 1. 메모리 보존 정책

```python
# 중요도에 따른 자동 정리
greeum_config = {
    "auto_cleanup": True,
    "cleanup_threshold": 0.3,  # 중요도 0.3 미만 자동 삭제
    "max_blocks": 10000        # 최대 블록 수
}
```

### 2. 다국어 설정

```python
# 자동 언어 감지 및 처리
greeum_config = {
    "default_language": "auto",
    "supported_languages": ["ko", "en", "ja", "zh"]
}
```

### 3. 임베딩 모델 커스터마이징

```python
# 외부 임베딩 모델 사용
greeum_config = {
    "embedding_model": "custom",
    "embedding_endpoint": "http://localhost:8080/embed"
}
```

### 4. 보안 설정

```python
# 데이터 암호화 (향후 지원 예정)
greeum_config = {
    "encryption": True,
    "encryption_key": "your-secret-key"
}
```

## 실전 시나리오

### 1. 프로젝트 관리
```
"프로젝트 마일스톤 기록: 
- Phase 1 (완료): 기본 아키텍처 설계
- Phase 2 (진행중): 핵심 기능 구현
- Phase 3 (예정): 테스트 및 최적화"
```

### 2. 학습 노트
```
"오늘 배운 것: React hooks의 useCallback은 함수를 메모이제이션하여 
불필요한 리렌더링을 방지한다. useMemo와 비슷하지만 함수에 특화됨."
```

### 3. 아이디어 수집
```
"아이디어: 음성 인식을 추가하여 회의 중 자동으로 중요한 내용을 
GreeumMCP에 저장하는 기능을 만들면 어떨까?"
```

### 4. 디버깅 기록
```
"디버그: API 호출 시 간헐적으로 timeout 발생. 
원인: 데이터베이스 연결 풀 고갈. 
해결: 연결 풀 크기를 10에서 50으로 증가."
```

## 문제 해결

### 메모리가 저장되지 않을 때
1. 데이터 디렉토리 권한 확인
2. 디스크 공간 확인
3. 로그 확인: `~/.greeummcp/logs/`

### 검색 결과가 부정확할 때
1. 키워드를 더 구체적으로 지정
2. 시간 범위를 좁혀서 검색
3. 중요도가 너무 낮게 설정되지 않았는지 확인

### 성능 이슈
1. 캐시 크기 증가: `cache_capacity: 50`
2. 오래된 메모리 정리: `cleanup_expired_memories()`
3. 인덱스 재구축 (향후 지원 예정)

## 다음 단계

- [API 레퍼런스](api-reference.md)에서 모든 도구의 상세 사양 확인
- [예제 코드](../examples/)에서 실제 구현 예시 학습
- [GitHub 이슈](https://github.com/GreeumAI/GreeumMCP/issues)에서 기능 요청 및 버그 리포트