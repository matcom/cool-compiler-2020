
########################################## AST ####################################################


class AST:
	def __init__(self):
		pass

	@property
	def clsname(self):
		return str(self.__class__.__name__)

	def to_readable(self):
		return "{}".format(self.clsname)

	def __repr__(self):
		return self.__str__()

	def __str__(self):
		return str(self.to_readable()) + "\n"


##################################### PROGRAM #####################################################


class Program(AST):
	def __init__(self, type_section, data_section, code_section):
		super(Program, self).__init__()
		self.code_section = code_section
		self.data_section = data_section
		self.type_section = type_section

	def to_readable(self):
		ttype = ""
		for t in self.type_section:
			ttype += str(t)
		data = ""
		for t in self.data_section:
			data += str(t)
		code = ""
		for t in self.code_section:
			code += str(t)
		return "CIL\n\t.TYPE\n{}\n\t.DATA\n{}\n\t.CODE\n{}\n".format(ttype, data, code)



################################ TYPES, DATAS, STATEMENTS #########################################


class Type(AST):
	def __init__(self, name, attributes = {}, methods= {}):
		self.type_name = name
		self.attributes = attributes
		self.methods = methods

	def to_readable(self):
		attrs = ""
		for t in self.attributes:
			attrs += str(t) + "\t"
		m = ""
		for t in self.methods:
			m += str(t) + "\t"
		return "type {} {}\n\t{}\n\t{}\n{}\n".format(self.type_name, "{", attrs, m, "}")


class Data(AST):
	def __init__(self, dest, value):
		self.dest = dest
		self.value = value

	def to_readable(self):
		return "{} = {}\n".format(self.dest, self.value)


class Statement(AST):
	pass


#################################### ATTRIBUTE ###################################################

class TypeFeature(AST):
	pass

class Attribute(TypeFeature):
	def __init__(self, name):
		self.name = name

	def to_readable(self):
		return "attribute {}\n".format(self.name)

class Method(TypeFeature):
	def __init__(self, name, function_name):
		self.name = name
		self.function_name = function_name

	def to_readable(self):
		return "method {} : {}\n".format(self.name, self.function_name)


#################################### FUNCTION ####################################################


class Function(TypeFeature):
	def __init__(self, name, args, vlocals, body):
		self.name = name
		self.args = args
		self.vlocals = vlocals
		self.body = body

	def to_readable(self):
		args = ""
		for t in self.args:
			args += str(t) + "\t"
		args += "\n"
		vlocals = ""
		for t in self.vlocals:
			vlocals += str(t) + "\t"
		args += "\n"
		body = ""
		for t in self.body:
			body += str(t) + "\t"
		body += "\n"
		return "function {} {}\n\t{}\n\n\t{}\n\n\t{}\n{}\n".format(self.name, "{", args, vlocals, body, "}")



class ArgDeclaration(AST):
	def __init__(self, name):
		self.name = name

	def to_readable(self):
		return "PARAM {}\n".format(self.name)


class LocalDeclaration(AST):
	def __init__(self, name):
		self.name = name

	def to_readable(self):
		return "LOCAL {}\n".format(self.name)


#################################### STATEMENTS #################################################


class Assign(Statement):
	def __init__(self, dest, source):
		self.dest = dest
		self.source = source

	def to_readable(self):
		return "{} = {}\n".format(self.dest, self.source)

#----------- BinaryOperator

class BinaryOperator(Statement):
	def __init__(self, dest, left, right, op):
		self.dest = dest
		self.left = left
		self.right = right
		self.op = op

	def to_readable(self):
		return "{} = {} {} {}\n".format(self.dest, self.left, self.op, self.right)

class Plus(BinaryOperator):
	def __init__(self, dest, left, right):
		super(Plus, self).__init__(dest, left, right, "+")

class Minus(BinaryOperator):
	def __init__(self, dest, left, right):
		super(Minus, self).__init__(dest, left, right, "-")

class Mult(BinaryOperator):
	def __init__(self, dest, left, right):
		super(Mult, self).__init__(dest, left, right, "*")

class Div(BinaryOperator):
	def __init__(self, dest, left, right):
		super(Div, self).__init__(dest, left, right, "/")

#---------- COMPARISONS

class Equal(BinaryOperator):
	def __init__(self, dest, left, right):
		super(Equal, self).__init__(dest, left, right, "==")

class LessThan(BinaryOperator):
	def __init__(self, dest, left, right):
		super(LessThan, self).__init__(dest, left, right, "<")

class EqualOrLessThan(BinaryOperator):
	def __init__(self, dest, left, right):
		super(EqualOrLessThan, self).__init__(dest, left, right, "<=")

#---------- TYPES

class GetAttrib(Statement):
	def __init__(self, dest, instance, attribute):
		self.dest = dest
		self.instance = instance
		self.attribute = attribute

	def to_readable(self):
		return "{} = GETATTR {} {}\n".format(self.dest, self.instance, self.attribute)

class SetAttrib(Statement):
	def __init__(self, instance, attribute, src):
		self.instance = instance
		self.attribute = attribute
		self.src = src

	def to_readable(self):
		return "SETATTR {} {} {}\n".format(self.instance, self.attribute, self.src)

#---------- ARRAYS

# self.attribute will represent the index

class GetIndex(GetAttrib):
	def to_readable(self):
		return "{} = GETINDEX {} {}\n".format(self.dest, self.instance, self.attribute)


class SetIndex(SetAttrib):
	def to_readable(self):
		return "SETINDEX {} {} {}\n".format(self.instance, self.attribute, self.src)


################################ MEMORY STATEMENTS ##############################################


class TypeOf(Statement):
	def __init__(self, dest, instance):
		self.dest = dest
		self.instance = instance

	def to_readable(self):
		return "{} = TYPEOF {}\n".format(self.dest, self.instance)



class Allocate(Statement):
	def __init__(self, dest, ttype):
		self.dest = dest
		self.ttype = ttype

	def to_readable(self):
		return "{} = ALLOCATE {}\n".format(self.dest, self.ttype)


class Array(Statement):
	def __init__(self, dest, src):
		self.dest = dest
		self.src = src

	def to_readable(self):		
		return "{} = ARRAY {}\n".format(self.dest, self.src)




################################# DISPATCH STATEMENTS, RETURN #################################


class Call(Statement):
	def __init__(self, dest, f):
		self.dest = dest
		self.f = f

	def to_readable(self):
		return "{} = CALL {}\n".format(self.dest, self.f)


class VCall(Statement):
	def __init__(self, dest, ttype, f):
		self.dest = dest
		self.ttype = ttype
		self.f = f

	def to_readable(self):
		return "{} = VCALL {} {}\n".format(self.dest, self.ttype, self.f)		


class PushParam(Statement):
	def __init__(self, name):
		self.name = name

	def to_readable(self):
		return "ARG {}\n".format(self.name)

class PopParam(Statement):
	def __init__(self, name):
		self.name = name

	def to_readable(self):
		return "POP {}\n".format(self.name)

class Return(Statement):
	def __init__(self, value=None):
		self.value = value

	def to_readable(self):
		return "RETURN {}\n".format(self.value)

################################## JUMP STATEMENTS ###########################################


class Label(Statement):
	def __init__(self, name):
		self.name = name

	def to_readable(self):
		return "LABEL {}\n".format(self.name)

class Goto(Statement):
	def __init__(self, label):
		self.label = label

	def to_readable(self):
		return "GOTO {}\n".format(self.label)

class IfGoto(Statement):
	def __init__(self, condition, label):
		self.condition = condition
		self.label = label

	def to_readable(self):
		return "IF {} GOTO {}\n".format(self.condition, self.label)

######################################## STR STATEMENTS ######################################


class Load(Statement):
	def __init__(self, dest, msg):
		self.dest = dest
		self.msg = msg

	def to_readable(self):
		return "{} = LOAD {}\n".format(self.dest, self.msg)



class Length(Statement):
	def __init__(self, dest, str_addr):
		self.dest = dest
		self.str_addr = str_addr

	def to_readable(self):
		return "{} = LENGTH {}\n".format(self.dest, self.str_addr)


class Concat(Statement):
	def __init__(self, dest, first, second):
		self.dest = dest
		self.first = first
		self.second = second

	def to_readable(self):
		return "{} = CONCAT {} {}\n".format(self.dest, self.first, self.second)


class Substring(Statement):
	def __init__(self, dest, str_addr, pos_left=0, pos_right=-1):
		self.dest = dest
		self.str_addr = str_addr
		self.pos_left = pos_left
		self.pos_right = pos_right

	def to_readable(self):
		return "{} = SUBSTRING {} {} {}\n".format(self.dest, self.str_addr, self.pos_left, self.pos_right)


class ToString(Statement):
	def __init__(self, dest, num):
		self.dest = dest
		self.num = num

	def to_readable(self):
		return "{} = STR {}\n".format(self.dest, self.num)


#################################### IO STATEMENTS ###########################################


class Read(Statement):
	def __init__(self, dest):
		self.dest = dest

	def to_readable(self):
		return "{} = READ\n".format(self.dest)


class Print(Statement):
	def __init__(self, str_addr):
		self.str_addr = str_addr

	def to_readable(self):
		return "PRINT {}\n".format(self.str_addr)

