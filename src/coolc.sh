# Incluya aquí las instrucciones necesarias para ejecutar su compilador

INPUT_FILE=$1
OUTPUT_FILE=${INPUT_FILE:0: -2}mips

echo "CodeStrange Cool Compiler v0.1"
echo "Copyright (c) 2020: Carlos Bermudez Porto, Leynier Gutiérrez González, Tony Raúl Blanco Fernández"

# Llamar al compilador
python coolc.py ${INPUT_FILE} ${OUTPUT_FILE}
