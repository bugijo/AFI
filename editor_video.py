#!/usr/bin/env python3
"""
Editor de Vídeo para Stories de Redes Sociais
Script robusto para automatizar a edição de vídeos usando MoviePy
"""

import os
import sys
import random
from pathlib import Path
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.video.VideoClip import TextClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.audio.AudioClip import concatenate_audioclips

# Configurar ImageMagick para Windows
try:
    import moviepy.config as config
    imagemagick_path = r"C:\Program Files\ImageMagick-7.1.2-Q16-HDRI\magick.exe"
    if os.path.exists(imagemagick_path):
        config.change_settings({"IMAGEMAGICK_BINARY": imagemagick_path})
except Exception:
    pass  # Continua sem ImageMagick se houver erro

def verificar_dependencias():
    """Verifica se todas as dependências estão disponíveis"""
    try:
        import moviepy
        print(f"[OK] MoviePy {moviepy.__version__} detectado")
        return True
    except ImportError:
        print("[ERRO] MoviePy não está instalado ou configurado corretamente")
        print("[INFO] Execute: pip install moviepy==1.0.3")
        return False

def criar_pastas_necessarias():
    """Cria as pastas necessárias se não existirem"""
    pastas = [
        "Videos_Para_Editar",
        "Videos_Editados", 
        "Videos_Agendados",
        "Musicas",
        "Musicas/Instrumental",
        "Musicas/Energetica",
        "Musicas/Relaxante"
    ]
    
    for pasta in pastas:
        Path(pasta).mkdir(parents=True, exist_ok=True)
    
    print("[INFO] Estrutura de pastas verificada/criada")

def validar_arquivo(caminho, tipo="arquivo"):
    """Valida se um arquivo existe"""
    if not os.path.exists(caminho):
        print(f"[ERRO] Erro: {tipo} não encontrado: {caminho}")
        return False
    return True

def editar_video_story(caminho_video_original: str, caminho_musica: str, frase_marketing: str, caminho_saida: str):
    """
    Edita um vídeo especializado para stories de 10 segundos com texto em duas partes
    
    Args:
        caminho_video_original (str): Caminho para o vídeo original (já no formato correto)
        caminho_musica (str): Caminho para a música de fundo
        frase_marketing (str): Frase de marketing a ser dividida em duas partes
        caminho_saida (str): Caminho onde salvar o vídeo editado
    """
    
    print("[INFO] Iniciando edição especializada para vídeo de 10s...")
    
    # Validar arquivos de entrada
    if not validar_arquivo(caminho_video_original, "Vídeo"):
        return False
    if not validar_arquivo(caminho_musica, "Música"):
        return False
    
    try:
        # 1. Carregar o clipe de vídeo original (assumindo formato correto)
        print("[INFO] Carregando vídeo original...")
        video_clip = VideoFileClip(caminho_video_original)
        
        # 2. Remover o áudio original do clipe de vídeo
        print("[INFO] Removendo áudio original...")
        video_clip = video_clip.without_audio()
        
        # 3. Garantir que o vídeo tenha exatamente 10 segundos
        print("[INFO] Ajustando vídeo para 10 segundos...")
        if video_clip.duration > 10:
            video_clip = video_clip.subclipped(0, 10)
        
        # 4. Implementar seleção de trecho de música aleatório
        print("[INFO] Carregando música e selecionando trecho aleatório...")
        musica_clip = AudioFileClip(caminho_musica)
        duracao_musica = musica_clip.duration
        
        if duracao_musica > 10:
            # Calcular ponto de início aleatório
            inicio_aleatorio = random.uniform(0, duracao_musica - 10)
            print(f"[INFO] Selecionando trecho da música: {inicio_aleatorio:.2f}s a {inicio_aleatorio + 10:.2f}s")
            audio_clip = musica_clip.subclipped(inicio_aleatorio, inicio_aleatorio + 10)
        else:
            # Se a música for menor que 10s, usar toda ela
            audio_clip = musica_clip.subclipped(0, min(10, duracao_musica))
        
        # 5. Aplicar áudio ao vídeo
        print("[INFO] Aplicando música de fundo...")
        video_clip = video_clip.with_audio(audio_clip)
        
        # 6. Implementar texto em duas partes
        video_final = video_clip
        try:
            print("[INFO] Criando texto em duas partes...")
            
            # Dividir a frase em duas metades
            palavras = frase_marketing.split()
            meio = len(palavras) // 2
            parte1 = " ".join(palavras[:meio])
            parte2 = " ".join(palavras[meio:])
            
            print(f"[INFO] Parte 1 (1s-5s): {parte1}")
            print(f"[INFO] Parte 2 (5s-10s): {parte2}")
            
            # Criar primeiro clipe de texto (1s a 5s)
            texto_clip1 = TextClip(
                parte1,
                font_size=70,
                color='white',
                font='Arial-Bold',
                stroke_color='black',
                stroke_width=2
            ).with_start(1).with_duration(4).with_position('center')
            
            # Criar segundo clipe de texto (5s a 10s)
            texto_clip2 = TextClip(
                parte2,
                font_size=70,
                color='white',
                font='Arial-Bold',
                stroke_color='black',
                stroke_width=2
            ).with_start(5).with_duration(5).with_position('center')
            
            # Compor vídeo final com ambos os textos
            print("[INFO] Compondo vídeo final com texto em duas partes...")
            video_final = CompositeVideoClip([video_clip, texto_clip1, texto_clip2])
            
        except Exception as e:
            print(f"[AVISO] Não foi possível adicionar texto (ImageMagick não configurado): {e}")
            print("[INFO] Continuando sem texto sobreposto...")
            video_final = video_clip
        
        # Criar pasta de saída se não existir
        pasta_saida = os.path.dirname(caminho_saida)
        if pasta_saida:
            Path(pasta_saida).mkdir(parents=True, exist_ok=True)
        
        # 7. Salvar o vídeo final
        print("[INFO] Salvando vídeo final...")
        video_final.write_videofile(
            caminho_saida,
            codec='libx264',
            audio_codec='aac',
            logger=None
        )
        
        # Limpar recursos
        video_clip.close()
        musica_clip.close()
        audio_clip.close()
        if 'texto_clip1' in locals():
            texto_clip1.close()
        if 'texto_clip2' in locals():
            texto_clip2.close()
        video_final.close()
        
        print(f"[SUCESSO] Vídeo de 10s editado com sucesso! Salvo em: {caminho_saida}")
        return True
        
    except Exception as e:
        print(f"[ERRO] Erro durante a edição: {str(e)}")
        return False

def obter_info_video(caminho_video):
    """Obtém informações básicas sobre um vídeo"""
    try:
        clip = VideoFileClip(caminho_video)
        info = {
            'duracao': clip.duration,
            'fps': clip.fps,
            'tamanho': clip.size,
            'tem_audio': clip.audio is not None
        }
        clip.close()
        return info
    except Exception as e:
        print(f"[ERRO] Erro ao obter informações do vídeo: {e}")
        return None

def listar_videos(pasta_videos="Videos_Para_Editar"):
    """Lista vídeos disponíveis na pasta"""
    if not os.path.exists(pasta_videos):
        return []
    
    extensoes_video = ['.mp4', '.mov', '.avi', '.mkv']
    videos = []
    
    for arquivo in os.listdir(pasta_videos):
        if any(arquivo.lower().endswith(ext) for ext in extensoes_video):
            videos.append(arquivo)
    
    if videos:
        print(f"\n[INFO] Vídeos em {pasta_videos}:")
        for i, video in enumerate(videos, 1):
            print(f"  {i}. {video}")
    else:
        print(f"\n[INFO] Nenhum vídeo encontrado em {pasta_videos}")
    
    return videos

def listar_musicas(pasta_musicas="Musicas"):
    """Lista músicas disponíveis na pasta"""
    if not os.path.exists(pasta_musicas):
        return []
    
    extensoes_audio = ['.mp3', '.wav', '.m4a', '.aac']
    musicas = []
    
    for arquivo in os.listdir(pasta_musicas):
        if any(arquivo.lower().endswith(ext) for ext in extensoes_audio):
            musicas.append(arquivo)
    
    if musicas:
        print(f"\n[INFO] Músicas em {pasta_musicas}:")
        for i, musica in enumerate(musicas, 1):
            print(f"  {i}. {musica}")
    else:
        print(f"\n[INFO] Nenhuma música encontrada em {pasta_musicas}")
    
    return musicas

def listar_arquivos_disponiveis():
    """Lista vídeos e músicas disponíveis nas pastas"""
    print("\n📂 Arquivos disponíveis:")
    
    # Listar vídeos
    pasta_videos = "Videos_Para_Editar"
    if os.path.exists(pasta_videos):
        videos = [f for f in os.listdir(pasta_videos) if f.lower().endswith(('.mp4', '.avi', '.mov', '.mkv'))]
        if videos:
            print(f"\n🎬 Vídeos em {pasta_videos}:")
            for i, video in enumerate(videos, 1):
                print(f"  {i}. {video}")
        else:
            print(f"\n🎬 Nenhum vídeo encontrado em {pasta_videos}")
    
    # Listar músicas
    pasta_musicas = "Musicas"
    if os.path.exists(pasta_musicas):
        musicas = []
        for root, dirs, files in os.walk(pasta_musicas):
            for file in files:
                if file.lower().endswith(('.mp3', '.wav', '.aac', '.m4a')):
                    musicas.append(os.path.relpath(os.path.join(root, file)))
        
        if musicas:
            print(f"\n🎵 Músicas em {pasta_musicas}:")
            for i, musica in enumerate(musicas, 1):
                print(f"  {i}. {musica}")
        else:
            print(f"\n🎵 Nenhuma música encontrada em {pasta_musicas}")

def main_interativo():
    """Modo interativo para guiar o usuário"""
    print("🎬 Editor de Vídeo para Stories - Modo Interativo")
    print("=" * 50)
    
    listar_arquivos_disponiveis()
    
    print("\n📝 Digite os caminhos dos arquivos:")
    video = input("Vídeo original: ").strip()
    musica = input("Música de fundo: ").strip()
    texto = input("Texto para sobrepor: ").strip()
    saida = input("Nome do arquivo de saída (ex: resultado.mp4): ").strip()
    
    if not saida.startswith("Videos_Editados/"):
        saida = f"Videos_Editados/{saida}"
    
    return editar_video_story(video, musica, texto, saida, duracao_maxima=60)

if __name__ == '__main__':
    # Verificar dependências
    if not verificar_dependencias():
        sys.exit(1)
    
    # Criar estrutura de pastas
    criar_pastas_necessarias()
    
    # Verificar argumentos da linha de comando
    if len(sys.argv) > 1:
        if sys.argv[1] == '--teste':
            print("[INFO] Executando modo de teste...")
            
            # Variáveis de teste conforme especificado
            video_teste = "Videos_Para_Editar/teste.mp4"
            musica_teste = "Musicas/musica.mp3"
            texto_exemplo = "Produto Incrível da Finiti!"
            video_final = "Videos_Editados/resultado_teste.mp4"
            
            print("[INFO] Edição iniciada...")
            sucesso = editar_video_story(video_teste, musica_teste, texto_exemplo, video_final)
            
            if sucesso:
                print("[SUCESSO] Edição finalizada!")
            else:
                print("[ERRO] Falha na edição")
                
        elif sys.argv[1] == '--info':
            listar_arquivos_disponiveis()
            
        elif len(sys.argv) == 5:
            # Modo direto: python editor_video.py video musica texto saida
            video_path = sys.argv[1]
            musica_path = sys.argv[2] 
            texto_overlay = sys.argv[3]
            saida_path = sys.argv[4]
            
            print(f"[INFO] Processando: {video_path}")
            print(f"[INFO] Música: {musica_path}")
            print(f"[INFO] Texto: {texto_overlay}")
            print(f"[INFO] Saída: {saida_path}")
            
            sucesso = editar_video_story(video_path, musica_path, texto_overlay, saida_path)
            
            if sucesso:
                print(f"[SUCESSO] Vídeo editado salvo em: {saida_path}")
                sys.exit(0)
            else:
                print("[ERRO] Falha na edição do vídeo")
                sys.exit(1)
            
        else:
            print("Uso: python editor_video.py [--teste|--info|video musica texto saida]")
            print("  --teste: Executa teste com arquivos padrão")
            print("  --info: Lista arquivos disponíveis")
            print("  video musica texto saida: Edição direta")
            print("  (sem argumentos): Modo interativo")
    else:
        # Modo interativo padrão
        main_interativo()