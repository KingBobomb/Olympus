# // --- start AI code ---
import sys
from pathlib import Path

project_folder = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(project_folder / "src"))

from scanner import Scanner

sources= [
    "",
    " \t\r\n ",
    '"Mount\nOlympus"\n+',
    '"// Zeus"',
]

for source in sources:
    print(f"\nInput: {source!r}")
    scanner = Scanner(source)

    for token in scanner.scan_tokens():
        print(f"{token} (line {token.line})")

    for error in scanner.errors:
        print(error)
# // --- end AI code ---