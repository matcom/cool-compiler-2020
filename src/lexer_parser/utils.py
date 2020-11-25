"""
Copyright (c) 2020 School of Math and Computer Science, University of Havana

COOL compiler project
"""


def find_column(text, pos):
    line_start = text.rfind('\n', 0, pos) + 1
    tabs = text.count('\t', line_start, pos)
    return (pos - line_start) + 1 + 3 * tabs
