import telebot
from get_env import get_env_data_as_dict

env = get_env_data_as_dict('/usr/med_exam_prep/.env')

bot = telebot.TeleBot(env["TG_BOT_TOKEN"])

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Howdy, how are you doing?")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
	bot.reply_to(message, message.text)

bot.infinity_polling()
