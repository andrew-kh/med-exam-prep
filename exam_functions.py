
ACTIVE_SESSIONS_TABLE = 'med.active_sessions'
QUESTIONS_TABLE = 'med.questions'

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
    registration_query = f'INSERT INTO {ACTIVE_SESSIONS_TABLE} (user_id) VALUES ({user_id});'
    execute_update_query(conn_object, registration_query)


def assign_question(conn_object, user_id, question_id):
    assign_question_query = f'UPDATE {ACTIVE_SESSIONS_TABLE} SET question_id = {question_id} WHERE user_id = {user_id}'
    execute_update_query(conn_object, assign_question_query)


def get_question_text(conn_object, question_id):
    get_question_query = f'SELECT question_text from {QUESTIONS_TABLE} where question_id = {question_id}'
    question_text = execute_select_query(conn_object, get_question_query)
    return(question_text[0])