import pytest
from .utils import getclfiles, load_file, compare_errors
from coolcmp.cmp_utils.source_code import SourceCode
from coolcmp.cmp_utils.print_ast import PrintAst
from coolcmp.cmp_utils.errors import CmpErrors
from coolcmp.cmp_utils.lexer import Lexer

PREFIX_DIR = 'coolcmp/unit_tests/'

tests = getclfiles('.') + getclfiles('../tests')

@pytest.mark.print_ast
@pytest.mark.parametrize('file', tests)
def test_parser_errors(file):
    sc = SourceCode(load_file(file))

    try:
        root = sc.syntacticAnalysis(Lexer())
    except CmpErrors:
        return
    
    PrintAst(root)
    assert root.class_name() == 'Program'
    return sc, root

tests = getclfiles(PREFIX_DIR + 'Custom/semantics/')

@pytest.mark.semantics
@pytest.mark.parametrize('file', tests)
def test_semantics(file, ans=None):
    if not ans:
        ans = file.split('/')[-2]
        assert ans == 'fail' or ans == 'success'

    sc, root = test_parser_errors(file)

    try:
        sc.semanticAnalysis(root)
    except CmpErrors as err:
        assert 'fail' == ans, err
        return

    assert 'success' == ans

    tot_cls = len(root.cls_list)

    root_inh = None
    for cls in sc.native_classes:
        if cls.type.value == 'Object':
            root_inh = cls

    seen = set()
    nodes = 0
    edges = 0

    def dfs(u):
        seen.add(u)

        nonlocal nodes, edges
        nodes += 1
        edges += len(u.children)

        for v in u.children:
            if v not in seen:
                dfs(v)

    assert root_inh
    dfs(root_inh)

    assert tot_cls == nodes, f'tot_cls = {tot_cls}, nodes = {nodes}'
    assert edges == nodes - 1, f'edges = {edges}, nodes = {nodes}'

    return sc

tests = getclfiles(PREFIX_DIR + 'Custom/type_checker/')

@pytest.mark.type_checker
@pytest.mark.parametrize('file', tests)
def test_type_checker(file, ans=None):
    if not ans:
        ans = file.split('/')[-2]
        assert ans == 'fail' or ans == 'success'

    sc = test_semantics(file, 'success')

    try:
        sc.runTypeChecker()
    except CmpErrors as err:
        assert 'fail' == ans, err
        return

    assert 'success' == ans

tests = getclfiles(PREFIX_DIR + 'Semantics/')

@pytest.mark.tc_others
@pytest.mark.parametrize('file', tests)
def test_tc_others(file, ans=None):
    if not ans:
        ans = file.split('/')[-2]
        assert ans == 'fail' or ans == 'success'

    sc = test_semantics(file, 'success')

    try:
        sc.runTypeChecker()
    except CmpErrors as err:
        assert 'fail' == ans, err
        return

    assert 'success' == ans
    
    assert ans == 'success'