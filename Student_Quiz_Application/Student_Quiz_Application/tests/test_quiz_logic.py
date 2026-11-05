import json
import tempfile
import unittest
from pathlib import Path

from quiz_logic import load_questions, normalize_answer, evaluate_answers, QuestionDataError
from score import calculate_score
from result import get_performance


class QuizLogicTests(unittest.TestCase):
    def setUp(self):
        self.questions = load_questions(Path(__file__).resolve().parents[1] / "questions.json")

    def test_question_bank_has_18_valid_questions(self):
        self.assertEqual(len(self.questions), 18)

    def test_question_ids_are_unique(self):
        ids = [q["id"] for q in self.questions]
        self.assertEqual(len(ids), len(set(ids)))

    def test_all_questions_have_four_options(self):
        for q in self.questions:
            self.assertEqual(set(q["options"]), {"A", "B", "C", "D"})

    def test_all_answers_are_valid(self):
        for q in self.questions:
            self.assertIn(q["answer"], {"A", "B", "C", "D"})

    def test_normalize_answer(self):
        self.assertEqual(normalize_answer(" b "), "B")
        self.assertIsNone(normalize_answer("X"))
        self.assertIsNone(normalize_answer(None))

    def test_all_correct_answers(self):
        answers = {q["id"]: q["answer"] for q in self.questions}
        score, review = evaluate_answers(self.questions, answers)
        self.assertEqual(score, len(self.questions))
        self.assertTrue(all(row["correct"] for row in review))

    def test_all_wrong_answers(self):
        answers = {q["id"]: next(k for k in "ABCD" if k != q["answer"]) for q in self.questions}
        score, review = evaluate_answers(self.questions, answers)
        self.assertEqual(score, 0)
        self.assertTrue(all(not row["correct"] for row in review))

    def test_unanswered_questions_are_incorrect(self):
        score, review = evaluate_answers(self.questions, {})
        self.assertEqual(score, 0)
        self.assertTrue(all(row["selected"] is None for row in review))

    def test_partial_answers(self):
        answers = {self.questions[0]["id"]: self.questions[0]["answer"]}
        score, _ = evaluate_answers(self.questions, answers)
        self.assertEqual(score, 1)

    def test_score_calculation(self):
        result = calculate_score(10, 7)
        self.assertEqual(result["wrong"], 3)
        self.assertEqual(result["percentage"], 70.0)

    def test_zero_score(self):
        self.assertEqual(calculate_score(5, 0)["percentage"], 0.0)

    def test_perfect_score(self):
        self.assertEqual(calculate_score(5, 5)["percentage"], 100.0)

    def test_invalid_total_rejected(self):
        with self.assertRaises(ValueError):
            calculate_score(0, 0)

    def test_invalid_correct_count_rejected(self):
        with self.assertRaises(ValueError):
            calculate_score(5, 6)

    def test_performance_boundaries(self):
        self.assertEqual(get_performance(80), "Excellent")
        self.assertEqual(get_performance(60), "Good")
        self.assertEqual(get_performance(40), "Average")
        self.assertEqual(get_performance(39.99), "Needs Improvement")

    def test_invalid_performance_percentage_rejected(self):
        with self.assertRaises(ValueError):
            get_performance(101)

    def test_missing_question_file(self):
        with self.assertRaises(QuestionDataError):
            load_questions(Path("file_that_does_not_exist.json"))

    def test_malformed_json_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "bad.json"
            path.write_text("{bad json", encoding="utf-8")
            with self.assertRaises(QuestionDataError):
                load_questions(path)

    def test_missing_field_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "bad.json"
            path.write_text(json.dumps([{"id": 1}]), encoding="utf-8")
            with self.assertRaises(QuestionDataError):
                load_questions(path)

    def test_invalid_options_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "bad.json"
            bad = [{"id": 1, "question": "Q?", "options": {"A": "a"}, "answer": "A"}]
            path.write_text(json.dumps(bad), encoding="utf-8")
            with self.assertRaises(QuestionDataError):
                load_questions(path)


if __name__ == "__main__":
    unittest.main()
