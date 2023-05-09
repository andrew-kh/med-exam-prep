import pandas as pd
from sqlalchemy import create_engine
from get_env import get_env_data_as_dict

env = get_env_data_as_dict('/usr/project_looker_bi/.env')
engine = create_engine(f'postgresql+psycopg2://{env["PG_USER"]}:{env["PG_PWD"]}@127.0.0.1/{env["PG_DB"]}')

df = pd.read_csv('./data/exam_questions_w_answers.txt', sep='\t')
