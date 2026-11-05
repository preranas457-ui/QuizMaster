# Student Quiz Application

A desktop GUI quiz application built with Python, Tkinter/ttk and a JSON question bank.

## Features
- Student name entry and welcome screen
- 18 multiple-choice questions loaded from `questions.json`
- Previous/Next navigation and saved selections
- Progress indicator
- Confirmation before submitting unanswered questions
- Automatic score, percentage and performance evaluation
- Answer review screen
- Restart option

## Requirements
- Python 3.9 or newer recommended
- Tkinter (normally included with standard Python installations)

No third-party Python packages are required.

## Run the application
1. Extract the project folder.
2. Open the folder in VS Code.
3. Open the terminal in the project folder.
4. Run: `python main.py` (Windows users can also try `py main.py`).

If Tkinter is missing on Linux, install the system package for your distribution (for example, `python3-tk`).

## Run the audit tests
Run: `python -m unittest discover -s tests -v`

## Project structure
- `main.py`: application entry point
- `gui.py`: Tkinter user interface
- `quiz_logic.py`: question loading, validation and answer evaluation
- `score.py`: score calculation
- `result.py`: performance classification
- `questions.json`: editable question bank
- `tests/`: automated logic and data-validation tests

## Performance scale
- 80–100%: Excellent
- 60–79.99%: Good
- 40–59.99%: Average
- Below 40%: Needs Improvement

## Notes
The application currently keeps results in memory for the current session. It does not save student records to a database or file.
