# GreeumMCP 테스트 및 사용 가이드

## 1. 패키지 설치

```bash
# 가상환경 생성 및 활성화
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate

# 패키지 설치
pip install -e .
```

## 2. MCP 서버 실행

### 직접 실행
```bash
# stdio transport (기본)
greeummcp run --data-dir ./data --transport stdio

# HTTP transport
greeummcp run --data-dir ./data --transport http --port 8000

# 또는 Python 모듈로 실행
python -m greeummcp.server --data-dir ./data --transport stdio
```

### 사용 가능한 명령어
```bash
# 버전 확인
greeummcp version

# 사용 가능한 도구 목록 확인
greeummcp list-tools --data-dir ./data
```

## 3. Claude Desktop 연동

### 자동 설정
```bash
# Claude Desktop 설정 파일 생성
python examples/claude_desktop.py --create --data-dir ./data

# 설정 확인
python examples/claude_desktop.py --check
```

### 수동 설정
Claude Desktop 설정 파일 위치:
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Linux: `~/.config/Claude/claude_desktop_config.json`

설정 파일 내용:
```json
{
    "mcpServers": {
        "greeum_mcp": {
            "command": "greeummcp",
            "args": [
                "run",
                "--data-dir", "C:\\Users\\USERNAME\\greeum-data",
                "--transport", "stdio"
            ]
        }
    }
}
```

## 4. Cursor IDE 연동

프로젝트 루트에 `.cursor/mcp.json` 파일 생성:
```json
{
  "greeum_mcp": {
    "command": "greeummcp",
    "args": [
      "run",
      "--data-dir", "${workspaceFolder}/data",
      "--transport", "stdio"
    ]
  }
}
```

## 5. 다른 MCP 호스트에서 사용하기

### HTTP Transport 사용
```bash
# 서버 실행
greeummcp run --data-dir ./data --transport http --port 8000

# MCP 클라이언트에서 연결
# URL: http://localhost:8000
```

### WebSocket Transport 사용
```bash
# 서버 실행
greeummcp run --data-dir ./data --transport websocket --port 8000

# MCP 클라이언트에서 연결
# URL: ws://localhost:8000
```

### Python 라이브러리로 사용
```python
from greeummcp import run_server

# 기본 설정으로 실행
run_server()

# 사용자 정의 설정
run_server(
    data_dir="./data",
    server_name="greeum_mcp",
    port=8000,
    transport="http",
    greeum_config={
        "ttl_short": 3600,  # 1시간
        "ttl_medium": 86400,  # 1일
        "ttl_long": 604800,  # 1주일
        "default_language": "auto"
    }
)
```

## 6. CLI 예제 실행

대화형 CLI로 메모리 기능 테스트:
```bash
python examples/cli_example.py --data-dir ./data
```

사용 예:
```
greeum> add 첫 번째 메모리입니다
Memory added with ID: 1

greeum> add Python에 대한 두 번째 메모리입니다
Memory added with ID: 2

greeum> search Python
Found 1 results:

--- Result 1 ---
ID: 2
Content: Python에 대한 두 번째 메모리입니다
Timestamp: 2023-07-01T12:34:56
Keywords: Python, 메모리, 두 번째
Importance: 0.65
```

## 7. 검증

1. Claude Desktop에서 🔨 아이콘을 클릭하여 도구 목록에 greeum_mcp가 표시되는지 확인
2. 메모리 추가 테스트: "이 정보를 저장해줘: Python은 귀도 반 로섬이 개발했습니다"
3. 메모리 검색 테스트: "Python에 대해 어떤 정보를 가지고 있니?"

## 주의사항

- 서버 이름에는 언더스코어(`_`)를 사용하고 하이픈(`-`)은 피하세요
- 데이터 디렉토리는 절대 경로를 사용하는 것이 안정적입니다
- Claude Desktop을 재시작해야 설정이 적용됩니다 