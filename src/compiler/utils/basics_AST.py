from compiler.components.lexer.lexer_analyzer import tokenizer, tokens
from compiler.components.parser.syntax_analyzer import run_parser

def build_basic_ast():
    fpath = "./basics_classes.cl"
    with open(fpath, encoding="utf-8") as file:
        code = file.read()
        _, _, real_col= tokenizer(code)
        ast_basic= run_parser(tokens= tokens, 
                            source_program= code, 
                            real_col= real_col)
        return ast_basic
    
