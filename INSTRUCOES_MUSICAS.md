# 🎵 Instruções para Configurar Músicas no Agente de Mídia Social

## Estrutura de Pastas Criada

O sistema criou automaticamente as seguintes pastas para organizar suas músicas:

```
C:\AFI\Musicas\
├── Rock\
├── Pop\
├── Eletronica\
├── Calma\
└── Instrumental\
```

## Como Adicionar Músicas

### 1. Baixar Músicas Livres de Direitos

**Sites Recomendados:**
- [YouTube Audio Library](https://studio.youtube.com/channel/UCuAXFkgsw1L7xaCfnd5JJOw/music)
- [Freesound.org](https://freesound.org/)
- [Pixabay Music](https://pixabay.com/music/)
- [Incompetech.com](https://incompetech.com/)
- [Zapsplat](https://www.zapsplat.com/)

### 2. Organizar por Estilo

Coloque as músicas nas pastas correspondentes ao estilo:

- **Rock**: Músicas energéticas, guitarras, bateria forte
- **Pop**: Músicas comerciais, melodias cativantes
- **Eletrônica**: Música eletrônica, EDM, synthwave
- **Calma**: Música relaxante, ambient, lo-fi
- **Instrumental**: Música sem vocal, orquestral, piano

### 3. Formatos Suportados

- **MP3** (recomendado)
- **WAV**
- **M4A**
- **OGG**

### 4. Exemplo de Organização

```
C:\AFI\Musicas\
├── Rock\
│   ├── energia_rock_01.mp3
│   ├── guitarra_power_02.mp3
│   └── rock_motivacional_03.mp3
├── Pop\
│   ├── pop_alegre_01.mp3
│   ├── melodia_comercial_02.mp3
│   └── pop_moderno_03.mp3
├── Eletronica\
│   ├── edm_energetico_01.mp3
│   ├── synthwave_retro_02.mp3
│   └── eletronica_dance_03.mp3
├── Calma\
│   ├── relaxante_piano_01.mp3
│   ├── ambient_natureza_02.mp3
│   └── lofi_chill_03.mp3
└── Instrumental\
    ├── orquestral_epico_01.mp3
    ├── piano_emocional_02.mp3
    └── violino_classico_03.mp3
```

## Como o Sistema Seleciona Músicas

1. **Análise AFI**: O sistema analisa o vídeo e sugere um estilo musical
2. **Seleção Automática**: Escolhe aleatoriamente uma música da pasta do estilo sugerido
3. **Fallback**: Se não houver música no estilo, usa qualquer música disponível

## Testando o Sistema

### Teste Rápido (Modo Setup)
```bash
py agente_midia_social.py --setup
```

### Teste com Vídeo Específico
```bash
py agente_midia_social.py --video "meu_video.mp4" --texto "🚀 Minha frase!"
```

### Modo Monitoramento Automático
```bash
py agente_midia_social.py
```

## Dicas Importantes

1. **Qualidade**: Use músicas de boa qualidade (128kbps ou superior)
2. **Duração**: Músicas de 30-60 segundos são ideais para stories
3. **Volume**: O sistema ajustará automaticamente o volume
4. **Direitos**: Use apenas músicas livres de direitos autorais
5. **Backup**: Mantenha backup de suas músicas favoritas

## Próximos Passos

1. Adicione pelo menos 2-3 músicas em cada pasta de estilo
2. Teste com um vídeo de exemplo
3. Configure o monitoramento automático
4. Aproveite a automação! 🤖

---

**💡 Dica Pro**: Crie uma biblioteca diversificada de músicas para que o AFI tenha mais opções para combinar com diferentes tipos de conteúdo!