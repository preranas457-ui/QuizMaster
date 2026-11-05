"""Application entry point."""
import tkinter as tk
from tkinter import messagebox
from gui import QuizApp


def main():
    try:
        app = QuizApp()
        app.mainloop()
    except tk.TclError as exc:
        messagebox.showerror(
            "Unable to start application",
            "Tkinter could not open a desktop window. Make sure you are running this "
            "program on a computer with a graphical desktop and Tk support.\\n\\n"
            f"Details: {exc}"
        )
        raise


if __name__ == "__main__":
    main()
