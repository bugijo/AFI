#!/usr/bin/env python3
"""
🤖 AFI v4.0 - Agente de Mídia Social Completo
Sistema Automatizado de Criação de Conteúdo para Redes Sociais

Este é o script principal que integra todos os componentes:
- 👁️ Guardião (Monitoramento de pastas)
- 🧠 Cérebro Criativo (Análise AFI)
- 🎬 Oficina de Edição (MoviePy)
- 📅 Fila de Saída (Agendamento)
"""

import os
import sys
import time
import logging
import argparse
from pathlib import Path
from datetime import datetime

# Importar módulos do sistema
try:
    from guardiao_midia import GuardiaoMidia, GuardiaoMidiaHandler
    from editor_video import editar_video_story, criar_pastas_necessarias
    from integracao_afi_midia import IntegradorAFIMidia
except ImportError as e:
    print(f"❌ Erro ao importar módulos: {e}")
    print("💡 Certifique-se de que todos os arquivos estão no mesmo diretório")
    sys.exit(1)

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('agente_midia_social.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class AgenteMidiaSocial:
    """
    Classe principal do Agente de Mídia Social.
    Coordena todos os componentes do sistema.
    """
    
    def __init__(self):
        """
        Inicializa o Agente de Mídia Social.
        """
        self.integrador_afi = IntegradorAFIMidia()
        self.guardiao = None
        self.estatisticas = {
            'videos_processados': 0,
            'videos_com_sucesso': 0,
            'videos_com_erro': 0,
            'inicio_execucao': datetime.now()
        }
        
    def inicializar_sistema(self):
        """
        Inicializa todo o sistema e cria estrutura necessária.
        """
        logger.info("🚀 Inicializando Agente de Mídia Social...")
        
        # Criar pastas necessárias
        logger.info("📁 Criando estrutura de pastas...")
        criar_pastas_necessarias()
        
        # Verificar dependências
        self._verificar_dependencias()
        
        # Inicializar guardião com integração AFI
        self._inicializar_guardiao_inteligente()
        
        logger.info("✅ Sistema inicializado com sucesso!")
        
    def _verificar_dependencias(self):
        """
        Verifica se todas as dependências estão instaladas.
        """
        dependencias = ['moviepy', 'watchdog']
        
        for dep in dependencias:
            try:
                __import__(dep)
                logger.info(f"✅ {dep} disponível")
            except ImportError:
                logger.error(f"❌ {dep} não encontrado")
                raise ImportError(f"Instale {dep}: pip install {dep}")
    
    def _inicializar_guardiao_inteligente(self):
        """
        Inicializa o guardião com integração AFI.
        """
        # Criar handler personalizado com AFI
        handler_inteligente = GuardiaoMidiaHandlerInteligente(
            afi_integration=self.integrador_afi,
            estatisticas=self.estatisticas
        )
        
        # Criar guardião
        self.guardiao = GuardiaoMidia()
        self.guardiao.handler = handler_inteligente
        
    def executar_modo_monitoramento(self):
        """
        Executa o sistema em modo de monitoramento contínuo.
        """
        logger.info("👁️ Iniciando modo de monitoramento...")
        self._exibir_status_inicial()
        
        try:
            self.guardiao.iniciar()
        except KeyboardInterrupt:
            logger.info("⏹️ Parando sistema...")
            self._exibir_estatisticas_finais()
    
    def processar_video_unico(self, caminho_video, caminho_musica=None, texto_personalizado=None):
        """
        Processa um único vídeo sem monitoramento.
        
        Args:
            caminho_video (str): Caminho para o vídeo
            caminho_musica (str): Caminho para música (opcional)
            texto_personalizado (str): Texto personalizado (opcional)
        """
        logger.info(f"🎬 Processando vídeo único: {caminho_video}")
        
        try:
            video_path = Path(caminho_video)
            if not video_path.exists():
                raise FileNotFoundError(f"Vídeo não encontrado: {caminho_video}")
            
            # Analisar com AFI se não houver texto personalizado
            if not texto_personalizado:
                frase, estilo = self.integrador_afi.analisar_video_com_afi(caminho_video)
            else:
                frase = texto_personalizado
                estilo = "Instrumental"  # Padrão
            
            # Selecionar música se não especificada
            if not caminho_musica:
                caminho_musica = self._selecionar_musica_automatica(estilo)
            
            # Gerar nome de saída
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
            nome_saida = f"{timestamp}_processado_{video_path.stem}.mp4"
            caminho_saida = Path("C:/AFI/Videos_Agendados") / nome_saida
            
            # Processar vídeo
            sucesso = editar_video_story(
                caminho_video_original=caminho_video,
                caminho_musica=caminho_musica,
                texto_overlay=frase,
                caminho_saida=str(caminho_saida)
            )
            
            if sucesso:
                logger.info(f"✅ Vídeo processado: {caminho_saida}")
                return str(caminho_saida)
            else:
                logger.error("❌ Erro no processamento")
                return None
                
        except Exception as e:
            logger.error(f"❌ Erro ao processar vídeo: {e}")
            return None
    
    def _selecionar_musica_automatica(self, estilo):
        """
        Seleciona uma música automaticamente baseada no estilo.
        """
        pasta_musicas = Path(f"C:/AFI/Musicas/{estilo}")
        
        if pasta_musicas.exists():
            musicas = list(pasta_musicas.glob("*.mp3"))
            if musicas:
                return str(musicas[0])  # Primeira música encontrada
        
        # Fallback: procurar em qualquer pasta
        for pasta in Path("C:/AFI/Musicas").iterdir():
            if pasta.is_dir():
                musicas = list(pasta.glob("*.mp3"))
                if musicas:
                    return str(musicas[0])
        
        return None
    
    def _exibir_status_inicial(self):
        """
        Exibe status inicial do sistema.
        """
        print("\n" + "="*60)
        print("🤖 AFI v4.0 - AGENTE DE MÍDIA SOCIAL")
        print("="*60)
        print(f"📁 Pasta monitorada: C:/AFI/Videos_Para_Editar")
        print(f"🎵 Pastas de música: C:/AFI/Musicas/[Rock|Pop|Calma|Eletronica|Instrumental]")
        print(f"📤 Saída: C:/AFI/Videos_Agendados")
        print(f"🕐 Iniciado em: {self.estatisticas['inicio_execucao'].strftime('%Y-%m-%d %H:%M:%S')}")
        print("\n📝 COMO USAR:")
        print("1. Adicione músicas nas pastas de estilo")
        print("2. Copie vídeos para a pasta monitorada")
        print("3. O sistema processará automaticamente!")
        print("\n⏹️ Pressione Ctrl+C para parar")
        print("="*60)
    
    def _exibir_estatisticas_finais(self):
        """
        Exibe estatísticas finais do sistema.
        """
        tempo_execucao = datetime.now() - self.estatisticas['inicio_execucao']
        
        print("\n" + "="*50)
        print("📊 ESTATÍSTICAS FINAIS")
        print("="*50)
        print(f"⏱️ Tempo de execução: {tempo_execucao}")
        print(f"🎬 Vídeos processados: {self.estatisticas['videos_processados']}")
        print(f"✅ Sucessos: {self.estatisticas['videos_com_sucesso']}")
        print(f"❌ Erros: {self.estatisticas['videos_com_erro']}")
        
        if self.estatisticas['videos_processados'] > 0:
            taxa_sucesso = (self.estatisticas['videos_com_sucesso'] / self.estatisticas['videos_processados']) * 100
            print(f"📈 Taxa de sucesso: {taxa_sucesso:.1f}%")
        
        print("="*50)

class GuardiaoMidiaHandlerInteligente(GuardiaoMidiaHandler):
    """
    Handler inteligente que integra com AFI e estatísticas.
    """
    
    def __init__(self, afi_integration=None, estatisticas=None):
        super().__init__(afi_integration)
        self.afi_integration = afi_integration
        self.estatisticas = estatisticas or {}
    
    def consultar_afi(self, caminho_video):
        """
        Usa a integração AFI real em vez da simulação.
        """
        if self.afi_integration:
            return self.afi_integration.analisar_video_com_afi(str(caminho_video))
        else:
            return super().consultar_afi(caminho_video)
    
    def processar_novo_video(self, caminho_video):
        """
        Processa novo vídeo com estatísticas.
        """
        self.estatisticas['videos_processados'] = self.estatisticas.get('videos_processados', 0) + 1
        
        try:
            super().processar_novo_video(caminho_video)
            self.estatisticas['videos_com_sucesso'] = self.estatisticas.get('videos_com_sucesso', 0) + 1
        except Exception as e:
            self.estatisticas['videos_com_erro'] = self.estatisticas.get('videos_com_erro', 0) + 1
            raise e

def main():
    """
    Função principal com interface de linha de comando.
    """
    parser = argparse.ArgumentParser(
        description="🤖 AFI v4.0 - Agente de Mídia Social",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:

  # Modo monitoramento (padrão)
  python agente_midia_social.py

  # Processar vídeo único
  python agente_midia_social.py --video "meu_video.mp4"

  # Processar com música específica
  python agente_midia_social.py --video "video.mp4" --musica "musica.mp3"

  # Processar com texto personalizado
  python agente_midia_social.py --video "video.mp4" --texto "🚀 Minha frase!"

  # Apenas configurar sistema
  python agente_midia_social.py --setup
        """
    )
    
    parser.add_argument('--video', help='Processar vídeo único')
    parser.add_argument('--musica', help='Música específica para usar')
    parser.add_argument('--texto', help='Texto personalizado para overlay')
    parser.add_argument('--setup', action='store_true', help='Apenas configurar sistema')
    
    args = parser.parse_args()
    
    # Criar agente
    agente = AgenteMidiaSocial()
    agente.inicializar_sistema()
    
    if args.setup:
        print("✅ Sistema configurado com sucesso!")
        print("📁 Pastas criadas em C:/AFI/")
        print("💡 Adicione músicas e vídeos para começar!")
        return
    
    if args.video:
        # Modo processamento único
        resultado = agente.processar_video_unico(
            caminho_video=args.video,
            caminho_musica=args.musica,
            texto_personalizado=args.texto
        )
        
        if resultado:
            print(f"✅ Vídeo processado: {resultado}")
        else:
            print("❌ Erro no processamento")
    else:
        # Modo monitoramento
        agente.executar_modo_monitoramento()

if __name__ == '__main__':
    main()