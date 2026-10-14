# // --- start AI code ---
import json

from expr import Binary, Grouping, Literal, Unary


class AstPrinter:
    def print(self, expression):
        if isinstance(expression, Literal):
            if isinstance(expression.value, bool):
                return "true" if expression.value else "false"
            if isinstance(expression.value, str):
                return json.dumps(expression.value, ensure_ascii=False)
            return str(expression.value)

        if isinstance(expression, Unary):
            return self.parenthesize(
                expression.operator.lexeme, expression.right
            )

        if isinstance(expression, Binary):
            return self.parenthesize(
                expression.operator.lexeme,
                expression.left,
                expression.right,
            )

        if isinstance(expression, Grouping):
            return self.parenthesize("group", expression.expression)

        raise TypeError("Unknown expression type.")

    def parenthesize(self, name, *expressions):
        parts = [name]
        for expression in expressions:
            parts.append(self.print(expression))
        return "(" + " ".join(parts) + ")"

# // --- end AI code ---