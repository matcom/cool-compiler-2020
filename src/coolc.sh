# Incluya aquí las instrucciones necesarias para ejecutar su compilador

INPUT_FILE=$1
OUTPUT_FILE=${INPUT_FILE:0: -2}mips

# Si su compilador no lo hace ya, aquí puede imprimir la información de contacto

# Llamar al compilador
#echo "Compiling $INPUT_FILE into $OUTPUT_FILE"
python COOLCompiler.py $INPUT_FILE $OUTPUT_FILE
