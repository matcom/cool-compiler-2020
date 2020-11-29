#!/bin/bash
# Execution details

INPUT_FILE=$1
OUTPUT_FILE=${INPUT_FILE:0: -2}mips

# Display project descripton here
#make info    # TODO: Ensure that this rule is executed a single time
echo "2kodevs - CoolCompilerv0.1"
echo "Copyright © 2020: Lázaro Raúl Iglesias Vera, Miguel Tenorio Potrony, Mauricio Lázaro Perdomo Cortéz"

# Compile and Run
#echo "Compiling $INPUT_FILE into $OUTPUT_FILE"
python3 main.py -f $INPUT_FILE
