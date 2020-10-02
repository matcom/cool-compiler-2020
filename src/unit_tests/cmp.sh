# input file
INPUT_FILE=$1

# output file (file_name.s)
OUTPUT_FILE=${INPUT_FILE:0: -2}s

# path to compiler executables
PATH_PREFIX=~/Projects/cool-compiler/bin

# generate mips code
$PATH_PREFIX/coolc $INPUT_FILE

# run the mips code
$PATH_PREFIX/spim $OUTPUT_FILE