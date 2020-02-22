"""
Utility to generate parser file given some grammar.txt file
"""

import re

output = ""

equiv = {
    "PLUS": r'\+',
    "MUL": r'\*',
    "DIV": r'\/',
    "MINUS": r'\-',
    "LESS": r'\<',
    "LESS_EQ": r'\<\=',
    "EQ": r'\=',
    "INT_COMP": r'\~',

    "ASSIGN": r'\<\-',

    "LPAREN": r'\(',
    "RPAREN": r'\)',
    "LBRACE": r'\{',
    "RBRACE": r'\}',
    "COLON": r'\:',
    "SEMICOLON": r'\;',
    "DOT": r'\.',
    "COMMA": r'\,',
    "CAST": r'\@',

    "ARROW": r'\=\>',
}


def get_method_docstring(token_list):
    output = "\"\"\"" + "\n"

    for token in token_list:
        if token == "::=":
            token = ":"

        elif token == "|":
            token = "\n|\t"

        else:
            for key, value in equiv.items():
                obj = re.search(value, token)

                if obj is not None and obj.start() == 0 and obj.end() == len(token):
                    token = key
                    break

        output += token + " "

    output += "\n" + "\"\"\""

    return output


def print_method(name, docstring):
    s = "def p_" + name + "(self, p):\n" + docstring + "\n\n"

    global output
    output += s


with open("grammar-BNF.txt", "r") as grammar_file:
    production = []

    for line in grammar_file:
        spl_line = line.split()

        if len(spl_line) == 0 or spl_line[0] == "#":
            if len(production) > 0:
                docstring = get_method_docstring(production)
                print_method(production[0], docstring)

            production = []
            continue

        production += spl_line


with open("output_file.py", "w") as f:
    print(output, file=f)
