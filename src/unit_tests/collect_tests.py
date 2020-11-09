from .utils import run_unconditionally
from pathlib import Path

def check_compiled(file):
    try:
        run_unconditionally(file)
    except AssertionError:
        return False

    return True

root = Path('..').resolve()
all_tests = list(root.rglob('*.cl'))

print(f'Analyzing {len(all_tests)} tests')

tests = []

# remove tests that don't compile
for i, t in enumerate(all_tests):
    verd = check_compiled(t)
    print(f'{i}, analizing file: {t} : result = {verd}')
    
    if verd:
        tests.append(t)

# save them
with open('unit_tests/compiled_files.txt', 'w') as f:
    for t in tests:
        with open(t) as code:
            code = code.readlines()
            code = ''.join(code)

            if 'in_string' in code or 'in_int' in code:
                continue

        print(t, file=f)