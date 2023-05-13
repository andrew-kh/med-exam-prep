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

	# ef.register_user(conn, message.chat.id)

	# rand_q_id = random.randint(0, 199)
	# ef.assign_question(conn, message.chat.id, rand_q_id)
	
	# question_text = ef.get_question_text(conn, rand_q_id)

	# answers = ef.get_answers(conn, rand_q_id)
	# answers_text, correct_ids_int, shuffled_ids_int = ef.shuffle_answers(answers)
	# ef.update_question_answers(
	# 	conn,
	# 	message.chat.id,
	# 	rand_q_id,
	# 	correct_ids_int,
	# 	shuffled_ids_int
	# )

	# is_multiple_answers = correct_ids_int > 9

	# if is_multiple_answers:
	# 	bot.send_message(message.chat.id, f'Вопрос (неск. ответов): {question_text}')
	# else:
	# 	bot.send_message(message.chat.id, f'Вопрос: {question_text}')

	# bot.send_message(message.chat.id, f'Варианты ответа:\n{answers_text}')

	
@bot.message_handler(func=lambda message: True)
def echo_all(message):
	
	expected_answer = ef.get_expected_answer(conn, message.chat.id)

	user_answer = set(list(message.text))

	if user_answer == expected_answer:
		bot.send_message(message.chat.id, 'Верно 😸')
		ef.remove_user(conn, message.chat.id)
		ef.ask_question(conn, message.chat.id, bot)
	else:
		bot.send_message(message.chat.id, 'Попробуй еще раз 😿')

bot.infinity_polling()
