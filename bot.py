import os
import requests
import sys

# --- CONFIGURAÇÕES ---
TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

if not TOKEN or not CHAT_ID:
    print("ERRO: Configure as Secrets (TELEGRAM_TOKEN e TELEGRAM_CHAT_ID) no GitHub!")
    sys.exit(1)


tipo = sys.argv[1] if len(sys.argv) > 1 else "geral"

def enviar_mensagem():
    # --- DICIONÁRIO DE MENSAGENS ---
    if tipo == "entrada":
        msg = "☀️ *Bom dia, Time SuperBid!* \n\n☕ 09h! Já bateu o ponto de entrada? Bora codar!"
    
    elif tipo == "almoco_ida":
        msg = "🍽️ *Hora do Almoço!* \n\n😋 12h! Pausa pro rango. Bate o ponto e bom apetite!"
    
    elif tipo == "almoco_volta":
        msg = "🔙 *De volta ao trabalho!* \n\n🔋 13h! Bate o ponto da volta e bora resolver esses tickets!"
    
    elif tipo == "saida":
        msg = "🏃 *Fim do expediente padrão!* \n\n🛑 16h! Se seu horário acabou, bate o ponto e vaza. Até amanhã!"
        
    elif tipo == "hora_extra":
        msg = "🦉 *Modo Corujão Ativado?* \n\n⚠️ 21h! Se ainda está por aí, não esqueça de registrar a hora extra (ou vai descansar, guerreiro!)."
    
    else:
        msg = "⚠️ *Lembrete de Ponto!* \nPassando pra lembrar de conferir seus registros hoje."

    
    
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": msg,
        "parse_mode": "Markdown"
    }

    try:
        requests.post(url, json=payload).raise_for_status()
        print(f"✅ Sucesso! Mensagem de '{tipo}' enviada.")
    except Exception as e:
        print(f"❌ Erro ao enviar: {e}")
        sys.exit(1)

if __name__ == "__main__":
    enviar_mensagem()
