# --- 1. IMPORTAÇÕES ---
# Importações padrão do Python
import sqlite3
import logging
import datetime
import pytz  # Para fusos horários
import os    # Para checar o sistema de arquivos do servidor

# Importações da biblioteca do Telegram
from telegram.ext import Application, CommandHandler

# --- 2. CONFIGURAÇÃO DO BANCO DE DADOS (PARA O SERVIDOR) ---
# O Render (servidor) nos dá um disco em '/var/data'
# Vamos checar se essa pasta existe para saber onde salvar o DB
if os.path.isdir('/var/data'):
    DB_PATH = '/var/data/users.db' # Caminho no servidor
    print(f"Usando banco de dados do servidor em: {DB_PATH}")
else:
    DB_PATH = 'users.db' # Caminho no seu PC
    print(f"Usando banco de dados local em: {DB_PATH}")

def setup_database():
    """Cria o banco de dados e a tabela de usuários se não existirem."""
    # Usa a variável DB_PATH que definimos acima
    conn = sqlite3.connect(DB_PATH) 
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            chat_id INTEGER PRIMARY KEY
        )
    ''')
    conn.commit()
    conn.close()

# --- 3. COMANDOS DO USUÁRIO (/start e /stop) ---
async def start(update, context):
    """Salva o chat_id do usuário que iniciou o bot."""
    chat_id = update.effective_chat.id
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        # "INSERT OR IGNORE" tenta inserir, mas ignora se o chat_id já existir
        cursor.execute("INSERT OR IGNORE INTO users (chat_id) VALUES (?)", (chat_id,))
        conn.commit()
        conn.close()
        
        await update.message.reply_text(
            'Olá! Você se inscreveu para receber os lembretes de ponto (de Seg a Sex).'
        )
    except Exception as e:
        print(f"Erro ao salvar usuário: {e}")
        await update.message.reply_text(
            'Ocorreu um erro ao te inscrever. Tente novamente.'
        )

async def stop(update, context):
    """Remove o chat_id do usuário do banco de dados."""
    chat_id = update.effective_chat.id
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE chat_id = ?", (chat_id,))
        conn.commit()
        conn.close()
        
        await update.message.reply_text(
            'Você foi removido da lista e não receberá mais lembretes.'
        )
    except Exception as e:
        print(f"Erro ao remover usuário: {e}")

# --- 4. FUNÇÕES DE DISPARO (BROADCAST) ---
async def broadcast_message(context, message_text):
    """Envia uma mensagem para TODOS os usuários no banco de dados."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT chat_id FROM users")
    chat_ids = cursor.fetchall()  # Retorna uma lista de IDs
    conn.close()
    
    print(f"Disparando mensagem para {len(chat_ids)} usuários...")
    
    for (chat_id,) in chat_ids:
        try:
            await context.bot.send_message(chat_id=chat_id, text=message_text)
        except Exception as e:
            # Se o bot for bloqueado, printa o erro e continua
            print(f"Erro ao enviar para {chat_id}: {e}")

async def send_msg_18h(context):
    """Prepara a mensagem das 18h."""
    mensagem = "Lembrete 1! Não esqueça de bater seu ponto :)"
    await broadcast_message(context, mensagem)

async def send_msg_22h(context):
    """Prepara a mensagem das 22h."""
    mensagem = "Lembrete 2! Não esqueça de bater seu ponto :)"
    await broadcast_message(context, mensagem)

# --- 5. FUNÇÃO PRINCIPAL (MAIN) ---
def main():
    """Função principal que roda o bot."""
    
    # 1. Cria o banco de dados ao iniciar
    setup_database()

    # 2. Configura o log (para vermos erros no terminal)
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    logger = logging.getLogger(__name__)

    # ==========================================================
    # !! IMPORTANTE !! Coloque seu Token aqui
    # ==========================================================
    TOKEN = "8547700177:AAGyW6hY9bgHzXeVaSDGcE_7LAOYUistegM"
    # ==========================================================

    # 3. Cria a 'Aplicação' do bot
    application = Application.builder().token(TOKEN).build()

    # 4. Define nosso fuso horário (ex: 'America/Sao_Paulo')
    fuso_horario = pytz.timezone("America/Sao_Paulo")

    # 5. Define os dias da semana (0=Seg, 1=Ter, 2=Qua, 3=Qui, 4=Sex)
    dias_de_semana = (0, 1, 2, 3, 4)

    # 6. Pega o 'JobQueue' (agendador)
    job_queue = application.job_queue

    # 7. Agenda os disparos (APENAS DIAS DE SEMANA)
    job_queue.run_daily(
        send_msg_18h,
        time=datetime.time(hour=18, minute=0, tzinfo=fuso_horario),
        days=dias_de_semana, # A mágica acontece aqui
        name="job_18h_semana"
    )
    
    job_queue.run_daily(
        send_msg_22h,
        time=datetime.time(hour=22, minute=0, tzinfo=fuso_horario),
        days=dias_de_semana, # E aqui
        name="job_22h_semana"
    )

    # 8. Registra os comandos que o bot 'ouve'
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("stop", stop))

    # 9. Inicia o bot
    logger.info("Bot iniciado e 'escutando'...")
    application.run_polling()

# --- 6. INICIALIZAÇÃO ---
if __name__ == '__main__':
    main()