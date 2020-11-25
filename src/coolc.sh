# Incluye aqui las instrucciones necesarias para ejecutar su compilador
INPUT_FILE=$1
OUTPUT_FILE=$INPUT_FILE
# OUTPUT_FILE=${INPUT_FILE:0:-2}
# Si su compilador no lo hace ya, aquí puede imprimir información de contacto
echo "LINEA_CON_NOMBRE_Y_VERSION_DEL_COMPILADOR"    # TODO: Recuerde cambiar estas lineas
echo "Copyright (c) 2019: Loraine Monteagudo, Amanda Marrero, Manuel Fernandez"

FILE="../src/main.py"
echo $FILE
python main.py
# echo "Compiling $INPUT_FILE into $OUTPUT_FILE"
python ${FILE} $INPUT_FILE 