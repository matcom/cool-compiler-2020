from semantic.visitors.type_collector import TypeCollector
from semantic.visitors.type_builder import TypeBuilder
from semantic.visitors.var_collector import VarCollector
from semantic.visitors.type_checker import TypeChecker


def semantic_analysis(ast, debug=False):
    if debug:
        print('============== COLLECTING TYPES ===============')
    errors = []
    collector = TypeCollector(errors)
    collector.visit(ast)
    context = collector.context
    if debug:
        print('Errors: [')
        for error in errors:
            print('\t', error)
        print('=============== BUILDING TYPES ================')
    builder = TypeBuilder(context, errors)
    builder.visit(ast)
    if debug:
        print('Errors: [')
        for error in errors:
            print('\t', error)
        print(']')
        print('=============== VAR COLLECTOR ================')
    checker = VarCollector(context, errors)
    scope = checker.visit(ast)
    if debug:
        print('Errors: [')
        for error in errors:
            print('\t', error)
        print(']')
        print('=============== CHECKING TYPES ================')
    checker = TypeChecker(context, errors)
    checker.visit(ast, scope)
    if debug:
        print('Errors: [')
        for error in errors:
            print('\t', error)
        print(']')
        print('Context:')
        print(context)
        print('Scope:')
        print(scope)
    return ast, errors, context, scope
