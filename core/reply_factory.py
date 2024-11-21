
from .constants import BOT_WELCOME_MESSAGE, PYTHON_QUESTION_LIST


def generate_bot_responses(message, session):
    bot_responses = []

    current_question_id = session.get("current_question_id")
    if not current_question_id:
        bot_responses.append(BOT_WELCOME_MESSAGE)

    success, error = record_current_answer(message, current_question_id, session)

    if not success:
        return [error]

    next_question, next_question_id = get_next_question(current_question_id)

    if next_question:
        bot_responses.append(next_question)
    else:
        final_response = generate_final_response(session)
        bot_responses.append(final_response)

    session["current_question_id"] = next_question_id
    session.save()

    return bot_responses


def record_current_answer(answer, current_question_id, session):
    '''
    Validates and stores the answer for the current question to django session.
    '''
    if 'answers' not in session:
        session['answers'] = {}
    session['answers'][current_question_id] = answer
    session.modified = True
    return True, ""


def get_next_question(current_question_id):
    '''
    Fetches the next question from the PYTHON_QUESTION_LIST based on the current_question_id.
    '''
    next_question = PYTHON_QUESTION_LIST[current_question_id]

    return next_question, -1


def generate_final_response(session):
    '''
    Creates a final result message including a score based on the answers
    by the user for questions in the PYTHON_QUESTION_LIST.
    '''
    user_answers = session.get('answers', {})
    score = 0
    total_questions = len(PYTHON_QUESTION_LIST)

    for i, question in enumerate(PYTHON_QUESTION_LIST):
        question_id = i + 1  # Question ID starts from 1 (index + 1)
        correct_answer = question["answer"]
        user_answer = user_answers.get(question_id, "").strip()
        if user_answer.lower() == correct_answer.lower():
            score += 1
    result_message = f"You scored {score} out of {total_questions}."
    if score == total_questions:
        result_message += " Perfect score!"
    elif score >= total_questions // 2:
        result_message += " Good job!"
    else:
        result_message += " Better luck next time!"

    return result_message
