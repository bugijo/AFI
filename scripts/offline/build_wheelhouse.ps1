# Script para criar wheelhouse com dependências offline
# Para uso em ambientes sem internet

Write-Host "=== AFI - Build Wheelhouse para Instalação Offline ===" -ForegroundColor Green

# Criar diretório wheels se não existir
if (!(Test-Path "wheels")) {
    New-Item -ItemType Directory -Name "wheels"
    Write-Host "Diretório 'wheels' criado." -ForegroundColor Yellow
}

# Baixar todas as dependências
Write-Host "Baixando dependências do requirements.txt..." -ForegroundColor Cyan
pip download -r requirements.txt -d wheels

# Criar arquivo zip com as wheels
Write-Host "Criando wheels.zip..." -ForegroundColor Cyan
Compress-Archive -Path "wheels\*" -DestinationPath "wheels.zip" -Force

Write-Host "=== Wheelhouse criado com sucesso! ===" -ForegroundColor Green
Write-Host "Arquivo: wheels.zip" -ForegroundColor Yellow
Write-Host "Para instalar offline: pip install --no-index --find-links wheels -r requirements.txt" -ForegroundColor Cyan