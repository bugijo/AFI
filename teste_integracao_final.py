#!/usr/bin/env python3
"""
🧪 Teste de Integração Final - AML Video Editor
===============================================
Este script testa toda a cadeia de funcionalidades refatoradas:
1. Função de nomeação de arquivos
2. Editor de vídeo com nova assinatura
3. Guardião com chamada refatorada
"""

import os
import sys
import subprocess
from datetime import datetime

def testar_nomeacao():
    """Testa a função de nomeação de arquivos"""
    print("🔍 Testando função de nomeação...")
    try:
        from guardiao import gerar_nome_arquivo_agendado
        nome = gerar_nome_arquivo_agendado()
        print(f"✅ Nome gerado: {nome}")
        return True
    except Exception as e:
        print(f"❌ Erro na nomeação: {e}")
        return False

def testar_editor():
    """Testa o editor de vídeo com nova assinatura"""
    print("\n🎬 Testando editor de vídeo...")
    
    # Verificar arquivos necessários
    video_entrada = "temp_uploads/20251016_102923.mp4"
    musica = "Musicas/musica.mp3"
    video_saida = "Videos_Editados/teste_integracao_final.mp4"
    
    if not os.path.exists(video_entrada):
        print(f"❌ Arquivo de vídeo não encontrado: {video_entrada}")
        return False
    
    if not os.path.exists(musica):
        print(f"❌ Arquivo de música não encontrado: {musica}")
        return False
    
    # Executar editor
    frase_teste = "Integração Final Funcionando Perfeitamente!"
    cmd = [
        sys.executable, "editor_video.py",
        video_entrada, musica, frase_teste, video_saida
    ]
    
    print(f"🚀 Executando: {' '.join(cmd)}")
    
    try:
        resultado = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        
        if resultado.returncode == 0:
            print("✅ Editor executado com sucesso!")
            if os.path.exists(video_saida):
                print(f"✅ Vídeo gerado: {video_saida}")
                return True
            else:
                print("❌ Vídeo não foi gerado")
                return False
        else:
            print(f"❌ Editor falhou (código {resultado.returncode})")
            print(f"Erro: {resultado.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Timeout na execução do editor")
        return False
    except Exception as e:
        print(f"❌ Erro na execução: {e}")
        return False

def testar_guardiao():
    """Testa a função do guardião com nova assinatura"""
    print("\n🛡️ Testando função do guardião...")
    try:
        from guardiao import GuardiaoVideoHandler
        
        # Simular parâmetros
        video_entrada = "temp_uploads/20251016_102923.mp4"
        musica = "Musicas/musica.mp3"
        frase_marketing = "Teste do Guardião Refatorado!"
        video_saida = "Videos_Editados/teste_guardiao_final.mp4"
        
        if not os.path.exists(video_entrada):
            print(f"❌ Arquivo de vídeo não encontrado: {video_entrada}")
            return False
        
        if not os.path.exists(musica):
            print(f"❌ Arquivo de música não encontrado: {musica}")
            return False
        
        # Criar instância do guardião e chamar função refatorada
        guardiao = GuardiaoVideoHandler("Musicas", "Videos_Editados")
        sucesso = guardiao.chamar_editor_video(video_entrada, musica, frase_marketing, video_saida)
        
        if sucesso:
            print("✅ Guardião executado com sucesso!")
            if os.path.exists(video_saida):
                print(f"✅ Vídeo gerado pelo guardião: {video_saida}")
                return True
            else:
                print("❌ Vídeo não foi gerado pelo guardião")
                return False
        else:
            print("❌ Guardião retornou falha")
            return False
            
    except Exception as e:
        print(f"❌ Erro no guardião: {e}")
        return False

def main():
    """Executa todos os testes de integração"""
    print("🧪 TESTE DE INTEGRAÇÃO FINAL - AML VIDEO EDITOR")
    print("=" * 50)
    print(f"⏰ Iniciado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    resultados = []
    
    # Teste 1: Nomeação
    resultados.append(("Nomeação", testar_nomeacao()))
    
    # Teste 2: Editor
    resultados.append(("Editor", testar_editor()))
    
    # Teste 3: Guardião
    resultados.append(("Guardião", testar_guardiao()))
    
    # Resumo
    print("\n" + "=" * 50)
    print("📊 RESUMO DOS TESTES")
    print("=" * 50)
    
    sucessos = 0
    for nome, sucesso in resultados:
        status = "✅ PASSOU" if sucesso else "❌ FALHOU"
        print(f"{nome:15} {status}")
        if sucesso:
            sucessos += 1
    
    print(f"\n🎯 Resultado: {sucessos}/{len(resultados)} testes passaram")
    
    if sucessos == len(resultados):
        print("🎉 TODOS OS TESTES PASSARAM! Integração completa funcionando!")
        return True
    else:
        print("⚠️  Alguns testes falharam. Verifique os logs acima.")
        return False

if __name__ == "__main__":
    sucesso = main()
    sys.exit(0 if sucesso else 1)