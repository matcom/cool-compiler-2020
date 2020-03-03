# Incluya aquí las instrucciones necesarias para ejecutar su compilador

INPUT_FILE=$1
#OUTPUT_FILE=${INPUT_FILE:0: -2}mips

# Si su compilador no lo hace ya, aquí puede imprimir la información de contacto
echo "COOL Compiler v1.0"                           # TODO: Recuerde cambiar estas
echo "Copyright (c) 2020: Carlos, Oscar, Harold"    # línea con info del compilador

# Llamar al compilador
#echo "Compiling $INPUT_FILE into $OUTPUT_FILE"

python3 main.py $INPUT_FILE