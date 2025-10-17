import streamlit as st
import time
import os
from pathlib import Path
from config import SERVER_CONFIG, get_server_port, get_server_url
from core_logic import verificar_conexao_ollama, carregar_memoria, processar_prompt_geral
from streamlit_chat import message
from streamlit_option_menu import option_menu
from llama_index.core import Settings, VectorStoreIndex, SimpleDirectoryReader
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.memory import ChatMemoryBuffer

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
        embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")
        Settings.embed_model = embed_model
        
        # Configurar LLM padrão
        llm = Ollama(model="llava-llama3", request_timeout=120.0)
        Settings.llm = llm
        
        return True
    except Exception as e:
        st.code(f"Erro na configuração do sistema: {str(e)}")
        return False

def inicializar_rag(pasta_memoria="memoria"):
    """Inicializa o motor RAG uma única vez - Padrão Singleton"""
    import traceback
    
    try:
        print("DEBUG: Inicializando o motor RAG...")
        
        # Primeiro, processar arquivos de mídia (vídeos, imagens)
        print("DEBUG: Processando arquivos de mídia...")
        carregar_memoria(pasta_memoria)
        
        # Verificar se a pasta existe e tem arquivos
        if not os.path.exists(pasta_memoria):
            print(f"DEBUG: Pasta não encontrada: {pasta_memoria}")
            return None, None
            
        print(f"DEBUG: Pasta encontrada: {pasta_memoria}")
        
        # Carregar documentos da pasta (excluindo vídeos se pydub não funcionar)
        print("DEBUG: Carregando documentos...")
        
        # Filtrar arquivos para evitar problemas com vídeos
        import glob
        arquivos_validos = []
        extensoes_video = ['.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv']
        
        for arquivo in glob.glob(os.path.join(pasta_memoria, "*")):
            if os.path.isfile(arquivo):
                extensao = os.path.splitext(arquivo)[1].lower()
                if extensao in extensoes_video:
                    print(f"DEBUG: Pulando arquivo de vídeo: {os.path.basename(arquivo)}")
                    continue
                arquivos_validos.append(arquivo)
        
        print(f"DEBUG: {len(arquivos_validos)} arquivos válidos encontrados")
        
        if not arquivos_validos:
            print("DEBUG: Nenhum arquivo válido encontrado (apenas vídeos)")
            return None, None
        
        # Carregar apenas arquivos válidos
        documents = SimpleDirectoryReader(input_files=arquivos_validos).load_data()
        
        if not documents:
            print(f"DEBUG: Nenhum documento carregado da pasta: {pasta_memoria}")
            return None, None
            
        print(f"DEBUG: {len(documents)} documentos carregados com sucesso!")
        
        # Criar índice
        print("DEBUG: Criando índice vetorial...")
        index = VectorStoreIndex.from_documents(documents)
        
        # Criar query engine
        print("DEBUG: Criando query engine...")
        query_engine = index.as_query_engine()
        
        # 🧠 NOVA FUNCIONALIDADE: Criar ChatEngine com memória conversacional
        print("DEBUG: Criando ChatEngine com memória conversacional...")
        memory = ChatMemoryBuffer.from_defaults(token_limit=3000)
        chat_engine = index.as_chat_engine(
            chat_mode="context",
            memory=memory,
            system_prompt=(
                "Você é o AFI (Assistente Finiti Inteligente), um assistente especializado em engenharia, "
                "construção e equipamentos da empresa Finiti. Você tem acesso à base de conhecimento da empresa "
                "e pode manter conversas contextuais. Sempre se lembre do contexto anterior da conversa. "
                "Quando o usuário se referir a 'isso', 'aquilo', ou usar pronomes, considere o contexto da conversa anterior."
            )
        )
        
        print("DEBUG: Motor RAG e ChatEngine inicializados com sucesso!")
        return query_engine, chat_engine
        
    except Exception as e:
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

# Configuração da página
st.set_page_config(
    page_title="AFI v3.0 - Assistente Finiti Inteligente",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

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

/* Melhora o espaçamento do container principal */
.main .block-container {
    padding-bottom: 120px !important;
}
</style>
"""
st.markdown(css, unsafe_allow_html=True)

# =================================================================================
# ARQUITETURA DE INICIALIZAÇÃO DEFINITIVA - SISTEMA ROBUSTO E À PROVA DE FALHAS
# =================================================================================

@st.cache_resource(show_spinner='Inicializando o cérebro do AFI... Este processo pode levar um momento.')
def inicializar_sistema(pasta_memoria="memoria"):
    """
    Função de inicialização definitiva do sistema AFI.
    Carrega TODA a lógica pesada de forma robusta e confiável.
    Retorna o query_engine pronto para uso.
    """
    import traceback
    
    try:
        print("DEBUG: Inicializando sistema AFI com arquitetura robusta...")
        
        # Configurar Settings do LlamaIndex
        print("DEBUG: Configurando Settings do LlamaIndex...")
        Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
        Settings.llm = Ollama(model="llama3.2", request_timeout=120.0)
        
        # Processar arquivos de mídia
        print("DEBUG: Processando arquivos de mídia...")
        carregar_memoria(pasta_memoria)
        
        # Verificar se a pasta existe
        if not os.path.exists(pasta_memoria):
            print(f"DEBUG: Pasta não encontrada: {pasta_memoria}")
            return None
            
        print(f"DEBUG: Pasta encontrada: {pasta_memoria}")
        
        # Filtrar arquivos válidos (excluindo vídeos)
        import glob
        arquivos_validos = []
        extensoes_video = ['.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv']
        
        for arquivo in glob.glob(os.path.join(pasta_memoria, "*")):
            if os.path.isfile(arquivo):
                extensao = os.path.splitext(arquivo)[1].lower()
                if extensao in extensoes_video:
                    print(f"DEBUG: Pulando arquivo de vídeo: {os.path.basename(arquivo)}")
                    continue
                arquivos_validos.append(arquivo)
        
        print(f"DEBUG: {len(arquivos_validos)} arquivos válidos encontrados")
        
        if not arquivos_validos:
            print("DEBUG: Nenhum arquivo válido encontrado")
            return None
        
        # Criar SimpleDirectoryReader com arquivos válidos
        print("DEBUG: Criando SimpleDirectoryReader...")
        documents = SimpleDirectoryReader(input_files=arquivos_validos).load_data()
        
        if not documents:
            print(f"DEBUG: Nenhum documento carregado da pasta: {pasta_memoria}")
            return None
            
        print(f"DEBUG: {len(documents)} documentos carregados com sucesso!")
        
        # Criar VectorStoreIndex
        print("DEBUG: Criando VectorStoreIndex...")
        index = VectorStoreIndex.from_documents(documents)
        
        # Criar query_engine
        print("DEBUG: Criando query_engine...")
        query_engine = index.as_query_engine()
        
        print("DEBUG: Sistema AFI inicializado com sucesso!")
        return query_engine
        
    except Exception as e:
        print("=" * 60)
        print("--- ERRO CRÍTICO NA INICIALIZAÇÃO DO SISTEMA ---")
        print(f"Tipo do erro: {type(e).__name__}")
        print(f"Mensagem: {str(e)}")
        print("Traceback completo:")
        traceback.print_exc()
        print("=" * 60)
        return None

# Carrega ou obtém do cache o motor RAG. A aplicação só continua depois que esta linha for concluída.
query_engine = inicializar_sistema()

# =================================================================================
# SEQUÊNCIA DE INICIALIZAÇÃO ROBUSTA - SISTEMA SEMPRE PRONTO
# =================================================================================

if not st.session_state.system_ready:
    # TELA DE CARREGAMENTO
    st.title("🏗️ AFI v3.0 - Assistente Finiti Inteligente")
    st.markdown("### 🧠 Inicializando o cérebro do AFI...")
    
    with st.spinner("Conectando memórias e IAs... Por favor, aguarde."):
        try:
            # Configurar sistema de IA
            sistema_ok = setup_sistema_ia()
            
            if sistema_ok:
                # Sinaliza que o sistema está pronto
                st.session_state.system_ready = True
                
                # Força o recarregamento do script
                st.rerun()
            else:
                st.error("❌ Erro na inicialização do sistema de IA")
                st.stop()
                
        except Exception as e:
            st.error(f"❌ Erro durante inicialização: {str(e)}")
            st.stop()

else:
    # =================================================================================
    # APLICAÇÃO PRINCIPAL - SISTEMA PRONTO
    # =================================================================================
    
    # Inicializar estado de navegação (PADRÃO: CHAT)
    if 'view' not in st.session_state:
        st.session_state.view = 'chat'

    # Inicializar session states
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Sidebar com menu de navegação
    with st.sidebar:
        st.title("🏗️ AFI v3.0")
        st.markdown("**Assistente Finiti Inteligente**")
        
        # Menu de navegação
        st.session_state.view = option_menu(
            menu_title=None,
            options=["Chat", "Painel", "Conhecimento", "Estúdio"],
            icons=["chat-dots", "speedometer2", "book", "camera-video-fill"],
            menu_icon="cast",
            default_index=0,
            key="main_menu"
        )

    # =================================================================================
    # RENDERIZAÇÃO CONDICIONAL POR ESTADO
    # =================================================================================

    # TELA DE CHAT (PADRÃO)
    if st.session_state.view == 'Chat':
        # Exibir mensagens do chat
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Input do chat
        if prompt := st.chat_input("Faça uma pergunta ao AFI v4.0..."):
            
            # Adiciona a mensagem do usuário ao histórico e à tela
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Lógica para obter e exibir a resposta da IA
            with st.chat_message("assistant", avatar="🏗️"):
                with st.spinner("Pensando..."):
                    # 🧠 NOVA LÓGICA: Usar ChatEngine com memória conversacional quando disponível
                    if st.session_state.chat_engine:
                        try:
                            # Usar ChatEngine que mantém contexto da conversa
                            resposta = st.session_state.chat_engine.chat(prompt)
                            resposta_texto = str(resposta)
                        except Exception as e:
                            # Fallback para o sistema antigo se ChatEngine falhar
                            resposta_texto = processar_prompt_geral(prompt, query_engine)
                            st.warning("⚠️ Usando modo compatibilidade (sem memória conversacional)")
                    else:
                        # Fallback para o sistema antigo
                        resposta_texto = processar_prompt_geral(prompt, query_engine)
                    
                    st.markdown(resposta_texto)
            
            # Adiciona a resposta da IA ao histórico
            st.session_state.messages.append({"role": "assistant", "content": resposta_texto})

    # TELA DE PAINEL
    elif st.session_state.view == 'Painel':
        st.title("📊 Painel do Sistema")
        
        # Layout do dashboard
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("📈 Estatísticas")
            # Métricas
            total_messages = len(st.session_state.messages)
            user_messages = len([m for m in st.session_state.messages if m["role"] == "user"])
            
            metric_col1, metric_col2 = st.columns(2)
            with metric_col1:
                st.metric("Mensagens Trocadas", total_messages)
            with metric_col2:
                st.metric("Perguntas do Usuário", user_messages)
            
            # Botão de limpeza
            if st.button("🗑️ Limpar Conversa", use_container_width=True):
                st.session_state.messages = []
                st.rerun()
        
        with col2:
            st.subheader("⚙️ Status do Sistema")
            status = verificar_status_sistema()
            
            st.code("Interface: Conectada ✅")
            st.code(f"Ollama: {'Conectado ✅' if status['ollama'] else 'Desconectado ❌'}")
            
            # Status do RAG usando a nova variável global
            if query_engine:
                st.success("RAG: Ativo ✅")
            else:
                st.error("RAG: Inativo ❌")
                
            st.code(f"Modelos Disponíveis: {status['models_count']}")

    # TELA DE GERENCIAMENTO DE CONHECIMENTO
    elif st.session_state.view == 'Conhecimento':
        st.title("📚 Gerenciamento de Conhecimento")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("🔗 Indexar Pasta por Referência")
            st.markdown("**🆕 Nova Funcionalidade:** Indexe uma pasta sem copiar os arquivos!")
            st.info("💡 Os arquivos permanecem em seus locais originais. Apenas as 'traduções' (embeddings) são armazenadas.")
            
            pasta_servidor = st.text_input(
                "",
                placeholder="\\\\SERVIDOR\\Documentos\\Manuais",
                label_visibility="collapsed"
            )
            
            if st.button("🔗 Indexar por Referência", use_container_width=True):
                if pasta_servidor and os.path.isdir(pasta_servidor):
                    try:
                        with st.spinner("🔗 Indexando arquivos por referência... Aguarde."):
                            # 🔗 USAR NOVA FUNÇÃO DE INDEXAÇÃO POR REFERÊNCIA
                            query_engine, chat_engine = indexar_por_referencia(pasta_servidor)
                            
                            if query_engine and chat_engine:
                                # Atualizar apenas o chat_engine (query_engine é gerenciado pelo cache)
                                st.session_state.chat_engine = chat_engine
                                
                                st.success(f"✅ Pasta indexada por referência com sucesso!")
                                st.info(f"📂 **Fonte:** {pasta_servidor}")
                                st.info("🧠 **Memória conversacional ativa!**")
                                st.warning("⚠️ Para usar a nova base, reinicie a aplicação para limpar o cache.")
                                
                                # Mostrar estatísticas
                                st.balloons()
                            else:
                                st.warning(f"⚠️ Pasta processada, mas nenhum documento válido encontrado!")
                    except Exception as e:
                        st.error(f"❌ Erro ao indexar por referência: {str(e)}")
                elif pasta_servidor:
                    st.error("❌ Caminho inválido ou diretório não encontrado!")
                else:
                    st.warning("⚠️ Por favor, insira um caminho válido!")
            
            # Separador visual
            st.markdown("---")
            
            # Seção de indexação tradicional (mantida para compatibilidade)
            st.subheader("📁 Indexação Tradicional")
            st.markdown("**(Modo Legado)** Indexar pasta local:")
            
            pasta_local = st.text_input(
                "",
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
             st.subheader("📊 Status da Base de Conhecimento")
             
             # Status dos engines
             if st.session_state.chat_engine:
                 st.success("🧠 **ChatEngine:** Ativo (com memória conversacional)")
             elif query_engine:
                 st.warning("🔍 **QueryEngine:** Ativo (sem memória conversacional)")
             else:
                 st.error("❌ **Nenhum engine ativo**")
             
             # 🔍 NOVA SEÇÃO: File System Watcher
             st.markdown("---")
             st.subheader("👁️ File System Watcher")
             
             if WATCHER_AVAILABLE:
                 # Inicializar o watcher service se ainda não foi feito
                 if not st.session_state.watcher_initialized:
                     try:
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
                             st.success("⏸️ Watcher parado!")
                             st.rerun()
                     
                     with col_watcher2:
                         if st.button("🔄 Reiniciar Watcher", use_container_width=True):
                             afi_watcher_service.stop()
                             afi_watcher_service.start()
                             st.success("🔄 Watcher reiniciado!")
                             st.rerun()
                     
                     # Adicionar pasta para monitoramento
                     st.markdown("**Adicionar pasta para monitoramento:**")
                     nova_pasta = st.text_input(
                         "",
                         placeholder="\\\\SERVIDOR\\Documentos\\Manuais",
                         label_visibility="collapsed",
                         key="nova_pasta_watcher"
                     )
                     
                     if st.button("➕ Adicionar Pasta", use_container_width=True):
                         if nova_pasta and os.path.isdir(nova_pasta):
                             try:
                                 afi_watcher_service.add_folder(nova_pasta)
                                 st.success(f"✅ Pasta adicionada ao monitoramento!")
                                 st.info(f"📂 {nova_pasta}")
                                 st.rerun()
                             except Exception as e:
                                 st.error(f"❌ Erro ao adicionar pasta: {str(e)}")
                         elif nova_pasta:
                             st.error("❌ Caminho inválido ou diretório não encontrado!")
                         else:
                             st.warning("⚠️ Por favor, insira um caminho válido!")
                 
                 else:
                     st.warning("👁️ **Watcher:** Inativo")
                     
                     if st.button("▶️ Iniciar Watcher", use_container_width=True):
                         try:
                             afi_watcher_service.start()
                             st.success("▶️ Watcher iniciado!")
                             st.rerun()
                         except Exception as e:
                             st.error(f"❌ Erro ao iniciar watcher: {str(e)}")
             else:
                 st.error("❌ **Watchdog não disponível**")
                 st.info("💡 Instale com: `pip install watchdog`")
             
             # Informações da pasta atual
             st.markdown("---")
             st.subheader("📋 Pasta de Memória Local")
             if os.path.exists("memoria"):
                 arquivos = os.listdir("memoria")
                 if arquivos:
                     st.write(f"📁 **Pasta de memória ativa:** `memoria/`")
                     st.write(f"📄 **Arquivos encontrados:** {len(arquivos)}")
                     
                     # Mostrar alguns arquivos
                     for arquivo in arquivos[:5]:
                         st.code(f"📄 {arquivo}")
                     
                     if len(arquivos) > 5:
                         st.code(f"... e mais {len(arquivos) - 5} arquivos")
                 else:
                     st.info("📁 Pasta de memória vazia")
             else:
                 st.warning("📁 Pasta de memória não encontrada")
             
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
                        from editor_video import obter_info_video
                        info = obter_info_video(str(video_path))
                        if info:
                            st.info(f"📊 Duração: {info['duracao']:.1f}s | Tamanho: {info['tamanho'][0]}x{info['tamanho'][1]}")
                    except:
                        pass
                
                st.markdown("---")
                st.subheader("🤖 Direção Criativa Automática")
                st.markdown("**A IA vai:**")
                st.markdown("• 🎯 Analisar o conteúdo do vídeo")
                st.markdown("• ✍️ Criar frase de marketing impactante")
                st.markdown("• 🎵 Escolher música perfeita")
                st.markdown("• 📱 Formatar para Stories (9:16)")
                st.markdown("• 🎨 Posicionar texto profissionalmente")
                
                st.markdown("---")
                
                # Botão de ação principal
                gerar_video_btn = st.button("🤖 Gerar Vídeo com IA", 
                                           disabled=not video_path,
                                           help="A IA fará toda a direção criativa automaticamente!")
                
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
                
                # Container para o vídeo
                video_result_container = st.container()
                
                with video_result_container:
                    # Verificar se há vídeo processado
                    if hasattr(st.session_state, 'video_processado') and st.session_state.video_processado:
                        video_path = st.session_state.video_processado
                        
                        if os.path.exists(video_path):
                            st.success("🎉 Vídeo editado pronto!")
                            
                            # Mostrar vídeo
                            with open(video_path, 'rb') as video_file:
                                video_bytes = video_file.read()
                                st.video(video_bytes)
                            
                            # Botão de download
                            st.download_button(
                                label="📥 Download do Vídeo",
                                data=video_bytes,
                                file_name=os.path.basename(video_path),
                                mime="video/mp4"
                            )
                            
                            # Informações do arquivo
                            file_size = os.path.getsize(video_path) / (1024 * 1024)  # MB
                            st.info(f"📁 Arquivo: {os.path.basename(video_path)} ({file_size:.1f} MB)")
                            
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
    
    try:
        print(f"DEBUG: Iniciando indexação por referência de: {caminho_diretorio}")
        
        # Verificar se o diretório existe
        if not os.path.exists(caminho_diretorio):
            print(f"DEBUG: Diretório não encontrado: {caminho_diretorio}")
            return None, None
            
        print(f"DEBUG: Diretório encontrado: {caminho_diretorio}")
        
        # Buscar todos os arquivos válidos recursivamente
        import glob
        arquivos_validos = []
        extensoes_video = ['.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv']
        extensoes_validas = ['.txt', '.pdf', '.docx', '.doc', '.md', '.rtf', '.odt']
        
        # Buscar recursivamente em todas as subpastas
        for extensao in extensoes_validas:
            pattern = os.path.join(caminho_diretorio, "**", f"*{extensao}")
            arquivos_encontrados = glob.glob(pattern, recursive=True)
            arquivos_validos.extend(arquivos_encontrados)
        
        # Filtrar arquivos de vídeo
        arquivos_finais = []
        for arquivo in arquivos_validos:
            if os.path.isfile(arquivo):
                extensao = os.path.splitext(arquivo)[1].lower()
                if extensao not in extensoes_video:
                    arquivos_finais.append(arquivo)
                else:
                    print(f"DEBUG: Pulando arquivo de vídeo: {os.path.basename(arquivo)}")
        
        print(f"DEBUG: {len(arquivos_finais)} arquivos válidos encontrados para indexação")
        
        if not arquivos_finais:
            print("DEBUG: Nenhum arquivo válido encontrado para indexação")
            return None, None
        
        # Mostrar alguns arquivos que serão indexados
        print("DEBUG: Primeiros arquivos a serem indexados:")
        for i, arquivo in enumerate(arquivos_finais[:5]):
            print(f"  {i+1}. {os.path.basename(arquivo)}")
        if len(arquivos_finais) > 5:
            print(f"  ... e mais {len(arquivos_finais) - 5} arquivos")
        
        # 🔗 INDEXAÇÃO POR REFERÊNCIA: Carregar documentos diretamente dos arquivos originais
        print("DEBUG: Carregando documentos por referência...")
        documents = SimpleDirectoryReader(input_files=arquivos_finais).load_data()
        
        if not documents:
            print(f"DEBUG: Nenhum documento carregado do diretório: {caminho_diretorio}")
            return None, None
            
        print(f"DEBUG: {len(documents)} documentos carregados com sucesso por referência!")
        
        # Criar índice
        print("DEBUG: Criando índice vetorial...")
        index = VectorStoreIndex.from_documents(documents)
        
        # Criar query engine
        print("DEBUG: Criando query engine...")
        query_engine = index.as_query_engine()
        
        # 🧠 Criar ChatEngine com memória conversacional
        print("DEBUG: Criando ChatEngine com memória conversacional...")
        memory = ChatMemoryBuffer.from_defaults(token_limit=3000)
        chat_engine = index.as_chat_engine(
            chat_mode="context",
            memory=memory,
            system_prompt=(
                f"Você é o AFI (Assistente Finiti Inteligente), um assistente especializado em engenharia, "
                f"construção e equipamentos da empresa Finiti. Você tem acesso à base de conhecimento da empresa "
                f"localizada em '{caminho_diretorio}' e pode manter conversas contextuais. "
                f"Sempre se lembre do contexto anterior da conversa. "
                f"Quando o usuário se referir a 'isso', 'aquilo', ou usar pronomes, considere o contexto da conversa anterior."
            )
        )
        
        print("DEBUG: Indexação por referência concluída com sucesso!")
        return query_engine, chat_engine
        
    except Exception as e:
        # DIAGNÓSTICO DETALHADO
        print("=" * 60)
        print("--- ERRO DETALHADO NA INDEXAÇÃO POR REFERÊNCIA ---")
        print(f"Tipo do erro: {type(e).__name__}")
        print(f"Mensagem: {str(e)}")
        print("Traceback completo:")
        traceback.print_exc()
        print("=" * 60)
        return None, None