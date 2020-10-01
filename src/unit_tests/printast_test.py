import pytest
from pathlib import Path
from .utils import load_file
from coolcmp.cmp.source_code import *
from coolcmp.cmp.errors import CmpErrors
from coolcmp.cmp.print_ast import PrintAst

root = Path('..').resolve()
tests = list(root.rglob('*.cl'))

@pytest.mark.printast
@pytest.mark.parametrize('file', tests, ids=map(str, tests))
def test_printast(file):
    try:
        sc = SourceCode(load_file(file))
        root = sc.syntacticAnalysis(Lexer())
    except CmpErrors:
        return
    
    PrintAst(root)
    assert root.class_name() == 'Program'