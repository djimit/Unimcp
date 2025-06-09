@echo off
REM Setup script for Unifi MCP Server on Windows

echo Setting up Unifi MCP Server...

REM Check if Python is installed
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Error: Python is not installed or not in PATH
    exit /b 1
)

REM Create virtual environment
echo Creating virtual environment...
if not exist .venv (
    python -m venv .venv
)

REM Activate virtual environment
call .venv\Scripts\activate

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Check if .env file exists
if not exist .env (
    echo Creating .env file from .env.example...
    if exist .env.example (
        copy .env.example .env
        echo Please edit .env file and set your UNIFI_API_KEY
    ) else (
        echo Error: .env.example file not found
        exit /b 1
    )
)

echo Setup complete!
echo.
echo Next steps:
echo 1. Edit .env file and set your UNIFI_API_KEY
echo 2. Run start_server.bat to start the server
echo 3. Run python configure_claude.py to configure Claude Desktop
echo.
echo For Docker users:
echo 1. Edit .env file and set your UNIFI_API_KEY
echo 2. Install Docker Desktop for Windows
echo 3. Run docker-compose up --build
