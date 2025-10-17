# 🤖 AFI v4.0 - Agente de Mídia Social

## 🎯 Visão Geral

O **Agente de Mídia Social** é um sistema automatizado completo que transforma vídeos em conteúdo otimizado para redes sociais. Ele combina inteligência artificial, edição automática de vídeo e monitoramento de arquivos para criar um fluxo de trabalho totalmente automatizado.

## 🏗️ Arquitetura do Sistema

### 🔍 1. O Guardião (Watcher)
- **Arquivo**: `guardiao_midia.py`
- **Função**: Monitora a pasta `C:/AFI/Videos_Para_Editar`
- **Tecnologia**: Biblioteca `watchdog`
- **Ação**: Detecta novos vídeos automaticamente

### 🧠 2. Cérebro Criativo (AFI)
- **Arquivo**: `integracao_afi_midia.py`
- **Função**: Analisa vídeos e gera frases de impacto
- **Tecnologia**: Integração com AFI Core + modo simulado
- **Ação**: Sugere texto e estilo musical

### 🎬 3. Oficina de Edição (Editor)
- **Arquivo**: `editor_video.py`
- **Função**: Edita vídeos automaticamente
- **Tecnologia**: Biblioteca `MoviePy`
- **Ação**: Remove áudio, adiciona música e texto

### 📅 4. Fila de Saída (Agendador)
- **Pasta**: `C:/AFI/Videos_Agendados`
- **Função**: Armazena vídeos prontos para publicação
- **Futuro**: Integração com APIs de redes sociais

## 🚀 Como Usar

### Configuração Inicial
```bash
# 1. Configurar sistema e criar pastas
py agente_midia_social.py --setup

# 2. Adicionar músicas nas pastas de estilo
# Ver: INSTRUCOES_MUSICAS.md
```

### Modo Automático (Recomendado)
```bash
# Inicia monitoramento contínuo
py agente_midia_social.py

# Agora apenas adicione vídeos em C:/AFI/Videos_Para_Editar
# O sistema processará automaticamente!
```

### Modo Manual
```bash
# Processar vídeo específico
py agente_midia_social.py --video "meu_video.mp4"

# Com música personalizada
py agente_midia_social.py --video "video.mp4" --musica "musica.mp3"

# Com texto personalizado
py agente_midia_social.py --video "video.mp4" --texto "🚀 Minha frase!"
```

## 📁 Estrutura de Pastas

```
C:\AFI\
├── Videos_Para_Editar\     # 📥 Entrada: Coloque vídeos aqui
├── Videos_Agendados\       # 📤 Saída: Vídeos processados
└── Musicas\               # 🎵 Biblioteca musical
    ├── Rock\
    ├── Pop\
    ├── Eletronica\
    ├── Calma\
    └── Instrumental\
```

## 🔧 Componentes do Sistema

### Scripts Principais
- `agente_midia_social.py` - **Script principal e orquestrador**
- `guardiao_midia.py` - **Monitoramento de arquivos**
- `editor_video.py` - **Edição automatizada**
- `integracao_afi_midia.py` - **Análise inteligente**

### Dependências
- `moviepy` - Edição de vídeo
- `watchdog` - Monitoramento de arquivos
- `pathlib` - Manipulação de caminhos
- `logging` - Sistema de logs

## 🎯 Fluxo de Trabalho

1. **📥 Entrada**: Usuário adiciona vídeo em `Videos_Para_Editar`
2. **👁️ Detecção**: Guardião detecta novo arquivo
3. **🧠 Análise**: AFI analisa e sugere frase + estilo musical
4. **🎵 Seleção**: Sistema escolhe música do estilo sugerido
5. **🎬 Edição**: MoviePy processa o vídeo:
   - Remove áudio original
   - Adiciona música de fundo
   - Sobrepõe texto personalizado
6. **📤 Saída**: Vídeo final salvo em `Videos_Agendados`

## 📊 Recursos Avançados

### Logging Inteligente
- Logs detalhados em `agente_midia_social.log`
- Estatísticas de processamento
- Monitoramento de erros

### Interface de Linha de Comando
- Múltiplos modos de operação
- Parâmetros personalizáveis
- Ajuda integrada (`--help`)

### Integração AFI
- Análise inteligente de conteúdo
- Modo simulado para testes
- Geração criativa de frases

## 🔍 Monitoramento e Estatísticas

O sistema fornece estatísticas em tempo real:
- ⏱️ Tempo de execução
- 🎬 Vídeos processados
- ✅ Taxa de sucesso
- ❌ Erros encontrados

## 🛠️ Solução de Problemas

### Erro: "ModuleNotFoundError"
```bash
# Reinstalar dependências
pip install moviepy==1.0.3
pip install watchdog
```

### Erro: "Arquivo não encontrado"
- Verifique se as pastas foram criadas (`--setup`)
- Confirme caminhos dos arquivos
- Verifique permissões de escrita

### Música não encontrada
- Adicione arquivos MP3 nas pastas de estilo
- Veja `INSTRUCOES_MUSICAS.md`

## 🚀 Próximos Passos

### Implementações Futuras
1. **API de Redes Sociais**: Publicação automática
2. **Análise de Vídeo**: Reconhecimento de objetos/cenas
3. **Templates Visuais**: Múltiplos estilos de texto
4. **Agendamento**: Publicação em horários específicos
5. **Dashboard Web**: Interface visual de controle

### Melhorias Planejadas
- Suporte a mais formatos de vídeo
- Edição de duração automática
- Filtros e efeitos visuais
- Análise de sentimento do conteúdo

## 📝 Exemplo de Uso Completo

```bash
# 1. Configurar sistema
py agente_midia_social.py --setup

# 2. Adicionar músicas (ver INSTRUCOES_MUSICAS.md)
# Copiar arquivos MP3 para C:\AFI\Musicas\[estilo]\

# 3. Iniciar monitoramento
py agente_midia_social.py

# 4. Em outra janela, adicionar vídeo
# Copiar video.mp4 para C:\AFI\Videos_Para_Editar\

# 5. Aguardar processamento automático
# Resultado em C:\AFI\Videos_Agendados\
```

## 🎉 Conclusão

O **AFI v4.0 - Agente de Mídia Social** representa um marco na automação de criação de conteúdo. Ele combina:

- 🤖 **Automação Completa**: Do upload à edição final
- 🧠 **Inteligência Artificial**: Análise e sugestões criativas
- 🎬 **Edição Profissional**: Qualidade de produção automatizada
- 📊 **Monitoramento**: Controle total do processo

**Resultado**: Transforme qualquer vídeo em conteúdo otimizado para redes sociais em segundos, sem intervenção manual!

---

*Desenvolvido com ❤️ usando AFI v4.0*
*Para suporte: Consulte os logs ou execute com `--help`*