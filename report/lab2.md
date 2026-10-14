# Lab 2: AST Printer
Name: Korey
Language: Olympus

## What this lab does

I added classes that store expressions as trees.
The printer shows the trees using parentheses.
It prints the structure without solving the expression.

## Grammar

```text
expression → equality ;
equality   → comparison ( ( "!=" | "==" ) comparison )* ;
comparison → term ( ( ">" | ">=" | "<" | "<=" ) term )* ;
term       → factor ( ( "-" | "+" ) factor )* ;
factor     → unary ( ( "/" | "*" ) unary )* ;
unary      → ( "!" | "-" ) unary | primary ;
primary    → NUMBER | STRING | "true" | "false"
           | "(" expression ")" ;
```

| means "or." * means something can repeat zero or more times.
NUMBER and STRING use the rules from Lab 1.

The expression types are numbers, strings, and true/false.
The unary operators are ! and -.
The binary operators are +, -, *, /, ==, !=, <, <=, >, and >=.

Unary operators come first, then multiplication and division,
then addition and subtraction, then comparisons, then equality.
Binary operators at the same level go from left to right.
Parentheses can change the order.

## Choices I made

I kept the expression operators similar to Lox.
I used Literal, Unary, Binary, and Grouping classes.

I left out nil and variable expressions for this version.
Keywords like forge and fate are for statements, so they
are not included in this expression grammar.

My printer checks the class using isinstance instead of
using Lox's visitor pattern.
Strings keep quotation marks in the output.
Boolean values print as true and false.

## Files

src/expr.py contains the expression classes.
src/ast_printer.py contains the printer.
test/lab2/test_ast.py builds and prints the test trees.

I reused Token and TokenType from Lab 1.

Literal stores a value.
Unary stores an operator and one expression.
Binary stores a left expression, an operator, and a right expression.
Grouping stores the expression inside the parentheses.

## How to run

I used Python 3 on Fedora KDE.
No extra packages are needed. The json module used by the printer
comes with Python.

From the Olympus folder, run:

```bash
python3 test/lab2/test_ast.py
```

This prints all the test trees. I checked the output manually
against the expected results.

## Tests

All tests are in test/lab2/test_ast.py.
The Token objects store the operator type, text, literal value,
and line number.

### Test 1: Numbers and grouping

Purpose: Check Binary, Unary, Literal, and Grouping together.

Tree:

```python
Binary(
    Unary(
        Token(TokenType.MINUS, "-", None, 1),
        Literal(123),
    ),
    Token(TokenType.STAR, "*", None, 1),
    Grouping(Literal(45.67)),
)
```

Expected:
```text
(* (- 123) (group 45.67))
```

Actual:
```text
(* (- 123) (group 45.67))
```

Result: Passed.

### Test 2: Boolean values

Purpose: Check true, false, !, and == in a nested tree.

Tree:

```python
Unary(
    Token(TokenType.BANG, "!", None, 1),
    Grouping(
        Binary(
            Literal(True),
            Token(TokenType.EQUAL_EQUAL, "==", None, 1),
            Literal(False),
        )
    ),
)
```

Expected:
```text
(! (group (== true false)))
```

Actual:
```text
(! (group (== true false)))
```

Result: Passed.

### Test 3: Strings

Purpose: Check strings, +, and a binary expression inside a group.

Tree:

```python
Binary(
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
```

Expected:
```text
(+ "Zeus" (group (+ " rules" " Olympus")))
```

Actual:
```text
(+ "Zeus" (group (+ " rules" " Olympus")))
```

Result: Passed.

### Test 4: Other operators

Purpose: Check every remaining binary operator.

Trees were built with this code:

```python
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
```

Expected:
```text
(- 10 2)
(/ 10 2)
(!= 10 2)
(< 10 2)
(<= 10 2)
(> 10 2)
(>= 10 2)
```

Actual:
```text
(- 10 2)
(/ 10 2)
(!= 10 2)
(< 10 2)
(<= 10 2)
(> 10 2)
(>= 10 2)
```

Result: All seven passed.

### Test 5: Small edge cases

Purpose: Check zero, an empty string, nested groups,
and nested unary expressions.

Trees:

```python
Literal(0)

Literal("")

Grouping(Grouping(Literal(5)))

Unary(
    Token(TokenType.MINUS, "-", None, 1),
    Unary(
        Token(TokenType.MINUS, "-", None, 1),
        Literal(3),
    ),
)
```

Expected:
```text
0
""
(group (group 5))
(- (- 3))
```

Actual:
```text
0
""
(group (group 5))
(- (- 3))
```

Result: All four passed.

## Limitations

The trees must be built directly in Python.
The program does not parse source code or calculate results.
It does not check whether operators are used with the right types.

All documented tests passed. I have no known failing tests.
I am not requesting extra credit.

## AI help

I used ChatGPT to help write the classes, printer, and tests.