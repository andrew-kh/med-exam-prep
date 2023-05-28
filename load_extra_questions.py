import pandas as pd
from sqlalchemy import create_engine
from get_env import get_env_data_as_dict

env = get_env_data_as_dict('/usr/med_exam_prep/.env')
engine = create_engine(f'postgresql+psycopg2://{env["PG_USER"]}:{env["PG_PWD"]}@127.0.0.1/{env["PG_DB"]}')

df_answers = pd.read_csv('./data/answers_endocrinology.txt', sep='\t', encoding='cp1251')

df_answers.to_sql('answers', con=engine, if_exists='append', schema='med', index=False)

df_questions = pd.read_csv('./data/questions_endocrinology.txt', sep='\t', encoding='cp1251')

df_questions.to_sql('questions', con=engine, if_exists='append', schema='med', index=False)