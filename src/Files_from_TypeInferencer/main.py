import eel
import logging
from time import sleep
from core.cmp.visitors import *
from core.cmp.evaluation import *
from core.cmp.lex import CoolLexer
import sys
from os.path import basename


def build_AST(G, text):
    data, err = [], False
    ast = None
    txt = '================== TOKENS =====================\n'
    tokens = tokenize_text(text)
    txt += format_tokens(tokens)
    data.append(txt)
    txt = '=================== PARSE =====================\n'
    #print(parser([t.token_type for t in tokens], get_shift_reduce=True))
    try:
        parse, operations = CoolParser([t.token_type for t in tokens], get_shift_reduce=True)
    except:
        err = True
        txt += 'Impossible to parse\n'
    #print('\n'.join(repr(x) for x in parse))
    data.append(txt)
    if not err:
        txt = '==================== AST ======================\n'
        ast = evaluate_reverse_parse(parse, operations, tokens)
        formatter = FormatVisitor()
        tree = formatter.visit(ast)
        txt += str(tree)
        data.append(txt)
    return ast, '\n\n'.join(data)

def error_formatter(errors):
    txt = 'Errors: [\n'
    for error in errors:
        txt += f'\t{error}\n'
    txt += ']\n'
    return txt

def run_pipeline(G, text):
    data, err = [], False
    ast, txt = build_AST(G, text)
    errors = context = scope = None
    data.append(txt)
    if ast:
        txt = '============== COLLECTING TYPES ===============\n'
        errors = []
        collector = TypeCollector(errors)
        collector.visit(ast)
        context = collector.context
        if len(errors):
            txt += error_formatter(errors)
            err = True
        txt += 'Context:\n'
        txt += str(context)
        data.append(txt)
        errors.clear()
        txt = '=============== BUILDING TYPES ================\n'
        builder = TypeBuilder(context, errors)
        builder.visit(ast)
        if len(errors):
            txt += error_formatter(errors)
            err = True
        errors.clear()
        data.append(txt)
        txt = '=============== CHECKING TYPES ================\n'
        checker = TypeChecker(context, errors)
        scope = checker.visit(ast)
        if len(errors):
            txt += error_formatter(errors)
            err = True
        errors.clear()
        data.append(txt)
        txt = '=============== INFERING TYPES ================\n'
        inferer = InferenceVisitor(context, errors)
        while True:
            old = scope.count_auto()
            scope = inferer.visit(ast)
            if old == scope.count_auto():
                break
        errors.clear()
        scope = inferer.visit(ast)
        if len(errors):
            txt += error_formatter(errors)
            err = True
        errors.clear()
        txt += 'Context:\n'
        txt += str(context) + '\n'
        formatter = ComputedVisitor()
        if not err:
            tree = formatter.visit(ast)
            txt += 'AST:\n' + str(tree)
        data.append(txt)
    return '\n\n'.join(data)

@eel.expose
def compile(text):
    sleep(2)
    return run_pipeline(CoolGrammar, text)

def main():
    eel.init('web')

    eel_options = {'port': 8045}
    eel.start('index.html', size=(1000, 860), options=eel_options, block=False)

    while True:
        eel.sleep(0.1)


if __name__ == '__main__':
    # main()
    input_file = sys.argv[1]
    text = ""
    with open(input_file, 'r') as f:
        text = f.read()
    lex = CoolLexer()
    lex.build()
    toks, errors = lex.tokenize(text)
    
    for token in toks:
        if token.token_type == "ERROR":
            print(token.lex)
       