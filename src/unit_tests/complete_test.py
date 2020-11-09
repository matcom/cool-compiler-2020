import pytest
from pathlib import Path
from coolcmp.cmp.source_code import *
from unit_tests.utils import run_test_codegen

tests = []

with open('unit_tests/compiled_files.txt') as f:
    for line in f:
        tests.append(Path(line.rstrip()).resolve())

@pytest.mark.complete
@pytest.mark.parametrize('file', tests, ids=map(str, tests))
def test_complete(file):
    run_test_codegen(file)