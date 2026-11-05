"""Core quiz data loading and answer-validation logic."""
import json
from pathlib import Path

VALID_OPTIONS = {"A", "B", "C", "D"}


class QuestionDataError(ValueError):
    """Raised when the question bank is missing or incorrectly formatted."""


def load_questions(file_path):
    """Load and validate a JSON question bank."""
    path = Path(file_path)
    try:
        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError as exc:
        raise QuestionDataError(f"Question file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise QuestionDataError(f"Invalid JSON in {path}: {exc}") from exc

    if not isinstance(data, list) or not data:
        raise QuestionDataError("The question file must contain a non-empty list.")

    seen_ids = set()
    cleaned = []
    for index, item in enumerate(data, start=1):
        if not isinstance(item, dict):
            raise QuestionDataError(f"Question {index} must be a JSON object.")
        required = {"id", "question", "options", "answer"}
        missing = required - item.keys()
        if missing:
            raise QuestionDataError(f"Question {index} is missing: {', '.join(sorted(missing))}.")
        if not isinstance(item["id"], int) or item["id"] in seen_ids:
            raise QuestionDataError(f"Question {index} must have a unique integer id.")
        seen_ids.add(item["id"])
        if not isinstance(item["question"], str) or not item["question"].strip():
            raise QuestionDataError(f"Question {index} has an empty question.")
        options = item["options"]
        if not isinstance(options, dict) or set(options.keys()) != VALID_OPTIONS:
            raise QuestionDataError(f"Question {index} must have exactly A, B, C and D options.")
        if any(not isinstance(v, str) or not v.strip() for v in options.values()):
            raise QuestionDataError(f"Question {index} contains an empty option.")
        answer = item["answer"]
        if not isinstance(answer, str) or answer.strip().upper() not in VALID_OPTIONS:
            raise QuestionDataError(f"Question {index} has an invalid correct answer.")
        cleaned_item = dict(item)
        cleaned_item["answer"] = answer.strip().upper()
        cleaned_item["options"] = dict(options)
        cleaned.append(cleaned_item)
    return cleaned


def normalize_answer(answer):
    """Normalize a selected option; return None for an invalid or missing choice."""
    if answer is None:
        return None
    value = str(answer).strip().upper()
    return value if value in VALID_OPTIONS else None


def evaluate_answers(questions, answers):
    """Return per-question correctness details and the total score."""
    review = []
    score = 0
    for question in questions:
        selected = normalize_answer(answers.get(question["id"]))
        correct = selected == question["answer"]
        score += int(correct)
        review.append({
            "id": question["id"],
            "question": question["question"],
            "selected": selected,
            "correct_answer": question["answer"],
            "correct": correct,
            "options": question["options"],
        })
    return score, review
