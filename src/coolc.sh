# Execution details

INPUT_FILE=$1
OUTPUT_FILE=${INPUT_FILE:0: -2}mips

# Display project descripton here
make info    # TODO: Ensure that this rule is executed a single time

# Compile and Run
echo "Compiling $INPUT_FILE into $OUTPUT_FILE"
python main.py -f $INPUT_FILE
