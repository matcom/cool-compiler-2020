def p_program(self, p):
    'program : class_list'
    p[0] = ProgramNode(p[1])