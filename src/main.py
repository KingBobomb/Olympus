# // --- start AI code ---
import sys
from pathlib import Path

from scanner import Scanner


class Olympus:
    def run(self, source):
        scanner = Scanner(source)

        for token in scanner.scan_tokens():
            print(token)

        for error in scanner.errors:
            print(error, file=sys.stderr)

        return not scanner.errors

    def run_file(self, filename):
        try:
            source = Path(filename).read_text(encoding="utf-8")
        except (OSError, UnicodeError) as error:
            print(f"Could not read file: {error}", file=sys.stderr)
            return 1

        return 0 if self.run(source) else 1
    
    def run_prompt(self):
        print("Olympus scanner. Press Ctrl+D to exit.")

        while True:
            try:
                source = input("olympus> ")
            except (EOFError, KeyboardInterrupt):
                print()
                return 0

            self.run(source)

def main():
    olympus = Olympus()

    if len(sys.argv) > 2:
        print("Usage: python3 src/main.py [source-file]", file=sys.stderr)
        return 1

    if len(sys.argv) == 2:
        return olympus.run_file(sys.argv[1])

    return olympus.run_prompt()


if __name__ == "__main__":
    sys.exit(main())
# // --- end AI code ---