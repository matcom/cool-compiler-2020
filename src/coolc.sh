# Incluya aqui las instrucciones necesarias para ejecutar su compilador

INPUT_FILE=$1
OUTPUT_FILE=${INPUT_FILE:0: -2}mips

# Si su compilador no lo hace ya, aqui puede imprimir la informacion de contacto
echo "Tiger and Buti Compiler 2020 V0.2.0"        # TODO: Recuerde cambiar estas
echo "Copyright (c) 2020: Jose Gabriel Navarro Comabella, Alberto Helguera Fleitas"    # TODO: lineas a los valores correctos

# Llamar al compilador

python TigerandButiCompiler.py $INPUT_FILE
