# 🤖 Bot Fiscal de Ponto



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

| Horário (BRT) | Tipo | Mensagem |
| :--- | :--- | :--- |
| **09:00** | ☀️ Entrada | "Bom dia! Já bateu o ponto?" |
| **12:00** | 🍽️ Almoço | "Hora do rango! Não esquece o ponto." |
| **13:00** | 🔙 Volta | "De volta ao trabalho!" |
| **16:00** | 🏃 Saída | "Fim de expediente padrão." |
| **21:00** | 🦉 Hora Extra | "Ainda por aí? Registre a hora extra." |

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
