# Incluya aquí las instrucciones necesarias para ejecutar su compilador

INPUT_FILE=$1
OUTPUT_FILE=${INPUT_FILE:0: -2}mips

# Si su compilador no lo hace ya, aquí puede imprimir la información de contacto
echo "LINEA_CON_NOMBRE_Y_VERSION_DEL_COMPILADOR"        # TODO: Recuerde cambiar estas
echo "Copyright (c) 2019: Carlos Bermudez Porto, Nombre2, Nombre3"    # TODO: líneas a los valores correctos

# Llamar al compilador
echo "Compiling $INPUT_FILE into $OUTPUT_FILE"
python coolc.py ${INPUT_FILE} ${OUTPUT_FILE}
