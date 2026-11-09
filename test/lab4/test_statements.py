# // --- start AI code ---
import sys
from pathlib import Path

project_folder = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(project_folder / "src"))

from Interpreter import Interpreter
from parser import Parser
from scanner import Scanner

sys.stdout.reconfigure(line_buffering=True)

sources = [
    'proclaim "Zeus";',
    "proclaim 10 + 2 * 3;",
    "proclaim (10 + 2) * 3;",
    "proclaim 1 == 1;",
    "proclaim !void;",
    "proclaim void == void;",
    "4 + 2;",
    "proclaim 1",
    "proclaim 1 +;\nproclaim 2;",
    "1 2;\nproclaim 3 * ;\nproclaim 4;",
    "proclaim ) ;\nproclaim (1 + 2;\nproclaim 5;",
    "proclaim 1 / 0;",
    'proclaim "a" - 1;',
    "",
]

for source in sources:
    print(f"Input: {source!r}")
    scanner = Scanner(source)
    tokens = scanner.scan_tokens()

    if scanner.errors:
        for error in scanner.errors:
            print(error)
    else:
        parser = Parser(tokens)
        statements = parser.parse()

        if parser.errors:
            for error in parser.errors:
                print(error)
        else:
            Interpreter().interpret(statements)

    print()

# // --- end AI code ---
