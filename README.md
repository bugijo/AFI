# AFI Offline Toolkit

AFI roda 100% offline com uma interface Streamlit (ou fallback em HTML puro) e utilitarios para diagnostico, ingestao de documentos e empacotamento. O modo **NO_DEPS** permite simular toda a geracao de arquivos sem depender de bibliotecas pesadas ou aceleracao multimedia.

## Estrutura recomendada

```
.
+- data/
¦  +- input/
¦  +- output/
+- logs/
+- knowledge_base/
+- third_party/
¦  +- ffmpeg/
+- scripts/
+- tools/
+- ui_fallback/
```

As pastas sao criadas automaticamente ao carregar `environment.load_settings()`, mas podem ser provisionadas com `mkdir` antecipadamente.

## Variaveis de ambiente (.env)

```
AFI_PORT=8507
AFI_INPUT_DIR=./data/input
AFI_OUTPUT_DIR=./data/output
AFI_LOG_DIR=./logs
NO_DEPS=1
```

Coloque os mesmos valores em `.env.example` para facilitar a replicacao do setup. Quando `NO_DEPS=1`, todo o sistema entra em **modo simulado**:

- O editor de video gera `dummy_arquivo.mp4` e `dummy_arquivo.json` em `AFI_OUTPUT_DIR`.
- O guardiao usa **polling** (sem watchdog) para detectar arquivos.
- A UI exibe um aviso permanente informando que o modo simulado esta ativo.

## Scripts principais

| Script | Descricao |
| --- | --- |
| `scripts/run_ui.sh` / `.bat` | Inicializa a UI. Se `streamlit` nao estiver disponivel, sobe o fallback em `ui_fallback/` automaticamente. |
| `scripts/run_guardian.sh` / `.bat` | Inicia o guardiao de videos com leitura das variaveis do `.env`. |
| `scripts/ingest_docs.py <pasta-ou-arquivo>` | Copia PDFs/TXT/MD/DOCX para `knowledge_base/`. |
| `scripts/build_wheelhouse.sh` / `.ps1` | Faz download das dependencias (com internet) para `wheelhouse/` e gera `wheels.zip`. |

Execute qualquer script a partir da raiz do projeto. Em Windows prefira `py` (ex.: `py scripts\ingest_docs.py docs/`).

## UI Fallback (HTML)

Quando o Streamlit nao esta instalado, os scripts de inicializacao chamam `ui_fallback/ui_fallback_server.py`. Ele expoe endpoints REST:

- `GET /api/status` – status geral e caminhos configurados.
- `GET /api/output` – lista de arquivos de saida com tamanho e data.
- `GET /api/log` – ultimos ~4000 caracteres do log mais recente.
- `POST /api/generate_dummy` – força a criacao de dummy (`executar_modo_simulado`).

A pagina `ui_fallback/index.html` e responsiva, tema dark neon, atualiza a cada 2 s, permite ordenar a tabela e exibe toasts para feedback.

## Ferramentas auxiliares (`tools/`)

- `diagnostics.py` – resume diretorios, uso de disco e localizacao do FFmpeg. Use `--json` para saida estruturada.
- `probe_models.py` – verifica a presenca de bibliotecas de IA (llama-index, transformers etc.) e lista arquivos da `knowledge_base`.

## Testes

O teste `tests/test_no_deps.py` garante que o modo simulado gera os artefatos dummy esperados. Rode com:

```
py -m unittest tests.test_no_deps
```

## Empacotamento offline

1. Gere as dependencias (em maquina com internet): `scripts/build_wheelhouse.sh` ou `.ps1`.
2. Copie `wheels.zip` para o ambiente isolado e instale com `pip install --no-index --find-links wheelhouse -r requirements.txt`.
3. Para montar o bundle final execute o passo de release (ver instrucoes do item 5 da tarefa).

## Dicas rapidas

- Verifique as pastas com `py tools/diagnostics.py`.
- Use `scripts/ingest_docs.py` sempre que novos PDFs precisarem entrar na base.
- No modo real (com dependencias instaladas), defina `NO_DEPS=0` no `.env` para habilitar a edicao real de videos.
- O guardiao pode ser parado com `Ctrl+C`; em modo polling ele continua verificando a cada 2 s.
