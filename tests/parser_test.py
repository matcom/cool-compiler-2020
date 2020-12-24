import pytest
import os
from utils import compare_errors

tests_dir = __file__.rpartition('/')[0] + '/parser/'
tests = [(file) for file in os.listdir(tests_dir) if file.endswith('.cl')]

@pytest.mark.parser
@pytest.mark.error
@pytest.mark.run(order=2)
@pytest.mark.parametrize("cool_file", tests)
def test_parser_errors(compiler_path, cool_file):
    compare_errors(compiler_path, tests_dir + cool_file, tests_dir + cool_file[:-3] + '_error.txt')