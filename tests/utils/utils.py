import subprocess
import re

COMPILER_TIMEOUT = 'El compilador tarda mucho en responder.'
TEST_MUST_FAIL = 'El test %s debe fallar al compilar'
TEST_MUST_COMPILE = 'El test %s debe compilar'
BAD_ERROR_FORMAT = '''El error no esta en formato: (<línea>,<columna>) - <tipo_de_error>: <texto_del_error>
                        o no se encuentra en la 3ra linea'''
UNEXPECTED_ERROR = 'Se esperaba un %s en (%d, %d). Su error fue un %s en (%d, %d)'

def parse_error(error: str):
    merror = re.fullmatch(r'^\s*\(\s*(\d+)\s*,\s*(\d+)\s*\)\s*-\s*(\w+)\s*:(.*)$', error)
    assert merror, BAD_ERROR_FORMAT

    return (t(x) for t, x in zip([int, int, str, str], merror.groups()))


def first_error(compiler_output: list, errors: list):
    line, column, error_type, _ = parse_error(errors[0])

    oline, ocolumn, oerror_type, _ = parse_error(compiler_output[0])

    assert line == oline and column == ocolumn and error_type == oerror_type,\
        UNEXPECTED_ERROR % (error_type, line, column, oerror_type, oline, ocolumn)


def compare_errors(compiler_path: str, cool_file_path: str, error_file_path: str, cmp=first_error, timeout=100):
    try:
        sp = subprocess.run(['bash', compiler_path, cool_file_path], capture_output=True, timeout=timeout)
        return_code, output = sp.returncode, sp.stdout.decode()
    except TimeoutError:
        assert False, COMPILER_TIMEOUT

    compiler_output = output.split('\n')

    if error_file_path:
        assert return_code == 1, TEST_MUST_FAIL % cool_file_path

        fd = open(error_file_path, 'r')
        errors = fd.read().split('\n')
        fd.close()

        # checking the errors of compiler
        cmp(compiler_output[2:], errors)
    else:
        print(return_code, output)
        assert return_code == 0, TEST_MUST_COMPILE % cool_file_path