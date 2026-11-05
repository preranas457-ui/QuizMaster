"""Tkinter graphical interface for the Student Quiz Application."""
import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path

from quiz_logic import load_questions, evaluate_answers, QuestionDataError
from score import calculate_score
from result import get_performance

APP_TITLE = "Student Quiz Application"
BG = "#F3F6FB"
NAVY = "#172B4D"
BLUE = "#315EFB"
TEAL = "#13A89E"
TEXT = "#1F2937"
MUTED = "#667085"
WHITE = "#FFFFFF"


class QuizApp(tk.Tk):
    def __init__(self, question_file=None):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry("900x680")
        self.minsize(760, 600)
        self.configure(bg=BG)
        self.question_file = Path(question_file) if question_file else Path(__file__).with_name("questions.json")
        self.questions = []
        self.answers = {}
        self.student_name = ""
        self.current_index = 0
        self.result_data = None
        self.review_data = []
        self._configure_styles()
        self._show_welcome()

    def _configure_styles(self):
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("TFrame", background=BG)
        style.configure("Card.TFrame", background=WHITE)
        style.configure("Title.TLabel", background=BG, foreground=NAVY,
                        font=("Segoe UI", 25, "bold"))
        style.configure("Subtitle.TLabel", background=BG, foreground=MUTED,
                        font=("Segoe UI", 11))
        style.configure("CardTitle.TLabel", background=WHITE, foreground=NAVY,
                        font=("Segoe UI", 17, "bold"))
        style.configure("Body.TLabel", background=WHITE, foreground=TEXT,
                        font=("Segoe UI", 12))
        style.configure("Muted.TLabel", background=WHITE, foreground=MUTED,
                        font=("Segoe UI", 10))
        style.configure("Primary.TButton", font=("Segoe UI", 11, "bold"),
                        padding=(18, 11), background=BLUE, foreground=WHITE)
        style.map("Primary.TButton", background=[("active", "#2449D8"), ("disabled", "#AAB6D3")])
        style.configure("Secondary.TButton", font=("Segoe UI", 10, "bold"),
                        padding=(14, 9), background="#E9EEFF", foreground=NAVY)
        style.map("Secondary.TButton", background=[("active", "#DCE5FF")])
        style.configure("TEntry", padding=10, font=("Segoe UI", 12))
        style.configure("TRadiobutton", background=WHITE, foreground=TEXT,
                        font=("Segoe UI", 12), padding=9)
        style.map("TRadiobutton", background=[("active", "#F2F5FF")])
        style.configure("Quiz.Horizontal.TProgressbar", troughcolor="#E4EAF4",
                        background=TEAL, thickness=9)

    def _clear(self):
        for child in self.winfo_children():
            child.destroy()

    def _page(self, heading, subtitle):
        self._clear()
        outer = ttk.Frame(self, padding=(42, 30))
        outer.pack(fill="both", expand=True)
        ttk.Label(outer, text=heading, style="Title.TLabel").pack(anchor="w")
        ttk.Label(outer, text=subtitle, style="Subtitle.TLabel").pack(anchor="w", pady=(6, 22))
        return outer

    def _card(self, parent, padding=28):
        card = ttk.Frame(parent, style="Card.TFrame", padding=padding)
        card.pack(fill="both", expand=True)
        return card

    def _show_welcome(self):
        outer = self._page("Student Quiz Application", "Test your knowledge • Track your score • Review your answers")
        card = self._card(outer, padding=38)
        ttk.Label(card, text="Welcome!", style="CardTitle.TLabel").pack(anchor="w", pady=(4, 8))
        ttk.Label(card, text="Enter your name to begin the quiz.", style="Body.TLabel").pack(anchor="w")
        ttk.Label(card, text="18 multiple-choice questions  |  One point for each correct answer",
                  style="Muted.TLabel").pack(anchor="w", pady=(8, 24))
        ttk.Label(card, text="Student name", style="Body.TLabel").pack(anchor="w", pady=(0, 8))
        self.name_var = tk.StringVar()
        entry = ttk.Entry(card, textvariable=self.name_var, width=42)
        entry.pack(anchor="w", ipady=3)
        entry.focus_set()
        entry.bind("<Return>", lambda _event: self._start_quiz())
        ttk.Button(card, text="Start Quiz  →", style="Primary.TButton",
                   command=self._start_quiz).pack(anchor="w", pady=(24, 10))
        ttk.Label(card, text="Built with Python, Tkinter and JSON.", style="Muted.TLabel").pack(anchor="w", pady=(12, 0))

    def _start_quiz(self):
        name = self.name_var.get().strip()
        if not name:
            messagebox.showwarning("Name required", "Please enter your name before starting.")
            return
        try:
            self.questions = load_questions(self.question_file)
        except QuestionDataError as exc:
            messagebox.showerror("Question bank error", str(exc))
            return
        self.student_name = name
        self.answers = {}
        self.current_index = 0
        self._show_question()

    def _show_question(self):
        question = self.questions[self.current_index]
        outer = self._page("Knowledge Check", f"Student: {self.student_name}")
        top = ttk.Frame(outer)
        top.pack(fill="x", pady=(0, 14))
        ttk.Label(top, text=f"QUESTION {self.current_index + 1:02d} OF {len(self.questions)}",
                  style="Subtitle.TLabel").pack(side="left")
        ttk.Label(top, text=question.get("difficulty", "General").title(),
                  style="Subtitle.TLabel").pack(side="right")
        progress = ttk.Progressbar(outer, style="Quiz.Horizontal.TProgressbar",
                                   maximum=len(self.questions), value=self.current_index + 1)
        progress.pack(fill="x", pady=(0, 18))
        card = self._card(outer, padding=30)
        ttk.Label(card, text=question.get("category", "General").upper(),
                  style="Muted.TLabel").pack(anchor="w", pady=(0, 10))
        ttk.Label(card, text=question["question"], style="CardTitle.TLabel",
                  wraplength=730, justify="left").pack(anchor="w", pady=(0, 22))
        self.answer_var = tk.StringVar(value=self.answers.get(question["id"], ""))
        for key in ("A", "B", "C", "D"):
            ttk.Radiobutton(card, text=f"{key}.  {question['options'][key]}",
                            variable=self.answer_var, value=key).pack(anchor="w", fill="x", pady=3)
        nav = ttk.Frame(card, style="Card.TFrame")
        nav.pack(fill="x", side="bottom", pady=(24, 0))
        if self.current_index > 0:
            ttk.Button(nav, text="← Previous", style="Secondary.TButton",
                       command=self._previous).pack(side="left")
        ttk.Button(nav, text="Next →" if self.current_index < len(self.questions) - 1 else "Submit Quiz",
                   style="Primary.TButton", command=self._next).pack(side="right")
        if self.answers.get(question["id"]):
            ttk.Label(nav, text="Answer saved", style="Muted.TLabel").pack(side="right", padx=12)

    def _save_current_answer(self):
        question = self.questions[self.current_index]
        selected = self.answer_var.get()
        if selected in {"A", "B", "C", "D"}:
            self.answers[question["id"]] = selected
        else:
            self.answers.pop(question["id"], None)

    def _previous(self):
        self._save_current_answer()
        self.current_index -= 1
        self._show_question()

    def _next(self):
        self._save_current_answer()
        if self.current_index < len(self.questions) - 1:
            self.current_index += 1
            self._show_question()
            return
        unanswered = len(self.questions) - len(self.answers)
        if unanswered and not messagebox.askyesno(
            "Unanswered questions", f"You have {unanswered} unanswered question(s). Submit anyway?"
        ):
            return
        self._finish_quiz()

    def _finish_quiz(self):
        score, review = evaluate_answers(self.questions, self.answers)
        stats = calculate_score(len(self.questions), score)
        self.review_data = review
        self.result_data = {**stats, "performance": get_performance(stats["percentage"])}
        self._show_result()

    def _show_result(self):
        data = self.result_data
        outer = self._page("Quiz Completed", f"Well done, {self.student_name}. Here is your performance summary.")
        card = self._card(outer, padding=30)
        score_box = tk.Frame(card, bg=NAVY, padx=24, pady=20)
        score_box.pack(fill="x", pady=(0, 22))
        tk.Label(score_box, text="YOUR FINAL SCORE", bg=NAVY, fg="#C7D2FE",
                 font=("Segoe UI", 10, "bold")).pack()
        tk.Label(score_box, text=f"{data['correct']} / {data['total']}", bg=NAVY, fg=WHITE,
                 font=("Segoe UI", 32, "bold")).pack(pady=4)
        tk.Label(score_box, text=f"{data['percentage']:.1f}%  •  {data['performance']}",
                 bg=NAVY, fg="#8FE3D7", font=("Segoe UI", 12, "bold")).pack()
        grid = ttk.Frame(card, style="Card.TFrame")
        grid.pack(fill="x", pady=(0, 18))
        metrics = [
            ("Student", self.student_name),
            ("Total questions", str(data["total"])),
            ("Correct answers", str(data["correct"])),
            ("Incorrect / unanswered", str(data["wrong"])),
        ]
        for i, (label, value) in enumerate(metrics):
            cell = ttk.Frame(grid, style="Card.TFrame", padding=10)
            cell.grid(row=i // 2, column=i % 2, sticky="ew", padx=5, pady=5)
            ttk.Label(cell, text=label, style="Muted.TLabel").pack(anchor="w")
            ttk.Label(cell, text=value, style="CardTitle.TLabel").pack(anchor="w", pady=(3, 0))
        grid.columnconfigure(0, weight=1)
        grid.columnconfigure(1, weight=1)
        ttk.Label(card, text="Performance guide: Excellent ≥80%  |  Good ≥60%  |  Average ≥40%",
                  style="Muted.TLabel").pack(anchor="w", pady=(0, 18))
        buttons = ttk.Frame(card, style="Card.TFrame")
        buttons.pack(fill="x")
        ttk.Button(buttons, text="Review Answers", style="Secondary.TButton",
                   command=self._show_review).pack(side="left")
        ttk.Button(buttons, text="Restart Quiz", style="Primary.TButton",
                   command=self._show_welcome).pack(side="right")

    def _show_review(self):
        outer = self._page("Answer Review", f"Review the answers submitted by {self.student_name}.")
        canvas = tk.Canvas(outer, bg=BG, highlightthickness=0)
        scrollbar = ttk.Scrollbar(outer, orient="vertical", command=canvas.yview)
        content = ttk.Frame(canvas)
        content.bind("<Configure>", lambda _e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas_window = canvas.create_window((0, 0), window=content, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        canvas.bind("<Configure>", lambda event: canvas.itemconfigure(canvas_window, width=event.width))
        for item in self.review_data:
            card = ttk.Frame(content, style="Card.TFrame", padding=18)
            card.pack(fill="x", pady=(0, 12))
            status = "Correct" if item["correct"] else "Incorrect"
            status_color = TEAL if item["correct"] else "#C2413B"
            tk.Label(card, text=f"QUESTION {item['id']}  •  {status}", bg=WHITE,
                     fg=status_color, font=("Segoe UI", 10, "bold")).pack(anchor="w")
            ttk.Label(card, text=item["question"], style="CardTitle.TLabel",
                      wraplength=760, justify="left").pack(anchor="w", pady=(7, 8))
            selected = item["selected"] or "Not answered"
            selected_text = item["options"].get(selected, selected)
            correct_text = item["options"][item["correct_answer"]]
            ttk.Label(card, text=f"Your answer: {selected} — {selected_text}",
                      style="Body.TLabel", wraplength=760).pack(anchor="w")
            ttk.Label(card, text=f"Correct answer: {item['correct_answer']} — {correct_text}",
                      style="Muted.TLabel", wraplength=760).pack(anchor="w", pady=(4, 0))
        ttk.Button(outer, text="Back to Results", style="Primary.TButton",
                   command=self._show_result).pack(anchor="e", pady=(14, 0))
