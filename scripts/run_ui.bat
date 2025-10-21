@echo off
setlocal enabledelayedexpansion

set ROOT_DIR=%~dp0..

if exist "%ROOT_DIR%\.env" (
  for /f "usebackq tokens=1,* delims==" %%A in ("%ROOT_DIR%\.env") do (
    if not "%%A"=="" (
      set "%%A=%%B"
    )
  )
)

if "%AFI_PORT%"=="" set "AFI_PORT=8507"
set "PYTHONPATH=%ROOT_DIR%;%PYTHONPATH%"

where streamlit >nul 2>nul
if %errorlevel%==0 (
  streamlit run "%ROOT_DIR%\app.py" --server.port %AFI_PORT% --server.headless true
) else (
  echo Streamlit nao encontrado. Executando UI fallback.
  py "%ROOT_DIR%\ui_fallback\ui_fallback_server.py" --port %AFI_PORT%
)

endlocal
