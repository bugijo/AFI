#!/usr/bin/env python3
"""
🔧 AFI v4.0 - Backend API
Backend simples na porta 8508 para seguir as regras do projeto
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import logging
from datetime import datetime
import os

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Criar aplicação Flask
app = Flask(__name__)
CORS(app)  # Permitir CORS para comunicação com frontend

# Configuração da porta conforme regras do projeto
BACKEND_PORT = 8508

@app.route('/', methods=['GET'])
def health_check():
    """Endpoint de verificação de saúde do backend"""
    return jsonify({
        "status": "healthy",
        "service": "AFI v4.0 Backend",
        "port": BACKEND_PORT,
        "timestamp": datetime.now().isoformat(),
        "message": "Backend funcionando corretamente na porta 8508"
    })

@app.route('/api/status', methods=['GET'])
def get_status():
    """Retorna status do sistema"""
    return jsonify({
        "backend_status": "running",
        "frontend_port": 8507,
        "backend_port": 8508,
        "timestamp": datetime.now().isoformat(),
        "uptime": "Sistema ativo"
    })

@app.route('/api/folders', methods=['GET'])
def get_monitored_folders():
    """Retorna pastas monitoradas"""
    try:
        # Verificar se existe pasta FINITI_CONHECIMENTO
        finiti_path = "C:\\FINITI_CONHECIMENTO"
        folders = []
        
        if os.path.exists(finiti_path):
            folders.append({
                "path": finiti_path,
                "status": "available",
                "type": "knowledge_sanctuary"
            })
        
        return jsonify({
            "monitored_folders": folders,
            "count": len(folders),
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500

@app.route('/api/knowledge', methods=['GET'])
def get_knowledge_info():
    """Retorna informações sobre a base de conhecimento"""
    try:
        storage_path = "storage"
        knowledge_info = {
            "storage_exists": os.path.exists(storage_path),
            "finiti_conhecimento_exists": os.path.exists("C:\\FINITI_CONHECIMENTO"),
            "timestamp": datetime.now().isoformat()
        }
        
        if os.path.exists(storage_path):
            files = os.listdir(storage_path)
            knowledge_info["storage_files"] = files
            knowledge_info["storage_file_count"] = len(files)
        
        return jsonify(knowledge_info)
    except Exception as e:
        return jsonify({
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500

if __name__ == '__main__':
    logger.info(f"🚀 Iniciando AFI v4.0 Backend na porta {BACKEND_PORT}")
    logger.info(f"🌐 Backend URL: http://localhost:{BACKEND_PORT}")
    logger.info("📡 Endpoints disponíveis:")
    logger.info("   GET / - Health check")
    logger.info("   GET /api/status - Status do sistema")
    logger.info("   GET /api/folders - Pastas monitoradas")
    logger.info("   GET /api/knowledge - Informações da base de conhecimento")
    
    app.run(
        host='localhost',
        port=BACKEND_PORT,
        debug=False
    )