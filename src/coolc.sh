#!/bin/bash
# Incluya aquí las instrucciones necesarias para ejecutar su compilador

INPUT_FILE=$1
OUTPUT_FILE=${INPUT_FILE:0: -2}mips
VERSION=0.2  # Release, branch
BUILD=$(wc -l .builds | awk '{ print $1 }')

# Si su compilador no lo hace ya, aquí puede imprimir la información de contacto
echo "pycoolc: version $VERSION"        # TODO: Recuerde cambiar estas
# echo "Build: $BUILD"
echo "Copyright (c) 2020 School of Math and Computer Science, University of Havana" # TODO: líneas a los valores correctos
#echo "Authors: Eliane Puerta, Adrian Gonzalez, Liset Alfaro"
# Llamar al compilador
python3 pycoolc.py $INPUT_FILE
