import telebot
import time
import random
import psycopg2
import exam_functions as ef
from get_env import get_env_data_as_dict

env = get_env_data_as_dict('/usr/med_exam_prep/.env')

conn = psycopg2.connect(
    host='localhost',
    database=env['PG_DB'],
    user=env['PG_USER'],
    password=env['PG_PWD']
)

bot = telebot.TeleBot(env['TG_BOT_TOKEN'])

@bot.message_handler(commands=['start'])
def send_welcome(message):
	
	bot.reply_to(message,
	('Привет! Бот для подготовки к гос экзамену.\n'
	'Ты зарегистрирован в сервисе.\n'
	f'Твой уникальный номер - {message.chat.id}\n'
	'Теперь нужно выбрать список вопросов, который ты хочешь отработать.'))

	# num_of_questions = ef.get_num_of_questions(conn)

	bot.send_message(message.chat.id,
	(f'В базе  2 набора вопросов:\n'
	'1 - 139: общие вопросы\n'
	'139 - 1336: эндокринология'
	'Чтобы отработать вопрос с n до m, отправь команду\n'
  	'/ask n m'))

	# ef.register_user(conn, message.chat.id)
	
	# ef.ask_question(conn, message.chat.id, bot)

@bot.message_handler(commands=['ask'])
def send_welcome(message):

	ef.register_user(conn, message.chat.id)

	session_id = ef.get_user_session(conn, message.chat.id)

	question_ids = message.text.split(' ')[1:]

	ef.set_session_question_range(conn, message.chat.id, session_id, int(question_ids[0])-1, int(question_ids[1])-1)

	bot.send_message(message.chat.id, f'Тебе добавлены вопросы с {question_ids[0]} по {question_ids[1]}')

	ef.ask_question(conn, message.chat.id, bot)
	

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
