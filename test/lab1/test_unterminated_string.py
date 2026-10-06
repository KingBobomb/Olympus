# // --- start AI code ---
import sys
from pathlib import Path

project_folder = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(project_folder / "src"))

from scanner import Scanner

source = '\n"Zeus'
scanner = Scanner(source)

for token in scanner.scan_tokens():
    print(token)

for error in scanner.errors:
    print(error)
# // --- end AI code ---