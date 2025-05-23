# GreeumMCP 기반 명세서

## 1. 프로젝트 개요

GreeumMCP는 Greeum 기억 엔진을 MCP(Model Context Protocol) 표준에 맞게 래핑하여 LLM과 외부 도구 간의 통합을 제공하는 독립적인 패키지입니다. 이 프로젝트는 Greeum 코어 패키지를 의존성으로 사용하면서 MCP 호환 엔드포인트를 제공합니다.

## 2. 프로젝트 구조

```
GreeumMCP/
├── greeummcp/                   # 메인 패키지
│   ├── __init__.py              # 패키지 초기화
│   ├── server.py                # MCP 서버 구현
│   ├── tools/                   # MCP 도구 구현
│   │   ├── __init__.py          
│   │   ├── memory_tools.py      # 기억 관리 도구
│   │   └── utility_tools.py     # 유틸리티 도구
│   ├── resources/               # MCP 리소스 구현
│   │   ├── __init__.py
│   │   └── memory_resources.py  # 기억 리소스
│   ├── prompts/                 # MCP 프롬프트 구현
│   │   ├── __init__.py
│   │   └── memory_prompts.py    # 기억 기반 프롬프트
│   └── adapters/                # Greeum 통합 어댑터
│       ├── __init__.py
│       └── greeum_adapter.py    # Greeum 기능 어댑터
├── examples/                    # 사용 예제
│   ├── cli_example.py           # CLI 예제
│   └── claude_desktop.py        # Claude Desktop 연동 예제
├── tests/                       # 테스트
│   ├── __init__.py
│   ├── test_server.py
│   └── test_tools.py
├── README.md                    # 프로젝트 설명
├── CONTRIBUTING.md              # 기여 가이드라인
├── setup.py                     # 패키지 설정
└── requirements.txt             # 의존성 정의
```

## 3. 의존성

```
greeum>=0.5.2      # Greeum 코어 패키지
mcp-python>=1.0.0  # MCP Python SDK
fastapi>=0.100.0   # API 서버 (HTTP 전송용)
pydantic>=2.0.0    # 데이터 검증
uvicorn>=0.15.0    # ASGI 서버
typer>=0.9.0       # CLI 인터페이스
```

## 4. MCP 도구 설계

### 4.1 기억 관리 도구

| 도구 이름 | 설명 | 파라미터 | 반환 값 |
|---------|-----|---------|--------|
| `add-memory` | 새로운 기억 추가 | `content`: 기억 내용<br>`importance`: 중요도(선택) | 기억 ID |
| `query-memory` | 기억 검색 | `query`: 검색 쿼리<br>`limit`: 결과 제한(선택) | 기억 목록 |
| `retrieve-memory` | 특정 기억 조회 | `memory_id`: 기억 ID | 기억 내용 |
| `update-memory` | 기억 업데이트 | `memory_id`: 기억 ID<br>`content`: 새 내용 | 성공 여부 |
| `delete-memory` | 기억 삭제 | `memory_id`: 기억 ID | 성공 여부 |
| `search-time` | 시간 기반 기억 검색 | `time_query`: 시간 표현<br>`language`: 언어(선택) | 기억 목록 |

### 4.2 유틸리티 도구

| 도구 이름 | 설명 | 파라미터 | 반환 값 |
|---------|-----|---------|--------|
| `generate-prompt` | 기억 기반 프롬프트 생성 | `user_input`: 사용자 입력 | 완성된 프롬프트 |
| `extract-keywords` | 텍스트에서 키워드 추출 | `text`: 입력 텍스트<br>`language`: 언어(선택) | 키워드 목록 |
| `verify-chain` | 기억 블록체인 무결성 검증 | 없음 | 검증 결과 |
| `server-status` | 서버 상태 확인 | 없음 | 상태 정보 |

## 5. MCP 리소스 설계

| 리소스 타입 | 설명 | 속성 |
|-----------|-----|-----|
| `memory-block` | 기억 블록 객체 | `id`, `content`, `timestamp`, `keywords`, `importance` |
| `memory-chain` | 전체 기억 블록체인 | `blocks`, `count`, `last_block_id` |
| `stm-list` | 단기 기억 목록 | `memories`, `count` |
| `server-config` | 서버 구성 정보 | `settings`, `version`, `uptime` |

## 6. MCP 프롬프트 설계

| 프롬프트 이름 | 설명 | 변수 |
|------------|-----|-----|
| `memory-context` | 기억을 포함한 LLM 컨텍스트 | `user_input`, `related_memories` |
| `time-based-recall` | 시간 기반 기억 회상 | `time_reference`, `contextual_prompt` |
| `memory-organization` | 기억 조직화 및 요약 | `memory_subset`, `organization_goal` |

## 7. 인터페이스 명세

### 7.1 서버 초기화

```python
from greeummcp import MCPServer

# 기본 설정으로 서버 초기화
server = MCPServer()

# 또는 상세 설정으로 초기화
server = MCPServer(
    data_dir="./data",
    port=8000,
    transport="stdio",  # 'stdio', 'http', 'websocket' 중 선택
    greeum_config={"stm_ttl": 3600}
)

# 서버 시작
server.run()
```

### 7.2 구성 파일 형식 (mcp.json)

```json
{
  "greeum": {
    "command": "python",
    "args": ["-m", "greeummcp.server"]
  }
}
```

### 7.3 CLI 인터페이스

```bash
# 기본 설정으로 서버 시작
greeummcp run

# 전송 방식 지정
greeummcp run --transport stdio

# 포트 및 데이터 디렉토리 지정
greeummcp run --port 8000 --data-dir ./data

# 도구 목록 출력
greeummcp list-tools
```

## 8. Greeum 통합 방식

GreeumMCP는 Greeum 패키지를 직접 임포트하여 다음과 같은 방식으로 통합합니다:

1. **어댑터 패턴**: Greeum 컴포넌트는 MCP와 직접 상호작용하지 않고 어댑터를 통해 통신
2. **프록시 메소드**: MCP 도구는 해당 Greeum 메소드의 프록시 역할
3. **데이터 변환**: Greeum의 데이터 구조를 MCP 호환 형식으로 변환

## 9. 배포 계획

1. **PyPI 패키지**: `greeummcp` 패키지로 배포
2. **Docker 이미지**: `greeummcp:latest` 및 버전별 태그 제공
3. **바이너리 배포**: Windows, macOS, Linux용 실행 파일 제공

## 10. 구현 우선순위

1. 기본 MCP 서버 구현
2. 핵심 메모리 관리 도구 구현
3. HTTP 전송 방식 구현
4. stdio 전송 방식 구현
5. 유틸리티 도구 구현
6. 리소스 및 프롬프트 구현

이 명세서를 기반으로 GreeumMCP 개발을 시작할 수 있습니다. 첫 단계로는 기본 프로젝트 구조를 설정하고 `greeum` 패키지를 임포트하여 가장 기본적인 MCP 서버를 구현하는 것이 좋겠습니다.
