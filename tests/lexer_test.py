import pytest
import os
from utils import compare_errors

tests_dir = os.path.join(__file__.rpartition(os.path.sep)[0], 'lexer')
tests = [(file) for file in os.listdir(tests_dir) if file.endswith('.cl')]

@pytest.mark.lexer
@pytest.mark.error
@pytest.mark.run(order=1)
@pytest.mark.parametrize("cool_file", tests)
def test_lexer_errors(compiler_path, cool_file):
    compare_errors(compiler_path, os.path.join(tests_dir, cool_file), os.path.join(tests_dir, cool_file[:-3] + '_error.txt'))