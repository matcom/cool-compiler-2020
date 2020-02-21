from lexer import Cool_Lexer

import pathlib
import sys
import os


if __name__ == "__main__":
    cool_lexer = Cool_Lexer()
    cool_lexer.build()


    i = 1
    for t in os.listdir('./tests'):

        if t.endswith('.cl'):
            cool_lexer.build()
            lexer = cool_lexer.lexer
            with open('./tests/' + t) as f1:
               lexer.input(f1.read())
            for token in lexer:
                pass

            with open('./tests/' + t[:-3] + '_error.txt') as f2:
                print(f"Test #{i}: {t}")
                user_answer = ''
                for e in lexer.errors:
                    user_answer += e
                correct_answer = f2.read()
                print(f"Your answer: {user_answer}")
                print(f"Test answer: {correct_answer}")
                if user_answer.split() == correct_answer.split():
                    print("ACCEPTED")
                else:
                    print("FAIL")
            i += 1