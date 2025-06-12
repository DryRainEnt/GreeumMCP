@echo off
REM Get the directory where this batch file is located
set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%"

REM Check if Windows venv exists
IF NOT EXIST "venv-windows\Scripts\python.exe" (
    echo Creating Windows virtual environment...
    python -m venv venv-windows
    call venv-windows\Scripts\activate
    pip install -e .
    pip install -r requirements.txt
) ELSE (
    call venv-windows\Scripts\activate
)

REM Use relative path for data directory
python -m greeummcp.server --data-dir "%SCRIPT_DIR%data" --transport stdio 