"""Run automated unit tests and Python syntax compilation."""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def main():
    files = [ROOT / "main.py", ROOT / "gui.py", ROOT / "quiz_logic.py",
             ROOT / "score.py", ROOT / "result.py"]
    compile_errors = []
    for path in files:
        try:
            compile(path.read_text(encoding="utf-8"), str(path), "exec")
        except SyntaxError as exc:
            compile_errors.append(f"{path.name}: {exc}")

    if compile_errors:
        print("SYNTAX CHECK: FAIL")
        print("\\n".join(compile_errors))
        return 1

    print(f"SYNTAX CHECK: PASS ({len(files)} Python files)")
    result = subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"],
        cwd=ROOT
    )
    print("UNIT TESTS: " + ("PASS" if result.returncode == 0 else "FAIL"))
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
