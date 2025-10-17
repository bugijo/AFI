"""
🔍 AFI v4.0 - File System Watcher
Sistema de monitoramento automático de arquivos usando watchdog

Este módulo implementa o "Guardião" que monitora pastas 24/7 e 
automaticamente atualiza a base de conhecimento quando detecta
arquivos novos ou modificados.
"""

import os
import time
import threading
from pathlib import Path
from typing import Optional, Callable, List
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileModifiedEvent, FileCreatedEvent

class AFIFileWatcher(FileSystemEventHandler):
    """
    🔍 Guardião de Arquivos do AFI
    Monitora mudanças no sistema de arquivos e dispara reindexação automática
    """
    
    def __init__(self, callback_function: Callable[[str], None], 
                 extensoes_validas: Optional[List[str]] = None):
        """
        Inicializa o File Watcher
        
        Args:
            callback_function: Função a ser chamada quando um arquivo válido for detectado
            extensoes_validas: Lista de extensões de arquivo para monitorar
        """
        super().__init__()
        self.callback_function = callback_function
        self.extensoes_validas = extensoes_validas or [
            '.txt', '.pdf', '.docx', '.doc', '.md', '.rtf', '.odt'
        ]
        self.extensoes_ignoradas = ['.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv']
        
        # Controle de debounce para evitar múltiplas chamadas
        self.last_event_time = {}
        self.debounce_seconds = 2  # Aguardar 2 segundos antes de processar
        
        print("🔍 AFI File Watcher inicializado!")
        print(f"📄 Extensões monitoradas: {', '.join(self.extensoes_validas)}")
    
    def _is_valid_file(self, file_path: str) -> bool:
        """Verifica se o arquivo é válido para indexação"""
        if not os.path.isfile(file_path):
            return False
            
        # Verificar extensão
        extensao = Path(file_path).suffix.lower()
        
        # Ignorar arquivos de vídeo
        if extensao in self.extensoes_ignoradas:
            return False
            
        # Aceitar apenas extensões válidas
        if extensao not in self.extensoes_validas:
            return False
            
        # Ignorar arquivos temporários
        nome_arquivo = Path(file_path).name
        if nome_arquivo.startswith('.') or nome_arquivo.startswith('~'):
            return False
            
        return True
    
    def _should_process_event(self, file_path: str) -> bool:
        """Implementa debounce para evitar processamento excessivo"""
        current_time = time.time()
        
        # Verificar se já processamos este arquivo recentemente
        if file_path in self.last_event_time:
            time_diff = current_time - self.last_event_time[file_path]
            if time_diff < self.debounce_seconds:
                return False
        
        # Atualizar timestamp
        self.last_event_time[file_path] = current_time
        return True
    
    def on_created(self, event):
        """Chamado quando um arquivo é criado"""
        if isinstance(event, FileCreatedEvent):
            self._handle_file_event(event.src_path, "CRIADO")
    
    def on_modified(self, event):
        """Chamado quando um arquivo é modificado"""
        if isinstance(event, FileModifiedEvent):
            self._handle_file_event(event.src_path, "MODIFICADO")
    
    def _handle_file_event(self, file_path: str, event_type: str):
        """Processa eventos de arquivo"""
        try:
            # Verificar se é um arquivo válido
            if not self._is_valid_file(file_path):
                return
            
            # Aplicar debounce
            if not self._should_process_event(file_path):
                return
            
            print(f"🔍 Arquivo {event_type}: {Path(file_path).name}")
            
            # Chamar função de callback para reindexação
            if self.callback_function:
                # Executar em thread separada para não bloquear o watcher
                thread = threading.Thread(
                    target=self._safe_callback,
                    args=(file_path, event_type),
                    daemon=True
                )
                thread.start()
                
        except Exception as e:
            print(f"❌ Erro ao processar evento de arquivo: {str(e)}")
    
    def _safe_callback(self, file_path: str, event_type: str):
        """Executa callback de forma segura"""
        try:
            # Obter diretório pai para reindexação
            diretorio_pai = str(Path(file_path).parent)
            print(f"🔄 Iniciando reindexação automática de: {diretorio_pai}")
            
            # Chamar função de callback
            self.callback_function(diretorio_pai)
            
            print(f"✅ Reindexação automática concluída para: {Path(file_path).name}")
            
        except Exception as e:
            print(f"❌ Erro durante reindexação automática: {str(e)}")


class AFIWatcherService:
    """
    🛡️ Serviço de Monitoramento do AFI
    Gerencia múltiplos watchers e fornece interface de controle
    """
    
    def __init__(self):
        self.observers = {}  # Dicionário de observers por pasta
        self.is_running = False
        self.callback_function = None
        
    def set_callback(self, callback_function: Callable[[str], None]):
        """Define a função de callback para reindexação"""
        self.callback_function = callback_function
        print("🔗 Callback de reindexação configurado!")
    
    def add_watch_folder(self, folder_path: str) -> bool:
        """
        Adiciona uma pasta para monitoramento
        
        Args:
            folder_path: Caminho da pasta a ser monitorada
            
        Returns:
            bool: True se adicionado com sucesso
        """
        try:
            if not os.path.exists(folder_path):
                print(f"❌ Pasta não encontrada: {folder_path}")
                return False
            
            if folder_path in self.observers:
                print(f"⚠️ Pasta já está sendo monitorada: {folder_path}")
                return True
            
            # Criar event handler
            event_handler = AFIFileWatcher(self.callback_function)
            
            # Criar observer
            observer = Observer()
            observer.schedule(event_handler, folder_path, recursive=True)
            
            # Armazenar observer
            self.observers[folder_path] = observer
            
            # Iniciar se o serviço estiver rodando
            if self.is_running:
                observer.start()
                print(f"🔍 Monitoramento iniciado para: {folder_path}")
            
            return True
            
        except Exception as e:
            print(f"❌ Erro ao adicionar pasta para monitoramento: {str(e)}")
            return False
    
    def remove_watch_folder(self, folder_path: str) -> bool:
        """Remove uma pasta do monitoramento"""
        try:
            if folder_path not in self.observers:
                print(f"⚠️ Pasta não está sendo monitorada: {folder_path}")
                return False
            
            # Parar observer
            observer = self.observers[folder_path]
            observer.stop()
            observer.join()
            
            # Remover do dicionário
            del self.observers[folder_path]
            
            print(f"🛑 Monitoramento removido para: {folder_path}")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao remover pasta do monitoramento: {str(e)}")
            return False
    
    def start_service(self):
        """Inicia o serviço de monitoramento"""
        try:
            if self.is_running:
                print("⚠️ Serviço já está rodando!")
                return
            
            # Iniciar todos os observers
            for folder_path, observer in self.observers.items():
                observer.start()
                print(f"🔍 Monitoramento iniciado para: {folder_path}")
            
            self.is_running = True
            print("🛡️ Serviço de monitoramento AFI iniciado!")
            
        except Exception as e:
            print(f"❌ Erro ao iniciar serviço: {str(e)}")
    
    def stop_service(self):
        """Para o serviço de monitoramento"""
        try:
            if not self.is_running:
                print("⚠️ Serviço não está rodando!")
                return
            
            # Parar todos os observers
            for folder_path, observer in self.observers.items():
                observer.stop()
                print(f"🛑 Monitoramento parado para: {folder_path}")
            
            # Aguardar finalização
            for observer in self.observers.values():
                observer.join()
            
            self.is_running = False
            print("🛡️ Serviço de monitoramento AFI parado!")
            
        except Exception as e:
            print(f"❌ Erro ao parar serviço: {str(e)}")
    
    def get_status(self) -> dict:
        """Retorna status do serviço"""
        return {
            'is_running': self.is_running,
            'watched_folders': list(self.observers.keys()),
            'total_watchers': len(self.observers)
        }


# Instância global do serviço (Singleton)
afi_watcher_service = AFIWatcherService()


def inicializar_watcher_service(callback_function: Callable[[str], None]):
    """
    🚀 Função de inicialização do serviço de monitoramento
    
    Args:
        callback_function: Função que será chamada para reindexar quando arquivos mudarem
    """
    global afi_watcher_service
    
    try:
        # Configurar callback
        afi_watcher_service.set_callback(callback_function)
        
        print("🛡️ Serviço de File Watcher do AFI v4.0 inicializado!")
        print("💡 Use afi_watcher_service.add_watch_folder() para adicionar pastas")
        print("💡 Use afi_watcher_service.start_service() para iniciar o monitoramento")
        
        return afi_watcher_service
        
    except Exception as e:
        print(f"❌ Erro ao inicializar serviço de watcher: {str(e)}")
        return None


if __name__ == "__main__":
    # Teste do sistema
    def callback_teste(folder_path):
        print(f"🔄 CALLBACK TESTE: Reindexar {folder_path}")
    
    # Inicializar serviço
    service = inicializar_watcher_service(callback_teste)
    
    if service:
        # Adicionar pasta de teste
        service.add_watch_folder("./memoria")
        
        # Iniciar serviço
        service.start_service()
        
        try:
            print("🔍 Monitoramento ativo. Pressione Ctrl+C para parar...")
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Parando serviço...")
            service.stop_service()