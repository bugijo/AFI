@echo off
echo ========================================
echo    AFI v3.0 - Assistente Finiti Inteligente
echo    Porta Padrao: 8507
echo ========================================
echo.

REM Verificar se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Python nao encontrado!
    echo Instale o Python antes de continuar.
    pause
    exit /b 1
)

REM Verificar se py está disponível
py --version >nul 2>&1
if errorlevel 1 (
    echo Usando python...
    python start_server.py
) else (
    echo Usando py...
    py start_server.py
)

pause