CREATE TABLE med.questions AS
SELECT DISTINCT
	topic_id,
	question_id,
	question_text
FROM med.questions_raw

CREATE TABLE med.answers AS
SELECT DISTINCT
	question_id,
	answer_id,
	answer_text,
	is_correct_answer
FROM med.questions_raw

CREATE TABLE med.active_sessions (
	user_id INTEGER,
	session_id SERIAL PRIMARY KEY,
	question_id INTEGER,
	correct_answer_id INTEGER,
	shuffled_answer_id INTEGER,
	is_answered INTEGER
)
