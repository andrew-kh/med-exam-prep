import pandas as pd

df = pd.read_excel('./source_data/exam_source_final.xlsx')

df = df.dropna(how='all', axis=1, inplace=False)

df = df.rename(columns={
    '№ темы': 'topic_id',
    'Тип вопроса': 'question_type',
    'Текст вопроса': 'question_text'
})

answer_cols = [i for i in list(df.columns) if i.find('Ответ') >=0]

df = df.melt(
    id_vars=['topic_id', 'question_type', 'question_text'],
    value_vars=answer_cols,
    value_name='answer_text',
    var_name='answer_id',
    ignore_index=False
)

df.index.name='question_id'

df = df[df['answer_text'].isnull()==False]

df['answer_text'] = df['answer_text'].astype(str)

df['answer_id'] = (df['answer_id']
                   .str.replace('Ответ ', '', regex=True)
                   .astype(int))

df = df.drop(columns=['question_type'])

# use count to check for typos in answers
df['is_correct_answer'] = df['answer_text'].str.count('\*')

# check 1: unique answers are {0;1}
# output in console
check_ans = list(df.is_correct_answer.unique())
if len(check_ans)!=2 or sum(check_ans)!=1:
    print('check for unique answers {0;1} failed')

# if check 1 is passed, we can safely remove * sign
# from answer text
df['answer_text'] = df['answer_text'].str.replace('\*', '', regex=True).str.strip()

df.to_csv('./data/exam_questions_w_answers_final.txt', sep='\t', index=True)
