import os
import subprocess
from pathlib import Path

error_conversions = {
    'Dispatch on void': 'Dispatch to void.',
    'Division by zero': '[Breakpoint/Division by 0]  Execution aborted'
}

# lines that mimps simulator prints
USELESS_LINES = 5
USELESS_SUFFIX = 'COOL program successfully executed'

def load_file(file):
    with open(file) as f:
        content = f.read()
        
    return content

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

def get_output(p):
    output = p.stdout.split('\n')[USELESS_LINES:]
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
    ref_output = get_output(ref).rstrip()

    if mine.returncode == 1:  # runtime exception of my compiled code
        assert ref_output.endswith(error_conversions[my_output.rstrip()])

    else:
        if ref.stderr:  # ref compiler gave some runtime error (div0 or heap overflow can be)
            assert ref.stderr == mine.stderr, (f'Reference compiler gives error:\n{ref.stderr}\n'
                                                f'My compiler gives:\n{mine.stderr}\n')
 
        else:
            assert ref_output.endswith(USELESS_SUFFIX)
            assert my_output + USELESS_SUFFIX == ref_output