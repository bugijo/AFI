#!/usr/bin/env python3
"""
Editor de Vídeo para Stories de Redes Sociais
Script robusto para automatizar a edição de vídeos usando MoviePy
"""

import json
import os
import sys
import random
from datetime import datetime
from pathlib import Path

from environment import ROOT_DIR, load_settings

SETTINGS = load_settings()
NO_DEPS_MODE = SETTINGS.no_deps

MUSIC_DIR_ENV = os.getenv("AFI_MUSIC_DIR")
if MUSIC_DIR_ENV:
    MUSIC_DIR = Path(MUSIC_DIR_ENV)
    if not MUSIC_DIR.is_absolute():
        MUSIC_DIR = (ROOT_DIR / MUSIC_DIR).resolve()
else:
    MUSIC_DIR = (SETTINGS.input_dir.parent / "musics").resolve()

try:
    if NO_DEPS_MODE:
        raise ImportError("NO_DEPS ativo")
    from moviepy.video.io.VideoFileClip import VideoFileClip
    from moviepy.audio.io.AudioFileClip import AudioFileClip
    from moviepy.video.VideoClip import TextClip
    from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
    from moviepy.audio.AudioClip import concatenate_audioclips
    MOVIEPY_AVAILABLE = True
    MOVIEPY_IMPORT_ERROR = None
except Exception as exc:  # pragma: no cover - import guard
    VideoFileClip = None  # type: ignore
    AudioFileClip = None  # type: ignore
    TextClip = None  # type: ignore
    CompositeVideoClip = None  # type: ignore
    concatenate_audioclips = None  # type: ignore
    MOVIEPY_AVAILABLE = False
    MOVIEPY_IMPORT_ERROR = exc

if MOVIEPY_AVAILABLE:
    try:
        import moviepy.config as config
        imagemagick_path = r"C:\Program Files\ImageMagick-7.1.2-Q16-HDRI\magick.exe"
        if os.path.exists(imagemagick_path):
            config.change_settings({"IMAGEMAGICK_BINARY": imagemagick_path})
    except Exception:
        pass  # Continua sem ImageMagick se houver erro

def verificar_dependencias():
    """Verifica se as dependencias multimidia estao disponiveis."""
    if NO_DEPS_MODE:
        print("[INFO] NO_DEPS ativo: pulando verificacao de MoviePy.")
        return True

    if MOVIEPY_AVAILABLE:
        try:
            import moviepy  # type: ignore
            print(f"[OK] MoviePy {moviepy.__version__} detectado")
        except Exception:  # pragma: no cover - log informativo
            print("[OK] MoviePy carregado, mas a versao nao pode ser identificada.")
        return True

    print("[ERRO] MoviePy nao esta instalado ou configurado corretamente.")
    if MOVIEPY_IMPORT_ERROR:
        print(f"[DEBUG] Motivo: {MOVIEPY_IMPORT_ERROR}")
    print("[INFO] Execute: pip install moviepy==1.0.3")
    return False

def criar_pastas_necessarias():
    """Cria as pastas necessarias se nao existirem."""
    pastas = [
        SETTINGS.input_dir,
        SETTINGS.output_dir,
        SETTINGS.log_dir,
        MUSIC_DIR,
        MUSIC_DIR / "Instrumental",
        MUSIC_DIR / "Energetica",
        MUSIC_DIR / "Relaxante",
    ]

    for pasta in pastas:
        pasta.mkdir(parents=True, exist_ok=True)

    print("[INFO] Estrutura de pastas verificada/criada")

def executar_modo_simulado(destino_final: str | None = None, origem: str | None = None, musica: str | None = None, texto: str | None = None) -> bool:
    """Gera arquivos dummy quando o modo NO_DEPS esta ativo."""
    SETTINGS.output_dir.mkdir(parents=True, exist_ok=True)
    dummy_mp4 = SETTINGS.output_dir / "dummy_arquivo.mp4"
    dummy_json = SETTINGS.output_dir / "dummy_arquivo.json"

    payload = {
        "status": "simulado",
        "gerado_em": datetime.utcnow().isoformat() + "Z",
        "origem": origem,
        "musica": musica,
        "texto": texto,
        "destino_solicitado": destino_final,
    }

    if not dummy_mp4.exists():
        dummy_mp4.write_bytes(b"SIMULATED_MP4_CONTENT")
    dummy_json.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    if destino_final:
        destino_path = Path(destino_final)
        if not destino_path.is_absolute():
            destino_path = (ROOT_DIR / destino_path).resolve()
        destino_path.parent.mkdir(parents=True, exist_ok=True)
        destino_path.write_bytes(dummy_mp4.read_bytes())

    print(f"[INFO] Modo simulado ativo: arquivos dummy atualizados em {SETTINGS.output_dir}")
    return True


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
    """Lista videos e musicas disponiveis nas pastas configuradas."""
    print("\n[INFO] Arquivos disponiveis:")

    if SETTINGS.input_dir.exists():
        videos = [
            item.name
            for item in SETTINGS.input_dir.iterdir()
            if item.is_file() and item.suffix.lower() in ('.mp4', '.avi', '.mov', '.mkv')
        ]
        if videos:
            print(f"\n[INFO] Videos em {SETTINGS.input_dir}:")
            for idx, video in enumerate(videos, 1):
                print(f"  {idx}. {video}")
        else:
            print(f"\n[INFO] Nenhum video encontrado em {SETTINGS.input_dir}")

    if MUSIC_DIR.exists():
        musicas = []
        for item in MUSIC_DIR.rglob('*'):
            if item.is_file() and item.suffix.lower() in ('.mp3', '.wav', '.aac', '.m4a'):
                musicas.append(item.relative_to(MUSIC_DIR).as_posix())

        if musicas:
            print(f"\n[INFO] Musicas em {MUSIC_DIR}:")
            for idx, musica in enumerate(musicas, 1):
                print(f"  {idx}. {musica}")
        else:
            print(f"\n[INFO] Nenhuma musica encontrada em {MUSIC_DIR}")

def main_interativo():
    """Modo interativo para guiar o usuario."""
    if NO_DEPS_MODE:
        executar_modo_simulado()
        return True

    print("[INFO] Editor de Video para Stories - Modo Interativo")
    print("=" * 50)

    listar_arquivos_disponiveis()

    print("\nDigite os caminhos dos arquivos:")
    video = input("Video original: ").strip()
    musica = input("Musica de fundo: ").strip()
    texto = input("Texto para sobrepor: ").strip()
    saida = input("Nome do arquivo de saida (ex: resultado.mp4): ").strip()

    if not saida:
        saida = "resultado.mp4"

    saida_path = Path(saida)
    if not saida_path.is_absolute():
        saida_path = SETTINGS.output_dir / saida_path

    return editar_video_story(video, musica, texto, str(saida_path))

if __name__ == '__main__':
    criar_pastas_necessarias()

    args = sys.argv[1:]

    if args and args[0] == '--info':
        listar_arquivos_disponiveis()
        sys.exit(0)

    if NO_DEPS_MODE:
        destino_override = args[3] if len(args) >= 4 else None
        origem = args[0] if args else None
        musica = args[1] if len(args) >= 2 else None
        texto = args[2] if len(args) >= 3 else None
        executar_modo_simulado(destino_override, origem=origem, musica=musica, texto=texto)
        sys.exit(0)

    if not verificar_dependencias():
        sys.exit(1)

    if args:
        if args[0] == '--teste':
            print('[INFO] Executando modo de teste...')
            video_teste = str(SETTINGS.input_dir / 'teste.mp4')
            musica_teste = str(MUSIC_DIR / 'musica.mp3')
            texto_exemplo = 'Produto incrivel da Finiti!'
            video_final = str(SETTINGS.output_dir / 'resultado_teste.mp4')

            print('[INFO] Edicao iniciada...')
            sucesso = editar_video_story(video_teste, musica_teste, texto_exemplo, video_final)

            if sucesso:
                print('[SUCESSO] Edicao finalizada!')
            else:
                print('[ERRO] Falha na edicao')

        elif len(args) == 4:
            video_path, musica_path, texto_overlay, saida_path = args

            print(f'[INFO] Processando: {video_path}')
            print(f'[INFO] Musica: {musica_path}')
            print(f'[INFO] Texto: {texto_overlay}')
            print(f'[INFO] Saida: {saida_path}')

            sucesso = editar_video_story(video_path, musica_path, texto_overlay, saida_path)

            if sucesso:
                print(f'[SUCESSO] Video editado salvo em: {saida_path}')
                sys.exit(0)
            else:
                print('[ERRO] Falha na edicao do video')
                sys.exit(1)

        else:
            print('Uso: python editor_video.py [--teste|--info|video musica texto saida]')
            print('  --teste: Executa teste com arquivos padrao')
            print('  --info: Lista arquivos disponiveis')
            print('  video musica texto saida: Edicao direta')
            print('  (sem argumentos): Modo interativo')
    else:
        main_interativo()
