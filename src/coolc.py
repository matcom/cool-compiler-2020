from sys import argv
import cool_lang.utils as clutils

INPUT_FILE = argv[1]
OUTPUT_FILE = argv[2]

assert INPUT_FILE.endswith('.cl'), "Invalid input file extention."
assert OUTPUT_FILE.endswith('.mips'), "Invalid output file extention."

print(clutils.preprocessing.process(INPUT_FILE))

