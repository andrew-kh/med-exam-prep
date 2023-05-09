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
def send_welcome(message, conn):
	
	bot.reply_to(message,
	    """
		Привет! Это тестовая версия бота. Сейчас я отправлю тебе случайный вопрос.\n
		В ответ нужно прислать только номер правильного ответа\n
		(ели ответов несколько - пришли номера без пробелов, например, 24)""")
	
	bot.send_message(message.chat.id, f'Твой уникальный номер - {message.chat.id}')
	
	time.sleep(1)

	cur = conn.cursor()
	cur.execute(f'INSERT INTO med.user_questions (user_id, question_id) VALUES ({message.chat.id}, NULL)')
	conn.commit()
	cur.close()

	rand_q_id = random.randint(0, 1583)

	cur = conn.cursor()
	cur.execute(f'SELECT DISTINCT question_text FROM med.questions_raw WHERE question_id = {rand_q_id}')
	question_text = cur.fetchone()[0]

	bot.send_message(message.chat.id, f'Вопрос: {question_text}')
	
@bot.message_handler(func=lambda message: True)
def echo_all(message):
	bot.reply_to(message, message.text)

bot.infinity_polling()
