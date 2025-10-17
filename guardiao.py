#!/usr/bin/env python3
"""
🤖 GUARDIÃO AUTÔNOMO - Gerente de Produção de Vídeos
Sistema de monitoramento 24/7 para processamento automático de vídeos
"""

# ========================================
# 🎬 CONFIGURAÇÕES PERSONALIZADAS
# ========================================
# Modifique estas variáveis para personalizar seu vídeo:

TEXTO_PERSONALIZADO = "Produto Incrível da Finiti!"  # ← COLE SUA FRASE DO AFI AQUI
MUSICA_PERSONALIZADA = None  # ← COLOQUE O NOME DA MÚSICA AQUI (ex: "rock_instrumental.mp3") ou None para aleatória

# ========================================

def gerar_nome_arquivo_agendado():
    """
    Gera nome de arquivo baseado na data e hora atual
    
    Returns:
        str: Nome do arquivo no formato "DD-MM-AA.Descricao.mp4"
    """
    agora = datetime.now()
    
    # Determinar descrição baseada no dia da semana e hora
    if agora.weekday() == 5 or agora.weekday() == 6:  # Sábado (5) ou Domingo (6)
        descricao = "Bomdia"
    else:  # Dia de semana
        if agora.hour < 12:
            descricao = "Bomdia"
        else:
            descricao = "Encerramento"
    
    # Formatar nome do arquivo
    nome_arquivo = f"{agora.strftime('%d-%m-%y')}.{descricao}.mp4"
    return nome_arquivo

import os
import sys
import time
import random
import subprocess
from pathlib import Path
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Importar função de IA para gerar frases de marketing
try:
    from core_logic import processar_prompt_geral
    IA_DISPONIVEL = True
except ImportError:
    IA_DISPONIVEL = False
    print("[AVISO] IA não disponível - usando texto personalizado padrão")

class GuardiaoVideoHandler(FileSystemEventHandler):
    """Manipulador de eventos para detectar novos vídeos"""
    
    def __init__(self, pasta_musicas, pasta_saida):
        self.pasta_musicas = pasta_musicas
        self.pasta_saida = pasta_saida
        self.extensoes_video = {'.mp4', '.mov', '.avi', '.mkv', '.wmv', '.flv', '.webm'}
        self.processando = set()  # Evita processamento duplo
        
    def on_created(self, event):
        """Evento disparado quando um novo arquivo é criado"""
        if event.is_directory:
            return
            
        caminho_arquivo = Path(event.src_path)
        
        # Verifica se é um arquivo de vídeo
        if caminho_arquivo.suffix.lower() in self.extensoes_video:
            self.processar_novo_video(caminho_arquivo)
    
    def processar_novo_video(self, caminho_video):
        """Processa um novo vídeo detectado"""
        nome_video = caminho_video.name
        
        # Evita processamento duplo
        if nome_video in self.processando:
            return
            
        self.processando.add(nome_video)
        
        try:
            print(f"[DETECTADO] NOVO VÍDEO DETECTADO: {nome_video}")
            print("[INFO] Aguardando conclusão do upload...")
            
            # Aguarda alguns segundos para garantir que o arquivo foi copiado completamente
            time.sleep(3)
            
            # Verifica se o arquivo ainda existe e não está sendo usado
            if not self.arquivo_disponivel(caminho_video):
                print(f"[AVISO] Arquivo {nome_video} ainda está sendo copiado. Aguardando...")
                time.sleep(5)
                
            if not caminho_video.exists():
                print(f"[ERRO] Arquivo {nome_video} não encontrado. Cancelando processamento.")
                return
                
            # Escolhe música (personalizada ou aleatória)
            if MUSICA_PERSONALIZADA:
                musica_escolhida = self.pasta_musicas / MUSICA_PERSONALIZADA
                if not musica_escolhida.exists():
                    print(f"[ERRO] Música personalizada não encontrada: {MUSICA_PERSONALIZADA}")
                    print("[INFO] Usando música aleatória...")
                    musicas_disponiveis = list(self.pasta_musicas.glob("*.mp3"))
                    if not musicas_disponiveis:
                        print("[ERRO] Nenhuma música encontrada na pasta Musicas!")
                        return
                    musica_escolhida = random.choice(musicas_disponiveis)
            else:
                # Escolhe uma música aleatória
                musicas_disponiveis = list(self.pasta_musicas.glob("*.mp3"))
                if not musicas_disponiveis:
                    print("[ERRO] Nenhuma música encontrada na pasta Musicas!")
                    return
                musica_escolhida = random.choice(musicas_disponiveis)
                
            # 1. Gerar frase de marketing usando IA
            print("[INFO] Gerando frase de marketing com IA...")
            if IA_DISPONIVEL:
                try:
                    prompt_ia = "Crie uma frase de marketing impactante e persuasiva para um produto da Finiti. A frase deve ser curta, chamativa e motivar a compra. Responda apenas com a frase, sem explicações."
                    resposta_ia = processar_prompt_geral(prompt_ia)
                    if resposta_ia and 'response' in resposta_ia:
                        frase_marketing = resposta_ia['response'].strip()
                        print(f"[IA] Frase gerada: {frase_marketing}")
                    else:
                        frase_marketing = TEXTO_PERSONALIZADO
                        print(f"[AVISO] IA não respondeu adequadamente. Usando texto padrão: {frase_marketing}")
                except Exception as e:
                    frase_marketing = TEXTO_PERSONALIZADO
                    print(f"[ERRO] Erro na IA: {e}. Usando texto padrão: {frase_marketing}")
            else:
                frase_marketing = TEXTO_PERSONALIZADO
                print(f"[INFO] Usando texto padrão: {frase_marketing}")
            
            # 2. Gerar nome do arquivo baseado em data/hora
            nome_arquivo_agendado = gerar_nome_arquivo_agendado()
            arquivo_saida = self.pasta_saida / nome_arquivo_agendado
            print(f"[INFO] Nome do arquivo de saída: {nome_arquivo_agendado}")
            
            print(f"[INFO] Música escolhida: {musica_escolhida.name}")
            print(f"[INFO] Frase de marketing: {frase_marketing}")
            print(f"[INFO] Saída: {arquivo_saida.name}")
            print("[INFO] Iniciando processamento automático...")
            
            # 3. Chama o editor de vídeo com a nova assinatura
            sucesso = self.chamar_editor_video(
                str(caminho_video),
                str(musica_escolhida),
                frase_marketing,
                str(arquivo_saida)
            )
            
            if sucesso:
                print(f"[SUCESSO] SUCESSO! Vídeo processado: {arquivo_saida.name}")
                print("[INFO] Guardião pronto para o próximo vídeo!")
            else:
                print(f"[ERRO] ERRO no processamento de {nome_video}")
                
        except Exception as e:
            print(f"[ERRO] ERRO INESPERADO ao processar {nome_video}: {e}")
        finally:
            # Remove da lista de processamento
            self.processando.discard(nome_video)
            print("-" * 50)
    
    def arquivo_disponivel(self, caminho_arquivo):
        """Verifica se o arquivo está disponível para leitura"""
        try:
            # Tenta abrir o arquivo para verificar se não está sendo usado
            with open(caminho_arquivo, 'rb') as f:
                f.read(1)
            return True
        except (PermissionError, IOError):
            return False
    
    def escolher_musica_aleatoria(self):
        """Escolhe uma música aleatória da pasta Musicas"""
        extensoes_audio = {'.mp3', '.wav', '.aac', '.m4a', '.ogg'}
        
        # Lista todas as músicas disponíveis
        musicas = []
        
        # Busca na pasta principal
        for arquivo in self.pasta_musicas.iterdir():
            if arquivo.is_file() and arquivo.suffix.lower() in extensoes_audio:
                musicas.append(arquivo)
        
        # Busca nas subpastas (Energetica, Instrumental, Relaxante)
        for subpasta in self.pasta_musicas.iterdir():
            if subpasta.is_dir():
                for arquivo in subpasta.iterdir():
                    if arquivo.is_file() and arquivo.suffix.lower() in extensoes_audio:
                        musicas.append(arquivo)
        
        if not musicas:
            return None
            
        # Escolhe uma música aleatória
        return random.choice(musicas)
    
    def chamar_editor_video(self, video_entrada, musica, texto, video_saida):
        """Chama o editor_video.py usando subprocess"""
        try:
            # Comando para executar o editor de vídeo
            comando = [
                sys.executable,  # python
                "editor_video.py",
                video_entrada,
                musica,
                texto,
                video_saida
            ]
            
            print(f"[INFO] Executando: {' '.join(comando)}")
            
            # Executa o comando
            resultado = subprocess.run(
                comando,
                capture_output=True,
                text=True,
                timeout=300  # Timeout de 5 minutos
            )
            
            if resultado.returncode == 0:
                print("[SUCESSO] Editor executado com sucesso!")
                if resultado.stdout:
                    print("[INFO] Saída:", resultado.stdout.strip())
                return True
            else:
                print(f"[ERRO] Editor falhou com código: {resultado.returncode}")
                if resultado.stderr:
                    print("[ERRO] Erro:", resultado.stderr.strip())
                return False
                
        except subprocess.TimeoutExpired:
            print("[TIMEOUT] TIMEOUT: Processamento demorou mais de 5 minutos")
            return False
        except Exception as e:
            print(f"[ERRO] Erro ao executar editor: {e}")
            return False

class GuardiaoAutonomo:
    """Classe principal do Guardião Autônomo"""
    
    def __init__(self):
        self.pasta_entrada = Path("Videos_Para_Editar")
        self.pasta_musicas = Path("Musicas")
        self.pasta_saida = Path("Videos_Editados")
        self.observer = None
        
    def verificar_estrutura(self):
        """Verifica e cria a estrutura de pastas necessária"""
        print("📁 Verificando estrutura de pastas...")
        
        for pasta in [self.pasta_entrada, self.pasta_musicas, self.pasta_saida]:
            if not pasta.exists():
                pasta.mkdir(parents=True, exist_ok=True)
                print(f"✅ Pasta criada: {pasta}")
            else:
                print(f"✅ Pasta encontrada: {pasta}")
    
    def verificar_dependencias(self):
        """Verifica se o editor_video.py existe"""
        editor_path = Path("editor_video.py")
        if not editor_path.exists():
            print("❌ ERRO: editor_video.py não encontrado!")
            print("💡 Certifique-se de que o editor_video.py está na mesma pasta")
            return False
        
        print("✅ editor_video.py encontrado")
        return True
    
    def iniciar_monitoramento(self):
        """Inicia o monitoramento da pasta de entrada"""
        print("🤖 GUARDIÃO AUTÔNOMO - INICIANDO...")
        print("=" * 50)
        
        # Verificações iniciais
        if not self.verificar_dependencias():
            return False
            
        self.verificar_estrutura()
        
        # Configura o manipulador de eventos
        event_handler = GuardiaoVideoHandler(self.pasta_musicas, self.pasta_saida)
        
        # Configura o observador
        self.observer = Observer()
        self.observer.schedule(
            event_handler,
            str(self.pasta_entrada),
            recursive=False
        )
        
        # Inicia o monitoramento
        self.observer.start()
        
        print(f"👁️ MONITORANDO: {self.pasta_entrada.absolute()}")
        print("🎵 Músicas disponíveis:")
        self.listar_musicas()
        print("=" * 50)
        print("🚀 GUARDIÃO ATIVO! Aguardando novos vídeos...")
        print("💡 Para parar, pressione Ctrl+C")
        print("=" * 50)
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Parando o Guardião...")
            self.observer.stop()
            
        self.observer.join()
        print("✅ Guardião finalizado!")
        return True
    
    def listar_musicas(self):
        """Lista as músicas disponíveis"""
        extensoes_audio = {'.mp3', '.wav', '.aac', '.m4a', '.ogg'}
        count = 0
        
        # Músicas na pasta principal
        for arquivo in self.pasta_musicas.iterdir():
            if arquivo.is_file() and arquivo.suffix.lower() in extensoes_audio:
                print(f"   🎵 {arquivo.name}")
                count += 1
        
        # Músicas nas subpastas
        for subpasta in self.pasta_musicas.iterdir():
            if subpasta.is_dir():
                for arquivo in subpasta.iterdir():
                    if arquivo.is_file() and arquivo.suffix.lower() in extensoes_audio:
                        print(f"   🎵 {subpasta.name}/{arquivo.name}")
                        count += 1
        
        if count == 0:
            print("   ⚠️ Nenhuma música encontrada!")
        else:
            print(f"   📊 Total: {count} música(s)")

def main():
    """Função principal"""
    print("🤖 GUARDIÃO AUTÔNOMO v1.0")
    print("Sistema de Processamento Automático de Vídeos")
    print()
    
    guardiao = GuardiaoAutonomo()
    guardiao.iniciar_monitoramento()

if __name__ == "__main__":
    main()