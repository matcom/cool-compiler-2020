import pytest
from .utils import getclfiles
from coolcmp.cmp_utils.parser import Parser
from coolcmp.cmp_utils.print_ast import PrintAst
from coolcmp.cmp_utils.errors import CmpErrors

tests = getclfiles('.') + getclfiles('../tests')

@pytest.mark.print_ast
@pytest.mark.parametrize("file", tests)
def test_parser_errors(file):
    p = Parser()
    p.build()

    content = ""

    with open(file) as file:
        content = file.read()

    try:
        res = p.parser.parse(content)
    except CmpErrors as err:
        return
    
    PrintAst(res)
    assert(res.class_name() == "Program")
