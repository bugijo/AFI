#!/usr/bin/env python3
"""
Teste da nova assinatura do editor_video.py
"""

import subprocess
import sys
from pathlib import Path

def testar_editor_video():
    """
    Testa se o editor_video.py aceita a nova assinatura com frase_marketing
    """
    print("🧪 Teste da nova assinatura do editor_video.py")
    print("=" * 50)
    
    # Parâmetros de teste
    video_entrada = "temp_uploads/20251016_102923.mp4"  # Arquivo de exemplo
    musica = "Musicas/musica.mp3"  # Música de exemplo
    frase_marketing = "Teste da nova funcionalidade de texto em duas partes!"
    video_saida = "Videos_Editados/teste_output.mp4"
    
    # Verificar se os arquivos existem
    if not Path(video_entrada).exists():
        print(f"❌ Arquivo de vídeo não encontrado: {video_entrada}")
        return False
    
    if not Path(musica).exists():
        print(f"❌ Arquivo de música não encontrado: {musica}")
        return False
    
    print(f"📹 Vídeo: {video_entrada}")
    print(f"🎵 Música: {musica}")
    print(f"💬 Frase: {frase_marketing}")
    print(f"📁 Saída: {video_saida}")
    
    # Comando para testar
    comando = [
        sys.executable, "editor_video.py",
        video_entrada,
        musica,
        frase_marketing,
        video_saida
    ]
    
    print(f"\n🚀 Executando: {' '.join(comando)}")
    
    try:
        # Executar o comando
        resultado = subprocess.run(
            comando,
            capture_output=True,
            text=True,
            timeout=60  # Timeout de 1 minuto
        )
        
        print(f"\n📊 Código de saída: {resultado.returncode}")
        
        if resultado.stdout:
            print("📝 Saída padrão:")
            print(resultado.stdout)
        
        if resultado.stderr:
            print("⚠️ Saída de erro:")
            print(resultado.stderr)
        
        if resultado.returncode == 0:
            print("✅ Teste bem-sucedido!")
            return True
        else:
            print("❌ Teste falhou!")
            return False
            
    except subprocess.TimeoutExpired:
        print("⏰ Timeout - o processo demorou mais de 1 minuto")
        return False
    except Exception as e:
        print(f"💥 Erro durante execução: {e}")
        return False

if __name__ == "__main__":
    sucesso = testar_editor_video()
    if not sucesso:
        print("\n💡 Dica: Verifique se os arquivos de entrada existem e se o editor_video.py foi refatorado corretamente.")