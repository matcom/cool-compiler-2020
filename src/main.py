from sys import argv
from os import system


INPUT_FILE = argv[1]
OUTPUT_FILE = f'{INPUT_FILE[0: -2]}mips'

print('CodeStrange Cool Compiler v0.1')
print('Copyright (c) 2020: Carlos Bermudez Porto, Leynier Gutiérrez González, Tony Raúl Blanco Fernández')

system(f'python coolc.py {INPUT_FILE} {OUTPUT_FILE}')
