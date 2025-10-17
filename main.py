import requests
import argparse
import json


def verificar_modelos_ollama():
    """
    Função para verificar a conexão com a API do Ollama e listar os modelos disponíveis.
    """
    try:
        # Fazer requisição GET para o endpoint da API do Ollama
        response = requests.get("http://localhost:11434/api/tags")
        
        # Verificar se a resposta teve status 200 (sucesso)
        if response.status_code == 200:
            # Extrair o JSON da resposta
            data = response.json()
            
            # Pegar a lista de modelos
            modelos = data.get('models', [])
            
            # Extrair apenas os nomes dos modelos para exibição mais limpa
            nomes_modelos = [modelo.get('name', 'Nome não disponível') for modelo in modelos]
            
            # Imprimir mensagem de sucesso com os modelos encontrados
            print(f"✅ Conexão com Ollama bem-sucedida! Modelos disponíveis: {nomes_modelos}")
            return True
            
        else:
            # Se o status for diferente de 200, imprimir mensagem de erro
            print(f"❌ Erro na resposta da API. Estado: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        # Capturar erro de conexão e imprimir mensagem clara
        print("❌ Falha ao conectar com o Ollama. Verifique se o Ollama está em execução.")
        return False
        
    except Exception as e:
        # Capturar outros possíveis erros
        print(f"❌ Erro inesperado: {e}")
        return False


def gerar_resposta_llm(prompt_usuario: str):
    """
    Função para enviar um prompt para o modelo llava-llama3 e obter a resposta.
    
    Args:
        prompt_usuario (str): O prompt/pergunta do usuário
        
    Returns:
        str: A resposta do modelo ou None em caso de erro
    """
    try:
        # Endpoint da API para geração de texto
        url = "http://localhost:11434/api/generate"
        
        # Payload (corpo) da requisição JSON
        payload = {
            "model": "llava-llama3",
            "prompt": prompt_usuario,
            "stream": False
        }
        
        # Fazer requisição POST para o endpoint
        print("🤖 Gerando resposta... (isso pode levar alguns segundos)")
        response = requests.post(url, json=payload, timeout=120)
        
        # Verificar se a resposta teve status 200 (sucesso)
        if response.status_code == 200:
            # Extrair o JSON da resposta
            data = response.json()
            
            # Extrair o campo "response" do JSON
            resposta_ia = data.get('response', '')
            
            if resposta_ia:
                return resposta_ia
            else:
                print("❌ Resposta vazia recebida do modelo.")
                return None
                
        else:
            # Se o status for diferente de 200, imprimir mensagem de erro
            print(f"❌ Erro na resposta da API. Estado: {response.status_code}")
        print(f"Detalhes: {response.text}")
            return None
            
    except requests.exceptions.ConnectionError:
        # Capturar erro de conexão
        print("❌ Falha ao conectar com o Ollama. Verifique se o Ollama está em execução.")
        return None
        
    except requests.exceptions.Timeout:
        # Capturar erro de tempo limite
        print("❌ Tempo limite na requisição. O modelo pode estar demorando para responder.")
        return None
        
    except json.JSONDecodeError:
        # Capturar erro de decodificação JSON
        print("❌ Erro ao decodificar a resposta JSON da API.")
        return None
        
    except Exception as e:
        # Capturar outros possíveis erros
        print(f"❌ Erro inesperado: {e}")
        return None


if __name__ == "__main__":
    # Configurar argparse para capturar argumentos da linha de comando
    parser = argparse.ArgumentParser(description="Conversar com o modelo llava-llama3 via Ollama")
    parser.add_argument("prompt", nargs="?", help="O prompt/pergunta para enviar ao modelo")
    parser.add_argument("--testar", action="store_true", help="Apenas testar a conexão com o Ollama")
    
    args = parser.parse_args()
    
    # Se a flag --testar foi usada, apenas verificar conexão
    if args.testar:
        verificar_modelos_ollama()
    elif args.prompt:
        # Se um prompt foi fornecido, gerar resposta
        print(f"📝 Prompt: {args.prompt}")
        print("-" * 50)
        
        resposta = gerar_resposta_llm(args.prompt)
        
        if resposta:
            print("🤖 Resposta da IA:")
            print(resposta)
        else:
            print("❌ Não foi possível obter uma resposta da IA.")
    else:
        # Se nenhum argumento foi fornecido, mostrar ajuda
        print("❌ Por favor, forneça um prompt para a IA.")
        print("Exemplo: python3.13 main.py \"Qual o sentido da vida?\"")
        print("Para testar a conexão: python3.13 main.py --testar")
        parser.print_help()