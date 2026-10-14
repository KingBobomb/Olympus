# // --- start AI code ---
import sys
from pathlib import Path

project_folder = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(project_folder / "src"))

from ast_printer import AstPrinter
from expr import Binary, Grouping, Literal, Unary
from olympus_token import Token
from token_type import TokenType

expression = Binary(
    Unary(
        Token(TokenType.MINUS, "-", None, 1),
        Literal(123),
    ),
    Token(TokenType.STAR, "*", None, 1),
    Grouping(Literal(45.67)),
)

printer = AstPrinter()
print(printer.print(expression))

expression2 = Unary(
    Token(TokenType.BANG, "!", None, 1),
    Grouping(
        Binary(
            Literal(True),
            Token(TokenType.EQUAL_EQUAL, "==", None, 1),
            Literal(False),
        )
    ),
)

print(printer.print(expression2))

expression3 = Binary(
    Literal("Zeus"),
    Token(TokenType.PLUS, "+", None, 1),
    Grouping(
        Binary(
            Literal(" rules"),
            Token(TokenType.PLUS, "+", None, 1),
            Literal(" Olympus"),
        )
    ),
)

print(printer.print(expression3))

operators = [
    (TokenType.MINUS, "-"),
    (TokenType.SLASH, "/"),
    (TokenType.BANG_EQUAL, "!="),
    (TokenType.LESS, "<"),
    (TokenType.LESS_EQUAL, "<="),
    (TokenType.GREATER, ">"),
    (TokenType.GREATER_EQUAL, ">="),
]

for token_type, symbol in operators:
    expression = Binary(
        Literal(10),
        Token(token_type, symbol, None, 1),
        Literal(2),
    )
    print(printer.print(expression))

    edge_cases = [
    Literal(0),
    Literal(""),
    Grouping(Grouping(Literal(5))),
    Unary(
        Token(TokenType.MINUS, "-", None, 1),
        Unary(
            Token(TokenType.MINUS, "-", None, 1),
            Literal(3),
        ),
    ),
]

for expression in edge_cases:
    print(printer.print(expression))

# // --- end AI code ---