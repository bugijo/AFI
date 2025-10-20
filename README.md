# AFI Assistente - Guia Rápido

## Instalação
```bash
pip install -r requirements.txt
```

> **Pré-requisito:** tenha o [FFmpeg](https://ffmpeg.org/) instalado e disponível na variável de ambiente `PATH`.

### Instalação offline
1. Em uma máquina com internet execute `scripts/offline/build_wheelhouse.sh` (Linux/macOS) ou `scripts/offline/build_wheelhouse.ps1` (Windows) para gerar `wheels.zip` com todas as dependências.
2. Transfira `wheels.zip` para o ambiente isolado, extraia em `./wheels` e instale com:
   ```bash
   pip install --no-index --find-links wheels -r requirements.txt
   ```
3. Caso o FFmpeg não esteja disponível no `PATH`, copie o binário para `third_party/ffmpeg/<os>/bin/ffmpeg` e ajuste `IMAGEIO_FFMPEG_EXE` no `.env`.

### Modo NO_DEPS (simulado)
Quando estiver em um ambiente sem acesso à internet ou sem as bibliotecas multimídia instaladas, defina `NO_DEPS=1` no `.env`:

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