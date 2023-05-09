import telebot
from get_env import get_env_data_as_dict

env = get_env_data_as_dict('/usr/med_exam_prep/.env')

bot = telebot.TeleBot(env["TG_BOT_TOKEN"])

@bot.message_handler(commands=['start'])
def send_welcome(message):
	bot.reply_to(message, """
							Привет! Это тестовая версия бота. Сейчас я отправлю тебе случайный вопрос.\n
							В ответ нужно прислать только номер правильного ответа\n
							(ели ответов несколько - пришли номера без пробелов, например, 24)""")
	bot.send_message(message.chat.id, f'Твой уникальный номер - {message.chat.id}')
	
@bot.message_handler(func=lambda message: True)
def echo_all(message):
	bot.reply_to(message, message.text)

bot.infinity_polling()
