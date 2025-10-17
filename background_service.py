#!/usr/bin/env python3
"""
🔍 AFI v4.0 - Serviço de Background para Monitoramento Contínuo
Serviço independente que monitora pastas e atualiza automaticamente a base de conhecimento
"""

import os
import sys
import time
import signal
import logging
from datetime import datetime
from pathlib import Path

# Configurar logging com encoding UTF-8
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('afi_background_service.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Importar o watcher service
try:
    from file_watcher import afi_watcher_service, inicializar_watcher_service
    WATCHER_AVAILABLE = True
    logger.info("✅ Watchdog disponível - File System Watcher carregado")
except ImportError as e:
    logger.error(f"❌ Watchdog não disponível: {e}")
    logger.error("💡 Instale com: pip install watchdog")
    WATCHER_AVAILABLE = False
    sys.exit(1)

class AFIBackgroundService:
    """Serviço de background para monitoramento contínuo do AFI"""
    
    def __init__(self):
        self.running = False
        self.start_time = None
        self.monitored_folders = []
        
        # Configurar handlers para sinais do sistema
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
    def _signal_handler(self, signum, frame):
        """Handler para sinais do sistema (Ctrl+C, etc.)"""
        logger.info(f"🛑 Sinal recebido ({signum}). Parando serviço...")
        self.stop()
        
    def add_folder(self, folder_path):
        """Adiciona uma pasta para monitoramento"""
        if os.path.isdir(folder_path):
            if folder_path not in self.monitored_folders:
                self.monitored_folders.append(folder_path)
                logger.info(f"📁 Pasta adicionada ao monitoramento: {folder_path}")
                
                # Adicionar ao watcher service se estiver rodando
                if self.running and WATCHER_AVAILABLE:
                    try:
                        afi_watcher_service.add_folder(folder_path)
                        logger.info(f"✅ Pasta {folder_path} adicionada ao watcher ativo")
                    except Exception as e:
                        logger.error(f"❌ Erro ao adicionar pasta ao watcher: {e}")
                return True
            else:
                logger.warning(f"⚠️ Pasta já está sendo monitorada: {folder_path}")
                return False
        else:
            logger.error(f"❌ Pasta não encontrada: {folder_path}")
            return False
    
    def remove_folder(self, folder_path):
        """Remove uma pasta do monitoramento"""
        if folder_path in self.monitored_folders:
            self.monitored_folders.remove(folder_path)
            logger.info(f"📁 Pasta removida do monitoramento: {folder_path}")
            
            # Remover do watcher service se estiver rodando
            if self.running and WATCHER_AVAILABLE:
                try:
                    afi_watcher_service.remove_folder(folder_path)
                    logger.info(f"✅ Pasta {folder_path} removida do watcher ativo")
                except Exception as e:
                    logger.error(f"❌ Erro ao remover pasta do watcher: {e}")
            return True
        else:
            logger.warning(f"⚠️ Pasta não estava sendo monitorada: {folder_path}")
            return False
    
    def start(self):
        """Inicia o serviço de background"""
        if self.running:
            logger.warning("⚠️ Serviço já está rodando!")
            return False
            
        if not WATCHER_AVAILABLE:
            logger.error("❌ Watchdog não disponível. Não é possível iniciar o serviço.")
            return False
            
        logger.info("🚀 Iniciando AFI Background Service...")
        
        try:
            # Inicializar o watcher service
            inicializar_watcher_service()
            
            # Adicionar pastas monitoradas
            for folder in self.monitored_folders:
                afi_watcher_service.add_folder(folder)
                logger.info(f"📁 Monitorando: {folder}")
            
            # Iniciar o watcher
            afi_watcher_service.start()
            
            self.running = True
            self.start_time = datetime.now()
            
            logger.info("✅ AFI Background Service iniciado com sucesso!")
            logger.info(f"👁️ Monitorando {len(self.monitored_folders)} pasta(s)")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Erro ao iniciar serviço: {e}")
            return False
    
    def stop(self):
        """Para o serviço de background"""
        if not self.running:
            logger.warning("⚠️ Serviço não está rodando!")
            return False
            
        logger.info("🛑 Parando AFI Background Service...")
        
        try:
            # Parar o watcher service
            if WATCHER_AVAILABLE:
                afi_watcher_service.stop()
            
            self.running = False
            
            if self.start_time:
                uptime = datetime.now() - self.start_time
                logger.info(f"⏱️ Tempo de execução: {uptime}")
            
            logger.info("✅ AFI Background Service parado com sucesso!")
            return True
            
        except Exception as e:
            logger.error(f"❌ Erro ao parar serviço: {e}")
            return False
    
    def status(self):
        """Retorna o status do serviço"""
        status_info = {
            'running': self.running,
            'start_time': self.start_time,
            'monitored_folders': self.monitored_folders.copy(),
            'watcher_available': WATCHER_AVAILABLE
        }
        
        if self.running and self.start_time:
            status_info['uptime'] = datetime.now() - self.start_time
            
        return status_info
    
    def run_forever(self):
        """Executa o serviço indefinidamente"""
        if not self.start():
            logger.error("❌ Falha ao iniciar o serviço!")
            return False
            
        logger.info("🔄 Serviço rodando indefinidamente. Pressione Ctrl+C para parar.")
        
        try:
            while self.running:
                time.sleep(1)  # Sleep de 1 segundo
                
        except KeyboardInterrupt:
            logger.info("⌨️ Interrupção do teclado detectada")
        except Exception as e:
            logger.error(f"❌ Erro durante execução: {e}")
        finally:
            self.stop()
            
        logger.info("👋 Serviço finalizado")
        return True

# Instância global do serviço
afi_background_service = AFIBackgroundService()

def main():
    """Função principal para execução como script"""
    import argparse
    
    parser = argparse.ArgumentParser(description='AFI v4.0 Background Service')
    parser.add_argument('--add-folder', type=str, help='Adicionar pasta para monitoramento')
    parser.add_argument('--remove-folder', type=str, help='Remover pasta do monitoramento')
    parser.add_argument('--start', action='store_true', help='Iniciar o serviço')
    parser.add_argument('--stop', action='store_true', help='Parar o serviço')
    parser.add_argument('--status', action='store_true', help='Mostrar status do serviço')
    parser.add_argument('--run', action='store_true', help='Executar serviço indefinidamente')
    
    args = parser.parse_args()
    
    # Processar argumentos
    if args.add_folder:
        success = afi_background_service.add_folder(args.add_folder)
        if success:
            print(f"✅ Pasta adicionada: {args.add_folder}")
        else:
            print(f"❌ Falha ao adicionar pasta: {args.add_folder}")
            
    if args.remove_folder:
        success = afi_background_service.remove_folder(args.remove_folder)
        if success:
            print(f"✅ Pasta removida: {args.remove_folder}")
        else:
            print(f"❌ Falha ao remover pasta: {args.remove_folder}")
            
    if args.start:
        success = afi_background_service.start()
        if success:
            print("✅ Serviço iniciado")
        else:
            print("❌ Falha ao iniciar serviço")
            
    if args.stop:
        success = afi_background_service.stop()
        if success:
            print("✅ Serviço parado")
        else:
            print("❌ Falha ao parar serviço")
            
    if args.status:
        status = afi_background_service.status()
        print("📊 Status do AFI Background Service:")
        print(f"   🔄 Rodando: {'Sim' if status['running'] else 'Não'}")
        print(f"   👁️ Watchdog: {'Disponível' if status['watcher_available'] else 'Indisponível'}")
        print(f"   📁 Pastas monitoradas: {len(status['monitored_folders'])}")
        
        if status['monitored_folders']:
            for folder in status['monitored_folders']:
                print(f"      📂 {folder}")
                
        if status.get('start_time'):
            print(f"   ⏰ Iniciado em: {status['start_time'].strftime('%Y-%m-%d %H:%M:%S')}")
            
        if status.get('uptime'):
            print(f"   ⏱️ Tempo ativo: {status['uptime']}")
            
    if args.run:
        # Adicionar algumas pastas padrão se nenhuma foi especificada
        if not afi_background_service.monitored_folders:
            logger.info("📁 Nenhuma pasta configurada. Adicionando pasta padrão...")
            # Você pode adicionar pastas padrão aqui
            # afi_background_service.add_folder("\\\\SERVIDOR\\Documentos\\Manuais")
            
        afi_background_service.run_forever()
    
    # Se nenhum argumento foi fornecido, mostrar ajuda
    if not any(vars(args).values()):
        parser.print_help()
        print("\n💡 Exemplos de uso:")
        print("  python background_service.py --add-folder \"\\\\SERVIDOR\\Documentos\\Manuais\"")
        print("  python background_service.py --start")
        print("  python background_service.py --run")
        print("  python background_service.py --status")
        print("  python background_service.py --stop")

if __name__ == "__main__":
    main()