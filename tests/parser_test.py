import pytest
import os
from utils import compare_errors

tests_dir = __file__.rpartition('/')[0] + '/parser/'
tests = [(tests_dir + file) for file in os.listdir(tests_dir) if file.endswith('.cl')]

@pytest.mark.run(order=2)
@pytest.mark.parser
@pytest.mark.error
@pytest.mark.parametrize("cool_file", tests)
def test_parser_errors(compiler_path, cool_file):
    compare_errors(compiler_path, cool_file, cool_file[:-3] + '_error.txt')