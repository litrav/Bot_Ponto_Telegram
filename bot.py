# --- 1. IMPORTAÇÕES ---
import logging
import datetime
import pytz  # Para fusos horários
import os    # Para pegar a URL do DB
import psycopg2 # Nosso NOVO banco de dados
from urllib.parse import urlparse # Para ler a URL do DB

from telegram.ext import Application, CommandHandler

# --- 2. CONFIGURAÇÃO DO BANCO DE DADOS (Supabase) ---

# O Render vai nos dar a "chave" por uma variável de ambiente
# No seu PC, ele vai dar erro por enquanto, mas vamos arrumar
DATABASE_URL = os.environ.get('DATABASE_URL')

def get_db_connection():
    """Cria e retorna uma conexão com o banco de dados."""
    if not DATABASE_URL:
        raise ValueError("Variável DATABASE_URL não foi configurada!")
        
    # Conecta no Supabase
    conn = psycopg2.connect(DATABASE_URL)
    return conn

def setup_database():
    """Garante que a tabela 'users' exista."""
    # A tabela já foi criada no Supabase, mas é bom ter
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        # Cria a tabela se ela NÃO existir (garante)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                chat_id BIGINT UNIQUE NOT NULL,
                created_at TIMESTAMPTZ DEFAULT NOW()
            )
        ''')
        conn.commit()
        cursor.close()
        conn.close()
        print("Banco de dados verificado com sucesso.")
    except Exception as e:
        print(f"Erro ao verificar o banco de dados: {e}")


# --- 3. COMANDOS DO USUÁRIO (/start e /stop) ---
async def start(update, context):
    """Salva o chat_id do usuário no banco de dados Supabase."""
    chat_id = update.effective_chat.id
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # "ON CONFLICT (chat_id) DO NOTHING" é o novo "INSERT OR IGNORE"
        # Ele tenta inserir, mas se o chat_id (que é UNIQUE) já existir, não faz nada
        sql = "INSERT INTO users (chat_id) VALUES (%s) ON CONFLICT (chat_id) DO NOTHING"
        cursor.execute(sql, (chat_id,))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        await update.message.reply_text(
            'Olá! Você se inscreveu para receber os lembretes do martelo (de Seg a Sex).'
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
        conn = get_db_connection()
        cursor = conn.cursor()
        
        sql = "DELETE FROM users WHERE chat_id = %s"
        cursor.execute(sql, (chat_id,))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        await update.message.reply_text(
            'Você foi removido da lista e não receberá mais lembretes.'
        )
    except Exception as e:
        print(f"Erro ao remover usuário: {e}")

# --- 4. FUNÇÕES DE DISPARO (BROADCAST) ---
async def broadcast_message(context, message_text):
    """Envia uma mensagem para TODOS os usuários no banco de dados."""
    chat_ids = []
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT chat_id FROM users")
        # .fetchall() retorna uma lista de tuplas, ex: [(123,), (456,)]
        rows = cursor.fetchall()
        chat_ids = [row[0] for row in rows] # Transforma em [123, 456]
        
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Erro ao buscar usuários: {e}")

    if not chat_ids:
        print("Nenhum usuário inscrito para o broadcast.")
        return

    print(f"Disparando mensagem para {len(chat_ids)} usuários...")
    
    for chat_id in chat_ids:
        try:
            await context.bot.send_message(chat_id=chat_id, text=message_text)
        except Exception as e:
            print(f"Erro ao enviar para {chat_id}: {e}")

async def send_msg_18h(context):
    """Prepara a mensagem das 18h."""
    mensagem = "Lembrete das 18:00! Bata seu ponto :) 🌇"
    await broadcast_message(context, mensagem)

async def send_msg_22h(context):
    """Prepara a mensagem das 22h."""
    mensagem = "Lembrete das 22:00! Bata seu ponto :) 🌃"
    await broadcast_message(context, mensagem)

# --- 5. FUNÇÃO PRINCIPAL (MAIN) ---
def main():
    """Função principal que roda o bot."""
    
    # 1. Verifica o banco de dados ao iniciar
    setup_database()

    # 2. Configura o log
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
    
    # Checa se o TOKEN foi inserido
    if TOKEN == "COLOQUE_SEU_TOKEN_AQUI":
        logger.error("ERRO: O TOKEN do Telegram não foi configurado!")
        return
        
    # Checa se a URL do DB está disponível (senão o bot não funciona)
    if not DATABASE_URL:
        logger.error("ERRO: A DATABASE_URL não foi encontrada!")
        logger.warning("Para rodar localmente, veja o passo 3 das instruções.")
        return

    # 3. Cria a 'Aplicação' do bot
    application = Application.builder().token(TOKEN).build()

    # 4. Define fuso horário e dias da semana
    fuso_horario = pytz.timezone("America/Sao_Paulo")
    dias_de_semana = (0, 1, 2, 3, 4) # Seg a Sex

    # 5. Pega o 'JobQueue' (agendador)
    job_queue = application.job_queue

    # 6. Agenda os disparos (APENAS DIAS DE SEMANA)
    job_queue.run_daily(
        send_msg_18h,
        time=datetime.time(hour=18, minute=0, tzinfo=fuso_horario),
        days=dias_de_semana,
        name="job_18h_semana"
    )
    job_queue.run_daily(
        send_msg_22h,
        time=datetime.time(hour=22, minute=0, tzinfo=fuso_horario),
        days=dias_de_semana,
        name="job_22h_semana"
    )

    # 7. Registra os comandos
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("stop", stop))

    # 8. Inicia o bot
    logger.info("Bot iniciado e 'escutando'...")
    application.run_polling()

# --- 6. INICIALIZAÇÃO ---
if __name__ == '__main__':
    main()