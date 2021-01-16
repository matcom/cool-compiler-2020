from AST_CIL import *
import visitor

class Build_Mips:
    def __init__(self, ast):
        self.lines = []
        self.visit(ast)
    
    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(Program)
    def visit(self, program):
        self.lines  +=  '.data'
        for _str, tag in program.data_section.items():
            self.lines += tag+':'+ ' .asciiz "' + _str + '"'
        self.lines += '.text'
        for f in program.code_section:
            self.visit(f)

    @visitor.when(Function)
    def visit(self, function):
        self.lines += function.fname + ':'
        self.lines += 'addi $sp, $sp, -4'   # adjust stack for 1 item
        self.lines += 'sw $ra, 4($sp)'      # save return address
        #self.lines += 'sw $a0, 0($sp)'      # save argument esto se hace antes de entrar a la funcion
        #ya se guardaron los argumentos en la pila
        #tenemos que guardar espacio para las variables locales
        self.lines += 'move $fp, $sp' #first word of the frame
        self.lines += 'addi $sp, $sp, -' + str(4*len(function.localvars))#espacio para las variables locales



    @visitor.when(Param)
    def visit(self, function):
        pass

    @visitor.when(Local)
    def visit(self, local):
        pass

    @visitor.when(Assign)
    def visit(self, assign):
        pass

    @visitor.when(Plus)
    def visit(self, plus):
        pass

    @visitor.when(Minus)
    def visit(self, minus):
        pass

    @visitor.when(Star)
    def visit(self, star):
        pass

    @visitor.when(Div)
    def visit(self, div):
        pass

    @visitor.when(GetAttrib)
    def visit(self, get):
        pass

    @visitor.when(SetAttrib)
    def visit(self, set):
        pass

    @visitor.when(Allocate)
    def visit(self, allocate):
        pass

    @visitor.when(TypeOf)
    def visit(self, typeOf):
        pass

    @visitor.when(Label)
    def visit(self, label):
        pass

    @visitor.when(Goto)
    def visit(self, goto):
        pass

    @visitor.when(GotoIf)
    def visit(self, gotoIf):
        pass

    @visitor.when(Call)
    def visit(self, call):
        pass

    @visitor.when(VCall)
    def visit(self, vCall):
        pass

    @visitor.when(Arg)
    def visit(self, arg):
        pass

    @visitor.when(Return)
    def visit(self, _return):
        pass

    @visitor.when(Load)
    def visit(self, load):
        pass

    @visitor.when(Length)
    def visit(self, length):
        pass

    @visitor.when(Concat)
    def visit(self, concat):
        pass

    @visitor.when(Prefix)
    def visit(self, prefix):
        pass

    @visitor.when(Substring)
    def visit(self, substr):
        pass

    @visitor.when(ToStr)
    def visit(self, toStr):
        pass

    @visitor.when(Read)
    def visit(self, read):
        pass

    @visitor.when(Print)
    def visit(self, _print):
        pass

    @visitor.when(IsVoid)
    def visit(self, isVoid):
        pass

    @visitor.when(LowerThan)
    def visit(self, loweThan):
        pass

    @visitor.when(LowerEqualThan)
    def visit(self, lowerEqualThan):
        pass

    @visitor.when(EqualThan)
    def visit(self, equalThan):
        pass

    @visitor.when(EqualStrThanStr)
    def visit(self, equalStrThanStr):
        pass
