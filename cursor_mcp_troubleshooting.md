# Cursor IDE에서 GreeumMCP 로드 문제 해결 가이드

## 문제 진단

현재 `greeummcp` 명령어가 시스템 PATH에 없어서 Cursor가 MCP 서버를 시작할 수 없는 상황입니다.

## 해결 방법

### 방법 1: Python 직접 실행 (권장)

`.cursor/mcp.json` 파일을 다음과 같이 수정하세요:

```json
{
  "mcpServers": {
    "greeum_mcp": {
      "command": "python",
      "args": [
        "-m",
        "greeummcp.server",
        "--data-dir",
        "E:\\GreeumMCP\\data",
        "--transport",
        "stdio"
      ]
    }
  }
}
```

### 방법 2: 가상환경 사용

가상환경의 Python을 직접 지정:

```json
{
  "mcpServers": {
    "greeum_mcp": {
      "command": "E:\\GreeumMCP\\venv\\Scripts\\python.exe",
      "args": [
        "-m",
        "greeummcp.server",
        "--data-dir",
        "E:\\GreeumMCP\\data",
        "--transport",
        "stdio"
      ]
    }
  }
}
```

### 방법 3: 전역 설치

```bash
# 전역으로 GreeumMCP 설치
pip install greeummcp

# 또는 개발 버전 설치
cd E:\GreeumMCP
pip install -e .
```

그 후 원래 설정 사용:

```json
{
  "mcpServers": {
    "greeum_mcp": {
      "command": "greeummcp",
      "args": [
        "run",
        "--data-dir",
        "E:\\GreeumMCP\\data",
        "--transport",
        "stdio"
      ]
    }
  }
}
```

### 방법 4: 배치 파일 사용

`E:\GreeumMCP\run_mcp.bat` 파일 생성:

```batch
@echo off
cd /d E:\GreeumMCP
call venv\Scripts\activate
python -m greeummcp.server --data-dir E:\GreeumMCP\data --transport stdio
```

그 후 mcp.json 수정:

```json
{
  "mcpServers": {
    "greeum_mcp": {
      "command": "E:\\GreeumMCP\\run_mcp.bat"
    }
  }
}
```

## 추가 확인 사항

### 1. 데이터 디렉토리 생성
```powershell
mkdir E:\GreeumMCP\data
```

### 2. 의존성 확인
```powershell
cd E:\GreeumMCP
venv\Scripts\activate
pip install -r requirements.txt
```

### 3. 직접 테스트
```powershell
cd E:\GreeumMCP
venv\Scripts\python.exe -m greeummcp.server --data-dir E:\GreeumMCP\data --transport stdio
```

### 4. Cursor 재시작
- 설정을 변경한 후 반드시 Cursor를 완전히 종료하고 다시 시작하세요.
- Windows 작업 관리자에서 Cursor 관련 프로세스가 모두 종료되었는지 확인하세요.

## 디버깅

### MCP 로그 확인
1. Cursor의 Output 패널 열기 (View > Output)
2. 드롭다운에서 "MCP" 선택
3. 오류 메시지 확인

### 일반적인 오류 메시지
- `'greeummcp' is not recognized`: PATH 문제
- `ModuleNotFoundError: No module named 'greeummcp'`: 설치 문제
- `No module named 'greeum'`: 의존성 문제

## 테스트된 작동 설정

다음은 Windows에서 테스트된 설정입니다:

```json
{
  "mcpServers": {
    "greeum_mcp": {
      "command": "cmd",
      "args": [
        "/c",
        "cd /d E:\\GreeumMCP && venv\\Scripts\\python.exe -m greeummcp.server --data-dir E:\\GreeumMCP\\data --transport stdio"
      ]
    }
  }
}
``` 