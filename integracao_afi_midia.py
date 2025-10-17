#!/usr/bin/env python3
"""
🧠 AFI v4.0 - Integração com Mídia Social
Conecta o Guardião de Mídia com o sistema AFI para análise inteligente

Este módulo integra o sistema de monitoramento de vídeos com o AFI,
permitindo análise inteligente de conteúdo e geração de frases de impacto.
"""

import os
import sys
import logging
from pathlib import Path

# Adicionar o diretório atual ao path para importar módulos locais
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from core_logic import AFICore
    from config import Config
except ImportError as e:
    logging.warning(f"Módulos AFI não encontrados: {e}")
    AFICore = None
    Config = None

logger = logging.getLogger(__name__)

class IntegradorAFIMidia:
    """
    Classe que integra o AFI com o sistema de mídia social.
    """
    
    def __init__(self):
        """
        Inicializa o integrador AFI-Mídia.
        """
        self.afi_core = None
        self.config = None
        self.inicializar_afi()
        
    def inicializar_afi(self):
        """
        Inicializa a conexão com o AFI.
        """
        try:
            if Config and AFICore:
                self.config = Config()
                self.afi_core = AFICore()
                logger.info("✅ AFI Core inicializado com sucesso")
            else:
                logger.warning("⚠️ AFI Core não disponível - usando modo simulado")
        except Exception as e:
            logger.error(f"❌ Erro ao inicializar AFI: {e}")
            
    def analisar_video_com_afi(self, caminho_video):
        """
        Analisa um vídeo usando o AFI e gera frase de impacto + estilo musical.
        
        Args:
            caminho_video (str): Caminho para o arquivo de vídeo
            
        Returns:
            tuple: (frase_impacto, estilo_musica)
        """
        try:
            nome_arquivo = Path(caminho_video).stem
            
            if self.afi_core:
                # Usar AFI real para análise
                return self._analisar_com_afi_real(caminho_video, nome_arquivo)
            else:
                # Usar análise simulada
                return self._analisar_simulado(nome_arquivo)
                
        except Exception as e:
            logger.error(f"❌ Erro na análise do vídeo: {e}")
            return self._analisar_simulado(Path(caminho_video).stem)
    
    def _analisar_com_afi_real(self, caminho_video, nome_arquivo):
        """
        Análise usando o AFI real.
        """
        try:
            # Prompt para o AFI analisar o vídeo
            prompt_analise = f"""
            Analise este arquivo de vídeo: {nome_arquivo}
            
            Com base no nome do arquivo e no contexto da FINITI (empresa de equipamentos airless),
            gere:
            1. Uma frase de impacto curta (máximo 30 caracteres) para story de rede social
            2. Um estilo musical adequado: Rock, Pop, Calma, Eletronica ou Instrumental
            
            Responda no formato:
            FRASE: [sua frase aqui]
            ESTILO: [estilo musical]
            """
            
            # Consultar AFI
            resposta = self.afi_core.processar_consulta(prompt_analise)
            
            # Extrair frase e estilo da resposta
            frase, estilo = self._extrair_frase_estilo(resposta)
            
            logger.info(f"🧠 AFI analisou: Frase='{frase}', Estilo='{estilo}'")
            return frase, estilo
            
        except Exception as e:
            logger.error(f"❌ Erro na análise AFI real: {e}")
            return self._analisar_simulado(nome_arquivo)
    
    def _extrair_frase_estilo(self, resposta_afi):
        """
        Extrai frase e estilo da resposta do AFI.
        """
        try:
            linhas = resposta_afi.split('\n')
            frase = "🚀 Inovação FINITI"
            estilo = "Instrumental"
            
            for linha in linhas:
                if 'FRASE:' in linha.upper():
                    frase = linha.split(':', 1)[1].strip()
                elif 'ESTILO:' in linha.upper():
                    estilo = linha.split(':', 1)[1].strip()
            
            # Validar estilo
            estilos_validos = ['Rock', 'Pop', 'Calma', 'Eletronica', 'Instrumental']
            if estilo not in estilos_validos:
                estilo = 'Instrumental'
            
            return frase, estilo
            
        except Exception as e:
            logger.error(f"❌ Erro ao extrair frase/estilo: {e}")
            return "🚀 Inovação FINITI", "Instrumental"
    
    def _analisar_simulado(self, nome_arquivo):
        """
        Análise simulada baseada em palavras-chave.
        """
        nome_lower = nome_arquivo.lower()
        
        # Mapeamento de palavras-chave para frases e estilos
        mapeamentos = {
            'airless': ("🔧 Tecnologia Airless", "Instrumental"),
            'manual': ("📖 Guia Completo", "Calma"),
            'tecnico': ("⚙️ Precisão Técnica", "Instrumental"),
            'vendas': ("💰 Oportunidade Única", "Pop"),
            'promocao': ("🎁 Oferta Especial", "Pop"),
            'treino': ("💪 Capacitação Pro", "Rock"),
            'energia': ("⚡ Força Total", "Rock"),
            'qualidade': ("🏆 Excelência FINITI", "Instrumental"),
            'inovacao': ("🚀 Futuro Agora", "Eletronica"),
            'produto': ("✨ Solução Ideal", "Pop")
        }
        
        # Buscar correspondência
        for palavra, (frase, estilo) in mapeamentos.items():
            if palavra in nome_lower:
                logger.info(f"🎯 Análise simulada: '{palavra}' → Frase='{frase}', Estilo='{estilo}'")
                return frase, estilo
        
        # Padrão se nenhuma palavra-chave for encontrada
        frase_padrao = "🚀 FINITI Inovação"
        estilo_padrao = "Instrumental"
        
        logger.info(f"📝 Usando padrão: Frase='{frase_padrao}', Estilo='{estilo_padrao}'")
        return frase_padrao, estilo_padrao
    
    def gerar_prompt_criativo(self, nome_arquivo, contexto=""):
        """
        Gera um prompt criativo para análise mais detalhada.
        """
        prompt = f"""
        🎬 ANÁLISE CRIATIVA DE VÍDEO - AFI v4.0
        
        Arquivo: {nome_arquivo}
        Contexto: {contexto}
        
        Como especialista em marketing digital da FINITI, analise este vídeo e crie:
        
        1. FRASE DE IMPACTO (máximo 25 caracteres):
           - Deve ser cativante para stories
           - Incluir emoji relevante
           - Focar no benefício principal
        
        2. ESTILO MUSICAL:
           - Rock: Para energia e motivação
           - Pop: Para vendas e promoções
           - Calma: Para tutoriais e explicações
           - Eletronica: Para inovação e tecnologia
           - Instrumental: Para conteúdo técnico
        
        3. JUSTIFICATIVA:
           - Por que essa combinação funciona?
        
        Responda no formato:
        FRASE: [sua frase]
        ESTILO: [estilo escolhido]
        JUSTIFICATIVA: [explicação]
        """
        
        return prompt

def testar_integracao():
    """
    Testa a integração AFI-Mídia.
    """
    print("🧠 Testando Integração AFI-Mídia")
    print("=" * 40)
    
    integrador = IntegradorAFIMidia()
    
    # Testes com diferentes tipos de arquivo
    testes = [
        "manual_airless_1095.mp4",
        "promocao_outubro_rosa.mp4", 
        "treino_vendas_finiti.mp4",
        "tutorial_tecnico_equipamento.mp4",
        "inovacao_produto_2025.mp4"
    ]
    
    for arquivo_teste in testes:
        print(f"\n📹 Analisando: {arquivo_teste}")
        frase, estilo = integrador.analisar_video_com_afi(arquivo_teste)
        print(f"   📝 Frase: {frase}")
        print(f"   🎵 Estilo: {estilo}")

if __name__ == '__main__':
    testar_integracao()