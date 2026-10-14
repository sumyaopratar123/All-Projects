from pathlib import Path
from datetime import datetime

project_dir = Path(__file__).resolve().parent
file = project_dir / "automation-demo.txt"

with file.open("a", encoding="utf-8") as f:
    f.write(f"Python Git automation demo: {datetime.now().isoformat()}\n")

print(f"Demo successful! File: {file}")
