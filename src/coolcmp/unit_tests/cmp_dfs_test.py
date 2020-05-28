import pytest
from .utils import getclfiles
from coolcmp.cmp_utils.parser import Parser

tests = getclfiles('.') + getclfiles('../tests')

@pytest.mark.cmp_dfs
@pytest.mark.parametrize("file", tests)
def test_parser_errors(file):
    p = Parser()
    p.build()

    content = ""

    with open(file) as file:
        content = file.read()

    res = p.parser.parse(content)
    
    if len(p.errors) == 0:
        x = res.dfs_rec_rep()
        y = res.dfs_iter_rep()
        assert(x == y)
