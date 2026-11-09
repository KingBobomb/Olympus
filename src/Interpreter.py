# // --- start AI code ---

import sys

from expr import Binary, Grouping, Literal, Unary
from stmt import Expression, Print
from token_type import TokenType


class OlympusRuntimeError(Exception):
    pass


class Interpreter:
    def interpret(self, statements):
        try:
            for statement in statements:
                self.execute(statement)
        except OlympusRuntimeError as error:
            print(f"Runtime error: {error}", file=sys.stderr)
            return False

        return True

    def execute(self, statement):
        if isinstance(statement, Print):
            value = self.evaluate(statement.expression)
            print(self.stringify(value))
            return

        if isinstance(statement, Expression):
            self.evaluate(statement.expression)
            return

        raise OlympusRuntimeError("Unknown statement.")

    def evaluate(self, expression):
        if isinstance(expression, Literal):
            return expression.value

        if isinstance(expression, Grouping):
            return self.evaluate(expression.expression)

        if isinstance(expression, Unary):
            right = self.evaluate(expression.right)

            if expression.operator.token_type == TokenType.MINUS:
                return -self.as_number(right)

            if expression.operator.token_type == TokenType.BANG:
                return not self.is_truthy(right)

        if isinstance(expression, Binary):
            left = self.evaluate(expression.left)
            right = self.evaluate(expression.right)
            operator = expression.operator.token_type

            if operator == TokenType.PLUS:
                return self.as_number(left) + self.as_number(right)

            if operator == TokenType.MINUS:
                return self.as_number(left) - self.as_number(right)

            if operator == TokenType.STAR:
                return self.as_number(left) * self.as_number(right)

            if operator == TokenType.SLASH:
                divisor = self.as_number(right)

                if divisor == 0:
                    raise OlympusRuntimeError("Division by zero.")

                return self.as_number(left) / divisor

            if operator == TokenType.GREATER:
                return self.as_number(left) > self.as_number(right)

            if operator == TokenType.GREATER_EQUAL:
                return self.as_number(left) >= self.as_number(right)

            if operator == TokenType.LESS:
                return self.as_number(left) < self.as_number(right)

            if operator == TokenType.LESS_EQUAL:
                return self.as_number(left) <= self.as_number(right)

            if operator == TokenType.EQUAL_EQUAL:
                return self.are_equal(left, right)

            if operator == TokenType.BANG_EQUAL:
                return not self.are_equal(left, right)

        raise OlympusRuntimeError("Unknown expression.")

    def as_number(self, value):
        if isinstance(value, bool):
            return 1 if value else 0

        if isinstance(value, (int, float)):
            return value

        raise OlympusRuntimeError("Operand must be a number.")

    def is_truthy(self, value):
        if isinstance(value, bool):
            return value

        if isinstance(value, (int, float)):
            return value != 0

        return bool(value)

    def are_equal(self, left, right):
        numeric_types = (bool, int, float)

        if isinstance(left, numeric_types) and isinstance(right, numeric_types):
            return self.as_number(left) == self.as_number(right)

        return left == right

    def stringify(self, value):
        if value is None:
            return "void"

        if value is True:
            return "true"

        if value is False:
            return "false"

        if isinstance(value, float) and value.is_integer():
            return str(int(value))

        return str(value)


# // --- end AI code ---