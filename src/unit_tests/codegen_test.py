import pytest
from pathlib import Path
from coolcmp.cmp.source_code import *
from coolcmp.cmp.errors import CmpErrors
from unit_tests.utils import load_file

root = Path('unit_tests/CustCodeGeneration')
tests = list(root.rglob('*.cl'))

@pytest.mark.codegen
@pytest.mark.parametrize('file', tests, ids=map(str, tests))
def test_codegen(file):
    pass