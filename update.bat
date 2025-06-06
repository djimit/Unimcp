@echo off
REM Update script for Unifi MCP Server on Windows

echo Updating Unifi MCP Server...

REM Check if git is installed
git --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Error: git is not installed or not in PATH
    exit /b 1
)

REM Check if we're in a git repository
if not exist .git (
    echo Error: Not a git repository
    echo This script is intended to be run from a git repository
    exit /b 1
)

REM Save current branch
for /f "tokens=*" %%a in ('git symbolic-ref --short HEAD') do set current_branch=%%a

REM Fetch latest changes
echo Fetching latest changes...
git fetch

REM Check if there are any updates
for /f "tokens=*" %%a in ('git rev-parse HEAD') do set local_rev=%%a
for /f "tokens=*" %%a in ('git rev-parse origin/%current_branch%') do set remote_rev=%%a

if "%local_rev%" == "%remote_rev%" (
    echo Already up to date
    exit /b 0
)

REM Pull latest changes
echo Pulling latest changes...
git pull

REM Check if requirements.txt has changed
git diff --name-only HEAD@{1} HEAD | findstr "requirements.txt" >nul
if %ERRORLEVEL% EQU 0 (
    echo requirements.txt has changed, updating dependencies...
    
    REM Update dependencies
    call .venv\Scripts\activate
    pip install -r requirements.txt
)

echo Update complete!
echo.
echo You may need to restart the server for changes to take effect.