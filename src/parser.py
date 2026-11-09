# // --- start AI code ---
from expr import Binary, Grouping, Literal, Unary
from stmt import Expression, Print
from token_type import TokenType


class ParseError(Exception):
    pass


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0
        self.errors = []

    def peek(self):
        return self.tokens[self.current]

    def previous(self):
        return self.tokens[self.current - 1]

    def is_at_end(self):
        return self.peek().token_type == TokenType.EOF

    def advance(self):
        if not self.is_at_end():
            self.current += 1
        return self.previous()

    def check(self, token_type):
        return self.peek().token_type == token_type

    def match(self, *token_types):
        for token_type in token_types:
            if self.check(token_type):
                self.advance()
                return True
        return False

    def error(self, token, message):
        location = (
            "at end" if token.token_type == TokenType.EOF
            else f"at {token.lexeme!r}"
        )
        return ParseError(
            f"[line {token.line}] Error {location}: {message}"
        )

    def consume(self, token_type, message):
        if self.check(token_type):
            return self.advance()
        raise self.error(self.peek(), message)
    
    def parse(self):
        statements = []

        while not self.is_at_end():
            statement = self.declaration()

            if statement is not None:
                statements.append(statement)

        return statements

    def parse_expression(self):
        expression = self.expression()

        if not self.is_at_end():
            raise self.error(
                self.peek(), "Unexpected token after expression."
            )

        return expression

    def declaration(self):
        try:
            return self.statement()
        except ParseError as error:
            self.errors.append(error)
            self.synchronize()
            return None

    def statement(self):
        if self.match(TokenType.PROCLAIM):
            return self.print_statement()

        return self.expression_statement()

    def print_statement(self):
        value = self.expression()
        self.consume(TokenType.SEMICOLON, "Expected ';' after value.")
        return Print(value)

    def expression_statement(self):
        expression = self.expression()
        self.consume(
            TokenType.SEMICOLON, "Expected ';' after expression."
        )
        return Expression(expression)

    def synchronize(self):
        self.advance()

        while not self.is_at_end():
            if self.previous().token_type == TokenType.SEMICOLON:
                return

            if self.peek().token_type in (
                TokenType.FORGE,
                TokenType.PROCLAIM,
                TokenType.FATE,
                TokenType.CYCLE,
            ):
                return

            self.advance()

    def expression(self):
        return self.equality()

    def equality(self):
        expression = self.comparison()

        while self.match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            operator = self.previous()
            right = self.comparison()
            expression = Binary(expression, operator, right)

        return expression

    def comparison(self):
        expression = self.term()

        while self.match(
            TokenType.GREATER,
            TokenType.GREATER_EQUAL,
            TokenType.LESS,
            TokenType.LESS_EQUAL,
        ):
            operator = self.previous()
            right = self.term()
            expression = Binary(expression, operator, right)

        return expression

    def term(self):
        expression = self.factor()

        while self.match(TokenType.MINUS, TokenType.PLUS):
            operator = self.previous()
            right = self.factor()
            expression = Binary(expression, operator, right)

        return expression

    def factor(self):
        expression = self.unary()

        while self.match(TokenType.SLASH, TokenType.STAR):
            operator = self.previous()
            right = self.unary()
            expression = Binary(expression, operator, right)

        return expression

    def unary(self):
        if self.match(TokenType.BANG, TokenType.MINUS):
            operator = self.previous()
            right = self.unary()
            return Unary(operator, right)

        return self.primary()

    def primary(self):
        if self.match(TokenType.FALSE):
            return Literal(False)

        if self.match(TokenType.TRUE):
            return Literal(True)

        if self.match(TokenType.VOID):
            return Literal(None)

        if self.match(TokenType.NUMBER, TokenType.STRING):
            return Literal(self.previous().literal)

        if self.match(TokenType.LEFT_PAREN):
            expression = self.expression()
            self.consume(
                TokenType.RIGHT_PAREN,
                "Expected ')' after expression.",
            )
            return Grouping(expression)

        raise self.error(self.peek(), "Expected expression.")

# // --- end AI code ---