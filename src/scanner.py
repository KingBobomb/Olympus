# // --- start AI code ---
from token_type import TokenType
from olympus_token import Token


class Scanner:
    def __init__(self, source):
        self.source = source
        self.tokens = []
        self.errors = []
        self.start = 0
        self.current = 0
        self.line = 1
        self.start_line = 1

    def is_at_end(self):
        return self.current >= len(self.source)

    def advance(self):
        character = self.source[self.current]
        self.current += 1
        return character

    def peek(self):
        if self.is_at_end():
            return "\0"
        return self.source[self.current]

    def match(self, expected):
        if self.is_at_end():
            return False
        if self.source[self.current] != expected:
            return False

        self.current += 1
        return True

    def add_token(self, token_type, literal=None):
        lexeme = self.source[self.start:self.current]
        token = Token(token_type, lexeme, literal, self.start_line)
        self.tokens.append(token)

    def peek_next(self):
        if self.current + 1 >= len(self.source):
            return "\0"
        return self.source[self.current + 1]

    def is_digit(self, character):
        return "0" <= character <= "9"
    
    def is_alpha(self, character):
        return (
            "a" <= character <= "z"
            or "A" <= character <= "Z"
            or character == "_"
        )

    def identifier(self):
        while self.is_alpha(self.peek()) or self.is_digit(self.peek()):
            self.advance()

        keywords = {
            "forge": TokenType.FORGE,
            "proclaim": TokenType.PROCLAIM,
            "fate": TokenType.FATE,
            "otherwise": TokenType.OTHERWISE,
            "cycle": TokenType.CYCLE,
            "true": TokenType.TRUE,
            "false": TokenType.FALSE,
        }

        text = self.source[self.start:self.current]
        token_type = keywords.get(text, TokenType.IDENTIFIER)
        self.add_token(token_type)

    def number(self):
        while self.is_digit(self.peek()):
            self.advance()

        if self.peek() == "." and self.is_digit(self.peek_next()):
            self.advance()

            while self.is_digit(self.peek()):
                self.advance()

        value = float(self.source[self.start:self.current])
        self.add_token(TokenType.NUMBER, value)

    def string(self):
        while self.peek() != '"' and not self.is_at_end():
            if self.peek() == "\n":
                self.line += 1
            self.advance()

        if self.is_at_end():
            self.errors.append(
                f"[line {self.start_line}] Error: Unterminated string."
            )
            return

        self.advance()
        value = self.source[self.start + 1:self.current - 1]
        self.add_token(TokenType.STRING, value)

    def scan_tokens(self):
        while not self.is_at_end():
            self.start = self.current
            self.start_line = self.line
            self.scan_token()

        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens

    def scan_token(self):
        character = self.advance()

        single_char_tokens = {
            "(": TokenType.LEFT_PAREN,
            ")": TokenType.RIGHT_PAREN,
            "{": TokenType.LEFT_BRACE,
            "}": TokenType.RIGHT_BRACE,
            ",": TokenType.COMMA,
            ".": TokenType.DOT,
            ";": TokenType.SEMICOLON,
            "+": TokenType.PLUS,
            "-": TokenType.MINUS,
            "*": TokenType.STAR,
        }

        if character in single_char_tokens:
            self.add_token(single_char_tokens[character])
        elif character == "/":
            if self.match("/"):
                while self.peek() != "\n" and not self.is_at_end():
                    self.advance()
            else:
                self.add_token(TokenType.SLASH)
        elif character == "!":
            self.add_token(
                TokenType.BANG_EQUAL if self.match("=") else TokenType.BANG
            )
        elif character == "=":
            self.add_token(
                TokenType.EQUAL_EQUAL if self.match("=") else TokenType.EQUAL
            )
        elif character == "<":
            self.add_token(
                TokenType.LESS_EQUAL if self.match("=") else TokenType.LESS
            )
        elif character == ">":
            self.add_token(
                TokenType.GREATER_EQUAL if self.match("=") else TokenType.GREATER
            )
        elif character == '"':
            self.string()
        elif self.is_digit(character):
            self.number()
        elif self.is_alpha(character):
            self.identifier()
        elif character in " \r\t":
            pass
        elif character == "\n":
            self.line += 1
        else:
            self.errors.append(
                f"[line {self.start_line}] Error: Unexpected character {character!r}."
            )
# // --- end AI code ---