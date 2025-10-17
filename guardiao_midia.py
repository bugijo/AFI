#!/usr/bin/env python3
"""
👁️ AFI v4.0 - Guardião de Mídia Social
O "Guardião" do Agente de Mídia Social - monitora pastas e aciona o fluxo automatizado

Este módulo implementa o sistema de monitoramento que detecta novos vídeos
e aciona automaticamente o processo de edição com IA.
"""

import os
import time
import logging
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import random
from editor_video import editar_video_story

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class GuardiaoMidiaHandler(FileSystemEventHandler):
    """
    Handler que processa eventos de arquivo na pasta monitorada.
    """
    
    def __init__(self, afi_integration=None):
        """
        Inicializa o handler do Guardião.
        
        Args:
            afi_integration: Função para integração com AFI (opcional)
        """
        self.afi_integration = afi_integration
        self.extensoes_video = {'.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm'}
        self.extensoes_audio = {'.mp3', '.wav', '.aac', '.ogg', '.m4a'}
        
    def on_created(self, event):
        """
        Chamado quando um novo arquivo é criado na pasta monitorada.
        """
        if event.is_directory:
            return
            
        arquivo = Path(event.src_path)
        
        # Verificar se é um arquivo de vídeo
        if arquivo.suffix.lower() in self.extensoes_video:
            logger.info(f"🎬 Novo vídeo detectado: {arquivo.name}")
            self.processar_novo_video(arquivo)
    
    def processar_novo_video(self, caminho_video):
        """
        Processa um novo vídeo detectado pelo Guardião.
        
        Args:
            caminho_video (Path): Caminho para o novo vídeo
        """
        try:
            logger.info(f"🧠 Analisando vídeo com AFI: {caminho_video.name}")
            
            # Simular consulta ao AFI (aqui você integraria com o sistema RAG real)
            frase_impacto, estilo_musica = self.consultar_afi(caminho_video)
            
            # Selecionar música aleatória do estilo sugerido
            musica_selecionada = self.selecionar_musica(estilo_musica)
            
            if not musica_selecionada:
                logger.warning(f"⚠️ Nenhuma música encontrada para o estilo: {estilo_musica}")
                return
            
            # Gerar nome do arquivo de saída
            nome_saida = self.gerar_nome_saida(caminho_video, frase_impacto)
            caminho_saida = Path("C:/AFI/Videos_Agendados") / nome_saida
            
            logger.info(f"🎵 Música selecionada: {musica_selecionada.name}")
            logger.info(f"📝 Frase de impacto: {frase_impacto}")
            logger.info(f"🎯 Iniciando edição automatizada...")
            
            # Executar edição automatizada
            sucesso = editar_video_story(
                caminho_video_original=str(caminho_video),
                caminho_musica=str(musica_selecionada),
                texto_overlay=frase_impacto,
                caminho_saida=str(caminho_saida)
            )
            
            if sucesso:
                logger.info(f"✅ Vídeo editado com sucesso: {caminho_saida.name}")
                logger.info(f"📁 Vídeo salvo em: {caminho_saida}")
            else:
                logger.error(f"❌ Erro na edição do vídeo: {caminho_video.name}")
                
        except Exception as e:
            logger.error(f"❌ Erro ao processar vídeo {caminho_video.name}: {str(e)}")
    
    def consultar_afi(self, caminho_video):
        """
        Consulta o AFI para gerar frase de impacto e sugerir estilo musical.
        
        Args:
            caminho_video (Path): Caminho do vídeo para análise
            
        Returns:
            tuple: (frase_impacto, estilo_musica)
        """
        # TODO: Integrar com o sistema RAG real do AFI
        # Por enquanto, vamos simular respostas baseadas no nome do arquivo
        
        nome_arquivo = caminho_video.stem.lower()
        
        # Frases de impacto baseadas em palavras-chave
        frases_motivacionais = [
            "🚀 Transforme sua vida hoje!",
            "💪 Você é mais forte do que imagina!",
            "🌟 Seu momento é agora!",
            "🔥 Desperte seu potencial!",
            "⚡ Energia para conquistar!"
        ]
        
        frases_tecnicas = [
            "🔧 Inovação em cada detalhe",
            "⚙️ Tecnologia que funciona",
            "🛠️ Qualidade comprovada",
            "🎯 Precisão em cada movimento",
            "💡 Soluções inteligentes"
        ]
        
        frases_vendas = [
            "💰 Oportunidade única!",
            "🎁 Oferta especial para você",
            "⏰ Por tempo limitado",
            "🏆 A melhor escolha",
            "✨ Qualidade excepcional"
        ]
        
        # Determinar estilo baseado no conteúdo
        if any(palavra in nome_arquivo for palavra in ['motivacao', 'treino', 'energia', 'forca']):
            frase = random.choice(frases_motivacionais)
            estilo = 'Rock'
        elif any(palavra in nome_arquivo for palavra in ['tecnico', 'manual', 'tutorial', 'airless']):
            frase = random.choice(frases_tecnicas)
            estilo = 'Instrumental'
        elif any(palavra in nome_arquivo for palavra in ['venda', 'promocao', 'oferta', 'produto']):
            frase = random.choice(frases_vendas)
            estilo = 'Pop'
        else:
            frase = random.choice(frases_motivacionais)
            estilo = 'Calma'
        
        logger.info(f"🧠 AFI sugeriu: Frase='{frase}', Estilo='{estilo}'")
        return frase, estilo
    
    def selecionar_musica(self, estilo):
        """
        Seleciona uma música aleatória do estilo especificado.
        
        Args:
            estilo (str): Estilo musical (Rock, Pop, Calma, etc.)
            
        Returns:
            Path: Caminho para a música selecionada ou None
        """
        pasta_musicas = Path(f"C:/AFI/Musicas/{estilo}")
        
        if not pasta_musicas.exists():
            logger.warning(f"⚠️ Pasta de músicas não encontrada: {pasta_musicas}")
            return None
        
        # Buscar arquivos de música na pasta
        musicas = [
            arquivo for arquivo in pasta_musicas.iterdir()
            if arquivo.suffix.lower() in self.extensoes_audio
        ]
        
        if not musicas:
            logger.warning(f"⚠️ Nenhuma música encontrada em: {pasta_musicas}")
            return None
        
        # Selecionar música aleatória
        musica_selecionada = random.choice(musicas)
        return musica_selecionada
    
    def gerar_nome_saida(self, caminho_video, frase_impacto):
        """
        Gera nome para o arquivo de saída baseado no vídeo original e frase.
        
        Args:
            caminho_video (Path): Caminho do vídeo original
            frase_impacto (str): Frase de impacto gerada
            
        Returns:
            str: Nome do arquivo de saída
        """
        # Remover emojis e caracteres especiais da frase para o nome do arquivo
        frase_limpa = ''.join(c for c in frase_impacto if c.isalnum() or c.isspace())
        frase_limpa = frase_limpa.strip().replace(' ', '_')[:20]  # Limitar tamanho
        
        # Gerar timestamp para agendamento (exemplo: próxima hora)
        timestamp = time.strftime("%Y-%m-%d_%H-%M", time.localtime(time.time() + 3600))
        
        nome_original = caminho_video.stem
        nome_saida = f"{timestamp}_post_{nome_original}_{frase_limpa}.mp4"
        
        return nome_saida

class GuardiaoMidia:
    """
    Classe principal do Guardião de Mídia Social.
    """
    
    def __init__(self, pasta_monitorada="C:/AFI/Videos_Para_Editar"):
        """
        Inicializa o Guardião.
        
        Args:
            pasta_monitorada (str): Pasta a ser monitorada
        """
        self.pasta_monitorada = Path(pasta_monitorada)
        self.observer = Observer()
        self.handler = GuardiaoMidiaHandler()
        
        # Criar pasta se não existir
        self.pasta_monitorada.mkdir(parents=True, exist_ok=True)
        
    def iniciar(self):
        """
        Inicia o monitoramento da pasta.
        """
        logger.info(f"👁️ Guardião iniciado - Monitorando: {self.pasta_monitorada}")
        logger.info("🎬 Aguardando novos vídeos...")
        
        self.observer.schedule(
            self.handler,
            str(self.pasta_monitorada),
            recursive=False
        )
        
        self.observer.start()
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("⏹️ Parando Guardião...")
            self.observer.stop()
        
        self.observer.join()
        logger.info("✅ Guardião parado com sucesso!")

def main():
    """
    Função principal para executar o Guardião.
    """
    print("👁️ AFI v4.0 - Guardião de Mídia Social")
    print("=" * 50)
    print("🎯 Sistema de Monitoramento Automatizado")
    print()
    
    # Verificar se as pastas necessárias existem
    pastas_necessarias = [
        "C:/AFI/Videos_Para_Editar",
        "C:/AFI/Videos_Agendados",
        "C:/AFI/Musicas"
    ]
    
    for pasta in pastas_necessarias:
        if not Path(pasta).exists():
            logger.warning(f"⚠️ Pasta não encontrada: {pasta}")
            logger.info("💡 Execute 'python editor_video.py' primeiro para criar as pastas")
    
    # Inicializar e executar o Guardião
    guardiao = GuardiaoMidia()
    
    print(f"📁 Pasta monitorada: {guardiao.pasta_monitorada}")
    print("📝 Para testar:")
    print("   1. Adicione músicas nas pastas C:/AFI/Musicas/[Rock|Pop|Calma|Instrumental]")
    print("   2. Copie um vídeo para C:/AFI/Videos_Para_Editar")
    print("   3. O Guardião detectará e processará automaticamente!")
    print()
    print("⏹️ Pressione Ctrl+C para parar")
    print()
    
    guardiao.iniciar()

if __name__ == '__main__':
    main()