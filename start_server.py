#!/usr/bin/env python3
"""
Script de Inicialização Padronizado - AFI v3.0
Este script garante que o sistema sempre use a porta 8507
"""

import subprocess
import sys
import os
from config import get_streamlit_command, get_server_port, get_server_url

def verificar_dependencias():
    """Verifica se todas as dependências estão instaladas"""
    try:
        import streamlit
        import llama_index
        import sentence_transformers
        print("✅ Todas as dependências principais estão instaladas")
        return True
    except ImportError as e:
        print(f"❌ Dependência faltando: {e}")
        return False

def verificar_arquivos():
    """Verifica se os arquivos necessários existem"""
    arquivos_necessarios = ['app.py', 'core_logic.py', 'config.py']
    
    for arquivo in arquivos_necessarios:
        if not os.path.exists(arquivo):
            print(f"❌ Arquivo não encontrado: {arquivo}")
            return False
    
    print("✅ Todos os arquivos necessários estão presentes")
    return True

def criar_pastas():
    """Cria as pastas necessárias se não existirem"""
    pastas = ['memoria', 'storage']
    
    for pasta in pastas:
        if not os.path.exists(pasta):
            os.makedirs(pasta)
            print(f"📁 Pasta criada: {pasta}")
        else:
            print(f"📁 Pasta já existe: {pasta}")

def iniciar_servidor():
    """Inicia o servidor Streamlit na porta padrão"""
    print(f"\n🚀 Iniciando AFI v3.0 na porta {get_server_port()}...")
    print(f"🌐 URL: {get_server_url()}")
    print("=" * 50)
    
    comando = get_streamlit_command()
    print(f"Executando: {comando}")
    
    try:
        # Executar o comando
        subprocess.run(comando.split(), check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao iniciar o servidor: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n🛑 Servidor interrompido pelo usuário")
        sys.exit(0)

def main():
    """Função principal"""
    print("🏗️ AFI v3.0 - Assistente Finiti Inteligente")
    print("=" * 50)
    
    # Verificações pré-inicialização
    if not verificar_dependencias():
        print("❌ Instale as dependências antes de continuar")
        sys.exit(1)
    
    if not verificar_arquivos():
        print("❌ Arquivos necessários não encontrados")
        sys.exit(1)
    
    # Criar pastas necessárias
    criar_pastas()
    
    # Iniciar servidor
    iniciar_servidor()

if __name__ == "__main__":
    main()