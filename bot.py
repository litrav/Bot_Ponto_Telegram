import os
import requests
import sys

TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

if not TOKEN or not CHAT_ID:
    sys.exit(1)

tipo = sys.argv[1] if len(sys.argv) > 1 else "geral"

def enviar_mensagem():
    msgs = {
        "saida": "🏃 *Fim do expediente padrão!* \n\n🛑 16h! Se seu horário acabou, bate o ponto e até amanhã!",
        "turno_19": "🕖 *Aviso das 19h!* \n\nCheck-point noturno. Se continua logado, foco total ou hora de ir!",
        "turno_21": "🦉 *Modo Corujão (21h)* \n\n⚠️ Hora extra rolando? Não esqueça de registrar. Se já acabou, vai descansar!",
        "geral": "⚠️ *Lembrete de Ponto!* \nConferir registros."
    }

    msg = msgs.get(tipo, msgs["geral"])
    
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"}

    try:
        requests.post(url, json=payload).raise_for_status()
    except Exception:
        sys.exit(1)

if __name__ == "__main__":
    enviar_mensagem()
