import pytest
import os
from utils import compare_outputs

tests_dir = os.path.join(__file__.rpartition(os.path.sep)[0], 'codegen')
tests = [(file) for file in os.listdir(tests_dir) if file.endswith('.cl')]

# @pytest.mark.lexer
# @pytest.mark.parser
# @pytest.mark.semantic
@pytest.mark.codegen
@pytest.mark.ok
@pytest.mark.run(order=4)
@pytest.mark.parametrize("cool_file", tests)
def test_codegen(compiler_path, cool_file):
    compare_outputs(compiler_path, os.path.join(tests_dir, cool_file), os.path.join(tests_dir, cool_file[:-3] + '_input.txt'), \
                    os.path.join(tests_dir, cool_file[:-3] + '_output.txt'))
