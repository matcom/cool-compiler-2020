# Incluya aquí las instrucciones necesarias para ejecutar su compilador

INPUT_FILE=$1
OUTPUT_FILE=${INPUT_FILE:0: -2}mips

# Si su compilador no lo hace ya, aquí puede imprimir la información de contacto
echo "DLR MATCOM COOL COMPILER V 0.1"        # TODO: Recuerde cambiar estas
echo "Copyright (c) 2020: Leonel Alejandro García López, Jorge Daniel Valle Díaz, Roberto Marti Cedeño"    # TODO: líneas a los valores correctos

# Llamar al compilador
echo "Compiling $INPUT_FILE into $OUTPUT_FILE"
