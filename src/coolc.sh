# Incluya aquí las instrucciones necesarias para ejecutar su compilador


INPUT_FILE=$1
OUTPUT_FILE=${INPUT_FILE:0: -2}mips


#El compilador va a ser un py.
#Aquí llamamos al compilador con los valores de la entrada estándar.



# Si su compilador no lo hace ya, aquí puede imprimir la información de contacto
echo "LINEA_CON_NOMBRE_Y_VERSION_DEL_COMPILADOR"        # TODO: Recuerde cambiar estas
echo "CopyLeft (L) 2020: Alejandro Díaz Roque, Rafael Horrach"    

# Llamar al compilador
python main.py "$@"
#echo "Compiling $INPUT_FILE into $OUTPUT_FILE"

