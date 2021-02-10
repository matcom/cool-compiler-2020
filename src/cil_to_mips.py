from AST_CIL import *
import visitor

class Build_Mips:
    def __init__(self, ast):
        self.lines = []
        self.current_function = None
        self.visit(ast)

    def add(self, line):
        self.lines.append(line)

    def stack_pos(self, name):
        temp = self.current_function.params + self.current_function.localvars
        index = 4*temp.index(name)
        return -index

    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(Program)
    def visit(self, program):

        self.add('.data')
        for _str, tag in program.data_section.items():
            self.add(tag + ':' + ' .asciiz ' + _str)
        self.add('.text')
        self.add('entry:')
        self.add('jal function_Main_main')
        self.add('li $v0, 10') #exit()
        self.add('syscall')
        for f in program.code_section:
            self.visit(f)

    @visitor.when(Function)
    def visit(self, function):
        #ya se pusieron los argumentos en la pila
        self.current_function = function
        self.add(function.fname + ':')        

        #ya se guardaron los argumentos en la pila
        #tenemos que guardar espacio para las variables locales        

        line = 'addi $sp, $sp, -' + str(4*len(function.localvars))  #espacio para las variables locales
        self.add(line)        

        self.add('addi $sp, $sp, -8')   # adjust stack for 2 item
        self.add('sw $ra, 4($sp)')      # save return address
        self.add('sw $fp, 0($sp)')      # save old frame pointer

        n = 4*(len(function.params) + len(function.localvars) + 1)
        self.add('addi $fp, $sp, {}'.format(n)) # fp apunta al primer argumento

        for intr in function.instructions:
            self.visit(intr)
        
        #restaurar los valores de los registros
        #poner el frame pointer donde estaba

        self.add('lw $ra, 4($sp)')#restauro direccion de retorno
        self.add('lw $t1, 0($sp)')
        self.add('addi $sp, $fp, 4')
        self.add('move $fp, $t1')
        
        self.add('jr $ra')    # and return
        self.current_function = None

    @visitor.when(Arg)
    def visit(self, arg):
        self.add('addi $sp, $sp, -4')   # adjust stack for 1 item
        #localizar el valor de arg en las variables locales
        index = self.stack_pos(arg.vinfo)
        #pasarlo a un registro
        self.add('lw $t1, {}($fp)'.format(index))
        self.add('sw $t1, 0($sp)')     # save argument for next function

    @visitor.when(Call)
    def visit(self, call):
        #ya se pusieron los argumentos en la pila
        self.add('jal ' + call.func)
        index = self.stack_pos(call.dest)
        self.add('sw $v0, {}($fp)'.format(index))

    @visitor.when(Load)
    def visit(self, load):
        index = self.stack_pos(load.dest)
        self.add('la $t1, {}'.format(load.msg))
        self.add('sw $t1, {}($fp)'.format(index))

    @visitor.when(Print)
    def visit(self, _print):
        self.add('li $v0, 4')		                    # system call code for print_str
        index = self.stack_pos(_print.str_addr)         #pos en la pila
        self.add('lw $a0, {}($fp)'.format(index)) 	    # str to print
        self.add('syscall')			                    # print it

    @visitor.when(Return)
    def visit(self, ret):
        index = self.stack_pos(ret.value)
        self.add('lw $t1, {}($fp)'.format(index))
        self.add('move $v0, $t1')