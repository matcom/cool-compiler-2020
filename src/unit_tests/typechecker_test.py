import pytest
from pathlib import Path
from coolcmp.cmp.source_code import *
from coolcmp.cmp.errors import CmpErrors
from unit_tests.utils import load_file, run_test

root = Path('unit_tests/TypeChecker')
tests = list(root.rglob('*.cl'))

root = Path('unit_tests/Semantics')
tests.extend(list(root.rglob('*.cl')))

@pytest.mark.typechecker
@pytest.mark.parametrize('file', tests, ids=map(str, tests))
def test_typechecker(file):
    run_test(file, add_args=['--no_mips'])