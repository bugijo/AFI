# AFI v3.0 - Assistente Finiti Inteligente

## 🚀 Inicialização Rápida

### Porta Padrão: 8507

Este sistema foi configurado para usar **SEMPRE** a porta **8507** para evitar confusão com múltiplas portas.

### Formas de Iniciar o Sistema

#### 1. Método Recomendado (Windows)
```bash
start_afi.bat
```

#### 2. Script Python
```bash
python start_server.py
```

#### 3. Comando Direto
```bash
py -m streamlit run app.py --server.port 8507 --server.headless true
```

## 📋 URLs de Acesso

- **Local:** http://localhost:8507
- **Rede:** http://192.168.1.27:8507 (substitua pelo seu IP)

## 📁 Estrutura do Projeto

```
AML/
├── app.py              # Aplicação principal Streamlit
├── core_logic.py       # Lógica principal do sistema
├── config.py           # Configurações (PORTA PADRÃO: 8507)
├── start_server.py     # Script de inicialização
├── start_afi.bat       # Arquivo batch para Windows
├── memoria/            # Pasta de arquivos para processamento
├── storage/            # Armazenamento do índice RAG
└── README.md           # Este arquivo
```

## ⚙️ Configuração

A porta padrão está definida no arquivo `config.py`:

```python
SERVER_CONFIG = {
    "port": 8507,  # Porta padrão única
    "host": "localhost",
    "headless": True
}
```

## 🔧 Resolução de Problemas

### Porta em Uso
Se a porta 8507 estiver em uso, pare todos os processos Streamlit:
```bash
taskkill /f /im streamlit.exe
```

### Dependências
Certifique-se de que todas as dependências estão instaladas:
```bash
pip install streamlit llama-index sentence-transformers
```

## 📝 Regras Importantes

1. **SEMPRE use a porta 8507**
2. **NÃO inicie múltiplos servidores**
3. **Use os scripts fornecidos para inicialização**
4. **Verifique se a porta está livre antes de iniciar**

## 🎯 Funcionalidades

- ✅ Chat inteligente com IA
- ✅ Processamento de documentos (PDF, TXT)
- ✅ Transcrição de vídeos (quando disponível)
- ✅ Análise de imagens
- ✅ Sistema RAG (Retrieval-Augmented Generation)
- ✅ Interface web moderna

---

**Desenvolvido para Finiti - Versão 3.0**