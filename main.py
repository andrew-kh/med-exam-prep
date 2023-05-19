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
		Привет! Это тестовая версия бота.
		Ты зарегистрирован в сервисе.
		Теперь нужно выбрать список вопросов, который ты хочешь решать.""")
	
	bot.send_message(message.chat.id, f'Твой уникальный номер - {message.chat.id}')

	ef.register_user(conn, message.chat.id)
	
	# ef.ask_question(conn, message.chat.id, bot)

@bot.message_handler(commands=['ask'])
def send_welcome(message):


	session_id = ef.get_user_session(conn, message.chat.id)

	question_ids = message.text.split(' ')[1:]

	ef.set_session_question_range(conn, message.chat.id, session_id, question_ids[0], question_ids[1])

	bot.send_message(message.chat.id, f'Ваши вопросы добавлены: с {question_ids[0]} по {question_ids[1]}')

	#TODO: ef.ask_question here
	

@bot.message_handler(func=lambda message: int(message.text))
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
