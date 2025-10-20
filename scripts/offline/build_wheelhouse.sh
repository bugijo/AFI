#!/bin/bash
# Script para criar wheelhouse com dependências offline
# Para uso em ambientes sem internet

echo "=== AFI - Build Wheelhouse para Instalação Offline ==="

# Criar diretório wheels se não existir
if [ ! -d "wheels" ]; then
    mkdir wheels
    echo "Diretório 'wheels' criado."
fi

# Baixar todas as dependências
echo "Baixando dependências do requirements.txt..."
pip download -r requirements.txt -d wheels

# Criar arquivo zip com as wheels
echo "Criando wheels.zip..."
zip -r wheels.zip wheels/

echo "=== Wheelhouse criado com sucesso! ==="
echo "Arquivo: wheels.zip"
echo "Para instalar offline: pip install --no-index --find-links wheels -r requirements.txt"