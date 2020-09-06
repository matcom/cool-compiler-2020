import pytest
from .utils import getclfiles
from coolcmp.cmp_utils.source_code import SourceCode
from coolcmp.cmp_utils.print_ast import PrintAst
from coolcmp.cmp_utils.errors import CmpErrors
from coolcmp.cmp_utils.lexer import Lexer

tests = getclfiles('.') + getclfiles('../tests')

@pytest.mark.print_ast
@pytest.mark.parametrize("file", tests)
def test_parser_errors(file):
    with open(file) as file:
        content = file.read()

    source_code = SourceCode(content)

    try:
        root = source_code.syntacticAnalysis(Lexer())
    except CmpErrors:
        return
    
    PrintAst(root)
    assert(root.class_name() == "Program")
