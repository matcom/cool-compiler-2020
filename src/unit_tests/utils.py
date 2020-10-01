import os
import subprocess

def getclfiles(root):
    return [ os.path.join(dir_path, file) for dir_path, _, file_list in os.walk(root)
                                             for file in file_list if file.endswith('cl') ]

def load_file(file):
    with open(file) as f:
        content = f.read()
        
    return content

def run_test(file):
    verdict = file.parts[-2]
    assert verdict == 'success' or verdict == 'fail'

    try:
        p = subprocess.run(args=['python3', '-m', 'coolcmp', '--no_mips', file], capture_output=True, timeout=2, text=True)
    except subprocess.TimeoutExpired:
        assert 0, 'Timeout Expired'
        return

    if p.stdout:
        assert p.returncode == 1, f'Return code must be 1, found {p.returncode}'
        assert verdict == 'fail'

    else:
        assert p.returncode == 0, f'File {file} must compile'
        assert verdict == 'success'