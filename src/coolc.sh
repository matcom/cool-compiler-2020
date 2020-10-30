# Incluya aquí las instrucciones necesarias para ejecutar su compilador

INPUT_FILE=$1
OUTPUT_FILE=${INPUT_FILE:0: -2}mips

# Si su compilador no lo hace ya, aquí puede imprimir la información de contacto
echo "+COOL"        
echo "Copyright (c) 2019: Karl Lewis Sosa Justiz, Juan David Menendez del Cueto"

# Llamar al compilador
#echo "Compiling $INPUT_FILE into $OUTPUT_FILE"
python3.7 exec_cool.py $INPUT_FILE
