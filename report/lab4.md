# Lab 4: Statements
Name: Korey
Language: Olympus

## What the program does

This lab adds statements to Olympus. Before, the program could only
read one expression. Now it can read a whole program made of statements
and run them.

There are two kinds of statements. An expression statement is just an
expression with a semicolon at the end, like 4 + 2; and it gets
calculated but nothing is printed. A print statement uses the keyword
proclaim, like proclaim 1 + 2; and it prints the value.

The scanner makes the tokens, the parser turns them into a list of
statements, and the interpreter runs them in order.

## Grammar

I added these rules on top of the expression grammar from Lab 3:

```
program    → statement* EOF ;
statement  → printStmt | exprStmt ;
printStmt  → "proclaim" expression ";" ;
exprStmt   → expression ";" ;
```

I also added void to primary. void means "no value" and works like
nil in Lox.

## What I changed

I added a new file, src/stmt.py, with the Expression and Print
statement classes. The parser now returns a list of statements
instead of one expression. I added interpret and execute to the
interpreter, and main.py now runs the program instead of printing
the AST. The scanner now knows the void keyword.

I kept the old Lab 3 parse in a method called parse_expression so
the Lab 3 test script still works.

## Panic-mode error recovery

In Lab 3 the parser stopped at the first syntax error. Now it saves
the error and keeps going. After an error it skips tokens until it
gets past a semicolon or reaches a keyword that starts a statement
(forge, proclaim, fate, or cycle). Then it keeps parsing from there.
This way one run can show more than one syntax error.

If there are any syntax errors, the program prints them all and does
not run anything.

## Runtime errors

The interpreter also reports runtime errors, like dividing by zero or
using a string where a number is needed. The program stops at the
first runtime error.

## How to run

I used Python 3 on Fedora KDE. Run these from the main Olympus folder.

To run a file: python3 src/main.py test/lab4/valid.olympus

To start the prompt: python3 src/main.py (Ctrl+D to exit)

To run my extra tests: python3 test/lab4/test_statements.py

## Test 1

File: test/lab4/errors.olympus

```
"one"
true;
proclaim 2 +
```

Output:

```
[line 2] Error at 'true': Expected ';' after expression.
[line 4] Error at end: Expected expression.
```

The first line is missing a semicolon, so the error shows up at true.
The parser skips to the semicolon after true and keeps going. Then
proclaim 2 + is missing the number after the +, so it gives a second
error. It says line 4 because the file ends with a newline.

Both errors show up in one run, so the error recovery works.

## Test 2

File: test/lab4/valid.olympus

```
4 + 2;
proclaim "one";
proclaim true;
proclaim 1 + 2;
proclaim void;
```

Output:

```
one
true
3
void
```

4 + 2; doesn't print anything because it is not a proclaim statement.
Every proclaim prints one line.

## Extra tests

I also wrote test/lab4/test_statements.py with more inputs. Some of
the results:

proclaim 10 + 2 * 3; printed 16 and proclaim (10 + 2) * 3; printed 36.

proclaim void == void; printed true.

proclaim 1 printed: [line 1] Error at end: Expected ';' after value.

With three lines (1 2; then proclaim 3 * ; then proclaim 4;) it showed
two errors, one on line 1 and one on line 2. This shows the parser
keeps going after an error.

proclaim 1 / 0; printed: Runtime error: Division by zero.

proclaim "a" - 1; printed: Runtime error: Operand must be a number.

All the tests gave the output I expected.

## Limitations

Only expression statements and print statements work right now.
forge, fate, and cycle are keywords but they don't do anything yet.
There are no variables, blocks, or and/or.

## AI help

I used Claude to help write the statement classes, the parser
changes, error recovery, and the tests. The AI code is marked with start and end AI code
comments.
