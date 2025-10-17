"""
Módulo de Lógica Central - AFI (Assistente Finiti Inteligente)
Este módulo contém apenas as funções de transcrição e processamento multimodal.
A lógica de RAG e LLM foi movida para app.py com cache_resource.
"""

import requests
import json
import os
import traceback
from pathlib import Path

# Importações condicionais para funcionalidades multimodais
try:
    from moviepy.video.io.VideoFileClip import VideoFileClip
    MOVIEPY_AVAILABLE = True
except ImportError:
    MOVIEPY_AVAILABLE = False
    print("⚠️ MoviePy não disponível - funcionalidades de vídeo desabilitadas")

try:
    import whisper
    WHISPER_AVAILABLE = True
except ImportError:
    WHISPER_AVAILABLE = False
    print("⚠️ Whisper não disponível - transcrição de áudio desabilitada")

try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    print("⚠️ PIL não disponível - processamento de imagem desabilitado")

try:
    from duckduckgo_search import DDGS
    DDGS_AVAILABLE = True
except ImportError:
    DDGS_AVAILABLE = False
    print("⚠️ DuckDuckGo Search não disponível - pesquisa web desabilitada")

# Carregar modelo Whisper globalmente para eficiência
whisper_model = None

def carregar_whisper():
    """Carrega o modelo Whisper apenas uma vez."""
    global whisper_model
    if not WHISPER_AVAILABLE:
        return None
    if whisper_model is None:
        print("🎤 Carregando modelo Whisper...")
        whisper_model = whisper.load_model("base")
        print("✅ Modelo Whisper carregado!")
    return whisper_model

def transcrever_video(caminho_video: str) -> str:
    """
    Extrai áudio de um vídeo e transcreve usando Whisper.
    
    Args:
        caminho_video (str): Caminho para o arquivo de vídeo
        
    Returns:
        str: Texto transcrito do áudio
    """
    if not MOVIEPY_AVAILABLE or not WHISPER_AVAILABLE:
        return "Erro: Bibliotecas de vídeo/áudio não disponíveis"
    
    try:
        # Verificar se pydub está disponível
        try:
            from pydub import AudioSegment
        except ImportError:
            raise ImportError("Please install pydub 'pip install pydub'")
        
        # Carregar modelo Whisper
        model = carregar_whisper()
        if model is None:
            return "Erro: Não foi possível carregar o modelo Whisper"
        
        # Extrair áudio do vídeo
        video = VideoFileClip(caminho_video)
        audio_path = caminho_video.replace(Path(caminho_video).suffix, "_temp_audio.wav")
        video.audio.write_audiofile(audio_path, logger=None)
        
        # Transcrever áudio
        result = model.transcribe(audio_path)
        transcricao = result["text"]
        
        # Limpar arquivo temporário
        os.remove(audio_path)
        video.close()
        
        return transcricao
        
    except ImportError as e:
        if "pydub" in str(e):
            print(f"⚠️ Pydub não disponível - transcrição de vídeo desabilitada: {str(e)}")
            return "Transcrição de vídeo não disponível - pydub não instalado"
        else:
            return f"Erro de importação: {str(e)}"
    except Exception as e:
        return f"Erro na transcrição: {str(e)}"

def descrever_imagem(caminho_imagem: str) -> str:
    """
    Gera uma descrição de uma imagem usando llava-llama3 via Ollama.
    
    Args:
        caminho_imagem (str): Caminho para o arquivo de imagem
        
    Returns:
        str: Descrição da imagem
    """
    if not PIL_AVAILABLE:
        return "Erro: Biblioteca PIL não disponível"
    
    try:
        # Verificar se a imagem existe e é válida
        if not os.path.exists(caminho_imagem):
            return f"Erro: Arquivo não encontrado: {caminho_imagem}"
        
        # Tentar abrir a imagem para validar
        with Image.open(caminho_imagem) as img:
            # Converter para base64 para enviar ao Ollama
            import base64
            with open(caminho_imagem, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        
        # Preparar payload para Ollama
        payload = {
            "model": "llava-llama3",
            "prompt": "Descreva esta imagem de forma detalhada e técnica, focando em equipamentos, processos ou elementos relevantes para engenharia e construção.",
            "images": [encoded_string],
            "stream": False
        }
        
        # Fazer requisição ao Ollama
        response = requests.post("http://localhost:11434/api/generate", json=payload, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            return result.get("response", "Erro: Resposta vazia do modelo")
        else:
            return f"Erro na API do Ollama: {response.status_code}"
            
    except Exception as e:
        return f"Erro na descrição da imagem: {str(e)}"

def verificar_conexao_ollama():
    """
    Verifica se o servidor Ollama está rodando e acessível.
    
    Returns:
        bool: True se conectado, False caso contrário
    """
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        return response.status_code == 200
    except:
        return False

def carregar_memoria(pasta_memoria="memoria"):
    """
    Processa arquivos na pasta de memória, incluindo transcrição de vídeos
    e descrição de imagens, salvando os resultados como arquivos de texto.
    
    Args:
        pasta_memoria (str): Caminho para a pasta de memória
        
    Returns:
        str: Status do processamento
    """
    if not os.path.exists(pasta_memoria):
        os.makedirs(pasta_memoria)
        return "Pasta de memória criada"
    
    arquivos_processados = 0
    
    # Verificar se pydub está disponível para processamento de vídeos
    pydub_disponivel = True
    try:
        from pydub import AudioSegment
    except ImportError:
        pydub_disponivel = False
        print("⚠️ Pydub não disponível - processamento de vídeos desabilitado")
    
    for arquivo in os.listdir(pasta_memoria):
        caminho_arquivo = os.path.join(pasta_memoria, arquivo)
        
        # Pular se for um diretório
        if os.path.isdir(caminho_arquivo):
            continue
            
        # Processar vídeos (apenas se pydub estiver disponível)
        if arquivo.lower().endswith(('.mp4', '.avi', '.mov')) and pydub_disponivel:
            arquivo_transcricao = caminho_arquivo.replace(Path(arquivo).suffix, "_transcricao.txt")
            
            # Só processar se a transcrição não existir
            if not os.path.exists(arquivo_transcricao):
                print(f"🎬 Transcrevendo vídeo: {arquivo}")
                transcricao = transcrever_video(caminho_arquivo)
                
                # Verificar se a transcrição foi bem-sucedida
                if not transcricao.startswith("Erro") and not transcricao.startswith("Transcrição de vídeo não disponível"):
                    # Salvar transcrição
                    with open(arquivo_transcricao, 'w', encoding='utf-8') as f:
                        f.write(f"Transcrição do vídeo: {arquivo}\n\n")
                        f.write(transcricao)
                    
                    arquivos_processados += 1
                    print(f"✅ Transcrição salva: {os.path.basename(arquivo_transcricao)}")
                else:
                    print(f"⚠️ Falha na transcrição de {arquivo}: {transcricao}")
        elif arquivo.lower().endswith(('.mp4', '.avi', '.mov')) and not pydub_disponivel:
            print(f"⚠️ Pulando vídeo {arquivo} - pydub não disponível")
        
        # Processar imagens
        elif arquivo.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
            arquivo_descricao = caminho_arquivo.replace(Path(arquivo).suffix, "_descricao.txt")
            
            # Só processar se a descrição não existir
            if not os.path.exists(arquivo_descricao):
                print(f"🖼️ Descrevendo imagem: {arquivo}")
                descricao = descrever_imagem(caminho_arquivo)
                
                # Salvar descrição
                with open(arquivo_descricao, 'w', encoding='utf-8') as f:
                    f.write(f"Descrição da imagem: {arquivo}\n\n")
                    f.write(descricao)
                
                arquivos_processados += 1
                print(f"✅ Descrição salva: {os.path.basename(arquivo_descricao)}")
    
    if arquivos_processados > 0:
        return f"Processados {arquivos_processados} arquivos multimodais"
    else:
        return "Nenhum arquivo novo para processar"

def pesquisar_na_web(query: str) -> str:
    """
    Realiza pesquisa web em tempo real usando DuckDuckGo
    
    Args:
        query (str): Termo de pesquisa
        
    Returns:
        str: Resultados formatados da pesquisa
    """
    if not DDGS_AVAILABLE:
        return "❌ Pesquisa web não disponível - biblioteca DuckDuckGo Search não instalada."
    
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=5))
            
        if not results:
            return f"🔍 Nenhum resultado encontrado para: {query}"
        
        # Formatar resultados
        formatted_results = f"🌐 **Resultados da pesquisa para: {query}**\n\n"
        
        for i, result in enumerate(results, 1):
            title = result.get('title', 'Sem título')
            body = result.get('body', 'Sem descrição')
            href = result.get('href', '#')
            
            formatted_results += f"**{i}. {title}**\n"
            formatted_results += f"{body}\n"
            formatted_results += f"🔗 {href}\n\n"
        
        return formatted_results
        
    except Exception as e:
        return f"❌ Erro na pesquisa web: {str(e)}"

def processar_prompt_geral(prompt: str, query_engine=None):
    """
    Roteador inteligente que analisa o prompt e direciona para a funcionalidade adequada
    
    Args:
        prompt (str): O prompt do usuário
        query_engine: Engine de consulta RAG configurado
    
    Returns:
        str: Resposta processada pelo modelo adequado
    """
    prompt_lower = prompt.lower()
    
    # 1. Roteamento para transcrição de vídeo
    palavras_transcricao = ['transcreva', 'transcrever', 'roteiro do vídeo', 'áudio do vídeo', 'fala do vídeo']
    if any(palavra in prompt_lower for palavra in palavras_transcricao):
        return "Para transcrever vídeos, por favor faça upload do arquivo de vídeo através do gerenciador de memória na sidebar. O sistema processará automaticamente o áudio e criará a transcrição."
    
    # 2. Roteamento para geração de imagens
    palavras_imagem = ['gere uma imagem', 'desenhe', 'crie uma imagem', 'gerar imagem', 'criar desenho']
    if any(palavra in prompt_lower for palavra in palavras_imagem):
        return "🎨 **Funcionalidade de Geração de Imagem em Desenvolvimento**\n\nEsta funcionalidade estará disponível em breve! Por enquanto, você pode:\n- Fazer upload de imagens para análise\n- Solicitar descrições de imagens existentes\n- Usar outras funcionalidades do AFI"
    
    # 3. Roteamento para pesquisa web em tempo real
    palavras_pesquisa = ['pesquise sobre', 'notícias de', 'qual o preço atual de', 'quem é', 'o que é', 'pesquisar', 'buscar na internet', 'procurar na web']
    if any(palavra in prompt_lower for palavra in palavras_pesquisa):
        # Extrair termo de pesquisa do prompt
        termo_pesquisa = prompt
        for palavra in palavras_pesquisa:
            if palavra in prompt_lower:
                termo_pesquisa = prompt_lower.replace(palavra, '').strip()
                break
        
        # Realizar pesquisa web
        resultados_web = pesquisar_na_web(termo_pesquisa)
        
        # Combinar resultados com análise do LLM
        try:
            if verificar_conexao_ollama():
                import requests
                payload = {
                    "model": "llava-llama3",
                    "prompt": f"Com base nos seguintes resultados de pesquisa, forneça uma resposta completa e informativa para a pergunta: '{prompt}'\n\nResultados da pesquisa:\n{resultados_web}",
                    "stream": False
                }
                
                response = requests.post("http://localhost:11434/api/generate", json=payload, timeout=60)
                if response.status_code == 200:
                    return response.json().get("response", resultados_web)
                else:
                    return resultados_web
            else:
                return resultados_web
        except Exception as e:
            return f"{resultados_web}\n\n⚠️ Nota: Não foi possível processar os resultados com IA local: {str(e)}"
    
    # 4. Roteamento para consultas sobre produtos/memória (RAG com llava-llama3)
    palavras_produtos = ['produto', 'equipamento', 'orçamento', 'preço', 'finiti', 'memoria', 'arquivo']
    tem_arquivos_memoria = os.path.exists("./memoria") and len(os.listdir("./memoria")) > 0
    
    if any(palavra in prompt_lower for palavra in palavras_produtos) or tem_arquivos_memoria:
        if query_engine:
            try:
                response = query_engine.query(prompt)
                return str(response)
            except Exception as e:
                return f"Erro ao processar consulta RAG: {str(e)}"
        else:
            return "Sistema RAG não está disponível no momento."
    
    # 4. Fallback para perguntas gerais (phi-3-mini simulado)
    try:
        # Verificar se o servidor Ollama está rodando
        if verificar_conexao_ollama():
            try:
                # Usar llava-llama3 para perguntas gerais
                import requests
                payload = {
                    "model": "llava-llama3",
                    "prompt": prompt,
                    "stream": False
                }
                
                response = requests.post("http://localhost:11434/api/generate", json=payload, timeout=60)
                
                if response.status_code == 200:
                    result = response.json()
                    return result.get("response", "Erro: Resposta vazia do modelo")
                else:
                    return f"Erro na API do Ollama: {response.status_code}"
            except Exception as e:
                return f"Erro ao processar consulta: {str(e)}"
        else:
            return "⚠️ **Servidor Ollama Desconectado**\n\nO servidor Ollama não está disponível no momento. Por favor:\n1. Verifique se o Ollama está instalado\n2. Inicie o servidor Ollama\n3. Tente novamente"
            
    except Exception as e:
        return f"Erro inesperado ao processar prompt: {str(e)}"


def extrair_texto_de_url(url: str) -> str:
    """
    Extrai texto de uma URL fornecida usando web scraping.
    
    Args:
        url (str): A URL da página web para extrair o texto
        
    Returns:
        str: O texto extraído da página ou mensagem de erro
    """
    try:
        from bs4 import BeautifulSoup
        import requests
        from urllib.parse import urlparse
        
        # Validar se a URL é válida
        parsed_url = urlparse(url)
        if not parsed_url.scheme or not parsed_url.netloc:
            return "Erro: URL inválida. Certifique-se de incluir http:// ou https://"
        
        # Headers para simular um navegador real
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # Fazer a requisição HTTP
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()  # Levanta exceção para códigos de erro HTTP
        
        # Parsear o HTML com BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remover scripts e estilos
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Extrair texto de tags relevantes
        texto_extraido = []
        
        # Título da página
        title = soup.find('title')
        if title:
            texto_extraido.append(f"TÍTULO: {title.get_text().strip()}")
        
        # Cabeçalhos (h1, h2, h3, h4, h5, h6)
        for heading in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
            texto = heading.get_text().strip()
            if texto:
                texto_extraido.append(f"CABEÇALHO: {texto}")
        
        # Parágrafos
        for paragrafo in soup.find_all('p'):
            texto = paragrafo.get_text().strip()
            if texto and len(texto) > 20:  # Filtrar parágrafos muito curtos
                texto_extraido.append(texto)
        
        # Itens de lista
        for item in soup.find_all('li'):
            texto = item.get_text().strip()
            if texto and len(texto) > 10:  # Filtrar itens muito curtos
                texto_extraido.append(f"• {texto}")
        
        # Juntar todo o texto extraído
        texto_final = '\n\n'.join(texto_extraido)
        
        if not texto_final.strip():
            return "Erro: Não foi possível extrair texto significativo da página"
        
        # Limitar o tamanho do texto (máximo 10000 caracteres)
        if len(texto_final) > 10000:
            texto_final = texto_final[:10000] + "\n\n[TEXTO TRUNCADO - PÁGINA MUITO LONGA]"
        
        return texto_final
        
    except requests.exceptions.Timeout:
        return "Erro: Tempo limite esgotado ao acessar a URL. Tente novamente."
    except requests.exceptions.ConnectionError:
        return "Erro: Não foi possível conectar à URL. Verifique sua conexão com a internet."
    except requests.exceptions.HTTPError as e:
        return f"Erro HTTP: {e.response.status_code} - Não foi possível acessar a página"
    except requests.exceptions.RequestException as e:
        return f"Erro na requisição: {str(e)}"
    except ImportError:
        return "Erro: Biblioteca BeautifulSoup4 não encontrada. Execute: pip install beautifulsoup4"
    except Exception as e:
        return f"Erro inesperado ao extrair texto da URL: {str(e)}"


def criar_video_propaganda_ia(caminho_video_original: str) -> str:
    """
    🤖 DIRETOR DE ARTE ROBÔ - Função principal do Estúdio de IA
    
    Esta função é o cérebro criativo que automatiza todo o processo de criação de vídeos para redes sociais.
    Ela combina análise de conteúdo, IA generativa, seleção musical inteligente e edição automática.
    
    Args:
        caminho_video_original (str): Caminho para o arquivo de vídeo original
        
    Returns:
        str: Caminho para o vídeo final editado ou None em caso de erro
    """
    import os
    import random
    import glob
    from datetime import datetime
    from pathlib import Path
    
    # 🔍 SISTEMA DE DIAGNÓSTICO ATIVADO
    try:
        # Importar streamlit para checkpoints visuais
        try:
            import streamlit as st
            STREAMLIT_AVAILABLE = True
        except ImportError:
            STREAMLIT_AVAILABLE = False
        
        print("🤖 DIRETOR DE ARTE ROBÔ INICIADO")
        print("=" * 50)
        
        # ========================================
        # FASE 1: ANÁLISE DE CONTEÚDO (O CÉREBRO)
        # ========================================
        print("🧠 Fase 1: Analisando conteúdo do vídeo...")
        
        # Transcrever o vídeo para entender o contexto
        transcricao = transcrever_video(caminho_video_original)
        
        if transcricao.startswith("Erro") or "não disponível" in transcricao:
            print(f"⚠️ Transcrição falhou: {transcricao}")
            # Fallback: usar nome do arquivo como contexto
            nome_arquivo = Path(caminho_video_original).stem
            contexto = f"vídeo sobre {nome_arquivo.replace('_', ' ').replace('-', ' ')}"
            print(f"📝 Usando contexto do nome do arquivo: {contexto}")
        else:
            contexto = transcricao[:200]  # Primeiros 200 caracteres
            print(f"✅ Transcrição obtida: {contexto[:100]}...")
        
        # 🔍 CHECKPOINT 1 DE 5
        if STREAMLIT_AVAILABLE:
            st.info("✅ Passo 1 de 5: Transcrição do vídeo concluída.")
        print("🔍 CHECKPOINT 1/5: Transcrição do vídeo concluída.")
        
        # ========================================
        # FASE 2: GERAÇÃO DE TEXTO COM IA (O COPYWRITER)
        # ========================================
        print("✍️ Fase 2: Gerando frase de marketing com IA...")
        
        # Criar prompt de marketing poderoso
        prompt_marketing = f"""Você é um especialista em marketing da Finiti, empresa de equipamentos industriais. 

Com base no seguinte contexto de um vídeo: '{contexto}'

Crie uma única frase de impacto, curta e poderosa, com no máximo 8 palavras, para um story no Instagram sobre o produto ou ação mostrada.

A frase deve ser:
- Direta e impactante
- Focada no benefício ou resultado
- Adequada para redes sociais
- Em português brasileiro

Responda APENAS com a frase, sem explicações."""

        # Gerar frase com IA
        try:
            frase_marketing = processar_prompt_geral(prompt_marketing)
            # Limpar a resposta (remover quebras de linha extras, etc.)
            frase_marketing = frase_marketing.strip().replace('\n', ' ')
            
            # Se a frase for muito longa, pegar apenas a primeira parte
            if len(frase_marketing) > 50:
                frase_marketing = frase_marketing[:50] + "..."
                
            print(f"✅ Frase gerada: '{frase_marketing}'")
            
        except Exception as e:
            print(f"⚠️ Erro na geração de texto: {e}")
            # Fallback: frase padrão baseada no contexto
            frase_marketing = "🚀 Inovação que Transforma!"
            print(f"📝 Usando frase padrão: '{frase_marketing}'")
        
        # 🔍 CHECKPOINT 2 DE 5
        if STREAMLIT_AVAILABLE:
            st.info("✅ Passo 2 de 5: Frase de marketing gerada pela IA.")
        print("🔍 CHECKPOINT 2/5: Frase de marketing gerada pela IA.")
        
        # ========================================
        # FASE 3: SELEÇÃO MUSICAL INTELIGENTE (O DJ)
        # ========================================
        print("🎵 Fase 3: Selecionando música automaticamente...")
        
        # Buscar todas as músicas disponíveis
        pasta_musicas = "./Musicas"
        extensoes_audio = ['*.mp3', '*.wav', '*.m4a']
        musicas_encontradas = []
        
        # Buscar em todas as subpastas
        for root, dirs, files in os.walk(pasta_musicas):
            for extensao in extensoes_audio:
                musicas_encontradas.extend(glob.glob(os.path.join(root, extensao)))
        
        if not musicas_encontradas:
            return "❌ Erro: Nenhuma música encontrada na pasta Musicas"
        
        # Selecionar música aleatoriamente
        musica_selecionada = random.choice(musicas_encontradas)
        nome_musica = os.path.basename(musica_selecionada)
        print(f"✅ Música selecionada: {nome_musica}")
        
        # 🔍 CHECKPOINT 3 DE 5
        if STREAMLIT_AVAILABLE:
            st.info("✅ Passo 3 de 5: Música selecionada com sucesso.")
        print("🔍 CHECKPOINT 3/5: Música selecionada com sucesso.")
        
        # ========================================
        # FASE 4: PROCESSAMENTO DE VÍDEO (O EDITOR)
        # ========================================
        print("🎬 Fase 4: Processando vídeo com MoviePy...")
        
        if not MOVIEPY_AVAILABLE:
            return "❌ Erro: MoviePy não disponível para edição de vídeo"
        
        # Carregar vídeo original
        video_clip = VideoFileClip(caminho_video_original)
        print(f"📐 Dimensões originais: {video_clip.w}x{video_clip.h}")
        
        # ========================================
        # FORMATAÇÃO 9:16 ROBUSTA - VERSÃO SIMPLIFICADA
        # ========================================
        print("📱 Aplicando formatação 9:16 robusta para Stories...")
        
        # Importar função de corte
        from moviepy.video.fx.Crop import Crop
        
        # Verifica se o vídeo já é vertical (ou quase)
        if video_clip.w / video_clip.h < 1.0:
            print("DEBUG: Vídeo já está em formato vertical. Pulando o corte.")
            clip_formatado = video_clip
        else:
            print("DEBUG: Vídeo horizontal detectado. Aplicando corte 9:16.")
            (w, h) = video_clip.size
            target_ratio = 9.0 / 16.0
            new_width = int(target_ratio * h)
            # Usa a sintaxe de função direta e confiável
            clip_formatado = Crop(video_clip, width=new_width, x_center=w/2)
            print(f"✂️ Cortado lateralmente: {new_width}x{h} (removidas laterais)")
        
        # Usar o clipe formatado diretamente (sem redimensionamento)
        video_clip.close()
        video_clip = clip_formatado
        
        print(f"✅ Formato final calibrado: {video_clip.w}x{video_clip.h}")
        
        # 🔍 CHECKPOINT 4 DE 5
        if STREAMLIT_AVAILABLE:
            st.info("✅ Passo 4 de 5: Vídeo formatado para o padrão de Stories.")
        print("🔍 CHECKPOINT 4/5: Vídeo formatado para o padrão de Stories.")
        
        # ========================================
        # APLICAÇÃO DE ÁUDIO (O SONOPLASTA)
        # ========================================
        print("🔊 Aplicando trilha sonora...")
        
        # Carregar música
        from moviepy.audio.io.AudioFileClip import AudioFileClip
        audio_clip = AudioFileClip(musica_selecionada)
        
        # Ajustar duração do áudio
        if audio_clip.duration < video_clip.duration:
            # Repetir áudio se necessário
            repeticoes = int(video_clip.duration / audio_clip.duration) + 1
            from moviepy.audio.AudioClip import concatenate_audioclips
            audio_clip = concatenate_audioclips([audio_clip] * repeticoes)
        
        # Cortar áudio para duração exata
        audio_clip = audio_clip.subclipped(0, video_clip.duration)
        
        # Aplicar áudio ao vídeo
        video_clip = video_clip.with_audio(audio_clip)
        
        # ========================================
        # COLOCAÇÃO DE TEXTO INTELIGENTE EM DUAS PARTES (O DESIGNER)
        # ========================================
        print("🎨 Criando overlay de texto em duas partes...")
        
        # Quebrar frase em duas metades
        palavras = frase_marketing.split()
        metade = len(palavras) // 2
        parte1_texto = " ".join(palavras[:metade])
        parte2_texto = " ".join(palavras[metade:])
        
        # Calcular duração do vídeo
        duracao_total = video_clip.duration
        
        print(f"📝 Parte 1: '{parte1_texto}' (0 - {duracao_total/2:.1f}s)")
        print(f"📝 Parte 2: '{parte2_texto}' ({duracao_total/2:.1f}s - {duracao_total:.1f}s)")
        
        # Criar TextClips
        try:
            from moviepy.video.VideoClip import TextClip
            from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
            
            # Criar primeiro TextClip
            texto_clip1 = TextClip(
                parte1_texto,
                font_size=60,
                color='white',
                font='Arial-Bold',
                stroke_color='black',
                stroke_width=3,
                method='caption',
                size=(video_clip.w * 0.8, None)  # 80% da largura do vídeo
            ).set_position(('center', video_clip.h * 0.35)).set_duration(duracao_total / 2)
            
            # Criar segundo TextClip
            texto_clip2 = TextClip(
                parte2_texto,
                font_size=60,
                color='white',
                font='Arial-Bold',
                stroke_color='black',
                stroke_width=3,
                method='caption',
                size=(video_clip.w * 0.8, None)  # 80% da largura do vídeo
            ).set_position(('center', video_clip.h * 0.35)).set_duration(duracao_total / 2).set_start(duracao_total / 2)
            
            # Compor vídeo final com os DOIS clipes de texto
            video_com_texto = CompositeVideoClip([video_clip, texto_clip1, texto_clip2])
            video_final = video_com_texto
            print(f"✅ Texto em duas partes aplicado: '{parte1_texto}' + '{parte2_texto}'")
            
        except Exception as e:
            print(f"⚠️ Erro ao aplicar texto: {e}")
            video_final = video_clip
        
        # 🔍 CHECKPOINT 5 DE 5
        if STREAMLIT_AVAILABLE:
            st.info("✅ Passo 5 de 5: Composição final do vídeo concluída.")
        print("🔍 CHECKPOINT 5/5: Composição final do vídeo concluída.")
        
        # ========================================
        # EXPORTAÇÃO FINAL (O FINALIZADOR)
        # ========================================
        print("💾 Exportando vídeo final...")
        
        # Gerar nome único para o arquivo
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nome_saida = f"estudio_ia_{timestamp}.mp4"
        caminho_saida = os.path.join("./Videos_Editados", nome_saida)
        
        # Garantir que a pasta existe
        os.makedirs("./Videos_Editados", exist_ok=True)
        
        # Exportar vídeo
        video_final.write_videofile(
            caminho_saida,
            codec='libx264',
            audio_codec='aac',
            temp_audiofile='temp-audio.m4a',
            remove_temp=True,
            logger=None
        )
        
        # Limpar recursos
        video_final.close()
        video_clip.close()
        audio_clip.close()
        
        print("🎉 DIRETOR DE ARTE ROBÔ CONCLUÍDO!")
        print("=" * 50)
        print(f"📁 Vídeo salvo: {nome_saida}")
        print(f"🎵 Música: {nome_musica}")
        print(f"✍️ Frase: {texto_final}")
        print(f"📱 Formato: 9:16 (Stories)")
        
        return caminho_saida
        
    except Exception as e:
        # 🚨 SISTEMA DE DIAGNÓSTICO DE ERRO ATIVADO
        print("--- ERRO CRÍTICO NO DIRETOR DE ARTE ROBÔ ---")
        traceback.print_exc()
        print("---------------------------------------------")
        
        # Mostrar erro na interface Streamlit se disponível
        try:
            import streamlit as st
            st.error(f"Ocorreu uma falha no processo criativo. Detalhe do erro: {e}")
        except ImportError:
            pass
        
        # Retornar None em caso de erro
        return None