import pandas as pd

df = pd.read_excel('./source_data/exam_source_final.xlsx')

with open("exam_materials_final.txt", "w") as file:
    for index, row in df.iterrows():
        
        non_empty_items = [str(i).strip() for i in row[3:] if i==i]
        
        answer_options = [f'{i}) ' for i in range(1, len(non_empty_items)+1)]
        
        formatted_answers_list = [''.join(i) for i in zip(answer_options, non_empty_items)]
        
        formatted_answers_text = '\n'.join(formatted_answers_list)
        
        file.write(f'Вопрос {index+1} - {row["Текст вопроса"].strip()}:\n')
        file.write(formatted_answers_text+'\n\n')
