# Incluya aquí las instrucciones necesarias para ejecutar su compilador

INPUT_FILE=$1
OUTPUT_FILE=${INPUT_FILE:0: -2}mips

# Si su compilador no lo hace ya, aquí puede imprimir la información de contacto
echo "cool ytejeda03 v0.1"
echo "Copyright (c) 2019: Yunior Alexander Tejeda Illana, Gabriela Mijenes"

# Llamar al compilador
echo "Compiling $INPUT_FILE into $OUTPUT_FILE"
