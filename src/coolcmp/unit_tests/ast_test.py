import pytest
import os
import sys
from coolcmp.cmp_utils.parser import Parser

def get_cl_files(root):
    return [ os.path.join(dir_path, file) for dir_path, _, file_list in os.walk(root)
                                             for file in file_list if file.endswith('cl') ]

tests = get_cl_files('.') + get_cl_files('../tests')

print(tests)

@pytest.mark.parametrize("file", tests)
def test_parser_errors(file):
    p = Parser()
    p.build()

    content = ""

    with open(file) as file:
        content = file.read()

    res = p.parser.parse(content)
    
    if len(p.errors) == 0:
        print(res.__repr__())
        assert(res.__class__.__name__ == "Program")
