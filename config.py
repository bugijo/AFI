# Configurações do Sistema AFI v3.0
# Este arquivo define as configurações padrão do sistema

# Configuração do Servidor
SERVER_CONFIG = {
    "port": 8507,  # Porta padrão única para o frontend
    "host": "localhost",
    "headless": True,
    "debug": False
}

# Configuração de Pastas
FOLDERS_CONFIG = {
    "memoria": "memoria",
    "storage": "storage"
}

# Configuração do RAG
RAG_CONFIG = {
    "model_name": "sentence-transformers/all-MiniLM-L6-v2",
    "chunk_size": 1000,
    "chunk_overlap": 200
}

# Configuração de Logs
LOG_CONFIG = {
    "level": "INFO",
    "format": "%(asctime)s - %(levelname)s - %(message)s"
}

def get_server_port():
    """Retorna a porta padrão do servidor"""
    return SERVER_CONFIG["port"]

def get_server_url():
    """Retorna a URL completa do servidor"""
    return f"http://{SERVER_CONFIG['host']}:{SERVER_CONFIG['port']}"

def get_streamlit_command():
    """Retorna o comando padrão para iniciar o Streamlit"""
    return f"py -m streamlit run app.py --server.port {SERVER_CONFIG['port']} --server.headless {str(SERVER_CONFIG['headless']).lower()}"