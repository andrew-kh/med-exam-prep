import telebot
import time
import random
from get_env import get_env_data_as_dict

env = get_env_data_as_dict('/usr/med_exam_prep/.env')
engine = create_engine(f'postgresql+psycopg2://{env["PG_USER"]}:{env["PG_PWD"]}@127.0.0.1/{env["PG_DB"]}')

bot = telebot.TeleBot(env["TG_BOT_TOKEN"])

@bot.message_handler(commands=['start'])
def send_welcome(message):
	
	bot.reply_to(message,
	    """
		Привет! Это тестовая версия бота. Сейчас я отправлю тебе случайный вопрос.\n
		В ответ нужно прислать только номер правильного ответа\n
		(ели ответов несколько - пришли номера без пробелов, например, 24)""")
	
	bot.send_message(message.chat.id, f'Твой уникальный номер - {message.chat.id}')
	
	time.wait(1)

	with engine.connect() as conn:
		conn.execute(f'INSERT INTO med.user_questions (user_id, question_id) VALUES ({message.chat.id}, NULL)')

	rand_q_id = random.randint(0, 1583)

	with engine.connect() as conn:
		result = conn.execute(f'SELECT DISTINCT question_text FROM med.questions_raw WHERE question_id = {rand_q_id}').fetchone()[0]

	bot.send_message(message.chat.id, f'Вопрос: {result}')
	
@bot.message_handler(func=lambda message: True)
def echo_all(message):
	bot.reply_to(message, message.text)

bot.infinity_polling()
