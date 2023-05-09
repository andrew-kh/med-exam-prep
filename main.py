import telebot
import time
import random
import psycopg2
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
	
	time.sleep(1)

	rand_q_id = random.randint(0, 1583)

	cur = conn.cursor()
	cur.execute(f'SELECT DISTINCT question_text FROM med.questions_raw WHERE question_id = {rand_q_id}')
	question_text = cur.fetchone()[0]

	cur.execute(f'SELECT answer_text FROM med.questions_raw WHERE question_id = {rand_q_id}')	
	answer_text = cur.fetchall()
	answer_text = [i[0] for i in answer_text]
	answers_id = list(range(1,len(answer_text)+1))
	pos_answers = [f'{a_num} - {a_text}' for a_num, a_text in zip(answers_id, answer_text)]
	pos_answers = '\n'.join(pos_answers)

	cur = conn.cursor()
	cur.execute(f'INSERT INTO med.user_questions (user_id, question_id) VALUES ({message.chat.id}, {rand_q_id})')
	conn.commit()
	cur.close()

	bot.send_message(message.chat.id, f'Вопрос: {question_text}')
	bot.send_message(message.chat.id, f'Варианты ответа:\n{pos_answers}')

	
@bot.message_handler(func=lambda message: True)
def echo_all(message):
	
	cur = conn.cursor()
	cur.execute(f'SELECT question_id FROM med.user_questions WHERE user_id = {message.chat.id}')
	current_question_id = int(cur.fetchone()[0])

	cur.execute(f'SELECT answer_id FROM med.questions_raw WHERE question_id = {current_question_id} and is_correct_answer=1')
	correct_answers = cur.fetchall()
	correct_answers = set([i[0] for i in correct_answers])

	user_answer = set([int(i) for i in message.text])

	if user_answer == correct_answers:
		bot.send_message(message.chat.id, 'Верно 😸')
		cur = conn.cursor()
		cur.execute(f'DELETE FROM med.user_questions WHERE user_id = {message.chat.id}')
		conn.commit()
		cur.close()
	else:
		bot.send_message(message.chat.id, 'Попробуй еще раз 😿')

bot.infinity_polling()
