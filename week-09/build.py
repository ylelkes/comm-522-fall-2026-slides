"""Build all Week 9 slide views and the instructor guide from index.qmd."""
from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parent.parent
subprocess.run([sys.executable, str(root / "week-09/sync-notes.py")], cwd=root, check=True)
for source in ("index.qmd", "presenter.qmd", "with-notes.qmd", "instructor-notes.qmd"):
    subprocess.run(["quarto", "render", f"week-09/{source}"], cwd=root, check=True)
subprocess.run([sys.executable, str(root / "week-09/finalize-student.py")], cwd=root, check=True)
