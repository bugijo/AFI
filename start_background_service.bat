@echo off
echo.
echo ========================================
echo   AFI v4.0 - Background Service
echo ========================================
echo.
echo 🔍 Iniciando serviço de monitoramento...
echo.

REM Verificar se Python está disponível
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python não encontrado! Tentando 'py'...
    py --version >nul 2>&1
    if errorlevel 1 (
        echo ❌ Python não está instalado ou não está no PATH!
        pause
        exit /b 1
    ) else (
        set PYTHON_CMD=py
    )
) else (
    set PYTHON_CMD=python
)

echo ✅ Python encontrado: %PYTHON_CMD%
echo.

REM Verificar se o arquivo background_service.py existe
if not exist "background_service.py" (
    echo ❌ Arquivo background_service.py não encontrado!
    echo    Certifique-se de estar na pasta correta do AFI.
    pause
    exit /b 1
)

echo 📁 Arquivo background_service.py encontrado
echo.

REM Mostrar opções
echo Escolha uma opção:
echo.
echo 1. Iniciar serviço (uma vez)
echo 2. Executar serviço continuamente
echo 3. Verificar status
echo 4. Parar serviço
echo 5. Adicionar pasta para monitoramento
echo 6. Sair
echo.

set /p choice="Digite sua escolha (1-6): "

if "%choice%"=="1" (
    echo.
    echo 🚀 Iniciando serviço...
    %PYTHON_CMD% background_service.py --start
    pause
) else if "%choice%"=="2" (
    echo.
    echo 🔄 Executando serviço continuamente...
    echo    Pressione Ctrl+C para parar
    echo.
    %PYTHON_CMD% background_service.py --run
    pause
) else if "%choice%"=="3" (
    echo.
    echo 📊 Verificando status...
    %PYTHON_CMD% background_service.py --status
    pause
) else if "%choice%"=="4" (
    echo.
    echo 🛑 Parando serviço...
    %PYTHON_CMD% background_service.py --stop
    pause
) else if "%choice%"=="5" (
    echo.
    set /p folder_path="Digite o caminho da pasta para monitorar: "
    echo.
    echo 📁 Adicionando pasta: !folder_path!
    %PYTHON_CMD% background_service.py --add-folder "!folder_path!"
    pause
) else if "%choice%"=="6" (
    echo.
    echo 👋 Saindo...
    exit /b 0
) else (
    echo.
    echo ❌ Opção inválida!
    pause
    goto :eof
)

echo.
echo ✅ Operação concluída!
pause