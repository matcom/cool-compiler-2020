# Incluya aquí las instrucciones necesarias para ejecutar su compilador

INPUT_FILE=$1
OUTPUT_FILE=${INPUT_FILE:0: -2}mips

# Si su compilador no lo hace ya, aquí puede imprimir la información de contacto
echo "Cool ml-uh v0.0.1"
echo "Copyright (c) 2019: Lazaro Jesus Suarez Nuñez, Marcos Antonio Maceo Reyes"

# Llamar al compilador
echo "Compiling $INPUT_FILE into $OUTPUT_FILE"

python compiler.py "$INPUT_FILE" -o "$OUTPUT_FILE"
