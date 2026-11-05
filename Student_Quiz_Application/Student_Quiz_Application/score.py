"""Score calculation helpers."""


def calculate_score(total_questions, correct_answers):
    if not isinstance(total_questions, int) or total_questions <= 0:
        raise ValueError("Total questions must be a positive integer.")
    if not isinstance(correct_answers, int) or not 0 <= correct_answers <= total_questions:
        raise ValueError("Correct answers must be between zero and total questions.")
    wrong_answers = total_questions - correct_answers
    percentage = (correct_answers / total_questions) * 100
    return {
        "total": total_questions,
        "correct": correct_answers,
        "wrong": wrong_answers,
        "percentage": percentage,
    }
