import pytest
import os
from utils import compare_errors

tests_dir = __file__.rpartition('/')[0] + '/semantic/'
tests = [(tests_dir + file) for file in os.listdir(tests_dir) if file.endswith('.cl')]

@pytest.mark.run(order=3)
@pytest.mark.semantic
@pytest.mark.error
@pytest.mark.parametrize("cool_file", [])
def test_semantic_errors(compiler_path, cool_file):
    compare_errors(compiler_path, cool_file, cool_file[:-3] + '_error.txt')