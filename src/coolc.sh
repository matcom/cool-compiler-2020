# Incluya aquí las instrucciones necesarias para ejecutar su compilador

INPUT_FILE=$1
OUTPUT_FILE=${INPUT_FILE:0: -2}mips

# Si su compilador no lo hace ya, aquí puede imprimir la información de contacto
echo "DLR MATCOM COOL COMPILER V 0.1"
echo "Copyright (c) 2020: Leonel Alejandro García López, Jorge Daniel Valle Díaz, Roberto Marti Cedeño"

# Llamar al compilador
#echo "Compiling $INPUT_FILE into $OUTPUT_FILE"

python3 main.py $INPUT_FILE $OUTPUT_FILE do_cil
