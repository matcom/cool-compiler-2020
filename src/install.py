import cloudpickle
from coolgrammar.grammar import build_cool_grammar
from parserr.lr import LALRParser
from argparse import ArgumentParser


def generate_py(f):
    gram, lexer = build_cool_grammar()
    parser = LALRParser(gram, verbose=True)
    lexer_str = cloudpickle.dumps(lexer)
    parser_str = cloudpickle.dumps(parser)
    f.write("""
import cloudpickle
import sys
sys.path.append('..')
PARSER = cloudpickle.loads(%s)
LEXER = cloudpickle.loads(%s)
""" % (parser_str, lexer_str))


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('file', type=str)
    arg = parser.parse_args()
    with open(arg.file, "w+") as f:
        generate_py(f)
