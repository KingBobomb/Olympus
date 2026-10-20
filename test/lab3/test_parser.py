# // --- start AI code ---
import sys
from pathlib import Path

project_folder = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(project_folder / "src"))

from ast_printer import AstPrinter
from parser import Parser, ParseError
from scanner import Scanner

sources = [
    "(1 + 2",
    "1 +",
    "* 2",
    "1 2",
    "1 + )",
    "",
    "1 +\n)",
    "1 + @ 2",
    '"Zeus',
]

for source in sources:
    print(f"Input: {source}")
    scanner = Scanner(source)
    tokens = scanner.scan_tokens()

    if scanner.errors:
        for error in scanner.errors:
            print(error)
    else:
        try:
            expression = Parser(tokens).parse()
            print(AstPrinter().print(expression))
        except ParseError as error:
            print(error)

    print()

# // --- end AI code ---