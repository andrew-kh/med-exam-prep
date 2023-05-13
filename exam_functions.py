
ACTIVE_SESSIONS_TABLE = 'med.active_sessions'

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
