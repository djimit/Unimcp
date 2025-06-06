@echo off
REM Start the Unifi MCP Server for Windows

REM Load environment variables from .env file if it exists
if exist .env (
    echo Loading environment variables from .env file
    for /f "tokens=*" %%a in (.env) do (
        set %%a
    )
)

REM Check if UNIFI_API_KEY is set
if "%UNIFI_API_KEY%"=="" (
    echo Error: UNIFI_API_KEY environment variable is not set
    echo Please set it in your .env file or set it manually
    exit /b 1
)

REM Check if Python virtual environment exists
if exist .venv (
    echo Activating Python virtual environment
    call .venv\Scripts\activate
) else (
    echo Warning: No virtual environment found (.venv directory missing)
    echo It's recommended to create a virtual environment:
    echo   python -m venv .venv
    echo   .venv\Scripts\activate
    echo   pip install -r requirements.txt
    echo.
    echo Continuing without virtual environment...
)

REM Start the server
echo Starting Unifi MCP Server...
python main.py