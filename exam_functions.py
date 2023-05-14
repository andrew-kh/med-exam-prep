import random

ACTIVE_SESSIONS_TABLE = 'med.active_sessions'
QUESTIONS_TABLE = 'med.questions'
ANSWERS_TABLE = 'med.answers'

def execute_select_query(conn_object, query_text):
    cur = conn_object.cursor()
    cur.execute(query_text)
    # list of tuples
    query_res = cur.fetchall()
    return query_res


def execute_update_query(conn_object, query_text):
	cur = conn_object.cursor()
	cur.execute(query_text)
	conn_object.commit()
	cur.close()
        

def register_user(conn_object, user_id):
    registration_query = f'INSERT INTO {ACTIVE_SESSIONS_TABLE} (user_id, creation_ts) VALUES ({user_id}, NOW());'
    execute_update_query(conn_object, registration_query)


def assign_question(conn_object, user_id, question_id):
    assign_question_query = f"""
    UPDATE {ACTIVE_SESSIONS_TABLE}
    SET
        question_id = {question_id}
    WHERE
        user_id = {user_id}
        and is_answered is null
    """
    execute_update_query(conn_object, assign_question_query)


def get_question_text(conn_object, question_id):
    get_question_query = f'SELECT question_text from {QUESTIONS_TABLE} where question_id = {question_id}'
    question_text = execute_select_query(conn_object, get_question_query)
    return(question_text[0][0])

def get_answers(conn_object, question_id):
    get_answer_query = f'SELECT answer_id, answer_text, is_correct_answer from {ANSWERS_TABLE} where question_id = {question_id}'
    answers = execute_select_query(conn_object, get_answer_query)
    return answers

def shuffle_answers(answers):
    # answers is a list of tuples
    random.shuffle(answers)
    answers = [list(i) for i in answers]
    answers_text = [f'{a_num}) {a_text[1]}' for a_num, a_text in zip(range(1,len(answers)+1), answers)]
    answers_text = '\n'.join(answers_text)
    correct_answer_ids = [i[0] for i in answers if i[2]==1]
    shuffled_answer_ids = [j for i,j in zip(answers, range(1,len(answers)+1)) if i[2]==1]
    correct_answer_int = int(''.join([str(i) for i in correct_answer_ids]))
    shuffled_answer_int = int(''.join([str(i) for i in shuffled_answer_ids]))
    return answers_text, correct_answer_int, shuffled_answer_int


def update_question_answers(conn_object, user_id, question_id, correct_answer_id, shuffled_answer_id):
    update_question_answers_query = f"""
    update {ACTIVE_SESSIONS_TABLE}
    set correct_answer_id = {correct_answer_id},
        shuffled_answer_id = {shuffled_answer_id}
    where
        user_id = {user_id}
        and question_id = {question_id}
        and is_answered is null
    """
    execute_update_query(conn_object, update_question_answers_query)

def get_expected_answer(conn_object, user_id):
    get_expected_answer_query = f'SELECT shuffled_answer_id FROM {ACTIVE_SESSIONS_TABLE} WHERE user_id = {user_id} and is_answered is null'
    expected_answer_int = execute_select_query(conn_object, get_expected_answer_query)[0][0]
    return set(list(str(expected_answer_int)))

def finish_session(conn_object, user_id):
    finish_session_query = f"""
    update {ACTIVE_SESSIONS_TABLE}
    set
        closing_ts = NOW(),
	    is_answered = 1
    where
        user_id = {user_id}
	    and is_answered is null
    """
    execute_update_query(conn_object, finish_session_query)

def ask_question(conn_object, user_id, bot_object):
	
    register_user(conn_object, user_id)

    question_id = select_random_q_from_range(
            conn_object,
            user_id,
            0,
            5)
    
    question_id[0][0]

    if question_id != None:

        assign_question(conn_object, user_id, question_id)

        question_text = get_question_text(conn_object, question_id)

        answers = get_answers(conn_object, question_id)
        answers_text, correct_ids_int, shuffled_ids_int = shuffle_answers(answers)
        update_question_answers(
            conn_object,
            user_id,
            question_id,
            correct_ids_int,
            shuffled_ids_int
        )

        is_multiple_answers = correct_ids_int > 9

        if is_multiple_answers:
            bot_object.send_message(user_id, f'Вопрос (неск. ответов): {question_text}')
        else:
            bot_object.send_message(user_id, f'Вопрос: {question_text}')

        bot_object.send_message(user_id, f'Варианты ответа:\n{answers_text}')
        
    else:

        bot_object.send_message(user_id, f'Поздравляю, все назначенные вопросы решены. Свяжись с администратором для доступа к следующему набору.')

def validate_answer_message(message_text):
    try:
        int(message_text)
    except ValueError:
        return True
    

def select_random_q_from_range(conn_object, user_id, lbound, ubound):
    random_q_from_range_query = f"""
    select
        q.question_id
    from {QUESTIONS_TABLE} q
    left join {ACTIVE_SESSIONS_TABLE} act
        on q.question_id = act.question_id
        and act.user_id = {user_id}
        and act.is_answered = 1
    where
        act.question_id is null
        and q.question_id between {lbound} and {ubound}
    order by random()
    limit 1
    """
    question_id = execute_select_query(conn_object, random_q_from_range_query)
    return question_id