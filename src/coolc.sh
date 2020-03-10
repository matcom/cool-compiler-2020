# Incluya aquí las instrucciones necesarias para ejecutar su compilador

INPUT_FILE=$1
OUTPUT_FILE=${INPUT_FILE:0: -2}mips

# Si su compilador no lo hace ya, aquí puede imprimir la información de contacto
echo "Lexer and Parser"        # TODO: Recuerde cambiar estas
echo "Carlos Martinez Molina y Eziel Ramos Pinon"    # TODO: líneas a los valores correctos

# Llamar al compilador
#echo "Compiling $INPUT_FILE into $OUTPUT_FILE"
#45280254
python parserTest.py ${INPUT_FILE} ${OUTPUT_FILE}