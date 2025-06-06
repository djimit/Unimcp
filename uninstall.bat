@echo off
REM Uninstall script for Unifi MCP Server on Windows

echo Uninstalling Unifi MCP Server...

REM Check if Claude Desktop is configured with this server
python --version >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo Checking Claude Desktop configuration...
    if exist configure_claude.py (
        REM Add --remove option to configure_claude.py if it doesn't exist
        findstr /c:"def remove_from_config" configure_claude.py >nul
        if %ERRORLEVEL% NEQ 0 (
            echo Adding remove option to configure_claude.py...
            echo. >> configure_claude.py
            echo def remove_from_config(config_path): >> configure_claude.py
            echo     """Remove the Unifi MCP server from Claude Desktop config""" >> configure_claude.py
            echo     if not config_path: >> configure_claude.py
            echo         print("Could not find Claude Desktop config file.") >> configure_claude.py
            echo         return False >> configure_claude.py
            echo. >> configure_claude.py
            echo     try: >> configure_claude.py
            echo         with open(config_path, 'r') as f: >> configure_claude.py
            echo             config = json.load(f) >> configure_claude.py
            echo     except (json.JSONDecodeError, FileNotFoundError): >> configure_claude.py
            echo         print("Could not read Claude Desktop config file.") >> configure_claude.py
            echo         return False >> configure_claude.py
            echo. >> configure_claude.py
            echo     # Remove the unifi server config if it exists >> configure_claude.py
            echo     if 'mcpServers' in config and 'unifi' in config['mcpServers']: >> configure_claude.py
            echo         del config['mcpServers']['unifi'] >> configure_claude.py
            echo         print("Removed Unifi MCP server from Claude Desktop config.") >> configure_claude.py
            echo. >> configure_claude.py
            echo         # Write the updated config >> configure_claude.py
            echo         try: >> configure_claude.py
            echo             with open(config_path, 'w') as f: >> configure_claude.py
            echo                 json.dump(config, f, indent=2) >> configure_claude.py
            echo             return True >> configure_claude.py
            echo         except Exception as e: >> configure_claude.py
            echo             print(f"Error writing config file: {e}") >> configure_claude.py
            echo             return False >> configure_claude.py
            echo     else: >> configure_claude.py
            echo         print("Unifi MCP server not found in Claude Desktop config.") >> configure_claude.py
            echo         return True >> configure_claude.py
            echo. >> configure_claude.py
            echo if __name__ == "__main__": >> configure_claude.py
            echo     import sys >> configure_claude.py
            echo     if len(sys.argv) ^> 1 and sys.argv[1] == "--remove": >> configure_claude.py
            echo         config_path = find_claude_config() >> configure_claude.py
            echo         if remove_from_config(config_path): >> configure_claude.py
            echo             print("Successfully removed from Claude Desktop config.") >> configure_claude.py
            echo             print("Please restart Claude Desktop to apply the changes.") >> configure_claude.py
            echo         else: >> configure_claude.py
            echo             print("Failed to remove from Claude Desktop config.") >> configure_claude.py
            echo             sys.exit(1) >> configure_claude.py
            echo         sys.exit(0) >> configure_claude.py
        )
        
        python configure_claude.py --remove
    )
)

REM Stop and remove Docker containers if they exist
docker-compose --version >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    if exist docker-compose.yml (
        echo Stopping and removing Docker containers...
        docker-compose down
    )
)

REM Ask for confirmation before removing files
echo.
echo This will remove all files in the current directory.
echo Are you sure you want to continue? (y/n)
set /p confirm=

if /i "%confirm%"=="y" (
    REM Remove virtual environment
    if exist .venv (
        echo Removing virtual environment...
        rmdir /s /q .venv
    )
    
    REM Create a temporary batch file to delete all files except this one
    echo @echo off > temp_delete.bat
    echo setlocal enabledelayedexpansion >> temp_delete.bat
    echo for %%F in (*) do ( >> temp_delete.bat
    echo   if not "%%F"=="uninstall.bat" if not "%%F"=="temp_delete.bat" del "%%F" >> temp_delete.bat
    echo ) >> temp_delete.bat
    echo for /d %%D in (*) do ( >> temp_delete.bat
    echo   rmdir /s /q "%%D" >> temp_delete.bat
    echo ) >> temp_delete.bat
    echo del temp_delete.bat >> temp_delete.bat
    
    echo Removing all files...
    call temp_delete.bat
    
    echo Uninstall complete!
    echo You can now delete this directory and the uninstall script.
) else (
    echo Uninstall cancelled.
)