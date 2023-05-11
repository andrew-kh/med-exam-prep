import pandas as pd

df = pd.read_excel('./source_data/exam_source.xlsx')

df_temp = df.loc[:3,:]

with open("exam_materials.txt", "w") as file:
    for index, row in df_temp.iterrows():
        non_empty_items = [i for i in row[3:] if i==i]
        answer_options = [f'{i}) ' for i in range(1, len(non_empty_items)+1)]
        formatted_answers_list = [''.join(i) for i in zip(answer_options, non_empty_items)]
        formatted_answers_text = '\n'.join(formatted_answers_list)
        file.write(f'Вопрос {index+1} - {row["Текст вопроса"]}:\n')
        file.write(formatted_answers_text+'\n\n')