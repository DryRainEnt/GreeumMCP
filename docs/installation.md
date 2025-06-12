# GreeumMCP 설치 가이드

GreeumMCP는 Greeum Memory Engine을 MCP(Model Context Protocol) 서버로 제공하여 Claude Desktop, Cursor IDE 등과 통합할 수 있게 해주는 패키지입니다.

## 필수 요구사항

- Python 3.10 이상
- pip (Python 패키지 관리자)

## 설치 방법

### 1. PyPI에서 설치 (권장)

```bash
# GreeumMCP 설치
pip install greeummcp

# 개발 도구 포함 설치
pip install "greeummcp[dev]"
```

### 2. 소스 코드에서 설치

```bash
git clone https://github.com/GreeumAI/GreeumMCP.git
cd GreeumMCP

# 개발 모드로 설치
pip install -e .

# 또는 개발 도구 포함
pip install -e ".[dev]"
```

### 3. 가상 환경 사용 (권장)

<details>
<summary>Windows</summary>

```powershell
# 가상 환경 생성
python -m venv venv

# 가상 환경 활성화
.\venv\Scripts\Activate.ps1

# GreeumMCP 설치
pip install greeummcp
```
</details>

<details>
<summary>macOS / Linux</summary>

```bash
# 가상 환경 생성
python3 -m venv venv

# 가상 환경 활성화
source venv/bin/activate

# GreeumMCP 설치
pip install greeummcp
```
</details>

## 설치 확인

```bash
# 버전 확인
greeummcp version

# 사용 가능한 도구 목록 확인
greeummcp list-tools
```

## 빠른 시작

### 1. 기본 실행

```bash
# 기본 설정으로 실행 (stdio transport, ./data 디렉토리)
greeummcp

# 커스텀 데이터 디렉토리 지정
greeummcp /path/to/data

# HTTP transport 사용
greeummcp --transport http --port 8000
```

### 2. Claude Desktop 통합

<details>
<summary>Windows</summary>

`%APPDATA%\Claude\claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "greeum_mcp": {
      "command": "greeummcp.exe",
      "args": ["C:\\Users\\USERNAME\\greeum-data"]
    }
  }
}
```

기본 설정 사용 시:
```json
{
  "mcpServers": {
    "greeum_mcp": {
      "command": "greeummcp.exe"
    }
  }
}
```
</details>

<details>
<summary>macOS</summary>

`~/Library/Application Support/Claude/claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "greeum_mcp": {
      "command": "greeummcp",
      "args": ["/Users/username/greeum-data"]
    }
  }
}
```
</details>

<details>
<summary>Linux</summary>

`~/.config/Claude/claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "greeum_mcp": {
      "command": "greeummcp",
      "args": ["/home/username/greeum-data"]
    }
  }
}
```
</details>

### 3. Cursor IDE 통합

프로젝트 루트에 `.cursor/mcp.json` 생성:
```json
{
  "greeum_mcp": {
    "command": "greeummcp",
    "args": ["${workspaceFolder}/data"]
  }
}
```

## 고급 설정

### 환경 변수

```bash
# 데이터 디렉토리 설정
export GREEUM_DATA_DIR=/path/to/data

# 로그 레벨 설정
export GREEUM_LOG_LEVEL=INFO
```

### Python API 사용

```python
from greeummcp import run_server

# 기본 설정으로 실행
run_server()

# 커스텀 설정
run_server(
    data_dir="./data",
    transport="http",
    port=8000,
    greeum_config={
        "ttl_short": 3600,     # 1시간
        "ttl_medium": 86400,   # 1일
        "ttl_long": 604800,    # 1주일
        "default_language": "auto"
    }
)
```

## 다음 단계

- [API 레퍼런스](api-reference.md)를 참조하여 MCP 도구들의 상세 기능을 알아보세요.
- [튜토리얼](tutorials.md)을 통해 GreeumMCP의 기본 사용법을 배워보세요.
- [예제 코드](../examples/)에서 실제 사용 방법을 확인하세요.

## 문제 해결

### ImportError: No module named 'greeum'

```bash
# Greeum 패키지가 설치되지 않은 경우
pip install greeum>=0.6.1

# 또는 GreeumMCP를 재설치
pip install --upgrade greeummcp
```

### Command not found: greeummcp

```bash
# PATH에 추가되지 않은 경우
python -m greeummcp.server

# 또는 가상 환경 활성화 확인
which greeummcp
```

### 포트 충돌 (HTTP transport)

```bash
# 다른 포트 사용
greeummcp --transport http --port 8080
```

### 권한 오류

```bash
# 데이터 디렉토리 권한 확인
chmod -R 755 ./data

# 또는 다른 디렉토리 사용
greeummcp ~/greeum-data
```

## 지원

문제가 계속되면 [GitHub 이슈](https://github.com/GreeumAI/GreeumMCP/issues)에 보고해주세요.
