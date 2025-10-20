
 (cd "$(git rev-parse --show-toplevel)" && git apply --3way <<'EOF' 
diff --git a/.env b/.env
new file mode 100644
index 0000000000000000000000000000000000000000..d049290387c3713dd9a5f17510c11a6b97d6171b
--- /dev/null
+++ b/.env
@@ -0,0 +1,8 @@
+AFI_PORT=8507
+AFI_BACKEND_PORT=8508
+AFI_INPUT_DIR=./data/Videos_Para_Editar
+AFI_OUTPUT_DIR=./data/Videos_Agendados
+AFI_MUSIC_DIR=./data/Musicas
+AFI_LOG_DIR=./logs
+IMAGEIO_FFMPEG_EXE=third_party/ffmpeg/linux/bin/ffmpeg
+NO_DEPS=1
diff --git a/.env.example b/.env.example
new file mode 100644
index 0000000000000000000000000000000000000000..d049290387c3713dd9a5f17510c11a6b97d6171b
--- /dev/null
+++ b/.env.example
@@ -0,0 +1,8 @@
+AFI_PORT=8507
+AFI_BACKEND_PORT=8508
+AFI_INPUT_DIR=./data/Videos_Para_Editar
+AFI_OUTPUT_DIR=./data/Videos_Agendados
+AFI_MUSIC_DIR=./data/Musicas
+AFI_LOG_DIR=./logs
+IMAGEIO_FFMPEG_EXE=third_party/ffmpeg/linux/bin/ffmpeg
+NO_DEPS=1
diff --git a/.gitignore b/.gitignore
index 30c163e5d551eaeff45c2e2c3a435429c03dfe64..669b6d802fe5d7f34e769362ffd1b1bb5b4f070a 100644
--- a/.gitignore
+++ b/.gitignore
@@ -134,26 +134,35 @@ temp-audio.m4a
 temp_uploads/
 Videos_Editados/
 Videos_Para_Editar/
 storage/
 memoria/
 __pycache__/
 
 # FFmpeg binaries and documentation
 ffmpeg-8.0-essentials_build/
 ffmpeg.zip
 ImageMagick-installer.exe
 
 # IDE files
 .vscode/
 .idea/
 *.swp
 *.swo
 
 # OS generated files
 .DS_Store
 .DS_Store?
 ._*
 .Spotlight-V100
 .Trashes
 ehthumbs.db
-Thumbs.db
\ No newline at end of file
+Thumbs.db
+# Track placeholder files inside data/logs volumes
+!data/Videos_Para_Editar/.gitkeep
+!data/Videos_Agendados/.gitkeep
+!data/Musicas/.gitkeep
+!logs/.gitkeep
+!data/
+!data/Videos_Para_Editar/
+!data/Videos_Agendados/
+!data/Musicas/
diff --git a/Dockerfile b/Dockerfile
new file mode 100644
index 0000000000000000000000000000000000000000..c86481655b403cfad3988c93807469db2dc985ef
--- /dev/null
+++ b/Dockerfile
@@ -0,0 +1,21 @@
+# syntax=docker/dockerfile:1
+FROM python:3.10-slim AS base
+
+ENV PYTHONDONTWRITEBYTECODE=1 \
+    PYTHONUNBUFFERED=1
+
+WORKDIR /app
+
+RUN apt-get update \
+    && apt-get install -y --no-install-recommends ffmpeg \
+    && rm -rf /var/lib/apt/lists/*
+
+COPY requirements.txt ./
+RUN pip install --no-cache-dir --upgrade pip \
+    && pip install --no-cache-dir -r requirements.txt
+
+COPY . .
+
+EXPOSE 8507
+
+CMD ["streamlit", "run", "app.py", "--server.port", "8507", "--server.headless", "true"]
diff --git a/README.md b/README.md
index c0787647485cad3c7d0b961063eb16598e1b5385..bcc816d11c1941044634ed5c89ca2840560d9d1f 100644
--- a/README.md
+++ b/README.md
@@ -1,89 +1,53 @@
-# AFI v3.0 - Assistente Finiti Inteligente
+# AFI Assistente - Guia Rápido
 
-## 🚀 Inicialização Rápida
-
-### Porta Padrão: 8507
-
-Este sistema foi configurado para usar **SEMPRE** a porta **8507** para evitar confusão com múltiplas portas.
-
-### Formas de Iniciar o Sistema
-
-#### 1. Método Recomendado (Windows)
-```bash
-start_afi.bat
-```
-
-#### 2. Script Python
+## Instalação
 ```bash
-python start_server.py
-```
-
-#### 3. Comando Direto
-```bash
-py -m streamlit run app.py --server.port 8507 --server.headless true
-```
-
-## 📋 URLs de Acesso
-
-- **Local:** http://localhost:8507
-- **Rede:** http://192.168.1.27:8507 (substitua pelo seu IP)
-
-## 📁 Estrutura do Projeto
-
-```
-AML/
-├── app.py              # Aplicação principal Streamlit
-├── core_logic.py       # Lógica principal do sistema
-├── config.py           # Configurações (PORTA PADRÃO: 8507)
-├── start_server.py     # Script de inicialização
-├── start_afi.bat       # Arquivo batch para Windows
-├── memoria/            # Pasta de arquivos para processamento
-├── storage/            # Armazenamento do índice RAG
-└── README.md           # Este arquivo
+pip install -r requirements.txt
 ```
 
-## ⚙️ Configuração
+> **Pré-requisito:** tenha o [FFmpeg](https://ffmpeg.org/) instalado e disponível na variável de ambiente `PATH`.
 
-A porta padrão está definida no arquivo `config.py`:
-
-```python
-SERVER_CONFIG = {
-    "port": 8507,  # Porta padrão única
-    "host": "localhost",
-    "headless": True
-}
-```
+### Instalação offline
+1. Em uma máquina com internet execute `scripts/offline/build_wheelhouse.sh` (Linux/macOS) ou `scripts/offline/build_wheelhouse.ps1` (Windows) para gerar `wheels.zip` com todas as dependências.
+2. Transfira `wheels.zip` para o ambiente isolado, extraia em `./wheels` e instale com:
+   ```bash
+   pip install --no-index --find-links wheels -r requirements.txt
+   ```
+3. Caso o FFmpeg não esteja disponível no `PATH`, copie o binário para `third_party/ffmpeg/<os>/bin/ffmpeg` e ajuste `IMAGEIO_FFMPEG_EXE` no `.env`.
 
-## 🔧 Resolução de Problemas
-
-### Porta em Uso
-Se a porta 8507 estiver em uso, pare todos os processos Streamlit:
-```bash
-taskkill /f /im streamlit.exe
-```
+### Modo NO_DEPS (simulado)
+Quando estiver em um ambiente sem acesso à internet ou sem as bibliotecas multimídia instaladas, defina `NO_DEPS=1` no `.env`:
 
-### Dependências
-Certifique-se de que todas as dependências estão instaladas:
 ```bash
-pip install streamlit llama-index sentence-transformers
-```
-
-## 📝 Regras Importantes
-
-1. **SEMPRE use a porta 8507**
-2. **NÃO inicie múltiplos servidores**
-3. **Use os scripts fornecidos para inicialização**
-4. **Verifique se a porta está livre antes de iniciar**
-
-## 🎯 Funcionalidades
-
-- ✅ Chat inteligente com IA
-- ✅ Processamento de documentos (PDF, TXT)
-- ✅ Transcrição de vídeos (quando disponível)
-- ✅ Análise de imagens
-- ✅ Sistema RAG (Retrieval-Augmented Generation)
-- ✅ Interface web moderna
-
----
-
-**Desenvolvido para Finiti - Versão 3.0**
\ No newline at end of file
+NO_DEPS=1
+```
+
+- A interface Streamlit inicia em modo "Simulado", exibindo apenas um painel informativo.
+- O Guardião utiliza polling (sem `watchdog`) e chama o editor no modo dummy.
+- `editor_video.py` gera arquivos `dummy_*.mp4` de 0,5 MB e um `.json` com metadados para validar a linha de montagem.
+
+Para voltar ao comportamento completo, redefina `NO_DEPS=0` e reinstale as dependências.
+
+## Como iniciar
+- **Launcher oficial (detecta modo real/fallback):**
+  ```bash
+  ./scripts/run_ui.sh
+  ```
+  - Se `streamlit` estiver disponível e `NO_DEPS=0`, a UI completa é iniciada.
+  - Caso contrário, o script ativa automaticamente o servidor em `ui_fallback/`.
+- **Guardião (monitoramento de arquivos):**
+  ```bash
+  ./scripts/run_guardian.sh
+  ```
+
+## Docker (alternativa recomendada)
+1. Construa as imagens e suba os serviços:
+   ```bash
+   docker compose build
+   docker compose up -d
+   ```
+2. Acesse a interface: http://localhost:8507
+3. Acompanhe os logs do guardião:
+   ```bash
+   docker compose logs guardian -f
+   ```
diff --git a/afi_v3_no_deps_release.zip b/afi_v3_no_deps_release.zip
new file mode 100644
index 0000000000000000000000000000000000000000..05190861386ed12dae0e07ab7664a987a7d9015c
GIT binary patch
literal 19754
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
L4pf)p>tFu|`0euu

literal 0
HcmV?d00001

diff --git a/agente_midia_social.py b/agente_midia_social.py
index eac87ef661248d9864d712fffce8624d1eb1042c..3be98f7fb1b02612aee806c43801bca514638f66 100644
--- a/agente_midia_social.py
+++ b/agente_midia_social.py
@@ -1,66 +1,81 @@
 #!/usr/bin/env python3
 """
 🤖 AFI v4.0 - Agente de Mídia Social Completo
 Sistema Automatizado de Criação de Conteúdo para Redes Sociais
 
 Este é o script principal que integra todos os componentes:
 - 👁️ Guardião (Monitoramento de pastas)
 - 🧠 Cérebro Criativo (Análise AFI)
 - 🎬 Oficina de Edição (MoviePy)
 - 📅 Fila de Saída (Agendamento)
 """
 
 import os
 import sys
 import time
 import logging
 import argparse
 from pathlib import Path
 from datetime import datetime
+try:
+    from dotenv import load_dotenv
+except ImportError:  # pragma: no cover - fallback for offline mode
+    def load_dotenv(*_args, **_kwargs):
+        return False
 
 # Importar módulos do sistema
 try:
     from guardiao_midia import GuardiaoMidia, GuardiaoMidiaHandler
     from editor_video import editar_video_story, criar_pastas_necessarias
     from integracao_afi_midia import IntegradorAFIMidia
 except ImportError as e:
     print(f"❌ Erro ao importar módulos: {e}")
     print("💡 Certifique-se de que todos os arquivos estão no mesmo diretório")
     sys.exit(1)
 
 # Configurar logging
 logging.basicConfig(
     level=logging.INFO,
     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
     handlers=[
         logging.FileHandler('agente_midia_social.log'),
         logging.StreamHandler()
     ]
 )
 logger = logging.getLogger(__name__)
 
+load_dotenv()
+
+AFI_INPUT_DIR = Path(os.getenv("AFI_INPUT_DIR", "./data/Videos_Para_Editar")).expanduser()
+AFI_OUTPUT_DIR = Path(os.getenv("AFI_OUTPUT_DIR", "./data/Videos_Agendados")).expanduser()
+AFI_MUSIC_DIR = Path(os.getenv("AFI_MUSIC_DIR", "./data/Musicas")).expanduser()
+AFI_LOG_DIR = Path(os.getenv("AFI_LOG_DIR", "./logs")).expanduser()
+
+for _path in {AFI_INPUT_DIR, AFI_OUTPUT_DIR, AFI_MUSIC_DIR, AFI_LOG_DIR}:
+    _path.mkdir(parents=True, exist_ok=True)
+
 class AgenteMidiaSocial:
     """
     Classe principal do Agente de Mídia Social.
     Coordena todos os componentes do sistema.
     """
     
     def __init__(self):
         """
         Inicializa o Agente de Mídia Social.
         """
         self.integrador_afi = IntegradorAFIMidia()
         self.guardiao = None
         self.estatisticas = {
             'videos_processados': 0,
             'videos_com_sucesso': 0,
             'videos_com_erro': 0,
             'inicio_execucao': datetime.now()
         }
         
     def inicializar_sistema(self):
         """
         Inicializa todo o sistema e cria estrutura necessária.
         """
         logger.info("🚀 Inicializando Agente de Mídia Social...")
         
@@ -125,101 +140,101 @@ class AgenteMidiaSocial:
             caminho_video (str): Caminho para o vídeo
             caminho_musica (str): Caminho para música (opcional)
             texto_personalizado (str): Texto personalizado (opcional)
         """
         logger.info(f"🎬 Processando vídeo único: {caminho_video}")
         
         try:
             video_path = Path(caminho_video)
             if not video_path.exists():
                 raise FileNotFoundError(f"Vídeo não encontrado: {caminho_video}")
             
             # Analisar com AFI se não houver texto personalizado
             if not texto_personalizado:
                 frase, estilo = self.integrador_afi.analisar_video_com_afi(caminho_video)
             else:
                 frase = texto_personalizado
                 estilo = "Instrumental"  # Padrão
             
             # Selecionar música se não especificada
             if not caminho_musica:
                 caminho_musica = self._selecionar_musica_automatica(estilo)
             
             # Gerar nome de saída
             timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
             nome_saida = f"{timestamp}_processado_{video_path.stem}.mp4"
-            caminho_saida = Path("C:/AFI/Videos_Agendados") / nome_saida
+            caminho_saida = AFI_OUTPUT_DIR / nome_saida
             
             # Processar vídeo
             sucesso = editar_video_story(
                 caminho_video_original=caminho_video,
                 caminho_musica=caminho_musica,
                 texto_overlay=frase,
                 caminho_saida=str(caminho_saida)
             )
             
             if sucesso:
                 logger.info(f"✅ Vídeo processado: {caminho_saida}")
                 return str(caminho_saida)
             else:
                 logger.error("❌ Erro no processamento")
                 return None
                 
         except Exception as e:
             logger.error(f"❌ Erro ao processar vídeo: {e}")
             return None
     
     def _selecionar_musica_automatica(self, estilo):
         """
         Seleciona uma música automaticamente baseada no estilo.
         """
-        pasta_musicas = Path(f"C:/AFI/Musicas/{estilo}")
-        
+        pasta_musicas = AFI_MUSIC_DIR / estilo
+
         if pasta_musicas.exists():
             musicas = list(pasta_musicas.glob("*.mp3"))
             if musicas:
                 return str(musicas[0])  # Primeira música encontrada
-        
+
         # Fallback: procurar em qualquer pasta
-        for pasta in Path("C:/AFI/Musicas").iterdir():
+        for pasta in AFI_MUSIC_DIR.iterdir():
             if pasta.is_dir():
                 musicas = list(pasta.glob("*.mp3"))
                 if musicas:
                     return str(musicas[0])
         
         return None
     
     def _exibir_status_inicial(self):
         """
         Exibe status inicial do sistema.
         """
         print("\n" + "="*60)
         print("🤖 AFI v4.0 - AGENTE DE MÍDIA SOCIAL")
         print("="*60)
-        print(f"📁 Pasta monitorada: C:/AFI/Videos_Para_Editar")
-        print(f"🎵 Pastas de música: C:/AFI/Musicas/[Rock|Pop|Calma|Eletronica|Instrumental]")
-        print(f"📤 Saída: C:/AFI/Videos_Agendados")
+        print(f"📁 Pasta monitorada: {AFI_INPUT_DIR}")
+        print(f"🎵 Pastas de música: {AFI_MUSIC_DIR}/[Rock|Pop|Calma|Eletronica|Instrumental]")
+        print(f"📤 Saída: {AFI_OUTPUT_DIR}")
         print(f"🕐 Iniciado em: {self.estatisticas['inicio_execucao'].strftime('%Y-%m-%d %H:%M:%S')}")
         print("\n📝 COMO USAR:")
         print("1. Adicione músicas nas pastas de estilo")
         print("2. Copie vídeos para a pasta monitorada")
         print("3. O sistema processará automaticamente!")
         print("\n⏹️ Pressione Ctrl+C para parar")
         print("="*60)
     
     def _exibir_estatisticas_finais(self):
         """
         Exibe estatísticas finais do sistema.
         """
         tempo_execucao = datetime.now() - self.estatisticas['inicio_execucao']
         
         print("\n" + "="*50)
         print("📊 ESTATÍSTICAS FINAIS")
         print("="*50)
         print(f"⏱️ Tempo de execução: {tempo_execucao}")
         print(f"🎬 Vídeos processados: {self.estatisticas['videos_processados']}")
         print(f"✅ Sucessos: {self.estatisticas['videos_com_sucesso']}")
         print(f"❌ Erros: {self.estatisticas['videos_com_erro']}")
         
         if self.estatisticas['videos_processados'] > 0:
             taxa_sucesso = (self.estatisticas['videos_com_sucesso'] / self.estatisticas['videos_processados']) * 100
             print(f"📈 Taxa de sucesso: {taxa_sucesso:.1f}%")
@@ -276,47 +291,47 @@ Exemplos de uso:
 
   # Processar com música específica
   python agente_midia_social.py --video "video.mp4" --musica "musica.mp3"
 
   # Processar com texto personalizado
   python agente_midia_social.py --video "video.mp4" --texto "🚀 Minha frase!"
 
   # Apenas configurar sistema
   python agente_midia_social.py --setup
         """
     )
     
     parser.add_argument('--video', help='Processar vídeo único')
     parser.add_argument('--musica', help='Música específica para usar')
     parser.add_argument('--texto', help='Texto personalizado para overlay')
     parser.add_argument('--setup', action='store_true', help='Apenas configurar sistema')
     
     args = parser.parse_args()
     
     # Criar agente
     agente = AgenteMidiaSocial()
     agente.inicializar_sistema()
     
     if args.setup:
         print("✅ Sistema configurado com sucesso!")
-        print("📁 Pastas criadas em C:/AFI/")
+        print(f"📁 Pastas configuradas em {AFI_INPUT_DIR.parent}")
         print("💡 Adicione músicas e vídeos para começar!")
         return
     
     if args.video:
         # Modo processamento único
         resultado = agente.processar_video_unico(
             caminho_video=args.video,
             caminho_musica=args.musica,
             texto_personalizado=args.texto
         )
         
         if resultado:
             print(f"✅ Vídeo processado: {resultado}")
         else:
             print("❌ Erro no processamento")
     else:
         # Modo monitoramento
         agente.executar_modo_monitoramento()
 
 if __name__ == '__main__':
     main()
\ No newline at end of file
diff --git a/app.py b/app.py
index 877399fa562b6befaead2efc46d74731db1ebd2f..6fd559c52602f02ae2d56505b727e51ad26c11f2 100644
--- a/app.py
+++ b/app.py
@@ -1,38 +1,99 @@
-import streamlit as st
-import time
 import os
+import time
 from pathlib import Path
+
+try:
+    from dotenv import load_dotenv
+except ImportError:  # pragma: no cover - fallback for offline mode
+    def load_dotenv(*_args, **_kwargs):
+        return False
+import streamlit as st
+
+load_dotenv()
+
+NO_DEPS = os.getenv("NO_DEPS", "0") == "1"
+
+AFI_INPUT_DIR = Path(os.getenv("AFI_INPUT_DIR", "./data/Videos_Para_Editar")).expanduser()
+AFI_OUTPUT_DIR = Path(os.getenv("AFI_OUTPUT_DIR", "./data/Videos_Agendados")).expanduser()
+AFI_MUSIC_DIR = Path(os.getenv("AFI_MUSIC_DIR", "./data/Musicas")).expanduser()
+AFI_LOG_DIR = Path(os.getenv("AFI_LOG_DIR", "./logs")).expanduser()
+
+for _path in {AFI_INPUT_DIR, AFI_OUTPUT_DIR, AFI_MUSIC_DIR, AFI_LOG_DIR}:
+    _path.mkdir(parents=True, exist_ok=True)
+
+st.set_page_config(
+    page_title="AFI v3.0 - Assistente Finiti Inteligente",
+    page_icon="🏗️",
+    layout="wide",
+    initial_sidebar_state="expanded"
+)
+
+if NO_DEPS:
+    st.title("AFI v3.0 - Assistente Finiti Inteligente")
+    st.subheader("Modo Simulado")
+    st.warning(
+        "NO_DEPS=1 habilitado. Recursos multimídia e RAG estão temporariamente desativados para permitir testes sem dependências."
+    )
+    st.markdown(
+        "- Use os scripts do Guardião e do Editor para validar a linha de montagem em modo dummy.\n"
+        "- Gere vídeos fictícios no diretório de entrada para observar arquivos `dummy_*.mp4` no diretório de saída.\n"
+        "- Ao reinstalar as dependências, defina `NO_DEPS=0` para reativar todas as funcionalidades."
+    )
+    st.stop()
+
 from config import SERVER_CONFIG, get_server_port, get_server_url
 from core_logic import verificar_conexao_ollama, carregar_memoria, processar_prompt_geral
 from streamlit_chat import message
 from streamlit_option_menu import option_menu
 from llama_index.core import Settings, VectorStoreIndex, SimpleDirectoryReader
 from llama_index.llms.ollama import Ollama
 from llama_index.embeddings.huggingface import HuggingFaceEmbedding
 from llama_index.core.memory import ChatMemoryBuffer
 
+try:
+    from rag.ingest import ingest_documents
+    RAG_INGEST_AVAILABLE = True
+except Exception as exc:  # pragma: no cover - interface degrade gracefully
+    ingest_documents = None
+    RAG_INGEST_AVAILABLE = False
+    RAG_INGEST_ERROR = exc
+else:
+    RAG_INGEST_ERROR = None
+
+try:
+    from publisher.instagram_stub import API_NOTES, generate_caption, schedule_post
+    INSTAGRAM_STUB_AVAILABLE = True
+except Exception as exc:  # pragma: no cover - optional integration
+    API_NOTES = {}
+    generate_caption = None
+    schedule_post = None
+    INSTAGRAM_STUB_AVAILABLE = False
+    INSTAGRAM_STUB_ERROR = exc
+else:
+    INSTAGRAM_STUB_ERROR = None
+
 # 🔍 NOVA IMPORTAÇÃO: File System Watcher
 try:
     from file_watcher import afi_watcher_service, inicializar_watcher_service
     WATCHER_AVAILABLE = True
 except ImportError:
     print("⚠️ Watchdog não disponível. Instale com: pip install watchdog")
     WATCHER_AVAILABLE = False
 
 # =================================================================================
 # CONTROLE DE ESTADO DE INICIALIZAÇÃO - SISTEMA ROBUSTO
 # =================================================================================
 if "system_ready" not in st.session_state:
     st.session_state.system_ready = False
 # Removido: inicialização manual do query_engine agora é feita via @st.cache_resource
 if "chat_engine" not in st.session_state:
     st.session_state.chat_engine = None
 # 🔍 NOVO: Estado do File Watcher
 if "watcher_initialized" not in st.session_state:
     st.session_state.watcher_initialized = False
 
 @st.cache_resource
 def setup_sistema_ia():
     """Configuração inicial do sistema de IA"""
     try:
         # Configurar embedding
@@ -126,58 +187,50 @@ def inicializar_rag(pasta_memoria="memoria"):
         # DIAGNÓSTICO DETALHADO - CAPTURANDO O ERRO COMPLETO
         print("=" * 60)
         print("--- ERRO DETALHADO AO INICIALIZAR O RAG ---")
         print(f"Tipo do erro: {type(e).__name__}")
         print(f"Mensagem: {str(e)}")
         print("Traceback completo:")
         traceback.print_exc()
         print("=" * 60)
         return None, None
 
 def criar_query_engine(pasta_memoria="memoria"):
     """Função mantida para compatibilidade - usa inicializar_rag()"""
     query_engine, chat_engine = inicializar_rag(pasta_memoria)
     return query_engine
 
 def verificar_status_sistema():
     """Verifica o status de todos os componentes do sistema"""
     status = {
         'ollama': verificar_conexao_ollama(),
         'rag': query_engine is not None,
         'chat_engine': st.session_state.chat_engine is not None,
         'models_count': 1 if verificar_conexao_ollama() else 0
     }
     return status
 
-# Configuração da página
-st.set_page_config(
-    page_title="AFI v3.0 - Assistente Finiti Inteligente",
-    page_icon="🏗️",
-    layout="wide",
-    initial_sidebar_state="expanded"
-)
-
 # CSS personalizado
 css = """
 <style>
 /* Estilo para o elemento fixo no rodapé */
 .fixed-bottom-center {
     position: fixed;
     bottom: 20px;
     left: 50%;
     transform: translateX(-50%);
     background-color: #262730;
     color: white;
     padding: 12px 24px;
     border-radius: 12px;
     box-shadow: 0 6px 16px rgba(0, 0, 0, 0.4);
     z-index: 1000;
     font-size: 14px;
     text-align: center;
     min-width: 220px;
     backdrop-filter: blur(10px);
 }
 
 /* Adiciona espaçamento inferior para o chat input */
 .stChatInput {
     margin-bottom: 100px !important;
 }
@@ -467,68 +520,93 @@ else:
                 placeholder="C:\\caminho\\para\\pasta\\local",
                 label_visibility="collapsed",
                 key="pasta_local"
             )
         
             if st.button("📁 Indexar Pasta Local", use_container_width=True):
                 if pasta_local and os.path.isdir(pasta_local):
                     try:
                         # Usar função tradicional
                         query_engine_local, chat_engine = inicializar_rag(pasta_local)
                         if query_engine_local and chat_engine:
                             st.session_state.chat_engine = chat_engine
                             st.success(f"✅ Pasta local indexada com sucesso!")
                             st.info(f"📂 Pasta: {pasta_local}")
                             st.warning("⚠️ Para usar a nova base, reinicie a aplicação para limpar o cache.")
                         else:
                             st.warning(f"⚠️ Pasta indexada, mas nenhum documento encontrado!")
                     except Exception as e:
                         st.error(f"❌ Erro ao indexar: {str(e)}")
                 elif pasta_local:
                     st.error("❌ Caminho inválido ou diretório não encontrado!")
                 else:
                     st.warning("⚠️ Por favor, insira um caminho válido!")
          
         with col2:
-             st.subheader("📊 Status da Base de Conhecimento")
-             
-             # Status dos engines
-             if st.session_state.chat_engine:
-                 st.success("🧠 **ChatEngine:** Ativo (com memória conversacional)")
-             elif query_engine:
-                 st.warning("🔍 **QueryEngine:** Ativo (sem memória conversacional)")
-             else:
-                 st.error("❌ **Nenhum engine ativo**")
-             
-             # 🔍 NOVA SEÇÃO: File System Watcher
-             st.markdown("---")
-             st.subheader("👁️ File System Watcher")
-             
-             if WATCHER_AVAILABLE:
-                 # Inicializar o watcher service se ainda não foi feito
-                 if not st.session_state.watcher_initialized:
-                     try:
+            st.subheader("⚙️ Operações da Memória")
+
+            if RAG_INGEST_AVAILABLE and ingest_documents:
+                if st.button("🔄 Atualizar Memória", use_container_width=True):
+                    try:
+                        with st.spinner("Atualizando base de conhecimento..."):
+                            ingest_result = ingest_documents()
+                    except Exception as exc:
+                        st.error(f"❌ Falha ao atualizar memória: {exc}")
+                    else:
+                        if ingest_result.get("ok"):
+                            docs = ingest_result.get("documents", 0)
+                            st.success(f"✅ Ingestão concluída com {docs} documento(s).")
+                            st.caption(f"📁 Fonte: {ingest_result.get('source')}")
+                            st.caption(f"💾 Persistência: {ingest_result.get('persist_dir')}")
+                        else:
+                            st.error("❌ Ingestão não foi concluída.")
+                            st.write(ingest_result)
+            else:
+                mensagem = "📦 Módulo de ingestão indisponível."
+                if RAG_INGEST_ERROR:
+                    mensagem += f" Detalhes: {RAG_INGEST_ERROR}"
+                st.warning(mensagem)
+
+            st.markdown("---")
+            st.subheader("📊 Status da Base de Conhecimento")
+
+            # Status dos engines
+            if st.session_state.chat_engine:
+                st.success("🧠 **ChatEngine:** Ativo (com memória conversacional)")
+            elif query_engine:
+                st.warning("🔍 **QueryEngine:** Ativo (sem memória conversacional)")
+            else:
+                st.error("❌ **Nenhum engine ativo**")
+
+            # 🔍 NOVA SEÇÃO: File System Watcher
+            st.markdown("---")
+            st.subheader("👁️ File System Watcher")
+
+            if WATCHER_AVAILABLE:
+                # Inicializar o watcher service se ainda não foi feito
+                if not st.session_state.watcher_initialized:
+                    try:
                          inicializar_watcher_service()
                          st.session_state.watcher_initialized = True
                          st.toast("✅ File System Watcher inicializado!", icon="👁️")
                      except Exception as e:
                          st.error(f"❌ Erro ao inicializar watcher: {str(e)}")
                  
                  # Status do watcher
                  if afi_watcher_service.is_running:
                      st.success("👁️ **Watcher:** Ativo (monitorando)")
                      
                      # Mostrar pastas monitoradas
                      pastas_monitoradas = afi_watcher_service.get_watched_folders()
                      if pastas_monitoradas:
                          st.write("📁 **Pastas monitoradas:**")
                          for pasta in pastas_monitoradas:
                              st.code(f"📂 {pasta}")
                      else:
                          st.info("📁 Nenhuma pasta sendo monitorada")
                      
                      # Controles do watcher
                      col_watcher1, col_watcher2 = st.columns(2)
                      
                      with col_watcher1:
                          if st.button("⏸️ Parar Watcher", use_container_width=True):
                              afi_watcher_service.stop()
@@ -602,51 +680,51 @@ else:
              # Botão para limpar memória
              st.markdown("---")
              if st.button("🗑️ Limpar Base de Conhecimento", use_container_width=True):
                  # Limpar apenas o chat_engine (query_engine é gerenciado pelo cache)
                  st.session_state.chat_engine = None
                  st.success("✅ Base de conhecimento limpa!")
                  st.info("💡 Para limpar completamente, reinicie a aplicação.")
                  st.rerun()
 
     # TELA DO ESTÚDIO DE IA
     elif st.session_state.view == 'Estúdio':
         st.title("🤖 Estúdio de IA AFI")
         st.markdown("### *Diretor de Arte Robô - Upload e Relaxe*")
         
         # Importar função de edição
         try:
             from editor_video import editar_video_story, criar_pastas_necessarias
             editor_disponivel = True
         except ImportError:
             editor_disponivel = False
             st.error("❌ Editor de vídeo não disponível. Verifique se o editor_video.py está presente.")
         
         if editor_disponivel:
             # Criar pastas necessárias
             criar_pastas_necessarias()
-            
+
             # Criar duas colunas
             col1, col2 = st.columns(2)
             
             with col1:
                 st.subheader("📹 Upload do Vídeo")
                 
                 # Upload de arquivo
                 video_upload = st.file_uploader("Faça o upload de um vídeo", type=["mp4", "mov", "avi"])
                 
                 # Salvar vídeo temporariamente se foi feito upload
                 video_path = None
                 if video_upload is not None:
                     # Criar pasta temporária se não existir
                     temp_dir = Path("temp_uploads")
                     temp_dir.mkdir(exist_ok=True)
                     
                     # Salvar arquivo temporariamente
                     video_path = temp_dir / video_upload.name
                     with open(video_path, "wb") as f:
                         f.write(video_upload.getbuffer())
                     
                     st.success(f"✅ Vídeo carregado: {video_upload.name}")
                     
                     # Mostrar informações do vídeo
                     try:
@@ -676,94 +754,140 @@ else:
                 # 🤖 PROCESSAMENTO COM DIRETOR DE ARTE ROBÔ
                 if gerar_video_btn and video_path:
                     with st.spinner("🤖 Diretor de Arte Robô trabalhando... A IA está analisando, criando e editando!"):
                         try:
                             # Importar a função do Diretor de Arte Robô
                             from core_logic import criar_video_propaganda_ia
                             
                             # Chamar o Diretor de Arte Robô
                             resultado = criar_video_propaganda_ia(str(video_path))
                             
                             # Verificar se foi bem-sucedido
                             if resultado and not resultado.startswith("❌") and not resultado.startswith("Erro"):
                                 st.session_state.video_processado = resultado
                                 st.success("🎉 Diretor de Arte Robô concluído! Vídeo criado com IA!")
                                 st.balloons()  # Celebração!
                                 st.rerun()
                             else:
                                 st.error(f"❌ {resultado}")
                                 
                         except Exception as e:
                             st.error(f"❌ Erro no Diretor de Arte Robô: {str(e)}")
                             st.info("💡 Verifique se todas as dependências estão instaladas (moviepy, whisper, etc.)")
             
             with col2:
                 st.subheader("Resultado")
-                
+
+                processed_video_path = getattr(st.session_state, "video_processado", None)
+
                 # Container para o vídeo
                 video_result_container = st.container()
-                
+
                 with video_result_container:
                     # Verificar se há vídeo processado
-                    if hasattr(st.session_state, 'video_processado') and st.session_state.video_processado:
-                        video_path = st.session_state.video_processado
-                        
-                        if os.path.exists(video_path):
+                    if processed_video_path:
+                        if os.path.exists(processed_video_path):
                             st.success("🎉 Vídeo editado pronto!")
-                            
+
                             # Mostrar vídeo
-                            with open(video_path, 'rb') as video_file:
+                            with open(processed_video_path, 'rb') as video_file:
                                 video_bytes = video_file.read()
                                 st.video(video_bytes)
-                            
+
                             # Botão de download
                             st.download_button(
                                 label="📥 Download do Vídeo",
                                 data=video_bytes,
-                                file_name=os.path.basename(video_path),
+                                file_name=os.path.basename(processed_video_path),
                                 mime="video/mp4"
                             )
-                            
+
                             # Informações do arquivo
-                            file_size = os.path.getsize(video_path) / (1024 * 1024)  # MB
-                            st.info(f"📁 Arquivo: {os.path.basename(video_path)} ({file_size:.1f} MB)")
-                            
+                            file_size = os.path.getsize(processed_video_path) / (1024 * 1024)  # MB
+                            st.info(f"📁 Arquivo: {os.path.basename(processed_video_path)} ({file_size:.1f} MB)")
+
                             # Botão para limpar resultado
                             if st.button("🗑️ Novo Vídeo"):
                                 if hasattr(st.session_state, 'video_processado'):
                                     del st.session_state.video_processado
                                 st.rerun()
                         else:
                             st.error("❌ Arquivo de vídeo não encontrado.")
                     else:
                         st.info("📹 Seu vídeo editado aparecerá aqui após o processamento.")
                         st.markdown("---")
                         st.markdown("**💡 Como usar:**")
                         st.markdown("1. Faça upload de um vídeo")
                         st.markdown("2. Digite o texto para o overlay")
                         st.markdown("3. Escolha uma música")
                         st.markdown("4. Clique em 'Gerar Vídeo Agora'")
+
+                st.markdown("---")
+                st.subheader("📣 Publicação (Stub)")
+
+                if INSTAGRAM_STUB_AVAILABLE and generate_caption and schedule_post:
+                    if "caption_context" not in st.session_state:
+                        st.session_state.caption_context = ""
+
+                    caption_context = st.text_area(
+                        "Contexto para a legenda",
+                        key="caption_context",
+                        help="Descreva o conteúdo para gerar uma legenda automática.",
+                    )
+
+                    if st.button("📝 Gerar Legenda (stub)", use_container_width=True):
+                        caption = generate_caption(caption_context)
+                        st.session_state.generated_caption = caption
+                        st.success("Legenda gerada!")
+                        st.write(caption)
+
+                    scheduled_caption = st.session_state.get("generated_caption", "")
+                    scheduled_date = st.date_input("Data de publicação", key="schedule_date")
+                    scheduled_time = st.time_input("Horário de publicação", key="schedule_time")
+
+                    if st.button("🗓️ Agendar (stub)", use_container_width=True):
+                        if not processed_video_path:
+                            st.error("Carregue ou gere um vídeo antes de agendar.")
+                        elif not scheduled_caption:
+                            st.error("Gere uma legenda antes de agendar.")
+                        else:
+                            from datetime import datetime
+
+                            when = datetime.combine(scheduled_date, scheduled_time)
+                            schedule_post(processed_video_path, scheduled_caption, when)
+                            st.success(f"Agendamento registrado para {when.isoformat()}.")
+                else:
+                    aviso = "Integração de publicação indisponível."
+                    if INSTAGRAM_STUB_ERROR:
+                        aviso += f" Detalhes: {INSTAGRAM_STUB_ERROR}"
+                    st.warning(aviso)
+
+                if API_NOTES:
+                    st.caption(
+                        "Integração futura: usar Graph API com variáveis de ambiente "
+                        + ", ".join(API_NOTES.get("required_env", []))
+                    )
         else:
             st.error("❌ Sistema de edição não disponível.")
 
 # Fixed bottom-center div element
 st.markdown(
     f'<div class="fixed-bottom-center">🏗️ AFI v3.0 - Sistema Robusto Ativo | Porta: {get_server_port()}</div>',
     unsafe_allow_html=True
 )
 
 # Informações do sistema no sidebar
 with st.sidebar:
     st.markdown("---")
     st.markdown("### ⚙️ Configuração do Sistema")
     st.info(f"🌐 **Porta Padrão:** {get_server_port()}")
     st.info(f"🔗 **URL:** {get_server_url()}")
     st.markdown("---")
     st.markdown("**📝 Nota:** Este sistema usa sempre a porta 8507 para evitar confusão.")
 
 
 def indexar_por_referencia(caminho_diretorio):
     """
     🔗 NOVA FUNCIONALIDADE: Indexação por referência
     Indexa arquivos diretamente de seus locais originais sem copiá-los
     """
     import traceback
diff --git a/data/Musicas/.gitkeep b/data/Musicas/.gitkeep
new file mode 100644
index 0000000000000000000000000000000000000000..e69de29bb2d1d6434b8b29ae775ad8c2e48c5391
diff --git a/data/Videos_Agendados/.gitkeep b/data/Videos_Agendados/.gitkeep
new file mode 100644
index 0000000000000000000000000000000000000000..e69de29bb2d1d6434b8b29ae775ad8c2e48c5391
diff --git a/data/Videos_Para_Editar/.gitkeep b/data/Videos_Para_Editar/.gitkeep
new file mode 100644
index 0000000000000000000000000000000000000000..e69de29bb2d1d6434b8b29ae775ad8c2e48c5391
diff --git a/docker-compose.yml b/docker-compose.yml
new file mode 100644
index 0000000000000000000000000000000000000000..ae4a656d63c26421505d827175b80e0ba87018ed
--- /dev/null
+++ b/docker-compose.yml
@@ -0,0 +1,27 @@
+version: "3.9"
+
+services:
+  app:
+    build: .
+    container_name: afi_app
+    env_file: .env
+    ports:
+      - "8507:8507"
+    volumes:
+      - ./data:/app/data
+      - ./logs:/app/logs
+      - ./knowledge_base:/app/knowledge_base
+    restart: unless-stopped
+
+  guardian:
+    build: .
+    container_name: afi_guardian
+    env_file: .env
+    command: ["python", "guardiao.py"]
+    depends_on:
+      - app
+    volumes:
+      - ./data:/app/data
+      - ./logs:/app/logs
+      - ./knowledge_base:/app/knowledge_base
+    restart: unless-stopped
diff --git a/editor_video.py b/editor_video.py
index 63460974a015a92c6d08ad9ed6b27475625533dd..0981fb4fab70fbe1becb69d5c64d412633fd5fb7 100644
--- a/editor_video.py
+++ b/editor_video.py
@@ -1,104 +1,176 @@
 #!/usr/bin/env python3
 """
 Editor de Vídeo para Stories de Redes Sociais
 Script robusto para automatizar a edição de vídeos usando MoviePy
 """
 
+import json
 import os
 import sys
 import random
 from pathlib import Path
-from moviepy.video.io.VideoFileClip import VideoFileClip
-from moviepy.audio.io.AudioFileClip import AudioFileClip
-from moviepy.video.VideoClip import TextClip
-from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
-from moviepy.audio.AudioClip import concatenate_audioclips
-
-# Configurar ImageMagick para Windows
 try:
-    import moviepy.config as config
-    imagemagick_path = r"C:\Program Files\ImageMagick-7.1.2-Q16-HDRI\magick.exe"
-    if os.path.exists(imagemagick_path):
-        config.change_settings({"IMAGEMAGICK_BINARY": imagemagick_path})
-except Exception:
-    pass  # Continua sem ImageMagick se houver erro
+    from dotenv import load_dotenv
+except ImportError:  # pragma: no cover - fallback for offline mode
+    def load_dotenv(*_args, **_kwargs):
+        return False
+
+load_dotenv()
+
+NO_DEPS = os.getenv("NO_DEPS", "0") == "1"
+
+if not NO_DEPS:
+    try:
+        from moviepy.video.io.VideoFileClip import VideoFileClip
+        from moviepy.audio.io.AudioFileClip import AudioFileClip
+        from moviepy.video.VideoClip import TextClip
+        from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
+        from moviepy.audio.AudioClip import concatenate_audioclips
+        import moviepy.config as config
+    except ImportError as exc:  # pragma: no cover - falha explícita no modo completo
+        print("[ERRO] MoviePy não está disponível. Configure o ambiente ou ative NO_DEPS=1.")
+        raise
+    else:
+        imagemagick_path = r"C:\Program Files\ImageMagick-7.1.2-Q16-HDRI\magick.exe"
+        if os.path.exists(imagemagick_path):
+            try:
+                config.change_settings({"IMAGEMAGICK_BINARY": imagemagick_path})
+            except Exception:
+                pass
+else:
+    VideoFileClip = None  # placeholders para type checkers
+    AudioFileClip = None
+    TextClip = None
+    CompositeVideoClip = None
+    concatenate_audioclips = None
+
+AFI_INPUT_DIR = Path(os.getenv("AFI_INPUT_DIR", "./data/Videos_Para_Editar")).expanduser()
+AFI_OUTPUT_DIR = Path(os.getenv("AFI_OUTPUT_DIR", "./data/Videos_Agendados")).expanduser()
+AFI_MUSIC_DIR = Path(os.getenv("AFI_MUSIC_DIR", "./data/Musicas")).expanduser()
+AFI_LOG_DIR = Path(os.getenv("AFI_LOG_DIR", "./logs")).expanduser()
+AFI_EDITED_DIR = AFI_OUTPUT_DIR
+
+for _path in {AFI_INPUT_DIR, AFI_OUTPUT_DIR, AFI_MUSIC_DIR, AFI_LOG_DIR}:
+    _path.mkdir(parents=True, exist_ok=True)
 
 def verificar_dependencias():
     """Verifica se todas as dependências estão disponíveis"""
+    if NO_DEPS:
+        print("[MODO] NO_DEPS=1 - executando sem MoviePy.")
+        return True
+
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
-        "Videos_Para_Editar",
-        "Videos_Editados", 
-        "Videos_Agendados",
-        "Musicas",
-        "Musicas/Instrumental",
-        "Musicas/Energetica",
-        "Musicas/Relaxante"
+        AFI_INPUT_DIR,
+        AFI_EDITED_DIR,
+        AFI_MUSIC_DIR,
+        AFI_MUSIC_DIR / "Instrumental",
+        AFI_MUSIC_DIR / "Energetica",
+        AFI_MUSIC_DIR / "Relaxante",
+        AFI_OUTPUT_DIR,
+        AFI_LOG_DIR,
     ]
-    
+
     for pasta in pastas:
-        Path(pasta).mkdir(parents=True, exist_ok=True)
-    
+        pasta.mkdir(parents=True, exist_ok=True)
+
     print("[INFO] Estrutura de pastas verificada/criada")
 
 def validar_arquivo(caminho, tipo="arquivo"):
     """Valida se um arquivo existe"""
-    if not os.path.exists(caminho):
-        print(f"[ERRO] Erro: {tipo} não encontrado: {caminho}")
-        return False
+    if os.path.exists(caminho):
+        return True
+
+    if NO_DEPS:
+        print(f"[SIMULAÇÃO] {tipo} '{caminho}' não encontrado. Continuando em modo NO_DEPS.")
+        return True
+
+    print(f"[ERRO] Erro: {tipo} não encontrado: {caminho}")
+    return False
+
+
+def _editar_video_dummy(caminho_video_original: str, frase_marketing: str, caminho_saida: str) -> bool:
+    """Cria um arquivo MP4 fictício e metadados JSON para simular a edição."""
+
+    destino = Path(caminho_saida)
+    destino.parent.mkdir(parents=True, exist_ok=True)
+
+    base_nome = destino.stem or "saida"
+    dummy_video = destino.parent / f"dummy_{base_nome}.mp4"
+    metadata_path = destino.parent / f"dummy_{base_nome}.json"
+
+    with open(dummy_video, "wb") as mp4:
+        mp4.write(os.urandom(512 * 1024))  # 0.5 MB
+
+    metadata = {
+        "origem_video": caminho_video_original,
+        "frase_marketing": frase_marketing,
+        "arquivo_dummy": dummy_video.name,
+        "modo": "NO_DEPS",
+        "tamanho_bytes": dummy_video.stat().st_size,
+    }
+
+    with open(metadata_path, "w", encoding="utf-8") as meta:
+        json.dump(metadata, meta, ensure_ascii=False, indent=2)
+
+    print(f"[SIMULAÇÃO] Vídeo dummy gerado em {dummy_video}")
+    print(f"[SIMULAÇÃO] Metadados salvos em {metadata_path}")
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
-    
+
+    if NO_DEPS:
+        return _editar_video_dummy(caminho_video_original, frase_marketing, caminho_saida)
+
     # Validar arquivos de entrada
     if not validar_arquivo(caminho_video_original, "Vídeo"):
         return False
     if not validar_arquivo(caminho_musica, "Música"):
         return False
-    
+
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
@@ -177,159 +249,164 @@ def editar_video_story(caminho_video_original: str, caminho_musica: str, frase_m
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
 
-def listar_videos(pasta_videos="Videos_Para_Editar"):
+def listar_videos(pasta_videos=None):
     """Lista vídeos disponíveis na pasta"""
-    if not os.path.exists(pasta_videos):
+    pasta_videos = Path(pasta_videos) if pasta_videos else AFI_INPUT_DIR
+
+    if not pasta_videos.exists():
         return []
-    
+
     extensoes_video = ['.mp4', '.mov', '.avi', '.mkv']
     videos = []
-    
+
     for arquivo in os.listdir(pasta_videos):
         if any(arquivo.lower().endswith(ext) for ext in extensoes_video):
             videos.append(arquivo)
-    
+
     if videos:
         print(f"\n[INFO] Vídeos em {pasta_videos}:")
         for i, video in enumerate(videos, 1):
             print(f"  {i}. {video}")
     else:
         print(f"\n[INFO] Nenhum vídeo encontrado em {pasta_videos}")
-    
+
     return videos
 
-def listar_musicas(pasta_musicas="Musicas"):
+def listar_musicas(pasta_musicas=None):
     """Lista músicas disponíveis na pasta"""
-    if not os.path.exists(pasta_musicas):
+    pasta_musicas = Path(pasta_musicas) if pasta_musicas else AFI_MUSIC_DIR
+
+    if not pasta_musicas.exists():
         return []
-    
+
     extensoes_audio = ['.mp3', '.wav', '.m4a', '.aac']
     musicas = []
-    
+
     for arquivo in os.listdir(pasta_musicas):
         if any(arquivo.lower().endswith(ext) for ext in extensoes_audio):
             musicas.append(arquivo)
-    
+
     if musicas:
         print(f"\n[INFO] Músicas em {pasta_musicas}:")
         for i, musica in enumerate(musicas, 1):
             print(f"  {i}. {musica}")
     else:
         print(f"\n[INFO] Nenhuma música encontrada em {pasta_musicas}")
-    
+
     return musicas
 
 def listar_arquivos_disponiveis():
     """Lista vídeos e músicas disponíveis nas pastas"""
     print("\n📂 Arquivos disponíveis:")
-    
+
     # Listar vídeos
-    pasta_videos = "Videos_Para_Editar"
-    if os.path.exists(pasta_videos):
+    pasta_videos = AFI_INPUT_DIR
+    if pasta_videos.exists():
         videos = [f for f in os.listdir(pasta_videos) if f.lower().endswith(('.mp4', '.avi', '.mov', '.mkv'))]
         if videos:
             print(f"\n🎬 Vídeos em {pasta_videos}:")
             for i, video in enumerate(videos, 1):
                 print(f"  {i}. {video}")
         else:
             print(f"\n🎬 Nenhum vídeo encontrado em {pasta_videos}")
-    
+
     # Listar músicas
-    pasta_musicas = "Musicas"
-    if os.path.exists(pasta_musicas):
+    pasta_musicas = AFI_MUSIC_DIR
+    if pasta_musicas.exists():
         musicas = []
         for root, dirs, files in os.walk(pasta_musicas):
             for file in files:
                 if file.lower().endswith(('.mp3', '.wav', '.aac', '.m4a')):
                     musicas.append(os.path.relpath(os.path.join(root, file)))
-        
+
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
-    
-    if not saida.startswith("Videos_Editados/"):
-        saida = f"Videos_Editados/{saida}"
-    
-    return editar_video_story(video, musica, texto, saida, duracao_maxima=60)
+
+    saida_path = Path(saida)
+    if not saida_path.is_absolute():
+        saida_path = AFI_OUTPUT_DIR / saida_path
+
+    return editar_video_story(video, musica, texto, str(saida_path))
 
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
-            video_teste = "Videos_Para_Editar/teste.mp4"
-            musica_teste = "Musicas/musica.mp3"
+            video_teste = str(AFI_INPUT_DIR / "teste.mp4")
+            musica_teste = str(AFI_MUSIC_DIR / "musica.mp3")
             texto_exemplo = "Produto Incrível da Finiti!"
-            video_final = "Videos_Editados/resultado_teste.mp4"
+            video_final = str(AFI_OUTPUT_DIR / "resultado_teste.mp4")
             
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
diff --git a/guardiao.py b/guardiao.py
index c465f66783c6b504987345e5b36c1072b8c2cd1c..ce93d317aa17b191162b8eadc2aa0feeb6af69f5 100644
--- a/guardiao.py
+++ b/guardiao.py
@@ -21,125 +21,164 @@ def gerar_nome_arquivo_agendado():
     Returns:
         str: Nome do arquivo no formato "DD-MM-AA.Descricao.mp4"
     """
     agora = datetime.now()
     
     # Determinar descrição baseada no dia da semana e hora
     if agora.weekday() == 5 or agora.weekday() == 6:  # Sábado (5) ou Domingo (6)
         descricao = "Bomdia"
     else:  # Dia de semana
         if agora.hour < 12:
             descricao = "Bomdia"
         else:
             descricao = "Encerramento"
     
     # Formatar nome do arquivo
     nome_arquivo = f"{agora.strftime('%d-%m-%y')}.{descricao}.mp4"
     return nome_arquivo
 
 import os
 import sys
 import time
 import random
 import subprocess
 from pathlib import Path
 from datetime import datetime
-from watchdog.observers import Observer
-from watchdog.events import FileSystemEventHandler
+try:
+    from dotenv import load_dotenv
+except ImportError:  # pragma: no cover - fallback for offline mode
+    def load_dotenv(*_args, **_kwargs):
+        return False
+
+load_dotenv()
+
+NO_DEPS = os.getenv("NO_DEPS", "0") == "1"
+
+if not NO_DEPS:
+    try:
+        from watchdog.observers import Observer
+        from watchdog.events import FileSystemEventHandler
+    except ImportError:
+        print("[AVISO] watchdog não encontrado. Ativando fallback de polling.")
+        NO_DEPS = True
+
+if NO_DEPS:
+    Observer = None  # type: ignore
+
+    class FileSystemEventHandler:  # type: ignore
+        """Stub mínima para reutilizar o handler no modo simulado."""
+
+        pass
 
 # Importar função de IA para gerar frases de marketing
 try:
     from core_logic import processar_prompt_geral
     IA_DISPONIVEL = True
 except ImportError:
     IA_DISPONIVEL = False
     print("[AVISO] IA não disponível - usando texto personalizado padrão")
 
+AFI_INPUT_DIR = Path(os.getenv("AFI_INPUT_DIR", "./data/Videos_Para_Editar")).expanduser()
+AFI_OUTPUT_DIR = Path(os.getenv("AFI_OUTPUT_DIR", "./data/Videos_Agendados")).expanduser()
+AFI_MUSIC_DIR = Path(os.getenv("AFI_MUSIC_DIR", "./data/Musicas")).expanduser()
+AFI_LOG_DIR = Path(os.getenv("AFI_LOG_DIR", "./logs")).expanduser()
+
+for _path in {AFI_INPUT_DIR, AFI_OUTPUT_DIR, AFI_MUSIC_DIR, AFI_LOG_DIR}:
+    _path.mkdir(parents=True, exist_ok=True)
+
 class GuardiaoVideoHandler(FileSystemEventHandler):
     """Manipulador de eventos para detectar novos vídeos"""
     
     def __init__(self, pasta_musicas, pasta_saida):
         self.pasta_musicas = pasta_musicas
         self.pasta_saida = pasta_saida
         self.extensoes_video = {'.mp4', '.mov', '.avi', '.mkv', '.wmv', '.flv', '.webm'}
         self.processando = set()  # Evita processamento duplo
         
     def on_created(self, event):
         """Evento disparado quando um novo arquivo é criado"""
         if event.is_directory:
             return
             
         caminho_arquivo = Path(event.src_path)
         
         # Verifica se é um arquivo de vídeo
         if caminho_arquivo.suffix.lower() in self.extensoes_video:
             self.processar_novo_video(caminho_arquivo)
     
     def processar_novo_video(self, caminho_video):
         """Processa um novo vídeo detectado"""
         nome_video = caminho_video.name
         
         # Evita processamento duplo
         if nome_video in self.processando:
             return
             
         self.processando.add(nome_video)
         
         try:
             print(f"[DETECTADO] NOVO VÍDEO DETECTADO: {nome_video}")
             print("[INFO] Aguardando conclusão do upload...")
             
             # Aguarda alguns segundos para garantir que o arquivo foi copiado completamente
             time.sleep(3)
             
             # Verifica se o arquivo ainda existe e não está sendo usado
             if not self.arquivo_disponivel(caminho_video):
                 print(f"[AVISO] Arquivo {nome_video} ainda está sendo copiado. Aguardando...")
                 time.sleep(5)
                 
             if not caminho_video.exists():
                 print(f"[ERRO] Arquivo {nome_video} não encontrado. Cancelando processamento.")
                 return
                 
             # Escolhe música (personalizada ou aleatória)
             if MUSICA_PERSONALIZADA:
                 musica_escolhida = self.pasta_musicas / MUSICA_PERSONALIZADA
                 if not musica_escolhida.exists():
-                    print(f"[ERRO] Música personalizada não encontrada: {MUSICA_PERSONALIZADA}")
+                    print(f"[ERRO] Música personalizada não encontrada em {self.pasta_musicas}: {MUSICA_PERSONALIZADA}")
                     print("[INFO] Usando música aleatória...")
                     musicas_disponiveis = list(self.pasta_musicas.glob("*.mp3"))
                     if not musicas_disponiveis:
-                        print("[ERRO] Nenhuma música encontrada na pasta Musicas!")
-                        return
-                    musica_escolhida = random.choice(musicas_disponiveis)
+                        if NO_DEPS:
+                            musica_escolhida = self.pasta_musicas / "dummy.mp3"
+                        else:
+                            print(f"[ERRO] Nenhuma música encontrada na pasta {self.pasta_musicas}!")
+                            return
+                    else:
+                        musica_escolhida = random.choice(musicas_disponiveis)
             else:
                 # Escolhe uma música aleatória
                 musicas_disponiveis = list(self.pasta_musicas.glob("*.mp3"))
                 if not musicas_disponiveis:
-                    print("[ERRO] Nenhuma música encontrada na pasta Musicas!")
-                    return
-                musica_escolhida = random.choice(musicas_disponiveis)
+                    if NO_DEPS:
+                        musica_escolhida = self.pasta_musicas / "dummy.mp3"
+                    else:
+                        print(f"[ERRO] Nenhuma música encontrada na pasta {self.pasta_musicas}!")
+                        return
+                else:
+                    musica_escolhida = random.choice(musicas_disponiveis)
                 
             # 1. Gerar frase de marketing usando IA
             print("[INFO] Gerando frase de marketing com IA...")
             if IA_DISPONIVEL:
                 try:
                     prompt_ia = "Crie uma frase de marketing impactante e persuasiva para um produto da Finiti. A frase deve ser curta, chamativa e motivar a compra. Responda apenas com a frase, sem explicações."
                     resposta_ia = processar_prompt_geral(prompt_ia)
                     if resposta_ia and 'response' in resposta_ia:
                         frase_marketing = resposta_ia['response'].strip()
                         print(f"[IA] Frase gerada: {frase_marketing}")
                     else:
                         frase_marketing = TEXTO_PERSONALIZADO
                         print(f"[AVISO] IA não respondeu adequadamente. Usando texto padrão: {frase_marketing}")
                 except Exception as e:
                     frase_marketing = TEXTO_PERSONALIZADO
                     print(f"[ERRO] Erro na IA: {e}. Usando texto padrão: {frase_marketing}")
             else:
                 frase_marketing = TEXTO_PERSONALIZADO
                 print(f"[INFO] Usando texto padrão: {frase_marketing}")
             
             # 2. Gerar nome do arquivo baseado em data/hora
             nome_arquivo_agendado = gerar_nome_arquivo_agendado()
             arquivo_saida = self.pasta_saida / nome_arquivo_agendado
             print(f"[INFO] Nome do arquivo de saída: {nome_arquivo_agendado}")
             
@@ -158,51 +197,51 @@ class GuardiaoVideoHandler(FileSystemEventHandler):
             
             if sucesso:
                 print(f"[SUCESSO] SUCESSO! Vídeo processado: {arquivo_saida.name}")
                 print("[INFO] Guardião pronto para o próximo vídeo!")
             else:
                 print(f"[ERRO] ERRO no processamento de {nome_video}")
                 
         except Exception as e:
             print(f"[ERRO] ERRO INESPERADO ao processar {nome_video}: {e}")
         finally:
             # Remove da lista de processamento
             self.processando.discard(nome_video)
             print("-" * 50)
     
     def arquivo_disponivel(self, caminho_arquivo):
         """Verifica se o arquivo está disponível para leitura"""
         try:
             # Tenta abrir o arquivo para verificar se não está sendo usado
             with open(caminho_arquivo, 'rb') as f:
                 f.read(1)
             return True
         except (PermissionError, IOError):
             return False
     
     def escolher_musica_aleatoria(self):
-        """Escolhe uma música aleatória da pasta Musicas"""
+        """Escolhe uma música aleatória na pasta de músicas configurada"""
         extensoes_audio = {'.mp3', '.wav', '.aac', '.m4a', '.ogg'}
         
         # Lista todas as músicas disponíveis
         musicas = []
         
         # Busca na pasta principal
         for arquivo in self.pasta_musicas.iterdir():
             if arquivo.is_file() and arquivo.suffix.lower() in extensoes_audio:
                 musicas.append(arquivo)
         
         # Busca nas subpastas (Energetica, Instrumental, Relaxante)
         for subpasta in self.pasta_musicas.iterdir():
             if subpasta.is_dir():
                 for arquivo in subpasta.iterdir():
                     if arquivo.is_file() and arquivo.suffix.lower() in extensoes_audio:
                         musicas.append(arquivo)
         
         if not musicas:
             return None
             
         # Escolhe uma música aleatória
         return random.choice(musicas)
     
     def chamar_editor_video(self, video_entrada, musica, texto, video_saida):
         """Chama o editor_video.py usando subprocess"""
@@ -227,120 +266,158 @@ class GuardiaoVideoHandler(FileSystemEventHandler):
                 timeout=300  # Timeout de 5 minutos
             )
             
             if resultado.returncode == 0:
                 print("[SUCESSO] Editor executado com sucesso!")
                 if resultado.stdout:
                     print("[INFO] Saída:", resultado.stdout.strip())
                 return True
             else:
                 print(f"[ERRO] Editor falhou com código: {resultado.returncode}")
                 if resultado.stderr:
                     print("[ERRO] Erro:", resultado.stderr.strip())
                 return False
                 
         except subprocess.TimeoutExpired:
             print("[TIMEOUT] TIMEOUT: Processamento demorou mais de 5 minutos")
             return False
         except Exception as e:
             print(f"[ERRO] Erro ao executar editor: {e}")
             return False
 
 class GuardiaoAutonomo:
     """Classe principal do Guardião Autônomo"""
     
     def __init__(self):
-        self.pasta_entrada = Path("Videos_Para_Editar")
-        self.pasta_musicas = Path("Musicas")
-        self.pasta_saida = Path("Videos_Editados")
+        self.pasta_entrada = AFI_INPUT_DIR
+        self.pasta_musicas = AFI_MUSIC_DIR
+        self.pasta_saida = AFI_OUTPUT_DIR
         self.observer = None
         
     def verificar_estrutura(self):
         """Verifica e cria a estrutura de pastas necessária"""
         print("📁 Verificando estrutura de pastas...")
         
         for pasta in [self.pasta_entrada, self.pasta_musicas, self.pasta_saida]:
             if not pasta.exists():
                 pasta.mkdir(parents=True, exist_ok=True)
                 print(f"✅ Pasta criada: {pasta}")
             else:
                 print(f"✅ Pasta encontrada: {pasta}")
     
     def verificar_dependencias(self):
         """Verifica se o editor_video.py existe"""
         editor_path = Path("editor_video.py")
         if not editor_path.exists():
             print("❌ ERRO: editor_video.py não encontrado!")
             print("💡 Certifique-se de que o editor_video.py está na mesma pasta")
             return False
         
         print("✅ editor_video.py encontrado")
         return True
     
     def iniciar_monitoramento(self):
         """Inicia o monitoramento da pasta de entrada"""
         print("🤖 GUARDIÃO AUTÔNOMO - INICIANDO...")
         print("=" * 50)
-        
+
         # Verificações iniciais
         if not self.verificar_dependencias():
             return False
-            
+
         self.verificar_estrutura()
-        
+
         # Configura o manipulador de eventos
         event_handler = GuardiaoVideoHandler(self.pasta_musicas, self.pasta_saida)
-        
-        # Configura o observador
+
+        if NO_DEPS or Observer is None:
+            print("[SIMULAÇÃO] Monitorando via polling (watchdog indisponível ou NO_DEPS=1).")
+            return self._loop_polling(event_handler)
+
+        # Configura o observador real
         self.observer = Observer()
         self.observer.schedule(
             event_handler,
             str(self.pasta_entrada),
             recursive=False
         )
-        
+
         # Inicia o monitoramento
         self.observer.start()
-        
+
         print(f"👁️ MONITORANDO: {self.pasta_entrada.absolute()}")
         print("🎵 Músicas disponíveis:")
         self.listar_musicas()
         print("=" * 50)
         print("🚀 GUARDIÃO ATIVO! Aguardando novos vídeos...")
         print("💡 Para parar, pressione Ctrl+C")
         print("=" * 50)
-        
+
         try:
             while True:
                 time.sleep(1)
         except KeyboardInterrupt:
             print("\n🛑 Parando o Guardião...")
             self.observer.stop()
-            
+
         self.observer.join()
         print("✅ Guardião finalizado!")
         return True
+
+    def _loop_polling(self, event_handler):
+        """Monitoramento simples quando watchdog não está disponível."""
+
+        print(f"👁️ MONITORANDO (polling): {self.pasta_entrada.absolute()}")
+        print("🕒 Intervalo: 2 segundos")
+        print("=" * 50)
+        print("🚀 GUARDIÃO ATIVO (modo simulado)! Aguardando novos vídeos...")
+        print("💡 Para parar, pressione Ctrl+C")
+        print("=" * 50)
+
+        arquivos_processados = set()
+
+        try:
+            while True:
+                for arquivo in self.pasta_entrada.iterdir():
+                    if not arquivo.is_file():
+                        continue
+
+                    if arquivo.suffix.lower() not in event_handler.extensoes_video:
+                        continue
+
+                    if arquivo.name in arquivos_processados:
+                        continue
+
+                    arquivos_processados.add(arquivo.name)
+                    event_handler.processar_novo_video(arquivo)
+
+                time.sleep(2)
+        except KeyboardInterrupt:
+            print("\n🛑 Parando o Guardião (polling)...")
+
+        print("✅ Guardião finalizado!")
+        return True
     
     def listar_musicas(self):
         """Lista as músicas disponíveis"""
         extensoes_audio = {'.mp3', '.wav', '.aac', '.m4a', '.ogg'}
         count = 0
         
         # Músicas na pasta principal
         for arquivo in self.pasta_musicas.iterdir():
             if arquivo.is_file() and arquivo.suffix.lower() in extensoes_audio:
                 print(f"   🎵 {arquivo.name}")
                 count += 1
         
         # Músicas nas subpastas
         for subpasta in self.pasta_musicas.iterdir():
             if subpasta.is_dir():
                 for arquivo in subpasta.iterdir():
                     if arquivo.is_file() and arquivo.suffix.lower() in extensoes_audio:
                         print(f"   🎵 {subpasta.name}/{arquivo.name}")
                         count += 1
         
         if count == 0:
             print("   ⚠️ Nenhuma música encontrada!")
         else:
             print(f"   📊 Total: {count} música(s)")
 
diff --git a/guardiao_midia.py b/guardiao_midia.py
index ace2207690e795e9e63d2844f6079ee4ca40da93..04cb180ed8eb56ef9ac375090a8acc2cda8b4319 100644
--- a/guardiao_midia.py
+++ b/guardiao_midia.py
@@ -1,113 +1,146 @@
 #!/usr/bin/env python3
 """
 👁️ AFI v4.0 - Guardião de Mídia Social
 O "Guardião" do Agente de Mídia Social - monitora pastas e aciona o fluxo automatizado
 
 Este módulo implementa o sistema de monitoramento que detecta novos vídeos
 e aciona automaticamente o processo de edição com IA.
 """
 
 import os
 import time
 import logging
 from pathlib import Path
-from watchdog.observers import Observer
-from watchdog.events import FileSystemEventHandler
 import random
+try:
+    from dotenv import load_dotenv
+except ImportError:  # pragma: no cover - fallback for offline mode
+    def load_dotenv(*_args, **_kwargs):
+        return False
 from editor_video import editar_video_story
 
-# Configurar logging
 logging.basicConfig(
     level=logging.INFO,
     format='%(asctime)s - %(levelname)s - %(message)s'
 )
 logger = logging.getLogger(__name__)
 
+load_dotenv()
+
+NO_DEPS = os.getenv("NO_DEPS", "0") == "1"
+
+if not NO_DEPS:
+    try:
+        from watchdog.observers import Observer
+        from watchdog.events import FileSystemEventHandler
+    except ImportError:
+        logging.warning("watchdog não encontrado. Ativando modo de polling simples.")
+        NO_DEPS = True
+
+if NO_DEPS:
+    Observer = None  # type: ignore
+
+    class FileSystemEventHandler:  # type: ignore
+        """Stub mínima para reutilizar o handler no modo simulado."""
+
+        pass
+
+AFI_INPUT_DIR = Path(os.getenv("AFI_INPUT_DIR", "./data/Videos_Para_Editar")).expanduser()
+AFI_OUTPUT_DIR = Path(os.getenv("AFI_OUTPUT_DIR", "./data/Videos_Agendados")).expanduser()
+AFI_MUSIC_DIR = Path(os.getenv("AFI_MUSIC_DIR", "./data/Musicas")).expanduser()
+AFI_LOG_DIR = Path(os.getenv("AFI_LOG_DIR", "./logs")).expanduser()
+
+for _path in {AFI_INPUT_DIR, AFI_OUTPUT_DIR, AFI_MUSIC_DIR, AFI_LOG_DIR}:
+    _path.mkdir(parents=True, exist_ok=True)
+
 class GuardiaoMidiaHandler(FileSystemEventHandler):
     """
     Handler que processa eventos de arquivo na pasta monitorada.
     """
     
     def __init__(self, afi_integration=None):
         """
         Inicializa o handler do Guardião.
         
         Args:
             afi_integration: Função para integração com AFI (opcional)
         """
         self.afi_integration = afi_integration
         self.extensoes_video = {'.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm'}
         self.extensoes_audio = {'.mp3', '.wav', '.aac', '.ogg', '.m4a'}
         
     def on_created(self, event):
         """
         Chamado quando um novo arquivo é criado na pasta monitorada.
         """
         if event.is_directory:
             return
             
         arquivo = Path(event.src_path)
         
         # Verificar se é um arquivo de vídeo
         if arquivo.suffix.lower() in self.extensoes_video:
             logger.info(f"🎬 Novo vídeo detectado: {arquivo.name}")
             self.processar_novo_video(arquivo)
     
     def processar_novo_video(self, caminho_video):
         """
         Processa um novo vídeo detectado pelo Guardião.
         
         Args:
             caminho_video (Path): Caminho para o novo vídeo
         """
         try:
             logger.info(f"🧠 Analisando vídeo com AFI: {caminho_video.name}")
             
             # Simular consulta ao AFI (aqui você integraria com o sistema RAG real)
             frase_impacto, estilo_musica = self.consultar_afi(caminho_video)
             
             # Selecionar música aleatória do estilo sugerido
             musica_selecionada = self.selecionar_musica(estilo_musica)
             
             if not musica_selecionada:
-                logger.warning(f"⚠️ Nenhuma música encontrada para o estilo: {estilo_musica}")
-                return
+                if NO_DEPS:
+                    musica_selecionada = AFI_MUSIC_DIR / "dummy.mp3"
+                else:
+                    logger.warning(f"⚠️ Nenhuma música encontrada para o estilo: {estilo_musica}")
+                    return
             
             # Gerar nome do arquivo de saída
             nome_saida = self.gerar_nome_saida(caminho_video, frase_impacto)
-            caminho_saida = Path("C:/AFI/Videos_Agendados") / nome_saida
+            caminho_saida = AFI_OUTPUT_DIR / nome_saida
             
             logger.info(f"🎵 Música selecionada: {musica_selecionada.name}")
             logger.info(f"📝 Frase de impacto: {frase_impacto}")
             logger.info(f"🎯 Iniciando edição automatizada...")
             
             # Executar edição automatizada
             sucesso = editar_video_story(
                 caminho_video_original=str(caminho_video),
-                caminho_musica=str(musica_selecionada),
-                texto_overlay=frase_impacto,
+                caminho_musica=str(musica_selecionada) if musica_selecionada else "",
+                frase_marketing=frase_impacto,
                 caminho_saida=str(caminho_saida)
             )
             
             if sucesso:
                 logger.info(f"✅ Vídeo editado com sucesso: {caminho_saida.name}")
                 logger.info(f"📁 Vídeo salvo em: {caminho_saida}")
             else:
                 logger.error(f"❌ Erro na edição do vídeo: {caminho_video.name}")
                 
         except Exception as e:
             logger.error(f"❌ Erro ao processar vídeo {caminho_video.name}: {str(e)}")
     
     def consultar_afi(self, caminho_video):
         """
         Consulta o AFI para gerar frase de impacto e sugerir estilo musical.
         
         Args:
             caminho_video (Path): Caminho do vídeo para análise
             
         Returns:
             tuple: (frase_impacto, estilo_musica)
         """
         # TODO: Integrar com o sistema RAG real do AFI
         # Por enquanto, vamos simular respostas baseadas no nome do arquivo
         
@@ -143,149 +176,179 @@ class GuardiaoMidiaHandler(FileSystemEventHandler):
             frase = random.choice(frases_motivacionais)
             estilo = 'Rock'
         elif any(palavra in nome_arquivo for palavra in ['tecnico', 'manual', 'tutorial', 'airless']):
             frase = random.choice(frases_tecnicas)
             estilo = 'Instrumental'
         elif any(palavra in nome_arquivo for palavra in ['venda', 'promocao', 'oferta', 'produto']):
             frase = random.choice(frases_vendas)
             estilo = 'Pop'
         else:
             frase = random.choice(frases_motivacionais)
             estilo = 'Calma'
         
         logger.info(f"🧠 AFI sugeriu: Frase='{frase}', Estilo='{estilo}'")
         return frase, estilo
     
     def selecionar_musica(self, estilo):
         """
         Seleciona uma música aleatória do estilo especificado.
         
         Args:
             estilo (str): Estilo musical (Rock, Pop, Calma, etc.)
             
         Returns:
             Path: Caminho para a música selecionada ou None
         """
-        pasta_musicas = Path(f"C:/AFI/Musicas/{estilo}")
+        pasta_musicas = AFI_MUSIC_DIR / estilo
         
         if not pasta_musicas.exists():
+            if NO_DEPS:
+                return AFI_MUSIC_DIR / f"{estilo.lower()}_dummy.mp3"
             logger.warning(f"⚠️ Pasta de músicas não encontrada: {pasta_musicas}")
             return None
         
         # Buscar arquivos de música na pasta
         musicas = [
             arquivo for arquivo in pasta_musicas.iterdir()
             if arquivo.suffix.lower() in self.extensoes_audio
         ]
         
         if not musicas:
+            if NO_DEPS:
+                return pasta_musicas / "dummy.mp3"
             logger.warning(f"⚠️ Nenhuma música encontrada em: {pasta_musicas}")
             return None
         
         # Selecionar música aleatória
         musica_selecionada = random.choice(musicas)
         return musica_selecionada
     
     def gerar_nome_saida(self, caminho_video, frase_impacto):
         """
         Gera nome para o arquivo de saída baseado no vídeo original e frase.
         
         Args:
             caminho_video (Path): Caminho do vídeo original
             frase_impacto (str): Frase de impacto gerada
             
         Returns:
             str: Nome do arquivo de saída
         """
         # Remover emojis e caracteres especiais da frase para o nome do arquivo
         frase_limpa = ''.join(c for c in frase_impacto if c.isalnum() or c.isspace())
         frase_limpa = frase_limpa.strip().replace(' ', '_')[:20]  # Limitar tamanho
         
         # Gerar timestamp para agendamento (exemplo: próxima hora)
         timestamp = time.strftime("%Y-%m-%d_%H-%M", time.localtime(time.time() + 3600))
         
         nome_original = caminho_video.stem
         nome_saida = f"{timestamp}_post_{nome_original}_{frase_limpa}.mp4"
         
         return nome_saida
 
 class GuardiaoMidia:
     """
     Classe principal do Guardião de Mídia Social.
     """
     
-    def __init__(self, pasta_monitorada="C:/AFI/Videos_Para_Editar"):
+    def __init__(self, pasta_monitorada=None):
         """
         Inicializa o Guardião.
         
         Args:
             pasta_monitorada (str): Pasta a ser monitorada
         """
-        self.pasta_monitorada = Path(pasta_monitorada)
-        self.observer = Observer()
+        self.pasta_monitorada = Path(pasta_monitorada) if pasta_monitorada else AFI_INPUT_DIR
+        self.observer = Observer() if (not NO_DEPS and Observer is not None) else None
         self.handler = GuardiaoMidiaHandler()
-        
+
         # Criar pasta se não existir
         self.pasta_monitorada.mkdir(parents=True, exist_ok=True)
-        
+
     def iniciar(self):
         """
         Inicia o monitoramento da pasta.
         """
         logger.info(f"👁️ Guardião iniciado - Monitorando: {self.pasta_monitorada}")
         logger.info("🎬 Aguardando novos vídeos...")
-        
+
+        if self.observer is None:
+            logger.info("⚙️ Modo polling simples (watchdog indisponível ou NO_DEPS=1). Intervalo: 2s")
+            return self._loop_polling()
+
         self.observer.schedule(
             self.handler,
             str(self.pasta_monitorada),
             recursive=False
         )
-        
+
         self.observer.start()
-        
+
         try:
             while True:
                 time.sleep(1)
         except KeyboardInterrupt:
             logger.info("⏹️ Parando Guardião...")
             self.observer.stop()
-        
+
         self.observer.join()
         logger.info("✅ Guardião parado com sucesso!")
 
+    def _loop_polling(self):
+        """Monitoramento simplificado sem watchdog."""
+
+        arquivos_processados = set()
+
+        try:
+            while True:
+                for arquivo in self.pasta_monitorada.iterdir():
+                    if not arquivo.is_file():
+                        continue
+
+                    if arquivo.suffix.lower() not in self.handler.extensoes_video:
+                        continue
+
+                    if arquivo.name in arquivos_processados:
+                        continue
+
+                    arquivos_processados.add(arquivo.name)
+                    self.handler.processar_novo_video(arquivo)
+
+                time.sleep(2)
+        except KeyboardInterrupt:
+            logger.info("⏹️ Parando Guardião (polling)...")
+
+        logger.info("✅ Guardião parado com sucesso!")
+
 def main():
     """
     Função principal para executar o Guardião.
     """
     print("👁️ AFI v4.0 - Guardião de Mídia Social")
     print("=" * 50)
     print("🎯 Sistema de Monitoramento Automatizado")
     print()
     
     # Verificar se as pastas necessárias existem
-    pastas_necessarias = [
-        "C:/AFI/Videos_Para_Editar",
-        "C:/AFI/Videos_Agendados",
-        "C:/AFI/Musicas"
-    ]
-    
+    pastas_necessarias = [AFI_INPUT_DIR, AFI_OUTPUT_DIR, AFI_MUSIC_DIR]
+
     for pasta in pastas_necessarias:
-        if not Path(pasta).exists():
+        if not pasta.exists():
             logger.warning(f"⚠️ Pasta não encontrada: {pasta}")
             logger.info("💡 Execute 'python editor_video.py' primeiro para criar as pastas")
     
     # Inicializar e executar o Guardião
     guardiao = GuardiaoMidia()
     
     print(f"📁 Pasta monitorada: {guardiao.pasta_monitorada}")
     print("📝 Para testar:")
-    print("   1. Adicione músicas nas pastas C:/AFI/Musicas/[Rock|Pop|Calma|Instrumental]")
-    print("   2. Copie um vídeo para C:/AFI/Videos_Para_Editar")
+    print(f"   1. Adicione músicas nas pastas {AFI_MUSIC_DIR}/[Rock|Pop|Calma|Instrumental]")
+    print(f"   2. Copie um vídeo para {AFI_INPUT_DIR}")
     print("   3. O Guardião detectará e processará automaticamente!")
     print()
     print("⏹️ Pressione Ctrl+C para parar")
     print()
     
     guardiao.iniciar()
 
 if __name__ == '__main__':
     main()
\ No newline at end of file
diff --git a/knowledge_base/fineti_intro.txt b/knowledge_base/fineti_intro.txt
new file mode 100644
index 0000000000000000000000000000000000000000..6d6f0b81e6aabd4ca0cd02983abee22169752808
--- /dev/null
+++ b/knowledge_base/fineti_intro.txt
@@ -0,0 +1 @@
+A Finiti vende equipamentos para pisos. Este documento serve para testes do RAG.
\ No newline at end of file
diff --git a/logs/.gitkeep b/logs/.gitkeep
new file mode 100644
index 0000000000000000000000000000000000000000..e69de29bb2d1d6434b8b29ae775ad8c2e48c5391
diff --git a/publisher/instagram_stub.py b/publisher/instagram_stub.py
new file mode 100644
index 0000000000000000000000000000000000000000..b46695a6a5443e80aef3e21234f526d3a86c7f0b
--- /dev/null
+++ b/publisher/instagram_stub.py
@@ -0,0 +1,32 @@
+"""Stub implementation for future Instagram publishing integration."""
+from __future__ import annotations
+
+from datetime import datetime
+def generate_caption(contexto: str) -> str:
+    """Generate a simple caption placeholder based on provided context."""
+    contexto_limpo = contexto.strip() or "Conteúdo da Finiti pronto para publicação!"
+    return (
+        "✨ Destaque do dia: "
+        + contexto_limpo
+        + " | #Finiti #Inovação #AFI"
+    )
+
+
+def schedule_post(path: str, caption: str, when: datetime) -> None:
+    """Log scheduling information for a future Instagram integration."""
+    timestamp = when.isoformat()
+    print(
+        f"[INSTAGRAM_STUB] Post agendado para {timestamp}: arquivo='{path}', legenda='{caption}'"
+    )
+
+
+# Pontos de integração futura
+API_NOTES = {
+    "endpoint": "API real do Meta/Instagram a ser integrada via Graph API",
+    "required_env": [
+        "INSTAGRAM_ACCESS_TOKEN",
+        "INSTAGRAM_BUSINESS_ACCOUNT_ID",
+        "INSTAGRAM_PUBLISH_URL",
+    ],
+    "notes": "Substituir schedule_post por chamada autenticada usando os dados acima.",
+}
diff --git a/rag/__init__.py b/rag/__init__.py
new file mode 100644
index 0000000000000000000000000000000000000000..893bd1f28c571904ae2e56f7daa0efd2f3c9ab9e
--- /dev/null
+++ b/rag/__init__.py
@@ -0,0 +1 @@
+"""RAG utilities for AFI."""
diff --git a/rag/ingest.py b/rag/ingest.py
new file mode 100644
index 0000000000000000000000000000000000000000..b33929864caa92c86dda1cfefab6b219aa897a7f
--- /dev/null
+++ b/rag/ingest.py
@@ -0,0 +1,77 @@
+"""Simple ingestion pipeline for AFI knowledge base."""
+from __future__ import annotations
+
+import os
+from pathlib import Path
+from typing import Dict, Any
+
+try:
+    from dotenv import load_dotenv
+except ImportError:  # pragma: no cover
+    def load_dotenv() -> None:  # type: ignore
+        print("[AVISO] python-dotenv não instalado; utilizando variáveis padrão.")
+
+load_dotenv()
+
+try:
+    from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
+except ImportError as exc:  # pragma: no cover - dependency missing
+    SimpleDirectoryReader = None  # type: ignore
+    VectorStoreIndex = None  # type: ignore
+    IMPORT_ERROR = exc
+else:
+    IMPORT_ERROR = None
+
+
+def ingest_documents(
+    source_dir: str | os.PathLike[str] | None = None,
+    persist_dir: str | os.PathLike[str] | None = None,
+) -> Dict[str, Any]:
+    """Run ingestion for the configured knowledge base directory."""
+    if IMPORT_ERROR is not None:
+        return {"ok": False, "error": f"llama-index indisponível: {IMPORT_ERROR}"}
+
+    source_path = Path(source_dir or os.getenv("AFI_KB_DIR", "./knowledge_base")).expanduser()
+    persist_path = Path(persist_dir or os.getenv("AFI_RAG_STORAGE", "./rag_storage")).expanduser()
+
+    persist_path.mkdir(parents=True, exist_ok=True)
+    source_path.mkdir(parents=True, exist_ok=True)
+
+    documents = []
+    try:
+        reader = SimpleDirectoryReader(input_dir=str(source_path))
+        documents = reader.load_data()
+    except Exception as exc:  # pragma: no cover - I/O failure
+        return {"ok": False, "error": f"falha ao carregar documentos: {exc}"}
+
+    if not documents:
+        return {"ok": False, "error": "nenhum documento encontrado para ingestão", "directory": str(source_path)}
+
+    try:
+        index = VectorStoreIndex.from_documents(documents)
+        index.storage_context.persist(persist_dir=str(persist_path))
+    except Exception as exc:  # pragma: no cover - runtime failure
+        return {"ok": False, "error": f"falha ao persistir índice: {exc}"}
+
+    return {
+        "ok": True,
+        "documents": len(documents),
+        "source": str(source_path),
+        "persist_dir": str(persist_path),
+    }
+
+
+def main() -> int:
+    result = ingest_documents()
+    if result.get("ok"):
+        print("Ingestão concluída com sucesso:")
+        print(result)
+        return 0
+
+    print("Falha na ingestão:")
+    print(result)
+    return 1
+
+
+if __name__ == "__main__":
+    raise SystemExit(main())
diff --git a/rag/query.py b/rag/query.py
new file mode 100644
index 0000000000000000000000000000000000000000..09d3d288dd1a798fb5476e715da8f90c5cc0f447
--- /dev/null
+++ b/rag/query.py
@@ -0,0 +1,63 @@
+"""Query interface for ingested AFI knowledge base."""
+from __future__ import annotations
+
+import os
+from pathlib import Path
+from typing import Any
+
+try:
+    from dotenv import load_dotenv
+except ImportError:  # pragma: no cover
+    def load_dotenv() -> None:  # type: ignore
+        print("[AVISO] python-dotenv não instalado; utilizando variáveis padrão.")
+
+load_dotenv()
+
+try:
+    from llama_index.core import StorageContext, VectorStoreIndex
+except ImportError as exc:  # pragma: no cover
+    StorageContext = None  # type: ignore
+    VectorStoreIndex = None  # type: ignore
+    IMPORT_ERROR = exc
+else:
+    IMPORT_ERROR = None
+
+
+def load_index(persist_dir: str | os.PathLike[str] | None = None) -> Any:
+    if IMPORT_ERROR is not None:
+        raise RuntimeError(f"llama-index indisponível: {IMPORT_ERROR}")
+
+    persist_path = Path(persist_dir or os.getenv("AFI_RAG_STORAGE", "./rag_storage")).expanduser()
+    if not persist_path.exists():
+        raise FileNotFoundError(f"Persistência não encontrada em {persist_path}")
+
+    storage_context = StorageContext.from_defaults(persist_dir=str(persist_path))
+    return VectorStoreIndex.from_storage(storage_context)
+
+
+def query(text: str, persist_dir: str | os.PathLike[str] | None = None) -> str:
+    index = load_index(persist_dir)
+    engine = index.as_query_engine()
+    response = engine.query(text)
+    return str(response)
+
+
+def main() -> int:
+    import argparse
+
+    parser = argparse.ArgumentParser(description="Consultar base de conhecimento do AFI")
+    parser.add_argument("prompt", help="Pergunta a ser respondida")
+    args = parser.parse_args()
+
+    try:
+        answer = query(args.prompt)
+    except Exception as exc:
+        print(f"Falha ao consultar: {exc}")
+        return 1
+
+    print(answer)
+    return 0
+
+
+if __name__ == "__main__":
+    raise SystemExit(main())
diff --git a/relatorio_paths.md b/relatorio_paths.md
new file mode 100644
index 0000000000000000000000000000000000000000..550b5518297c302e7c72a6d54937fd39cab0f2dd
--- /dev/null
+++ b/relatorio_paths.md
@@ -0,0 +1,42 @@
+# Relatório de ajustes de caminhos
+
+## Arquivos criados
+- `.env.example`: modelo de variáveis de ambiente com portas e diretórios padrão.
+- `.env`: cópia base para execução local com os mesmos valores do example.
+
+## Arquivos modificados e substituições principais
+
+### `app.py`
+- Carregamento do `.env` via `load_dotenv()` e criação automática das pastas definidas em `AFI_INPUT_DIR`, `AFI_OUTPUT_DIR`, `AFI_MUSIC_DIR` e `AFI_LOG_DIR`.
+
+### `guardiao_midia.py`
+- `Path("C:/AFI/Videos_Agendados")` → `AFI_OUTPUT_DIR / nome_saida`.
+- `Path(f"C:/AFI/Musicas/{estilo}")` → `AFI_MUSIC_DIR / estilo`.
+- Parâmetro padrão `"C:/AFI/Videos_Para_Editar"` → uso de `AFI_INPUT_DIR`.
+- Mensagens e verificações atualizadas para usar os diretórios carregados do `.env`.
+
+### `guardiao.py`
+- Diretórios fixos (`"Videos_Para_Editar"`, `"Musicas"`, `"Videos_Editados"`) substituídos pelos caminhos configuráveis (`AFI_INPUT_DIR`, `AFI_MUSIC_DIR`, `AFI_OUTPUT_DIR`).
+- Mensagens de erro e logs agora exibem os diretórios configurados dinamicamente.
+
+### `editor_video.py`
+- Inclusão de `load_dotenv()` e criação das pastas configuradas.
+- Listagens e utilitários passaram a usar `AFI_INPUT_DIR`, `AFI_MUSIC_DIR` e `AFI_OUTPUT_DIR` em vez de strings fixas (`"Videos_Para_Editar"`, `"Musicas"`, `"Videos_Editados"`).
+- Caminhos de teste e do modo interativo ajustados para respeitar os diretórios do `.env`.
+
+### `agente_midia_social.py`
+- `Path("C:/AFI/Videos_Agendados")` → `AFI_OUTPUT_DIR / nome_saida`.
+- `Path(f"C:/AFI/Musicas/{estilo}")` e iteração sobre `Path("C:/AFI/Musicas")` → versões baseadas em `AFI_MUSIC_DIR`.
+- Mensagens de status e configuração passaram a refletir os diretórios definidos via ambiente.
+
+### `app.py`, `guardiao_midia.py`, `guardiao.py`, `editor_video.py`, `agente_midia_social.py`
+- Todos os módulos de entrada carregam o `.env`, expõem constantes `AFI_*` e garantem a criação das pastas essenciais na inicialização.
+
+## Novas ferramentas e scripts
+- `tools/diagnostics.py`: diagnóstico de ambiente com verificação de Python, FFmpeg, imports e geração opcional de clipe.
+- `tools/probe_models.py`: inspeção de modelos locais (texto, áudio e visão) com quedas controladas.
+- `rag/ingest.py` e `rag/query.py`: pipeline simplificado de ingestão/consulta com persistência local configurável.
+- Scripts auxiliares em `scripts/`: `check_env`, `run_ui`, `run_guardian` e `ingest_docs` para padronizar execuções em Windows e Unix.
+- `tests/test_e2e_min.py`: teste E2E mínimo (com skips condicionais) cobrindo ingestão, guardião e saída automatizada.
+- `publisher/instagram_stub.py`: stub de publicação com funções de geração de legenda e agendamento e lista de variáveis necessárias para integração real.
+
diff --git a/requirements.txt b/requirements.txt
new file mode 100644
index 0000000000000000000000000000000000000000..c07f2db7abf80e792f6fee7754580b691f41cefa
--- /dev/null
+++ b/requirements.txt
@@ -0,0 +1,15 @@
+streamlit==1.38.0
+watchdog==4.0.2
+moviepy==1.0.3
+python-dotenv==1.0.1
+pydub==0.25.1
+faster-whisper==1.0.3
+pillow==10.4.0
+requests==2.32.3
+numpy==1.26.4
+llama-index==0.11.20
+sentence-transformers==3.0.1
+faiss-cpu==1.8.0
+duckduckgo-search==6.2.10
+flask==3.0.3
+flask-cors==4.0.1
diff --git a/scripts/check_env.bat b/scripts/check_env.bat
new file mode 100644
index 0000000000000000000000000000000000000000..c66268c0c5f14c454f8fc26e553f6fe500e6deae
--- /dev/null
+++ b/scripts/check_env.bat
@@ -0,0 +1,8 @@
+@echo off
+setlocal
+if exist ..\..\Scripts\activate.bat (
+    call ..\..\Scripts\activate.bat
+) else if exist .\.venv\Scripts\activate.bat (
+    call .\.venv\Scripts\activate.bat
+)
+python -m tools.diagnostics
diff --git a/scripts/check_env.sh b/scripts/check_env.sh
new file mode 100755
index 0000000000000000000000000000000000000000..372f2b8f0cffeb04625c7cc5966137fa7f059ef0
--- /dev/null
+++ b/scripts/check_env.sh
@@ -0,0 +1,7 @@
+#!/usr/bin/env bash
+set -euo pipefail
+if [[ -f ./.venv/bin/activate ]]; then
+  # shellcheck disable=SC1091
+  source ./.venv/bin/activate
+fi
+python -m tools.diagnostics
diff --git a/scripts/ingest_docs.bat b/scripts/ingest_docs.bat
new file mode 100644
index 0000000000000000000000000000000000000000..4873bc9457e47ff34b3a878a8df06dfebc9334d3
--- /dev/null
+++ b/scripts/ingest_docs.bat
@@ -0,0 +1,9 @@
+@echo off
+setlocal
+if exist .\.venv\Scripts\activate.bat (
+    call .\.venv\Scripts\activate.bat 2>nul
+)
+for /f "usebackq tokens=1* delims==" %%A in (`findstr /r "^[^#;].*=" .env 2^>nul`) do set "%%A=%%B"
+if not defined AFI_KB_DIR set "AFI_KB_DIR=./knowledge_base"
+if not exist "%AFI_KB_DIR%" mkdir "%AFI_KB_DIR%"
+python -m rag.ingest %*
diff --git a/scripts/ingest_docs.sh b/scripts/ingest_docs.sh
new file mode 100755
index 0000000000000000000000000000000000000000..88d5cbbe4cc56059deb7a076cf3188345d26948b
--- /dev/null
+++ b/scripts/ingest_docs.sh
@@ -0,0 +1,10 @@
+#!/usr/bin/env bash
+set -euo pipefail
+if [[ -f .env ]]; then
+  set -a
+  # shellcheck disable=SC1091
+  source .env
+  set +a
+fi
+mkdir -p "${AFI_KB_DIR:-./knowledge_base}"
+python -m rag.ingest "$@"
diff --git a/scripts/offline/build_wheelhouse.ps1 b/scripts/offline/build_wheelhouse.ps1
new file mode 100644
index 0000000000000000000000000000000000000000..dd3b4025223962d64a9d3a8395c559f7379803e5
--- /dev/null
+++ b/scripts/offline/build_wheelhouse.ps1
@@ -0,0 +1,14 @@
+$ErrorActionPreference = "Stop"
+python -m venv .venv
+. .\.venv\Scripts\Activate.ps1
+pip install -U pip wheel
+New-Item -ItemType Directory -Force -Path wheels | Out-Null
+pip download -r requirements.txt -d wheels
+$manifest = "wheels\manifest.txt"
+if (Test-Path $manifest) { Remove-Item $manifest }
+Get-ChildItem wheels -File | ForEach-Object {
+  $hash = (Get-FileHash $_.FullName -Algorithm SHA256).Hash.ToLower()
+  Add-Content $manifest ("{0}  sha256={1}" -f $_.Name, $hash)
+}
+Compress-Archive -Path wheels\* -DestinationPath wheels.zip -Force
+Write-Host "OK: wheels.zip criado"
diff --git a/scripts/offline/build_wheelhouse.sh b/scripts/offline/build_wheelhouse.sh
new file mode 100755
index 0000000000000000000000000000000000000000..6090eb617c1741cfd35fa201ebb5a23bd6cda5f8
--- /dev/null
+++ b/scripts/offline/build_wheelhouse.sh
@@ -0,0 +1,25 @@
+#!/usr/bin/env bash
+set -euo pipefail
+python3 -m venv .venv && source .venv/bin/activate
+pip install -U pip wheel
+mkdir -p wheels
+pip download -r requirements.txt -d wheels
+python - <<'PY'
+import glob
+import hashlib
+import os
+import pathlib
+
+out = pathlib.Path("wheels/manifest.txt")
+out.parent.mkdir(parents=True, exist_ok=True)
+with out.open("w", encoding="utf-8") as f:
+    for whl in sorted(glob.glob("wheels/*")):
+        if os.path.isdir(whl):
+            continue
+        with open(whl, "rb") as handle:
+            digest = hashlib.sha256(handle.read()).hexdigest()
+        f.write(f"{os.path.basename(whl)}  sha256={digest}\n")
+print("Manifesto gerado:", out)
+PY
+cd wheels && zip -r ../wheels.zip . && cd ..
+echo "OK: wheels.zip criado"
diff --git a/scripts/run_guardian.bat b/scripts/run_guardian.bat
new file mode 100644
index 0000000000000000000000000000000000000000..0fbaa58ed04c8192e25ab8afdb19e56d03d437ef
--- /dev/null
+++ b/scripts/run_guardian.bat
@@ -0,0 +1,10 @@
+@echo off
+setlocal
+if exist .\.venv\Scripts\activate.bat (
+    call .\.venv\Scripts\activate.bat 2>nul
+)
+for /f "usebackq tokens=1* delims==" %%A in (`findstr /r "^[^#;].*=" .env 2^>nul`) do set "%%A=%%B"
+if not defined AFI_LOG_DIR set "AFI_LOG_DIR=./logs"
+if not exist "%AFI_LOG_DIR%" mkdir "%AFI_LOG_DIR%"
+set PYTHONUNBUFFERED=1
+python -u guardiao.py >> "%AFI_LOG_DIR%\guardian.log" 2>>&1
diff --git a/scripts/run_guardian.sh b/scripts/run_guardian.sh
new file mode 100755
index 0000000000000000000000000000000000000000..f47e4c8a55c978b746e18505f05ae48924c450f5
--- /dev/null
+++ b/scripts/run_guardian.sh
@@ -0,0 +1,11 @@
+#!/usr/bin/env bash
+set -euo pipefail
+if [[ -f .env ]]; then
+  set -a
+  # shellcheck disable=SC1091
+  source .env
+  set +a
+fi
+LOG_DIR="${AFI_LOG_DIR:-./logs}"
+mkdir -p "$LOG_DIR"
+PYTHONUNBUFFERED=1 python -u guardiao.py >>"${LOG_DIR}/guardian.log" 2>&1
diff --git a/scripts/run_ui.bat b/scripts/run_ui.bat
new file mode 100644
index 0000000000000000000000000000000000000000..a2f4e360d87448b34ddd03b7b8c14ebb642bee0b
--- /dev/null
+++ b/scripts/run_ui.bat
@@ -0,0 +1,20 @@
+@echo off
+setlocal
+if exist .\.venv\Scripts\activate.bat (
+    call .\.venv\Scripts\activate.bat 2>nul
+)
+for /f "usebackq tokens=1* delims==" %%A in (`findstr /r "^[^#;].*=" .env 2^>nul`) do set "%%A=%%B"
+if not defined AFI_PORT set "AFI_PORT=8507"
+if "%NO_DEPS%"=="1" (
+    echo NO_DEPS=1 detectado - iniciando UI fallback
+    call "%~dp0run_ui_fallback.bat"
+    goto :eof
+)
+python -c "import streamlit" >nul 2>&1
+if %errorlevel% equ 0 (
+    set "STREAMLIT_BROWSER_GATHER_USAGE_STATS=false"
+    python -m streamlit run app.py --server.port %AFI_PORT%
+) else (
+    echo Streamlit indisponivel - iniciando UI fallback
+    call "%~dp0run_ui_fallback.bat"
+)
diff --git a/scripts/run_ui.sh b/scripts/run_ui.sh
new file mode 100755
index 0000000000000000000000000000000000000000..2a4d1ac269bcd9976cd1b0d5a352aded7ef3c566
--- /dev/null
+++ b/scripts/run_ui.sh
@@ -0,0 +1,21 @@
+#!/usr/bin/env bash
+set -euo pipefail
+if [[ -f .env ]]; then
+  set -a
+  # shellcheck disable=SC1091
+  source .env
+  set +a
+fi
+
+if [[ "${NO_DEPS:-0}" == "1" ]]; then
+  echo "NO_DEPS=1 detectado - iniciando UI fallback"
+  exec "$(dirname "$0")/run_ui_fallback.sh"
+fi
+
+if python -c "import streamlit" >/dev/null 2>&1; then
+  export STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
+  python -m streamlit run app.py --server.port "${AFI_PORT:-8507}"
+else
+  echo "Streamlit indisponível - iniciando UI fallback"
+  exec "$(dirname "$0")/run_ui_fallback.sh"
+fi
diff --git a/scripts/run_ui_fallback.bat b/scripts/run_ui_fallback.bat
new file mode 100644
index 0000000000000000000000000000000000000000..880eb5d6eb7caf22bb5fad169f03c59cbd1504b6
--- /dev/null
+++ b/scripts/run_ui_fallback.bat
@@ -0,0 +1,7 @@
+@echo off
+setlocal
+if exist .\.venv\Scripts\activate.bat (
+    call .\.venv\Scripts\activate.bat 2>nul
+)
+for /f "usebackq tokens=1* delims==" %%A in (`findstr /r "^[^#;].*=" .env 2^>nul`) do set "%%A=%%B"
+python ui_fallback\ui_fallback_server.py
diff --git a/scripts/run_ui_fallback.sh b/scripts/run_ui_fallback.sh
new file mode 100755
index 0000000000000000000000000000000000000000..b87839c9bb6c96cf9f116b268301a67ac38d48fd
--- /dev/null
+++ b/scripts/run_ui_fallback.sh
@@ -0,0 +1,9 @@
+#!/usr/bin/env bash
+set -euo pipefail
+if [[ -f .env ]]; then
+  set -a
+  # shellcheck disable=SC1091
+  source .env
+  set +a
+fi
+python ui_fallback/ui_fallback_server.py
diff --git a/tests/test_e2e_min.py b/tests/test_e2e_min.py
new file mode 100644
index 0000000000000000000000000000000000000000..675fec39d7f34550733b02222043e9868b2d9b04
--- /dev/null
+++ b/tests/test_e2e_min.py
@@ -0,0 +1,92 @@
+"""Minimum end-to-end smoke test for the AFI pipeline."""
+from __future__ import annotations
+
+import os
+import subprocess
+import sys
+import time
+from pathlib import Path
+
+import pytest
+
+try:
+    from dotenv import load_dotenv
+except ImportError:  # pragma: no cover - optional dependency
+    def load_dotenv() -> None:  # type: ignore
+        return None
+
+load_dotenv()
+
+ROOT = Path(__file__).resolve().parents[1]
+KNOWLEDGE_BASE = Path(os.getenv("AFI_KB_DIR", ROOT / "knowledge_base"))
+INPUT_DIR = Path(os.getenv("AFI_INPUT_DIR", ROOT / "data" / "Videos_Para_Editar"))
+OUTPUT_DIR = Path(os.getenv("AFI_OUTPUT_DIR", ROOT / "data" / "Videos_Agendados"))
+LOG_DIR = Path(os.getenv("AFI_LOG_DIR", ROOT / "logs"))
+
+
+def test_minimum_client_flow(tmp_path: Path) -> None:
+    try:
+        import watchdog  # noqa: F401
+    except ImportError as exc:  # pragma: no cover - dependency gate
+        pytest.skip(f"watchdog não disponível: {exc}")
+
+    try:
+        import moviepy  # noqa: F401
+    except ImportError as exc:
+        pytest.skip(f"moviepy não disponível: {exc}")
+
+    KNOWLEDGE_BASE.mkdir(parents=True, exist_ok=True)
+    INPUT_DIR.mkdir(parents=True, exist_ok=True)
+    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
+    LOG_DIR.mkdir(parents=True, exist_ok=True)
+
+    doc_path = KNOWLEDGE_BASE / "dummy.txt"
+    doc_path.write_text("AFI teste de ingestão.", encoding="utf-8")
+
+    ingest = subprocess.run(
+        [sys.executable, "-m", "rag.ingest"],
+        cwd=ROOT,
+        capture_output=True,
+        text=True,
+    )
+    if ingest.returncode != 0:
+        pytest.skip(f"ingestão indisponível: {ingest.stdout}\n{ingest.stderr}")
+
+    from moviepy.editor import ColorClip
+
+    video_path = INPUT_DIR / "teste_guardiao.mp4"
+    clip = ColorClip(size=(320, 240), color=(255, 0, 0), duration=3)
+    clip.write_videofile(str(video_path), fps=24, codec="libx264", audio=False, verbose=False, logger=None)
+    clip.close()
+
+    guardian_log = LOG_DIR / "guardian.log"
+    with open(guardian_log, "a", encoding="utf-8"):
+        pass
+
+    guardian = subprocess.Popen(
+        [sys.executable, "guardiao.py"],
+        cwd=ROOT,
+        stdout=subprocess.PIPE,
+        stderr=subprocess.STDOUT,
+        text=True,
+    )
+
+    try:
+        deadline = time.time() + 60
+        while time.time() < deadline:
+            if any(OUTPUT_DIR.glob("*.mp4")):
+                break
+            time.sleep(2)
+        else:
+            pytest.fail("Nenhum vídeo processado pelo guardião dentro do tempo limite")
+    finally:
+        guardian.terminate()
+        try:
+            guardian.wait(timeout=10)
+        except subprocess.TimeoutExpired:
+            guardian.kill()
+
+    outputs = list(OUTPUT_DIR.glob("*.mp4"))
+    assert outputs, "Esperava pelo menos um vídeo processado"
+    sizes = {path.name: path.stat().st_size for path in outputs}
+    print(f"Arquivos gerados: {sizes}")
diff --git a/tests/test_no_deps.py b/tests/test_no_deps.py
new file mode 100644
index 0000000000000000000000000000000000000000..32e6d430375223e58e938f87952a7f63fd563fc6
--- /dev/null
+++ b/tests/test_no_deps.py
@@ -0,0 +1,54 @@
+import json
+import sys
+from pathlib import Path
+import types
+
+ROOT = Path(__file__).resolve().parents[1]
+if str(ROOT) not in sys.path:
+    sys.path.insert(0, str(ROOT))
+
+
+def test_dummy_video_creation(tmp_path, monkeypatch):
+    monkeypatch.setenv("NO_DEPS", "1")
+    monkeypatch.setenv("AFI_INPUT_DIR", str(tmp_path / "input"))
+    monkeypatch.setenv("AFI_OUTPUT_DIR", str(tmp_path / "output"))
+    monkeypatch.setenv("AFI_MUSIC_DIR", str(tmp_path / "music"))
+    monkeypatch.setenv("AFI_LOG_DIR", str(tmp_path / "logs"))
+
+    tmp_path.joinpath("input").mkdir()
+    tmp_path.joinpath("music").mkdir()
+    tmp_path.joinpath("output").mkdir()
+
+    video_path = tmp_path / "input" / "video.mp4"
+    music_path = tmp_path / "music" / "song.mp3"
+    video_path.write_bytes(b"video")
+    music_path.write_bytes(b"audio")
+
+    fake_dotenv = types.ModuleType("dotenv")
+    fake_dotenv.load_dotenv = lambda *args, **kwargs: None
+    sys.modules.setdefault("dotenv", fake_dotenv)
+
+    from importlib import reload
+    import editor_video
+
+    reload(editor_video)
+
+    destino = tmp_path / "output" / "resultado.mp4"
+
+    assert editor_video.editar_video_story(
+        caminho_video_original=str(video_path),
+        caminho_musica=str(music_path),
+        frase_marketing="Testando modo simulado",
+        caminho_saida=str(destino),
+    )
+
+    dummy_mp4 = tmp_path / "output" / "dummy_resultado.mp4"
+    dummy_meta = tmp_path / "output" / "dummy_resultado.json"
+
+    assert dummy_mp4.exists()
+    assert dummy_meta.exists()
+    assert dummy_mp4.stat().st_size >= 512 * 1024
+
+    metadata = json.loads(dummy_meta.read_text(encoding="utf-8"))
+    assert metadata["modo"] == "NO_DEPS"
+    assert metadata["arquivo_dummy"] == dummy_mp4.name
diff --git a/third_party/ffmpeg/linux/bin/.gitkeep b/third_party/ffmpeg/linux/bin/.gitkeep
new file mode 100644
index 0000000000000000000000000000000000000000..e69de29bb2d1d6434b8b29ae775ad8c2e48c5391
diff --git a/third_party/ffmpeg/mac/bin/.gitkeep b/third_party/ffmpeg/mac/bin/.gitkeep
new file mode 100644
index 0000000000000000000000000000000000000000..e69de29bb2d1d6434b8b29ae775ad8c2e48c5391
diff --git a/third_party/ffmpeg/win/bin/.gitkeep b/third_party/ffmpeg/win/bin/.gitkeep
new file mode 100644
index 0000000000000000000000000000000000000000..e69de29bb2d1d6434b8b29ae775ad8c2e48c5391
diff --git a/tools/diagnostics.py b/tools/diagnostics.py
new file mode 100644
index 0000000000000000000000000000000000000000..6e7bd7836a8aff5134f3c26cee88bd4291a88f6c
--- /dev/null
+++ b/tools/diagnostics.py
@@ -0,0 +1,249 @@
+"""Environment diagnostics utilities for AFI."""
+from __future__ import annotations
+
+import os
+import subprocess
+import sys
+from pathlib import Path
+from typing import Dict, Any, List
+
+try:
+    from dotenv import load_dotenv
+except ImportError:  # pragma: no cover - graceful fallback when dependency is absent
+    def load_dotenv() -> None:
+        print("[AVISO] python-dotenv não instalado; variáveis de ambiente padrão serão utilizadas.")
+
+load_dotenv()
+
+REQUIRED_MODULES = [
+    "moviepy",
+    "watchdog",
+    "faster_whisper",
+    "streamlit",
+]
+
+DEFAULT_DIRECTORIES = {
+    "AFI_INPUT_DIR": "./data/Videos_Para_Editar",
+    "AFI_OUTPUT_DIR": "./data/Videos_Agendados",
+    "AFI_MUSIC_DIR": "./data/Musicas",
+    "AFI_LOG_DIR": "./logs",
+}
+
+FFMPEG_FALLBACK_ROOT = Path("third_party/ffmpeg")
+
+
+def _gather_ffmpeg_candidates() -> List[Path]:
+    candidates: List[Path] = []
+    env_value = os.getenv("IMAGEIO_FFMPEG_EXE")
+    if env_value:
+        candidates.append(Path(env_value).expanduser())
+
+    if FFMPEG_FALLBACK_ROOT.exists():
+        for candidate in sorted(FFMPEG_FALLBACK_ROOT.glob("*/bin/ffmpeg*")):
+            candidate_path = candidate.resolve()
+            if candidate_path.is_file() and candidate_path not in candidates:
+                candidates.append(candidate_path)
+
+    return candidates
+
+
+def check_python_version() -> Dict[str, Any]:
+    version = sys.version_info
+    meets_requirement = version >= (3, 10)
+    return {
+        "ok": meets_requirement,
+        "version": f"{version.major}.{version.minor}.{version.micro}",
+        "requirement": ">= 3.10",
+    }
+
+
+def check_ffmpeg() -> Dict[str, Any]:
+    try:
+        result = subprocess.run(
+            ["ffmpeg", "-version"],
+            capture_output=True,
+            text=True,
+            check=True,
+        )
+    except FileNotFoundError:
+        result = None
+    except subprocess.CalledProcessError as exc:
+        return {
+            "ok": False,
+            "error": f"ffmpeg returned non-zero exit status {exc.returncode}",
+            "details": exc.stderr,
+        }
+    else:
+        output = result.stdout or result.stderr
+        first_line = output.splitlines()[0] if output else ""
+        return {"ok": True, "version": first_line.strip(), "source": "PATH"}
+
+    fallback_errors = []
+    for candidate in _gather_ffmpeg_candidates():
+        if not candidate.exists():
+            fallback_errors.append(f"missing: {candidate}")
+            continue
+        try:
+            result = subprocess.run(
+                [str(candidate), "-version"],
+                capture_output=True,
+                text=True,
+                check=True,
+            )
+        except FileNotFoundError:
+            fallback_errors.append(f"not executable: {candidate}")
+            continue
+        except subprocess.CalledProcessError as exc:
+            fallback_errors.append(
+                f"{candidate} exited with {exc.returncode}: {exc.stderr.strip()}"
+            )
+            continue
+
+        os.environ["IMAGEIO_FFMPEG_EXE"] = str(candidate)
+        output = result.stdout or result.stderr
+        first_line = output.splitlines()[0] if output else ""
+        return {
+            "ok": True,
+            "version": first_line.strip(),
+            "source": "fallback",
+            "path": str(candidate),
+        }
+
+    error_message = "ffmpeg executable not found in PATH"
+    if fallback_errors:
+        error_message += "; checked fallbacks -> " + "; ".join(fallback_errors)
+
+    return {"ok": False, "error": error_message}
+
+
+def check_imports() -> Dict[str, Any]:
+    results: Dict[str, Any] = {}
+    for module_name in REQUIRED_MODULES:
+        try:
+            __import__(module_name)
+        except Exception as exc:  # pragma: no cover - diagnostic logging only
+            results[module_name] = {"ok": False, "error": repr(exc)}
+        else:
+            results[module_name] = {"ok": True}
+    return results
+
+
+def ensure_directories() -> Dict[str, Any]:
+    results: Dict[str, Any] = {}
+    for env_key, default in DEFAULT_DIRECTORIES.items():
+        configured = os.getenv(env_key, default)
+        path = Path(configured).expanduser()
+        try:
+            path.mkdir(parents=True, exist_ok=True)
+            results[env_key] = {"ok": True, "path": str(path.resolve())}
+        except Exception as exc:  # pragma: no cover - diagnostic logging only
+            results[env_key] = {
+                "ok": False,
+                "path": str(path),
+                "error": repr(exc),
+            }
+    return results
+
+
+def try_generate_test_clip(output_dir: str, ffmpeg_ok: bool, moviepy_ok: bool) -> Dict[str, Any]:
+    if not (ffmpeg_ok and moviepy_ok):
+        return {
+            "ok": False,
+            "skipped": True,
+            "reason": "moviepy import or ffmpeg check failed",
+        }
+
+    try:
+        from moviepy.editor import ColorClip
+    except Exception as exc:  # pragma: no cover - import guard
+        return {"ok": False, "error": repr(exc)}
+
+    output_path = Path(output_dir) / "diagnostics_test.mp4"
+
+    try:
+        clip = ColorClip(size=(640, 360), color=(0, 128, 255), duration=2)
+        clip.write_videofile(
+            str(output_path),
+            fps=24,
+            codec="libx264",
+            audio=False,
+            verbose=False,
+            logger=None,
+        )
+        clip.close()
+        return {"ok": True, "path": str(output_path.resolve())}
+    except Exception as exc:  # pragma: no cover - ffmpeg execution path
+        return {"ok": False, "error": repr(exc), "path": str(output_path)}
+
+
+def main() -> int:
+    python_info = check_python_version()
+    ffmpeg_info = check_ffmpeg()
+    import_info = check_imports()
+    directory_info = ensure_directories()
+
+    moviepy_ok = import_info.get("moviepy", {}).get("ok", False)
+    ffmpeg_ok = ffmpeg_info.get("ok", False)
+    output_dir = directory_info.get("AFI_OUTPUT_DIR", {}).get("path", DEFAULT_DIRECTORIES["AFI_OUTPUT_DIR"])
+    clip_info = try_generate_test_clip(output_dir, ffmpeg_ok, moviepy_ok)
+
+    print("=== AFI Environment Diagnostics ===")
+    print(f"Python version: {python_info['version']} (requires {python_info['requirement']}) - {'OK' if python_info['ok'] else 'FAIL'}")
+
+    if ffmpeg_info.get("ok"):
+        source = ffmpeg_info.get("source", "PATH")
+        message = ffmpeg_info["version"]
+        if source == "PATH":
+            message += " [PATH]"
+        elif source == "fallback":
+            path_hint = ffmpeg_info.get("path")
+            if path_hint:
+                message += f" [fallback -> {path_hint}]"
+            else:
+                message += " [fallback]"
+        print(f"FFmpeg: {message}")
+    else:
+        print("FFmpeg: NOT AVAILABLE")
+        if "error" in ffmpeg_info:
+            print(f"  Reason: {ffmpeg_info['error']}")
+        if "details" in ffmpeg_info and ffmpeg_info["details"]:
+            print(ffmpeg_info["details"])
+
+    print("\nModule imports:")
+    for module_name, info in import_info.items():
+        status = "OK" if info.get("ok") else "FAIL"
+        print(f"  - {module_name}: {status}")
+        if not info.get("ok") and "error" in info:
+            print(f"      {info['error']}")
+
+    print("\nDirectory checks:")
+    for env_key, info in directory_info.items():
+        status = "OK" if info.get("ok") else "FAIL"
+        print(f"  - {env_key}: {status} -> {info.get('path')}")
+        if not info.get("ok") and "error" in info:
+            print(f"      {info['error']}")
+
+    if clip_info.get("ok"):
+        print(f"\nTest clip generated at: {clip_info['path']}")
+    elif clip_info.get("skipped"):
+        print("\nTest clip generation skipped:")
+        print(f"  Reason: {clip_info['reason']}")
+    else:
+        print("\nTest clip generation failed:")
+        if "error" in clip_info:
+            print(f"  Error: {clip_info['error']}")
+        if "path" in clip_info:
+            print(f"  Intended path: {clip_info['path']}")
+
+    if not (python_info["ok"] and ffmpeg_info.get("ok") and all(info.get("ok") for info in import_info.values())):
+        print("\n[ATENÇÃO] Ambiente incompleto detectado. Verifique as instruções acima.")
+        if not ffmpeg_info.get("ok"):
+            print("Instale o FFmpeg e garanta que esteja no PATH do sistema.")
+        return 1
+
+    print("\nAmbiente pronto!")
+    return 0
+
+
+if __name__ == "__main__":
+    raise SystemExit(main())
diff --git a/tools/probe_models.py b/tools/probe_models.py
new file mode 100644
index 0000000000000000000000000000000000000000..fca6e65bbb1ed0ac96dae872976ea3d12b9a02eb
--- /dev/null
+++ b/tools/probe_models.py
@@ -0,0 +1,133 @@
+"""Utilities to probe local multimodal model availability."""
+from __future__ import annotations
+
+import json
+import os
+import tempfile
+from pathlib import Path
+from typing import Any, Dict
+
+try:
+    from dotenv import load_dotenv
+except ImportError:  # pragma: no cover - fallback when python-dotenv is unavailable
+    def load_dotenv() -> None:  # type: ignore
+        print("[AVISO] python-dotenv não instalado; usando variáveis padrão.")
+
+load_dotenv()
+
+
+def synthesize_audio(duration_ms: int = 2000) -> Dict[str, Any]:
+    try:
+        from pydub.generators import Sine
+    except Exception as exc:  # pragma: no cover - dependency missing
+        return {"ok": False, "error": f"pydub indisponível: {exc}"}
+
+    try:
+        tone = Sine(440).to_audio_segment(duration=duration_ms)
+    except Exception as exc:  # pragma: no cover - ffmpeg backend missing
+        return {"ok": False, "error": f"falha ao gerar áudio sintético: {exc}"}
+
+    tmp_dir = Path(tempfile.gettempdir())
+    audio_path = tmp_dir / "afi_probe_tone.wav"
+    try:
+        tone.export(audio_path, format="wav")
+    except Exception as exc:  # pragma: no cover - ffmpeg backend missing
+        return {"ok": False, "error": f"falha ao exportar áudio: {exc}"}
+
+    return {"ok": True, "path": str(audio_path)}
+
+
+def transcribe_audio(audio_path: str) -> Dict[str, Any]:
+    try:
+        from faster_whisper import WhisperModel
+    except Exception as exc:  # pragma: no cover - dependency missing
+        return {"ok": False, "error": f"faster-whisper indisponível: {exc}"}
+
+    model_size = os.getenv("AFI_WHISPER_MODEL", "small")
+    try:
+        model = WhisperModel(model_size)
+    except Exception as exc:  # pragma: no cover - missing model weights or GPU libs
+        return {"ok": False, "error": f"falha ao carregar modelo '{model_size}': {exc}"}
+
+    try:
+        segments, _ = model.transcribe(audio_path, beam_size=1)
+        transcript = "".join(segment.text for segment in segments)
+    except Exception as exc:  # pragma: no cover - runtime failure
+        return {"ok": False, "error": f"falha na transcrição: {exc}"}
+
+    return {"ok": True, "transcript": transcript.strip()}
+
+
+def query_text_llm(prompt: str = "Ping") -> Dict[str, Any]:
+    import json
+    import urllib.request
+    import urllib.error
+
+    endpoint = os.getenv("AFI_OLLAMA_ENDPOINT", "http://localhost:11434/api/chat")
+    model = os.getenv("AFI_OLLAMA_MODEL", "llama3")
+    payload = json.dumps({"model": model, "messages": [{"role": "user", "content": prompt}]})
+    data = payload.encode("utf-8")
+    request = urllib.request.Request(endpoint, data=data, headers={"Content-Type": "application/json"})
+
+    try:
+        with urllib.request.urlopen(request, timeout=10) as response:
+            raw = response.read().decode("utf-8")
+            parsed = json.loads(raw)
+            return {"ok": True, "response": parsed}
+    except urllib.error.URLError as exc:  # pragma: no cover - service offline
+        return {"ok": False, "error": f"não foi possível contatar Ollama em {endpoint}: {exc}"}
+    except Exception as exc:  # pragma: no cover - response parse issues
+        return {"ok": False, "error": f"erro inesperado ao consultar Ollama: {exc}"}
+
+
+def probe_vision_model() -> Dict[str, Any]:
+    image_endpoint = os.getenv("AFI_VISION_ENDPOINT")
+    if not image_endpoint:
+        return {"ok": False, "skipped": True, "reason": "Nenhum endpoint de visão configurado."}
+
+    import json
+    import urllib.request
+    import urllib.error
+
+    payload = json.dumps({"prompt": "Describe a sample image.", "image_path": ""}).encode("utf-8")
+    request = urllib.request.Request(image_endpoint, data=payload, headers={"Content-Type": "application/json"})
+
+    try:
+        with urllib.request.urlopen(request, timeout=10) as response:
+            raw = response.read().decode("utf-8")
+            parsed = json.loads(raw)
+            return {"ok": True, "response": parsed}
+    except urllib.error.URLError as exc:  # pragma: no cover
+        return {"ok": False, "error": f"não foi possível contatar o endpoint de visão {image_endpoint}: {exc}"}
+    except Exception as exc:  # pragma: no cover
+        return {"ok": False, "error": f"erro inesperado ao consultar o endpoint de visão: {exc}"}
+
+
+def main() -> int:
+    report: Dict[str, Any] = {}
+
+    audio_info = synthesize_audio()
+    report["audio_generation"] = audio_info
+
+    if audio_info.get("ok"):
+        report["audio_transcription"] = transcribe_audio(audio_info["path"])
+    else:
+        report["audio_transcription"] = {"ok": False, "skipped": True, "reason": "Áudio não gerado."}
+
+    report["text_llm"] = query_text_llm()
+    report["vision"] = probe_vision_model()
+
+    print(json.dumps(report, indent=2, ensure_ascii=False))
+
+    # Determine exit status: success only if all probes OK or intentionally skipped
+    status_codes = []
+    for key, info in report.items():
+        if info.get("skipped"):
+            continue
+        status_codes.append(info.get("ok", False))
+
+    return 0 if all(status_codes) else 1
+
+
+if __name__ == "__main__":
+    raise SystemExit(main())
diff --git a/ui_fallback/index.html b/ui_fallback/index.html
new file mode 100644
index 0000000000000000000000000000000000000000..4431299c687fdc7f2ed26d20550e70fbad19efdd
--- /dev/null
+++ b/ui_fallback/index.html
@@ -0,0 +1,157 @@
+<!DOCTYPE html>
+<html lang="pt-BR">
+  <head>
+    <meta charset="UTF-8" />
+    <title>AFI UI (Fallback Sem Dependências)</title>
+    <style>
+      body {
+        font-family: Arial, sans-serif;
+        margin: 0;
+        padding: 0;
+        background: #f6f8fb;
+        color: #1f2933;
+      }
+      header {
+        background: #0d9488;
+        color: #fff;
+        padding: 1rem 2rem;
+        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
+      }
+      main {
+        padding: 2rem;
+        max-width: 960px;
+        margin: 0 auto;
+      }
+      h1 {
+        margin: 0 0 0.5rem;
+      }
+      button {
+        background: #0d9488;
+        border: none;
+        color: #fff;
+        padding: 0.6rem 1.2rem;
+        margin-right: 0.5rem;
+        border-radius: 4px;
+        cursor: pointer;
+      }
+      button:hover {
+        background: #0f766e;
+      }
+      table {
+        width: 100%;
+        border-collapse: collapse;
+        margin-top: 1rem;
+      }
+      th, td {
+        padding: 0.6rem;
+        border-bottom: 1px solid #d9e2ec;
+        text-align: left;
+        font-size: 0.95rem;
+      }
+      #log {
+        white-space: pre-wrap;
+        background: #1f2933;
+        color: #e0f2f1;
+        padding: 1rem;
+        border-radius: 6px;
+        margin-top: 1.5rem;
+        height: 240px;
+        overflow-y: auto;
+      }
+      .status-box {
+        background: #ecfdf5;
+        border: 1px solid #99f6e4;
+        border-radius: 6px;
+        padding: 1rem;
+        margin: 1rem 0;
+      }
+    </style>
+  </head>
+  <body>
+    <header>
+      <h1>AFI UI (Fallback Sem Dependências)</h1>
+      <p id="banner"></p>
+    </header>
+    <main>
+      <section class="status-box">
+        <p><strong>Status:</strong> <span id="status"></span></p>
+        <p><strong>Entrada:</strong> <span id="input"></span></p>
+        <p><strong>Saída:</strong> <span id="output"></span></p>
+        <p><strong>Logs:</strong> <span id="logpath"></span></p>
+      </section>
+      <div>
+        <button onclick="generateDummy()">Gerar vídeo dummy</button>
+        <button onclick="refreshAll()">Recarregar lista</button>
+        <button onclick="loadLog()">Ver log</button>
+      </div>
+      <table>
+        <thead>
+          <tr>
+            <th>Arquivo</th>
+            <th>Tamanho (bytes)</th>
+            <th>Modificado</th>
+          </tr>
+        </thead>
+        <tbody id="files"></tbody>
+      </table>
+      <h2>Log do Guardião</h2>
+      <div id="log">Nenhum log carregado.</div>
+    </main>
+    <script>
+      const port = window.location.port || "8507";
+      function fmtDate(epoch) {
+        if (!epoch) return "-";
+        const d = new Date(epoch * 1000);
+        return d.toLocaleString();
+      }
+      async function fetchJson(path) {
+        const res = await fetch(path);
+        if (!res.ok) throw new Error(await res.text());
+        return res.json();
+      }
+      async function refreshStatus() {
+        const data = await fetchJson("/api/status");
+        document.getElementById("status").textContent = data.NO_DEPS ? "NO_DEPS=1" : "NO_DEPS=0";
+        document.getElementById("input").textContent = data.input;
+        document.getElementById("output").textContent = data.output;
+        document.getElementById("logpath").textContent = data.log;
+        document.getElementById("banner").textContent = `Porta ${port} — Atualizado em ${fmtDate(data.time)}`;
+      }
+      async function refreshFiles() {
+        const files = await fetchJson("/api/output");
+        const tbody = document.getElementById("files");
+        tbody.innerHTML = "";
+        files.forEach(item => {
+          const tr = document.createElement("tr");
+          const date = new Date(item.mtime * 1000).toLocaleString();
+          tr.innerHTML = `<td>${item.name}</td><td>${item.size}</td><td>${date}</td>`;
+          tbody.appendChild(tr);
+        });
+      }
+      async function loadLog() {
+        const res = await fetch("/api/log");
+        const text = await res.text();
+        document.getElementById("log").textContent = text || "(sem log)";
+      }
+      async function generateDummy() {
+        const res = await fetch("/api/generate_dummy", { method: "POST" });
+        if (!res.ok) {
+          alert("Erro ao gerar dummy");
+          return;
+        }
+        const payload = await res.json();
+        alert(`Gerado: ${payload.created}`);
+        await refreshAll();
+      }
+      async function refreshAll() {
+        await refreshStatus();
+        await refreshFiles();
+        await loadLog();
+      }
+      refreshAll().catch(err => {
+        document.getElementById("log").textContent = `Erro: ${err}`;
+      });
+      setInterval(refreshAll, 10000);
+    </script>
+  </body>
+</html>
diff --git a/ui_fallback/ui_fallback_server.py b/ui_fallback/ui_fallback_server.py
new file mode 100644
index 0000000000000000000000000000000000000000..5d9a5d28879b0fdbb247ea2d34d85ebe1b676db6
--- /dev/null
+++ b/ui_fallback/ui_fallback_server.py
@@ -0,0 +1,158 @@
+"""Fallback UI server using only the Python standard library."""
+from __future__ import annotations
+
+import json
+import os
+import time
+import socketserver
+from http import HTTPStatus
+from http.server import BaseHTTPRequestHandler, HTTPServer
+from pathlib import Path
+from typing import Dict, List
+from urllib.parse import urlparse
+
+try:  # Optional dependency
+    from dotenv import load_dotenv  # type: ignore
+except Exception:  # pragma: no cover - optional dependency missing
+    def load_dotenv() -> None:  # type: ignore
+        return None
+
+
+load_dotenv()
+
+BASE_DIR = Path(__file__).resolve().parent
+PROJECT_ROOT = BASE_DIR.parent
+
+DEFAULT_INPUT = PROJECT_ROOT / "data" / "Videos_Para_Editar"
+DEFAULT_OUTPUT = PROJECT_ROOT / "data" / "Videos_Agendados"
+DEFAULT_LOG = PROJECT_ROOT / "logs" / "guardian.log"
+
+PORT = int(os.environ.get("AFI_PORT", "8507"))
+NO_DEPS = os.environ.get("NO_DEPS", "0") == "1"
+INPUT_DIR = Path(os.environ.get("AFI_INPUT_DIR", str(DEFAULT_INPUT))).resolve()
+OUTPUT_DIR = Path(os.environ.get("AFI_OUTPUT_DIR", str(DEFAULT_OUTPUT))).resolve()
+LOG_FILE = Path(os.environ.get("AFI_LOG_DIR", str(DEFAULT_LOG.parent))).resolve() / "guardian.log"
+
+INPUT_DIR.mkdir(parents=True, exist_ok=True)
+OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
+LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
+
+TAIL_LINES = 200
+DUMMY_SIZE_BYTES = 512 * 1024
+
+
+def _tail_text(path: Path, lines: int) -> str:
+    if not path.exists() or not path.is_file():
+        return ""
+    try:
+        with path.open("r", encoding="utf-8", errors="ignore") as handle:
+            content = handle.readlines()
+        return "".join(content[-lines:])
+    except Exception as exc:  # pragma: no cover - log file edge cases
+        return f"<erro ao ler log: {exc}>"
+
+
+def _list_output() -> List[Dict[str, object]]:
+    entries: List[Dict[str, object]] = []
+    for child in sorted(OUTPUT_DIR.iterdir()):
+        if child.is_file():
+            stat = child.stat()
+            entries.append(
+                {
+                    "name": child.name,
+                    "size": stat.st_size,
+                    "mtime": stat.st_mtime,
+                }
+            )
+    return entries
+
+
+def _status_payload() -> Dict[str, object]:
+    return {
+        "NO_DEPS": NO_DEPS,
+        "input": str(INPUT_DIR),
+        "output": str(OUTPUT_DIR),
+        "log": str(LOG_FILE),
+        "time": time.time(),
+    }
+
+
+def _create_dummy_file() -> Path:
+    timestamp = int(time.time())
+    filename = f"dummy_{timestamp}.mp4"
+    target = INPUT_DIR / filename
+    random_bytes = os.urandom(DUMMY_SIZE_BYTES)
+    with target.open("wb") as handle:
+        handle.write(random_bytes)
+    return target
+
+
+class _RequestHandler(BaseHTTPRequestHandler):
+    server_version = "AfiFallback/1.0"
+
+    def log_message(self, format: str, *args) -> None:  # pragma: no cover - console noise
+        return
+
+    def _set_headers(self, status: HTTPStatus = HTTPStatus.OK, content_type: str = "application/json") -> None:
+        self.send_response(status)
+        self.send_header("Content-Type", content_type)
+        self.send_header("Access-Control-Allow-Origin", "*")
+        self.send_header("Access-Control-Allow-Headers", "*")
+        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
+        self.end_headers()
+
+    def do_OPTIONS(self) -> None:  # noqa: N802
+        self._set_headers(HTTPStatus.NO_CONTENT)
+
+    def do_GET(self) -> None:  # noqa: N802
+        parsed = urlparse(self.path)
+        if parsed.path == "/":
+            index_path = BASE_DIR / "index.html"
+            content = index_path.read_bytes()
+            self._set_headers(content_type="text/html; charset=utf-8")
+            self.wfile.write(content)
+            return
+        if parsed.path == "/api/status":
+            self._set_headers()
+            self.wfile.write(json.dumps(_status_payload()).encode("utf-8"))
+            return
+        if parsed.path == "/api/output":
+            self._set_headers()
+            self.wfile.write(json.dumps(_list_output()).encode("utf-8"))
+            return
+        if parsed.path == "/api/log":
+            self._set_headers(content_type="text/plain; charset=utf-8")
+            self.wfile.write(_tail_text(LOG_FILE, TAIL_LINES).encode("utf-8"))
+            return
+        self._set_headers(HTTPStatus.NOT_FOUND)
+        self.wfile.write(b"Not Found")
+
+    def do_POST(self) -> None:  # noqa: N802
+        parsed = urlparse(self.path)
+        if parsed.path == "/api/generate_dummy":
+            target = _create_dummy_file()
+            payload = {"created": str(target)}
+            self._set_headers()
+            self.wfile.write(json.dumps(payload).encode("utf-8"))
+            return
+        self._set_headers(HTTPStatus.NOT_FOUND)
+        self.wfile.write(b"Not Found")
+
+
+class ThreadedHTTPServer(socketserver.ThreadingMixIn, HTTPServer):
+    daemon_threads = True
+
+
+def run() -> None:
+    server = ThreadedHTTPServer(("0.0.0.0", PORT), _RequestHandler)
+    print(f"Fallback UI disponível em http://localhost:{PORT} (NO_DEPS={'1' if NO_DEPS else '0'})")
+    try:
+        server.serve_forever()
+    except KeyboardInterrupt:  # pragma: no cover - manual shutdown
+        pass
+    finally:
+        server.server_close()
+
+
+if __name__ == "__main__":
+    run()
 
EOF
)
