#!/usr/bin/env python3
"""
Teste da função de nomeação de arquivos do guardiao.py
"""

from datetime import datetime

def gerar_nome_arquivo_agendado():
    """
    Gera nome de arquivo baseado na data e hora atuais.
    Formato: DD-MM-AA.Descricao.mp4
    """
    agora = datetime.now()
    
    # Lógica de descrição baseada no dia da semana e horário
    if agora.weekday() == 5 or agora.weekday() == 6:  # Sábado ou Domingo
        descricao = "Bomdia"
    else:  # Dia de semana
        if agora.hour < 12:
            descricao = "Bomdia"
        else:
            descricao = "Encerramento"
    
    # Formato do nome do arquivo
    nome_arquivo = f"{agora.strftime('%d-%m-%y')}.{descricao}.mp4"
    return nome_arquivo

if __name__ == "__main__":
    print("🧪 Teste da função de nomeação de arquivos")
    print("=" * 50)
    
    # Teste atual
    nome_atual = gerar_nome_arquivo_agendado()
    print(f"📅 Data/Hora atual: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print(f"📁 Nome gerado: {nome_atual}")
    
    # Teste simulando diferentes horários
    print("\n🔄 Simulando diferentes cenários:")
    
    # Simular manhã de segunda
    agora_teste = datetime.now().replace(hour=9, minute=0, second=0)
    if agora_teste.weekday() < 5:  # Dia de semana
        descricao = "Bomdia" if agora_teste.hour < 12 else "Encerramento"
    else:
        descricao = "Bomdia"
    nome_teste = f"{agora_teste.strftime('%d-%m-%y')}.{descricao}.mp4"
    print(f"🌅 Segunda 09:00 → {nome_teste}")
    
    # Simular tarde de sexta
    agora_teste = datetime.now().replace(hour=15, minute=0, second=0)
    if agora_teste.weekday() < 5:  # Dia de semana
        descricao = "Bomdia" if agora_teste.hour < 12 else "Encerramento"
    else:
        descricao = "Bomdia"
    nome_teste = f"{agora_teste.strftime('%d-%m-%y')}.{descricao}.mp4"
    print(f"🌆 Sexta 15:00 → {nome_teste}")
    
    print("\n✅ Teste concluído!")