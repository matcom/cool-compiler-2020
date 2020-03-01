# Incluya aquí las instrucciones necesarias para ejecutar su compilador

INPUT_FILE=$1
OUTPUT_FILE=${INPUT_FILE:0: -2}mips

# Si su compilador no lo hace ya, aquí puede imprimir la información de contacto
echo "Tiger and Buti Compiler 2020 V0.2.0"        # TODO: Recuerde cambiar estas
echo "Copyright (c) 2020: José Gabriel Navarro Comabella, Alberto Helguera Fleitas"    # TODO: líneas a los valores correctos

# Llamar al compilador
echo "Compiling $INPUT_FILE into $OUTPUT_FILE"

python3.7 TigerandButiCompiler.py $INPUT_FILE
