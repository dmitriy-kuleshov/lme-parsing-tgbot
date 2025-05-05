import telebot
from src.config import TOKEN
from src.bot.handlers import handle_start, handle_text

bot = telebot.TeleBot(TOKEN)


# Регистрация обработчиков
@bot.message_handler(commands=['start'])
def start(message):
    handle_start(message, bot)

@bot.message_handler(content_types=['text'])
def text(message):
    handle_text(message, bot)

if __name__ == '__main__':
    print("Bot is polling...")
    bot.polling(none_stop=True)