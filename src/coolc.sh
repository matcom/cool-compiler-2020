# Incluya aquí las instrucciones necesarias para ejecutar su compilador

INPUT_FILE=$1
OUTPUT_FILE=${INPUT_FILE:0: -2}mips

echo "Cool Compiler v0.1"
echo "Copyright (c) 2020: Juan David Menendez del Cueto, Karl Lewis Sosa"

# Llamar al compilador
python3 exec_cool.py ${INPUT_FILE} 
