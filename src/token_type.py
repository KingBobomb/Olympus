from enum import Enum, auto


class TokenType(Enum):
    # Punctuation
    LEFT_PAREN = auto()
    RIGHT_PAREN = auto()
    LEFT_BRACE = auto()
    RIGHT_BRACE = auto()
    COMMA = auto()
    DOT = auto()
    SEMICOLON = auto()

    # Operators
    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    SLASH = auto()
    BANG = auto()
    BANG_EQUAL = auto()
    EQUAL = auto()
    EQUAL_EQUAL = auto()
    LESS = auto()
    LESS_EQUAL = auto()
    GREATER = auto()
    GREATER_EQUAL = auto()

    # Names and values
    IDENTIFIER = auto()
    STRING = auto()
    NUMBER = auto()

    # Olympus keywords
    FORGE = auto()
    PROCLAIM = auto()
    FATE = auto()
    OTHERWISE = auto()
    CYCLE = auto()
    TRUE = auto()
    FALSE = auto()

    EOF = auto()