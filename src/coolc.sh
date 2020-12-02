#!/bin/bash
# Incluya aquí las instrucciones necesarias para ejecutar su compilador

INPUT_FILE=$1
OUTPUT_FILE=${INPUT_FILE:0: -2}mips
VERSION=0.2  # Release, Minor
BUILD=$(wc -l .builds | awk '{ print $1 }')

# Si su compilador no lo hace ya, aquí puede imprimir la información de contacto
echo "pycoolc: version $VERSION Developed by Eliane Puerta, Liset Alfaro, Adrian Gonzalez"
# echo "Build: $BUILD"
echo "Copyright (c) 2020 School of Math and Computer Science, University of Havana"
python pycoolc.py $INPUT_FILE
