# 🤖 Bot Fiscal de Ponto - SuperBid

> "Código bom é código commitado, mas código pago é código com ponto batido!" 💸

Este projeto é um bot automatizado que envia lembretes diários no grupo do Telegram da equipe para garantir que ninguém esqueça de registrar o ponto (entrada, almoço, volta e saída).

## 👥 Autores

Projeto desenvolvido e mantido por:

* **[Henrique Pineda](https://github.com/Henriquepineda)**
* **[Pedro Trofino](https://github.com/litrav)**

---

## ⚙️ Como Funciona

O sistema roda 100% na nuvem usando **GitHub Actions** (Serverless). Não é necessário manter nenhum computador ligado.

1.  O **GitHub Actions** acorda nos horários agendados (Cron Job).
2.  Ele sobe um ambiente Linux temporário e instala o Python.
3.  O script verifica a hora atual e seleciona a mensagem correta.
4.  A mensagem é enviada via API para o grupo do Telegram.

## ⏰ Cronograma de Disparos

Os horários estão configurados para o fuso de Brasília (BRT / UTC-3):

 "saida": "🏃 *Fim do expediente padrão!* \n\n🛑 16h! Se seu horário acabou, bate o ponto e até amanhã!",
 "turno_19": "🕖 *Aviso das 19h!* \n\nCheck-point noturno. Se continua logado, foco total ou hora de ir!",
"turno_21": "🦉 *Modo Corujão (21h)* \n\n⚠️ Hora extra rolando? Não esqueça de registrar. Se já acabou, vai descansar!",
"geral": "⚠️ *Lembrete de Ponto!* \nConferir registros."

*Obs: O bot roda automaticamente de Segunda a Sexta.*

## 🚀 Como Configurar (Deploy)

Para rodar este bot no seu próprio repositório:

1.  **Clone este repositório.**
2.  **Crie um Bot no Telegram:**
    * Fale com o `@BotFather` e pegue o `Token`.
3.  **Descubra o ID do Grupo:**
    * Adicione o bot no grupo, mande uma mensagem e pegue o Chat ID via API.
4.  **Configure as Secrets no GitHub:**
    Vá em `Settings` > `Secrets and variables` > `Actions` e adicione:
    * `TELEGRAM_TOKEN`: O token do seu bot.
    * `TELEGRAM_CHAT_ID`: O ID do grupo (com o sinal de menos).

## 🛠️ Tecnologias

* [Python 3](https://www.python.org/)
* [GitHub Actions](https://github.com/features/actions)
* [Telegram API](https://core.telegram.org/bots/api)

---
*Feito com ☕ e Python.*
