@echo off
setlocal

set ROOT_DIR=%~dp0..

if exist "%ROOT_DIR%\.env" (
  for /f "usebackq tokens=1,* delims==" %%A in ("%ROOT_DIR%\.env") do (
    if not "%%A"=="" (
      set "%%A=%%B"
    )
  )
)

set "PYTHONPATH=%ROOT_DIR%;%PYTHONPATH%"
py "%ROOT_DIR%\guardiao.py" %*

endlocal
