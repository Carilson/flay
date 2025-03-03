import telebot
import openai
import os
from dotenv import load_dotenv

# 🔹 Carregar variáveis do .env
load_dotenv()

# 🔹 Configurar as chaves das APIs
OPENROUTER_API_KEY = os.getenv("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")
TOGETHER_AI_API_KEY = os.getenv("820c62f9b5f6100751cc6c146044443bf025e8b62495763e0b6471813d397684")
TOKEN = os.getenv("8192216721:AAFyfK_Fk0QSkDqsADB8YjmWb5lL0pirdH8")

bot = telebot.TeleBot(TOKEN)

def usar_openrouter(prompt):
    openai.api_base = "https://openrouter.ai/api/v1"
    openai.api_key = OPENROUTER_API_KEY
    resposta = openai.ChatCompletion.create(
        model="openrouter/gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return resposta["choices"][0]["message"]["content"]

def usar_together_ai(prompt):
    openai.api_base = "https://api.together.ai/v1"
    openai.api_key = TOGETHER_AI_API_KEY
    resposta = openai.ChatCompletion.create(
        model="together/mistral-7b",
        messages=[{"role": "user", "content": prompt}]
    )
    return resposta["choices"][0]["message"]["content"]

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "👋 Olá! Me envie um código para análise ou peça para eu gerar um novo.")

@bot.message_handler(func=lambda message: True)
def responder_usuario(message):
    texto = message.text.lower()
    if "gera um código" in texto:
        tipo = texto.replace("gera um código de", "").strip()
        resposta = usar_openrouter(f"Crie um código em Java/Kotlin para: {tipo}")
    else:
        resposta = usar_together_ai(f"Analise este código e encontre erros: {texto}")

    bot.reply_to(message, resposta)

bot.polling()
