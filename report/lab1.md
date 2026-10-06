# CIS 343 Lab 1: Scanning
Author: Korey
Language: Olympus 

## Overview

Olympus is a Greek mythology themed language. This scanner is programmed in python. The scanner converts source text into tokens and reports errors.
                                                       
Each token stores its type, lexeme, literal value, and starting line. The program supports source files and a prompt.

## Keywords

(Olympus keyword | Meaning)
(forge | Declare a variable)
(proclaim | Print a value)
(fate | Begin a conditional)
(otherwise | Other conditional branch)
(cycle | while loop)
(true | Boolean true)
(false | Boolean false)

This lab knows the keywords but this lab does not execute statements.

Olympus replaces var, print, if, else, and while keywords with the theme. It keeps true and false. Lox keywords are identifiers.

## Lexical rules

These expressions describe valid tokens.
The scanner rules are reading characters directly.

( Token | Regular expression )
( Number | `[0-9]+(\.[0-9]+)?` )
( Identifier | `[A-Za-z_][A-Za-z0-9_]*` )
( String | `"[^"]*"`  )

### Numbers

Numbers contain digits and may include a decimal point. Their literal values are stored as Python floats.

Examples: 0, 100, and 3.14.
A minus sign is a separate token, so -12 produces MINUS and NUMBER.
The input 42. produces NUMBER followed by DOT.

### Identifiers and keywords

Identifiers begin with an ASCII letter or underscore.

Keywords are case-sensitive and must match .
For example, forge is a keyword, but Forge and forge2 are identifiers.

### Strings

Strings use double quotation marks and may be on multiple lines.
The lexeme includes the quotation marks. Empty strings are allowed.

Escape sequences are not interpreted. Backslashes are ordinary
characters, and the next double quotation mark ends the string.

### Operators and punctuation

operators:
+ - * / ! != = == < <= > >=

punctuation:
( ) { } , . ;

### Whitespace and comments

Spaces, tabs, and carriage returns are ignored. Newlines increase
the line counter. Comments begin with // and continue to the newline. 

The scanner adds an EOF token at the end of every input.

## Setup and running

The project was developed on Fedora KDE using Python 3.14.7.
It uses only Python's standard library. No additional packages.

Runing all commands from the Olympus project folder.

### Source-file mode

bash
python3 src/main.py test/lab1/olympus_sample.olympus


The program prints the tokens, followed by any lexical errors.
It exits with status 0 for valid input and status 1 for lexical
errors.

### Interactive mode

bash
python3 src/main.py

Enter one line of Olympus source at each prompt. The program
prints its tokens and any errors, then displays another prompt.
Each input is scanned separately.

Press Ctrl+D to exit. Ctrl+C also exits the prompt.

### Running the test scripts

bash
python3 test/lab1/test_symbols.py
python3 test/lab1/test_operators.py
python3 test/lab1/test_comments.py
python3 test/lab1/test_strings.py
python3 test/lab1/test_unterminated_string.py
python3 test/lab1/test_numbers.py
python3 test/lab1/test_keywords.py
python3 test/lab1/test_unexpected.py
python3 test/lab1/test_edge_cases.py


These scripts print results for manual comparison.

### Error handling

Unexpected characters produce an error containing the character
and its line number.

An unterminated string produces an error reporting its starting
line. The scanner reaches the end of the source and adds EOF.

## Test results

I ran these tests and checked the output manually.
EOF marks the end of the input.

### Test 1: Symbols

File: test/lab1/test_symbols.py
Input: ( ) { } , . ; + - * /

Expected: A token for each symbol, then EOF.
Actual: Each symbol had the correct token. No errors.
Result: Passed.

### Test 2: Operators

File: test/lab1/test_operators.py
Input: ! != = == < <= > >=

Expected: A token for each operator, then EOF.
Actual: All eight operators had the correct token. No errors.
Result: Passed.

### Test 3: Comments

File: test/lab1/test_comments.py
Input:
  / // Zeus comment
    + // Athena comment

Expected: SLASH, PLUS, and EOF. Comments should be ignored.
Actual: SLASH, PLUS, and EOF appeared. No errors.
Result: Passed.

### Test 4: Strings

File: test/lab1/test_strings.py
Input: "Zeus" "" "Mount Olympus"

Expected: Three string tokens, then EOF. The values should be Zeus, an empty string, and Mount Olympus.
Actual: All three strings had the correct values. No errors.
Result: Passed.

### Test 5: Unfinished string

File: test/lab1/test_unterminated_string.py
Input: A blank first line, then "Zeus without a closing quote.

Expected: EOF and an unterminated string error on line 2.
Actual: EOF appeared with the correct error on line 2.
Result: Passed.

### Test 6: Numbers

File: test/lab1/test_numbers.py
Input: 0 100 3.14 -12 42.

Expected: NUMBER, NUMBER, NUMBER, MINUS, NUMBER, NUMBER, DOT, and EOF. Number values: 0.0, 100.0, 3.14, 12.0, 42.0.
Actual: The tokens and values matched. No errors.
Result: Passed.

### Test 7: Keywords and names

File: test/lab1/test_keywords.py
Input: forge proclaim fate otherwise cycle true false Zeus _power power2 forge2 Forge

Expected: The first seven words should be keywords.
The last five should be identifiers, followed by EOF.
Actual: All words had the correct token type. No errors.
Result: Passed.

### Test 8: Invalid characters

File: test/lab1/test_unexpected.py
Input:
    @
    $ +

Expected: Errors for @ on line 1 and $ on line 2. PLUS and EOF should still appear.
Actual: Both errors had the correct lines. PLUS and EOF appeared.
Result: Passed.

### Test 9: Edge cases

File: test/lab1/test_edge_cases.py

Input 1: Empty input.
Expected: EOF on line 1.
Actual: EOF on line 1.

Input 2: Spaces, a tab, a carriage return, and a newline.
Expected: EOF on line 2.
Actual: EOF on line 2.

Input 3: A quoted string containing Mount, a newline, and
Olympus, followed by a newline and +.
Expected: string on line 1, then PLUS and EOF on line 3.
Actual: The string kept its newline. The line numbers matched.

Input 4: "// Zeus"
Expected: STRING with the value // Zeus, then EOF.
Actual: STRING with the correct value, then EOF.

Result: All four passed. No errors.

### Test 10: source file

File: test/lab1/olympus_sample.olympus
Command: python3 src/main.py test/lab1/olympus_sample.olympus

Input: The file contains these statements plus line comments:
    forge power = 100;
    proclaim "Welcome to Olympus";

Expected: FORGE, IDENTIFIER, EQUAL, NUMBER, SEMICOLON,
PROCLAIM, STRING, SEMICOLON, and EOF. Comments are ignored.
The number value should be 100.0 and the string value should
be Welcome to Olympus.

Actual: The tokens and values matched. No errors.
Result: Passed.

### Test 11: Invalid source file

File: test/lab1/invalid.olympus
Command: python3 src/main.py test/lab1/invalid.olympus

Input:
    @
    "Zeus

Expected: EOF, an invalid character error on line 2,
and an unterminated string error starting on line 3.
The program should exit with status 1.

Actual: Both errors had the correct lines. EOF appeared.
Result: Passed.

### Test 12: Interactive

Command: python3 src/main.py

Inputs separate prompts:
    forge power = 100;
    @
    "Zeus
    proclaim "Recovered";

Expected: The first input should produce the correct tokens.
The next two should report errors on line 1.
The last input should produce PROCLAIM, STRING, SEMICOLON,
and EOF. The prompt should keep working after errors.
Ctrl+D should exit.

Actual: The valid inputs produced the correct tokens.
Both errors appeared on line 1. The prompt kept working,
and Ctrl+D exited.
Result: Passed.

## Limitations

Olympus only scans source code into tokens. 

Strings do not support escape sequences.
Only // line comments are supported.
Identifiers use ASCII letters, digits, and underscores.
Numbers do not support scientific notation.

The prompt scans one line at a time.

## AI assistance

I used ChatGPT to help write the scanner and the test scripts.
