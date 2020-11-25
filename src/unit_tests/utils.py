import os
import subprocess
from pathlib import Path
from coolcmp.cmp.constants import *

error_conversions = {
    rte_errors[LABEL_DISPATCH_VOID]: 'Dispatch to void.',
    rte_errors[LABEL_DIV_BY_0]: '[Breakpoint/Division by 0]  Execution aborted',
    rte_errors[LABEL_CASE_VOID]: 'Match on void in case statement.',
    rte_errors[LABEL_CASE_NO_BRANCH]: 'No match in case statement',
    rte_errors[LABEL_SUBSTR_TOO_LONG_INDEX]: 'Index to substr is too big',
    rte_errors[LABEL_SUBSTR_TOO_LONG_LENGTH]: 'Length to substr too long',
    rte_errors[LABEL_SUBSTR_NEG_INDEX]: 'Index to substr is negative',
    rte_errors[LABEL_SUBSTR_NEG_LENGTH]: 'Length to substr is negative'
}

# lines that mimps simulator prints
USELESS_LINES = 5
USELESS_SUFFIX = 'COOL program successfully executed'

def load_file(file):
    with open(file) as f:
        content = f.read()
        
    return content

def run_unconditionally(file, add_args=[]):
    try:
        p = subprocess.run(args=['python3', '-m', 'coolcmp', file] + add_args, capture_output=True, timeout=2, text=True)
    except subprocess.TimeoutExpired:
        assert 0, 'Timeout Expired'
        return

    mips_file = Path('.', f'{file.stem}.mips').resolve()
    assert mips_file.exists()
    # delete mips file
    mips_file.unlink()

def run_test(file, add_args=[], verdict=None):
    if not verdict:
        verdict = file.parts[-2]
        assert verdict == 'success' or verdict == 'fail'

    try:
        p = subprocess.run(args=['python3', '-m', 'coolcmp', file] + add_args, capture_output=True, timeout=2, text=True)
    except subprocess.TimeoutExpired:
        assert 0, 'Timeout Expired'
        return

    if p.stdout:
        assert p.returncode == 1, f'Return code must be 1, found {p.returncode}'
        assert verdict == 'fail'

    else:
        assert p.returncode == 0, f'File {file} must compile'
        assert verdict == 'success'

def get_output(p, is_ref=False):
    output = p.stdout.split('\n')[USELESS_LINES:]

    if is_ref:
        ok_out = []
        for line in output:
            if line == 'Increasing heap...':
                continue

            ok_out.append(line)

        output = ok_out

    output = '\n'.join(output)
    return output

def run_test_codegen(file, t=2):
    # it is assumed that tests in codegen can only have runtime errors
    run_test(file=file, verdict='success')

    mips_file = Path('.', f'{file.stem}.mips').resolve()

    assert mips_file.exists()

    try:
        mine = subprocess.run(args=['spim', '-f', mips_file], capture_output=True, text=True, timeout=t)
    except subprocess.TimeoutExpired:
        assert 0, 'Timeout Expired'
        return
    
    # delete mips file
    mips_file.unlink()

    try:
        ref = subprocess.run(args=['bash', 'unit_tests/cmp.sh', file], capture_output=True, text=True, timeout=t)
    except subprocess.TimeoutExpired:
        assert 0, 'Timeout Expired'
        return

    mips_file_ref = Path(file.parent, f'{file.stem}.s')

    assert mips_file_ref.exists()
    mips_file_ref.unlink()  # delete it

    my_output = get_output(mine)
    ref_output = get_output(ref, is_ref=True).rstrip()

    if mine.returncode == 1:  # runtime exception of my compiled code
        conv = None

        for k, v  in error_conversions.items():
            if k in my_output:
                conv = v

        assert conv
        assert conv in ref_output

    else:
        if ref.stderr:  # ref compiler gave some runtime error (div0 or heap overflow can be)
            assert ref.stderr == mine.stderr, (f'Reference compiler gives error:\n{ref.stderr}\n'
                                                f'My compiler gives:\n{mine.stderr}\n')
 
        else:
            if 'Abort called from class' in ref_output:
                assert my_output.rstrip() == ref_output

            else:
                assert ref_output.endswith(USELESS_SUFFIX)
                assert my_output + USELESS_SUFFIX == ref_output