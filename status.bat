@echo off
REM Status script for Unifi MCP Server on Windows

echo Checking Unifi MCP Server status...

REM Check if the server is running locally
tasklist /fi "imagename eq python.exe" | findstr "python.exe" >nul
if %ERRORLEVEL% EQU 0 (
    echo Server might be running locally
    
    REM Get the process ID
    for /f "tokens=2" %%a in ('tasklist /fi "imagename eq python.exe" ^| findstr "python.exe"') do set pid=%%a
    echo Process ID: %pid%
    
    REM Check if port 8000 is in use
    netstat -ano | findstr ":8000" | findstr "LISTENING" >nul
    if %ERRORLEVEL% EQU 0 (
        echo Listening on port: 8000
        echo Server URL: http://localhost:8000
        
        REM Check if the API is responding
        curl --version >nul 2>&1
        if %ERRORLEVEL% EQU 0 (
            for /f %%a in ('curl -s -o nul -w "%%{http_code}" http://localhost:8000/docs') do set response=%%a
            if "!response!"=="200" (
                echo API is responding (HTTP 200 OK)
            ) else (
                echo API is not responding properly (HTTP !response!)
            )
        )
    ) else (
        echo Could not determine port
    )
) else (
    echo Server is not running locally
)

REM Check if the server is running in Docker
docker-compose --version >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    if exist docker-compose.yml (
        for /f %%a in ('docker-compose ps -q unifi-mcp-server 2^>nul') do set container_id=%%a
        if defined container_id (
            for /f %%a in ('docker inspect --format="{{.State.Status}}" %container_id% 2^>nul') do set container_status=%%a
            if "!container_status!"=="running" (
                echo Server is running in Docker
                echo Container ID: %container_id%
                echo Container Status: !container_status!
                
                REM Get the port mapping
                for /f %%a in ('docker port %container_id% 2^>nul ^| findstr "8000/tcp" ^| findstr /r "[0-9]*$"') do set port_mapping=%%a
                if defined port_mapping (
                    echo Port mapping: !port_mapping!
                    echo Server URL: http://localhost:!port_mapping!
                    
                    REM Check if the API is responding
                    curl --version >nul 2>&1
                    if %ERRORLEVEL% EQU 0 (
                        for /f %%a in ('curl -s -o nul -w "%%{http_code}" http://localhost:!port_mapping!/docs') do set response=%%a
                        if "!response!"=="200" (
                            echo API is responding (HTTP 200 OK)
                        ) else (
                            echo API is not responding properly (HTTP !response!)
                        )
                    )
                ) else (
                    echo Could not determine port mapping
                )
            ) else (
                echo Server container exists but is not running
                echo Container Status: !container_status!
            )
        ) else (
            echo Server is not running in Docker
        )
    )
)

REM Check Claude Desktop integration
python --version >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    if exist configure_claude.py (
        echo Checking Claude Desktop integration...
        
        REM Add --status option to configure_claude.py if it doesn't exist
        findstr /c:"def check_status" configure_claude.py >nul
        if %ERRORLEVEL% NEQ 0 (
            echo Adding status check to configure_claude.py...
            echo. >> configure_claude.py
            echo def check_status(config_path): >> configure_claude.py
            echo     """Check if the Unifi MCP server is configured in Claude Desktop""" >> configure_claude.py
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
            echo     if 'mcpServers' in config and 'unifi' in config['mcpServers']: >> configure_claude.py
            echo         print("Unifi MCP server is configured in Claude Desktop.") >> configure_claude.py
            echo         server_config = config['mcpServers']['unifi'] >> configure_claude.py
            echo         print(f"Command: {server_config.get('command', 'N/A')}") >> configure_claude.py
            echo         print(f"Args: {server_config.get('args', [])}") >> configure_claude.py
            echo         return True >> configure_claude.py
            echo     else: >> configure_claude.py
            echo         print("Unifi MCP server is NOT configured in Claude Desktop.") >> configure_claude.py
            echo         return False >> configure_claude.py
            echo. >> configure_claude.py
            echo if __name__ == "__main__": >> configure_claude.py
            echo     if len(sys.argv) ^> 1 and sys.argv[1] == "--status": >> configure_claude.py
            echo         config_path = find_claude_config() >> configure_claude.py
            echo         check_status(config_path) >> configure_claude.py
            echo         sys.exit(0) >> configure_claude.py
        )
        
        python configure_claude.py --status
    )
)

echo Status check complete.