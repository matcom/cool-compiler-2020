import pytest
from pathlib import Path
from coolcmp.cmp.source_code import *
from coolcmp.cmp.errors import CmpErrors
from unit_tests.utils import load_file

root = Path('unit_tests/CustSemantics')
tests = list(root.rglob('*.cl'))

@pytest.mark.semantics
@pytest.mark.parametrize('file', tests, ids=map(str, tests))
def test_semantics(file):
    ans = file.parts[-2]

    try:
        sc = SourceCode(load_file(file))
        lexer = sc.lexicalAnalysis()
        root = sc.syntacticAnalysis(lexer)
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