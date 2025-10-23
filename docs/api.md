# 🌐 AFI Guardião - Documentação da API

## 📋 Visão Geral

O AFI Guardião expõe múltiplas interfaces de API para diferentes propósitos:
- **Frontend Streamlit** (porta 8507): Interface principal do usuário
- **Backend Flask** (porta 8508): API REST para comunicação entre serviços
- **UI Fallback** (porta 8507): Interface de emergência quando Streamlit não está disponível

## 🔌 Esquema de Portas

| Serviço | Porta | Protocolo | Descrição |
|---------|-------|-----------|-----------|
| **Frontend Streamlit** | `8507` | HTTP | Interface principal do usuário |
| **Backend API** | `8508` | HTTP | API REST para comunicação entre serviços |
| **UI Fallback** | `8507` | HTTP | Interface de emergência (fallback) |
| **Redis** | `6379` | TCP | Cache e sistema de filas |
| **Prometheus** | `9090` | HTTP | Métricas de monitoramento |
| **Grafana** | `3000` | HTTP | Dashboards de visualização |

### Variáveis de Ambiente

```bash
# Configurações de Rede
AFI_PORT=8507                    # Porta do frontend
AFI_BACKEND_PORT=8508           # Porta do backend
AFI_HOST=localhost              # Host padrão

# Configurações de Pastas
AFI_INPUT_DIR=./data/input      # Pasta de entrada
AFI_OUTPUT_DIR=./data/output    # Pasta de saída
AFI_LOG_DIR=./logs              # Pasta de logs
AFI_MUSIC_DIR=./data/musics     # Pasta de músicas

# Configurações de Processamento
AFI_WORKERS=2                   # Número de workers
AFI_PROCESSING_TIMEOUT=300      # Timeout em segundos
POLLING_INTERVAL=2              # Intervalo de polling
VIDEO_QUALITY=medium            # Qualidade do vídeo

# Configurações de IA
OLLAMA_URL=http://localhost:11434  # URL do Ollama
OLLAMA_MODEL=llava-llama3          # Modelo padrão

# Modo de Operação
NO_DEPS=0                       # Modo simulado (0=real, 1=simulado)
DEBUG_MODE=false                # Modo debug
```

---

## 🎯 Backend API (Porta 8508)

### Base URL
```
http://localhost:8508
```

### 1. Health Check

**Endpoint:** `GET /`

**Descrição:** Verificação de saúde do backend

**Resposta:**
```json
{
  "status": "healthy",
  "service": "AFI v4.0 Backend",
  "port": 8508,
  "timestamp": "2024-01-15T10:30:00.000Z",
  "message": "Backend funcionando corretamente na porta 8508"
}
```

### 2. Status do Sistema

**Endpoint:** `GET /api/status`

**Descrição:** Retorna status geral do sistema

**Resposta:**
```json
{
  "backend_status": "running",
  "frontend_port": 8507,
  "backend_port": 8508,
  "timestamp": "2024-01-15T10:30:00.000Z",
  "uptime": "Sistema ativo"
}
```

### 3. Pastas Monitoradas

**Endpoint:** `GET /api/folders`

**Descrição:** Lista pastas monitoradas pelo sistema

**Resposta:**
```json
{
  "monitored_folders": [
    {
      "path": "C:\\FINITI_CONHECIMENTO",
      "status": "available",
      "type": "knowledge_sanctuary"
    }
  ],
  "count": 1,
  "timestamp": "2024-01-15T10:30:00.000Z"
}
```

### 4. Base de Conhecimento

**Endpoint:** `GET /api/knowledge`

**Descrição:** Informações sobre a base de conhecimento

**Resposta:**
```json
{
  "knowledge_base": {
    "status": "active",
    "documents_count": 150,
    "last_updated": "2024-01-15T09:00:00.000Z",
    "index_size": "2.5MB"
  },
  "rag_system": {
    "model": "llava-llama3",
    "embedding_model": "sentence-transformers/all-MiniLM-L6-v2",
    "status": "ready"
  },
  "timestamp": "2024-01-15T10:30:00.000Z"
}
```

---

## 🔄 UI Fallback API (Porta 8507)

### Base URL
```
http://localhost:8507
```

### 1. Status do Sistema

**Endpoint:** `GET /api/status`

**Descrição:** Status geral do sistema via UI fallback

**Resposta:**
```json
{
  "no_deps_mode": false,
  "input_dir": "./data/input",
  "output_dir": "./data/output",
  "log_dir": "./logs",
  "output_count": 12,
  "timestamp": "2024-01-15T10:30:00.000Z",
  "system_info": {
    "python_version": "3.10.0",
    "platform": "Windows",
    "memory_usage": "256MB"
  }
}
```

### 2. Arquivos de Saída

**Endpoint:** `GET /api/output`

**Descrição:** Lista arquivos processados na pasta de saída

**Resposta:**
```json
{
  "files": [
    {
      "name": "video_processado_001.mp4",
      "size": 15728640,
      "modified": "2024-01-15T10:25:00.000Z",
      "type": "video"
    },
    {
      "name": "relatorio_001.json",
      "size": 2048,
      "modified": "2024-01-15T10:25:30.000Z",
      "type": "report"
    }
  ],
  "total_count": 2,
  "total_size": 15730688,
  "timestamp": "2024-01-15T10:30:00.000Z"
}
```

### 3. Logs do Sistema

**Endpoint:** `GET /api/log`

**Descrição:** Logs recentes do sistema

**Parâmetros de Query:**
- `file` (opcional): Nome específico do arquivo de log

**Resposta:**
```json
{
  "file": "afi_guardiao_2024-01-15.log",
  "content": "2024-01-15 10:30:00 INFO - Sistema iniciado\n2024-01-15 10:30:05 INFO - Monitoramento ativo\n2024-01-15 10:30:10 INFO - Processando vídeo: input_001.mp4",
  "lines": 150,
  "last_updated": "2024-01-15T10:30:00.000Z",
  "timestamp": "2024-01-15T10:30:00.000Z"
}
```

### 4. Gerar Arquivo Dummy

**Endpoint:** `POST /api/generate_dummy`

**Descrição:** Força geração de arquivo dummy para teste

**Resposta:**
```json
{
  "status": "ok",
  "message": "Arquivo dummy gerado com sucesso",
  "file": "dummy_video_001.mp4",
  "timestamp": "2024-01-15T10:30:00.000Z"
}
```

---

## 🎬 Streamlit Frontend (Porta 8507)

### Base URL
```
http://localhost:8507
```

### Funcionalidades Principais

#### 1. Chat Inteligente
- **Rota:** `/` (página principal)
- **Funcionalidade:** Interface de chat com IA
- **Recursos:**
  - Processamento de linguagem natural
  - Integração com RAG (Retrieval-Augmented Generation)
  - Memória conversacional
  - Suporte a múltiplos modelos de IA

#### 2. Painel de Controle
- **Rota:** `/` (aba "Painel")
- **Funcionalidade:** Monitoramento do sistema
- **Recursos:**
  - Status em tempo real
  - Métricas de performance
  - Logs do sistema
  - Controle de serviços

#### 3. Base de Conhecimento
- **Rota:** `/` (aba "Conhecimento")
- **Funcionalidade:** Gerenciamento da base de conhecimento
- **Recursos:**
  - Upload de documentos
  - Indexação automática
  - Busca semântica
  - Visualização de documentos

#### 4. Estúdio de Vídeo
- **Rota:** `/` (aba "Estúdio")
- **Funcionalidade:** Processamento de vídeos
- **Recursos:**
  - Upload de vídeos
  - Edição automática
  - Geração de legendas
  - Exportação em múltiplos formatos

---

## 🔧 APIs de Sistema

### 1. Sistema de Filas

**Funcionalidades:**
- Filas prioritárias com Redis
- Monitoramento de throughput
- Balanceamento de carga
- Persistência entre reinicializações

**Estrutura de Task:**
```json
{
  "id": "task_001",
  "type": "video_processing",
  "priority": "high",
  "payload": {
    "input_file": "video.mp4",
    "output_format": "mp4",
    "quality": "high"
  },
  "status": "pending",
  "created_at": "2024-01-15T10:30:00.000Z",
  "started_at": null,
  "completed_at": null
}
```

### 2. Monitor de Performance

**Métricas Coletadas:**
```json
{
  "system": {
    "cpu_usage": 45.2,
    "memory_usage": 68.5,
    "disk_usage": 23.1,
    "network_io": {
      "bytes_sent": 1024000,
      "bytes_recv": 2048000
    }
  },
  "application": {
    "active_tasks": 3,
    "completed_tasks": 127,
    "failed_tasks": 2,
    "queue_size": 5
  },
  "timestamp": "2024-01-15T10:30:00.000Z"
}
```

### 3. Sistema de Qualidade

**Métricas de Código:**
```json
{
  "quality": {
    "coverage": 85.2,
    "complexity": "low",
    "maintainability": "A",
    "security_score": 9.2
  },
  "tests": {
    "total": 156,
    "passed": 152,
    "failed": 2,
    "skipped": 2,
    "duration": "45.2s"
  },
  "timestamp": "2024-01-15T10:30:00.000Z"
}
```

---

## 🚨 Códigos de Erro

### Códigos HTTP Padrão

| Código | Descrição | Exemplo |
|--------|-----------|---------|
| `200` | Sucesso | Operação realizada com sucesso |
| `400` | Bad Request | Parâmetros inválidos |
| `404` | Not Found | Endpoint não encontrado |
| `500` | Internal Server Error | Erro interno do servidor |
| `503` | Service Unavailable | Serviço temporariamente indisponível |

### Estrutura de Erro

```json
{
  "error": true,
  "code": "INVALID_PARAMETER",
  "message": "Parâmetro 'file' é obrigatório",
  "details": {
    "parameter": "file",
    "expected_type": "string",
    "received": null
  },
  "timestamp": "2024-01-15T10:30:00.000Z",
  "request_id": "req_001"
}
```

---

## 🔐 Autenticação e Segurança

### Headers Recomendados

```http
Content-Type: application/json
Accept: application/json
User-Agent: AFI-Client/1.0
X-Request-ID: unique-request-id
```

### Limitação de Taxa

- **Limite:** 100 requisições por minuto por IP
- **Header de Resposta:** `X-RateLimit-Remaining: 95`
- **Reset:** `X-RateLimit-Reset: 1642248600`

### CORS

```http
Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS
Access-Control-Allow-Headers: Content-Type, Authorization, X-Request-ID
```

---

## 📊 Monitoramento e Observabilidade

### Métricas Prometheus

**Endpoint:** `http://localhost:9090/metrics`

**Métricas Principais:**
- `afi_requests_total`: Total de requisições
- `afi_request_duration_seconds`: Duração das requisições
- `afi_active_tasks`: Tarefas ativas
- `afi_system_cpu_usage`: Uso de CPU
- `afi_system_memory_usage`: Uso de memória

### Dashboards Grafana

**URL:** `http://localhost:3000`

**Dashboards Disponíveis:**
- **Sistema Geral**: Visão geral do sistema
- **Performance**: Métricas de performance
- **Aplicação**: Métricas específicas da aplicação
- **Infraestrutura**: Métricas de infraestrutura

---

## 🧪 Exemplos de Uso

### 1. Verificar Status do Sistema

```bash
curl -X GET http://localhost:8508/api/status
```

### 2. Listar Arquivos Processados

```bash
curl -X GET http://localhost:8507/api/output
```

### 3. Gerar Arquivo Dummy

```bash
curl -X POST http://localhost:8507/api/generate_dummy
```

### 4. Obter Logs Específicos

```bash
curl -X GET "http://localhost:8507/api/log?file=afi_guardiao_2024-01-15.log"
```

### 5. Monitorar Performance

```python
import requests

def monitor_system():
    response = requests.get('http://localhost:8508/api/status')
    if response.status_code == 200:
        data = response.json()
        print(f"Sistema: {data['backend_status']}")
        print(f"Timestamp: {data['timestamp']}")
    else:
        print(f"Erro: {response.status_code}")

monitor_system()
```

---

## 🔄 Integração com Docker

### Configuração de Rede

```yaml
networks:
  afi-network:
    driver: bridge
    ipam:
      config:
        - subnet: 172.20.0.0/16
```

### Mapeamento de Portas

```yaml
ports:
  - "8507:8507"  # Frontend
  - "8508:8508"  # Backend
  - "6379:6379"  # Redis
  - "9090:9090"  # Prometheus
  - "3000:3000"  # Grafana
```

### Health Checks

```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8508/"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 40s
```

---

## 📚 Recursos Adicionais

### Documentação Relacionada
- [Arquitetura do Sistema](./architecture.md)
- [Guia de Instalação](../README.md#instalação-rápida)
- [Configuração](../README.md#configuração)

### Ferramentas de Desenvolvimento
- **Postman Collection**: Disponível em `/tools/postman/`
- **OpenAPI Spec**: Disponível em `/docs/openapi.yaml`
- **Testes de API**: Disponível em `/tests/api/`

### Suporte
- **Issues**: [GitHub Issues](https://github.com/seu-usuario/afi-guardiao/issues)
- **Documentação**: [Wiki do Projeto](https://github.com/seu-usuario/afi-guardiao/wiki)
- **Comunidade**: [Discussions](https://github.com/seu-usuario/afi-guardiao/discussions)