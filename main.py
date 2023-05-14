import telebot
import time
import random
import psycopg2
import exam_functions as ef
from get_env import get_env_data_as_dict

env = get_env_data_as_dict('/usr/med_exam_prep/.env')

conn = psycopg2.connect(
    host="localhost",
    database=env["PG_DB"],
    user=env["PG_USER"],
    password=env["PG_PWD"]
)

bot = telebot.TeleBot(env["TG_BOT_TOKEN"])

@bot.message_handler(commands=['start'])
def send_welcome(message):
	
	bot.reply_to(message,
	    """
		Привет! Это тестовая версия бота. Сейчас я отправлю тебе случайный вопрос.\n
		В ответ нужно прислать только номер правильного ответа\n
		(ели ответов несколько - пришли номера без пробелов, например, 24)""")
	
	bot.send_message(message.chat.id, f'Твой уникальный номер - {message.chat.id}')
	
	ef.ask_question(conn, message.chat.id, bot)

	
@bot.message_handler(func=lambda message: True)
def echo_all(message):
	
	expected_answer = ef.get_expected_answer(conn, message.chat.id)

	user_answer = set(list(message.text))

	if ef.validate_answer_message(message.text):
		bot.send_message(message.chat.id, '🙀 это не похоже на вариант ответа. пожалуйста, пришли число без пробелов')
	else:
		if user_answer == expected_answer:
			bot.send_message(message.chat.id, 'Верно 😸')
			ef.finish_session(conn, message.chat.id)
			ef.ask_question(conn, message.chat.id, bot)
		else:
			bot.send_message(message.chat.id, 'Попробуй еще раз 😿')

bot.infinity_polling()
