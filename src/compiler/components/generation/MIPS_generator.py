from compiler.utils.visitors_definitions import NodeVisitor
import compiler.components.generation.CIL_definitions as cil
from compiler.utils.config import *


class MipsVisitor(NodeVisitor):
	def __init__(self, programContext):
		super().__init__(programContext= programContext)
		self.buffer= []
		self.type_index= []
		self.dispatchtable_code= []
		self.prototypes_code= []
		self.cur_labels_id = 0
		self.offset= {}
		self.code = ""
	
	def push(self):
		self.write_info('sw $a0 0($sp)')
		self.write_info('addiu $sp $sp -4')

	def pop(self, dest=None):
		self.write_info(f'addiu $sp $sp 4')

	def write_info(self, msg, tabbed= True):
		info = "{}{}\n".format("\t" if tabbed else "", msg)
		self.code += info
		self.buffer.append(info)
	
	def allocate_memory(self, size=None, register=False):
		if register:
			self.write_info('move $a0 {}'.format(size))
		else:
			if size:
				self.write_info('li $a0 {}'.format(size))
		self.write_info('li $v0 9')
		self.write_info('syscall')

	def new_labels_id(self):
		self.cur_labels_id += 1
		return self.cur_labels_id

	def visit_Data(self, node: cil.Data):
		self.write_info(f'{node.dest}: .align 2 \n \t\t\t.asciiz \"{str(node.value.encode())[2:-1]}\"')

	def visit_Program(self, node: cil.Program):
		#-------------------- DATA SECTION ----------------------------
		
		self.write_info('.data', tabbed= False)
		self.static_datas()	

		for data in node.data_section:
			self.visit(data)
		
		self.write_info('')
		for i in range(len(node.type_section)):
			self.type_index.append(node.type_section[i].type_name)
			self.write_info('classname_{}: .align 2 \n\t\t\t.asciiz \"{}\"'.format(node.type_section[i].type_name,
							node.type_section[i].type_name))

		self.write_info(f'type_void: .align 2 \n\t\t\t .asciiz \"\"')

		#-------------------- TEXT SECTION ----------------------------

		self.write_info('\n.text', tabbed= False)
		self.entrypoint()

		for t in node.type_section:
			self.visit(t)

		self.write_info('\n########## STATIC FUNCTIONS ##########\n')
		# CONFORMS
		self.conforms()
		# IS_VOID
		self.isvoid()
		# OBJECT
		self.object_abort()
		self.object_copy()
		self.object_typename()
		# STRING
		self.string_length()
		self.string_concat()
		self.string_substr()
		# IO
		self.io_in_int()
		self.io_in_string()
		self.io_out_int()
		self.io_out_string()
		
		self.write_info('\n############## TABLES ################\n')
		# Generate method that creates classes's name table
		self.write_info('function_build_class_name_table:', tabbed=False)
		self.allocate_memory(len(node.type_section) * 4)
		self.write_info('move $s1 $v0') # save the address of the table in a register
		for i in range(len(node.type_section)):
			self.write_info('la $t1 classname_{}'.format(node.type_section[i].type_name))
			self.write_info('sw $t1 {}($s1)'.format(4 * i))
		self.write_info('jr $ra')
		self.write_info('')

		# Generate method that allocates memory for prototypes table
		self.write_info('function_allocate_prototypes_table:', tabbed=False)
		self.allocate_memory(8 * len(self.type_index))
		self.write_info('move $s0 $v0') # save the address of the table in a register
		self.write_info('jr $ra')
		self.write_info('')

		# Generate mips method that builds prototypes
		self.write_info('function_build_prototypes:', tabbed=False)
		for ins in self.prototypes_code:
			self.write_info(ins)
		self.write_info('jr $ra')
		self.write_info('')

		# Generate mips method that builds dispatch tables
		self.write_info('function_build_dispatch_tables:', tabbed=False)
		for ins in self.dispatchtable_code:
			self.write_info(ins)
		self.write_info('jr $ra')
		self.write_info('')
		
		# Generate method that builds class parents table
		self.write_info('function_build_class_parents_table:', tabbed=False)
		self.allocate_memory(4 * len(self.type_index))
		self.write_info('move $s2 $v0') # save the address of the table in a register
		self.write_info('')

		# Fill table entry for each class type
		for parent in node.type_section:
			if parent.type_name != 'void':
				p_index = self.type_index.index(parent.type_name)
				for child in self.programContext.types[parent.type_name].children:
					ch_index = self.type_index.index(child)
					self.write_info(f'li $t0 {ch_index}')
					self.write_info(f'mul $t0 $t0 4')
					self.write_info(f'add $t0 $t0 $s2')
					self.write_info(f'li $t1 {p_index}')
					self.write_info(f'sw $t1 0($t0)')
					self.write_info('')

		self.write_info('jr $ra')
		self.write_info('')


		# Generate COOL functions
		self.write_info('\n########### COOL FUNCTIONS ##########\n')
		for func in node.code_section:
			is_built_in = False
			if not '__init' in func.name:
				is_built_in = [x for x in self.programContext.basics if f'{x}_' in func.name] != []
			if not is_built_in:
				self.visit(func)
		self.write_info('\n#####################################\n')
		return self.buffer


	
	def visit_Function(self, node: cil.Function):
		self.code = ""
		self.write_info(f'function_{node.name}:', tabbed=False)

		# Set up stack frame
		self.write_info(f'move $fp, $sp')
		self.write_info(f'subu $sp, $sp, {4 * len(node.vlocals)}')

		# Register arguments offsets
		for i in range(len(node.args)):
			self.offset[node.args[i].name] = 12 + i * 4

		# Register locals offsets
		for i in range(len(node.vlocals)):
			self.offset[node.vlocals[i].name] = i * (-4)

		# Generate mips code for the function's body
		for inst in node.body:
			# Equal node needs unique id for its labels
			if isinstance(inst, cil.Equal) or isinstance(inst, cil.Div):
				inst.id = self.new_labels_id()

			self.visit(inst)

		# Pop the stack frame
		self.write_info(f'addiu $sp, $sp, {4 * len(node.vlocals)}')

		# Return
		self.write_info('jr $ra')
		self.write_info('')			
	
	def visit_PushParam(self, node: cil.PushParam):
		self.write_info('# PUSHPARAM')
		if node.name[0] != "_":
			self.write_info('li $a0, {}'.format(self.type_index.index(node.name)))
		else:
			self.write_info('lw $a0, {}($fp)'.format(self.offset[node.name]))
		self.push()
		self.write_info('')


	def visit_PopParam(self, node: cil.PopParam):
		self.write_info('# POPPARAM')
		self.pop(node.name)
		self.write_info('')	
	
	def visit_Return(self, node: cil.Return):
		self.write_info('# RETURN')
		self.write_info('lw $v0, {}($fp)'.format(self.offset[node.value]))

	def visit_Call(self, node: cil.Call):
		self.write_info('# CALL')

		# Save return address and frame pointer
		self.write_info(f'addiu $sp, $sp, -8')
		self.write_info(f'sw $ra, 4($sp)')
		self.write_info(f'sw $fp, 8($sp)')

		# Call the function
		self.write_info(f'jal function_{node.f}')

		# Restore return address and frame pointer
		self.write_info(f'lw $fp, 8($sp)')
		self.write_info(f'lw $ra, 4($sp)')
		self.write_info(f'addiu $sp, $sp, 8')

		if node.dest:
			self.write_info(f'sw $v0 {self.offset[node.dest]}($fp)')

		self.write_info('')
	
	def visit_GetAttrib(self, node: cil.GetAttrib):
		self.write_info('# GETATTR')
		self.write_info(f'lw $a1 {self.offset[node.instance]}($fp)')
		self.write_info(f'lw $a0 {12 + 4 * node.attribute}($a1)')
		self.write_info(f'sw $a0 {self.offset[node.dest]}($fp)')
		self.write_info('')

	def visit_Allocate(self, node: cil.Allocate):
		self.write_info('# ALLOCATE')
		if node.ttype == 'void':
			self.write_info(f'la $v0 type_void')
			self.write_info(f'sw $v0 {self.offset[node.dest]}($fp)')			
		else:
			offset_proto = self.type_index.index(node.ttype) * 8
			self.write_info('lw $t0 {}($s0)'.format(offset_proto))
			self.write_info('sw $t0, 0($sp)')
			self.write_info('addiu $sp, $sp, -4')
			self.write_info('')
			self.visit(cil.Call(dest = node.dest, f = "Object_copy"))
			self.write_info('addiu $sp, $sp, 4')
		self.write_info('')


	def visit_SetAttrib(self, node: cil.SetAttrib):
		self.write_info('# SETATTR')
		self.write_info(f'lw $a1 {self.offset[node.instance]}($fp)')
		if isinstance(node.src, int):
			self.write_info(f'li $a0, {node.src}')
		elif node.src[:5] == "data_":
			self.write_info(f'la $a0, {node.src}')
		else:
			self.write_info(f'lw $a0 {self.offset[node.src]}($fp)')
		self.write_info(f'sw $a0 {12 + 4 * node.attribute}($a1)')
		self.write_info('')

	def visit_TypeOf(self, node: cil.TypeOf):
		self.write_info('# TYPEOF')
		self.write_info(f'lw $a1 {self.offset[node.instance]}($fp)')
		self.write_info(f'lw $a0 0($a1)')
		self.write_info(f'sw $a0 {self.offset[node.dest]}($fp)')
		self.write_info('')

	def visit_VCall(self, node: cil.VCall):
		self.write_info('# VCALL')

		# Save return address and frame pointer
		self.write_info(f'addiu $sp, $sp, -8')
		self.write_info(f'sw $ra, 4($sp)')
		self.write_info(f'sw $fp, 8($sp)')

		if node.ttype[0] == "_":
			# If node.type is a local CIL variable
			self.write_info(f'lw $a2, {self.offset[node.ttype]}($fp)')
		else:
			# If node.type a type name
			self.write_info(f'li $a2, {self.type_index.index(node.ttype)}')
		self.write_info(f'mul $a2, $a2, 8')
		self.write_info(f'addu $a2, $a2, $s0')
		self.write_info(f'lw $a1, 0($a2)')

		# Check the dispatch table for the method's address
		self.write_info(f'lw $a2, 8($a1)')
		self.write_info(f'lw $a0 {node.f * 4}($a2)')

		# Call the function at 0($a0)
		self.write_info(f'jalr $a0')

		# Restore return address and frame pointer
		self.write_info(f'lw $fp, 8($sp)')
		self.write_info(f'lw $ra, 4($sp)')
		self.write_info(f'addiu $sp, $sp, 8')

		# Save value after restoring $fp
		self.write_info(f'sw $v0 {self.offset[node.dest]}($fp)')

		# Check prototypes table for the dynamic type
		if node.ttype[0] != '_':
			self.write_info(f'li $a2, {self.type_index.index(node.ttype)}')
		else:
			self.write_info(f'lw $a2, {self.offset[node.ttype]}($fp)')

		self.write_info('')


	def visit_Type(self, node: cil.Type):
		# Allocate
		self.dispatchtable_code.append(f'# Type {node.type_name}')
		self.dispatchtable_code.append('li $a0 {}'.format(4 * len(node.methods)))
		self.dispatchtable_code.append('li $v0 9')
		self.dispatchtable_code.append('syscall')

		# Add dispatch table code
		for i in range(len(node.methods)):
			self.dispatchtable_code.append('la $t1 function_{}'.format(node.methods[i].function_name))
			self.dispatchtable_code.append('sw $t1 {}($v0)'.format(4 * i))
		self.dispatchtable_code.append('lw $t0 {}($s0)'.format(8 * self.type_index.index(node.type_name)))
		self.dispatchtable_code.append('sw $v0 8($t0)')
		self.dispatchtable_code.append('')

		# Allocate
		self.prototypes_code.append(f'# Type {node.type_name}')
		self.prototypes_code.append('li $a0 {}'.format(12 + 4 * len(node.attributes)))
		self.prototypes_code.append('li $v0 9')
		self.prototypes_code.append('syscall')

		# Add prototype code
		class_index = self.type_index.index(node.type_name)
		self.prototypes_code.append('li $a0 {}'.format(class_index))
		self.prototypes_code.append('sw $a0 0($v0)')
		self.prototypes_code.append('li $a0 {}'.format(12 + 4 * len(node.attributes)))
		self.prototypes_code.append('sw $a0 4($v0)')
		self.prototypes_code.append('sw $v0 {}($s0)'.format(8 * class_index))
		self.prototypes_code.append('')

####################### STATIC FUNCTIONS #######################

	#----- STATIC DATAs

	def static_datas(self):
		# Buffer for reading strings
		self.write_info('str_buffer: .space 1024')		
		self.write_info('')

		# Declare error mensages
		self.write_info('_index_negative_msg: .align 2 \n\t\t\t .asciiz \"Index to substr is negative\\n\"')
		self.write_info('_index_out_msg: .align 2 \n\t\t\t .asciiz \"Index out range exception\\n\"')
		self.write_info('_abort_msg: .align 2 \n\t\t\t .asciiz \"Execution aborted\\n\"')
		self.write_info('_div_zero_msg: .align 2 \n\t\t\t .asciiz \"Division by zero exception\\n\"')

		self.write_info('')

	def entrypoint(self):
		self.write_info('main:', tabbed=False)
		self.visit(cil.Call(dest = None, f = 'build_class_name_table'))
		self.visit(cil.Call(dest = None, f = 'allocate_prototypes_table'))
		self.visit(cil.Call(dest = None, f = 'build_prototypes'))
		self.visit(cil.Call(dest = None, f = 'build_dispatch_tables'))
		self.visit(cil.Call(dest = None, f = 'build_class_parents_table'))
		self.visit(cil.Allocate(dest = None, ttype = 'Main'))

		# Push main self
		self.write_info('sw $v0 0($sp)')
		self.write_info('addiu $sp $sp -4')

		self.visit(cil.Call(dest = None, f = f'Main__init'))
		self.write_info('addiu $sp $sp 4')

		# Push main self
		self.write_info('sw $v0 0($sp)')
		self.write_info('addiu $sp $sp -4')

		self.visit(cil.Call(dest = None, f = 'Main_main'))
		self.write_info('addiu $sp $sp 4')

		self.write_info('li $v0 10')
		self.write_info('syscall')


	#----- OBJECT METHODS

	def object_abort(self):
		self.write_info('function_Object_abort:', tabbed=False)
		# Set up stack frame
		self.write_info('move $fp, $sp')

		# Aborting
		self.write_info('li $v0 10')
		self.write_info('syscall')
		self.write_info('')

	def object_copy(self):
		self.write_info('function_Object_copy:', tabbed=False)
		# Set up stack frame
		self.write_info(f'move $fp, $sp')

		self.write_info('lw $t0 12($fp)')# recoger la instancia a copiar
		self.write_info('lw $a0 4($t0)')
		self.write_info('move $t4 $a0')
		self.write_info('li $v0 9')
		self.write_info('syscall')# guarda en v0 la direccion de memoria que se reservo
		self.write_info('move $t2 $v0')# salvar la direccion donde comienza el objeto
		self.write_info('li $t3 0') # size ya copiado
		self.write_info('_objcopy_loop:', tabbed=False)
		self.write_info('lw $t1 0($t0)') # cargar la palabra por la que voy
		self.write_info('sw $t1 0($v0)') # copiar la palabra
		self.write_info('addiu $t0 $t0 4') # posiciona el puntero en la proxima palabra a copiar
		self.write_info('addiu $v0 $v0 4')	# posiciona el puntero en la direccion donde copiar la proxima palabra
		self.write_info('addiu $t3 $t3 4') # actualizar el size copiado
		self.write_info('ble $t4 $t3 _objcopy_loop') # verificar si la condicion es igual o menor igual
		self.write_info('_objcopy_div_end_:', tabbed=False)
		self.write_info('move $v0 $t2') # dejar en v0 la direccion donde empieza el nuevo objeto
		self.write_info('jr $ra')
		self.write_info('')

	def object_typename(self):
		self.write_info('function_Object_type_name:', tabbed=False)
		# Set up stack frame
		self.write_info(f'move $fp, $sp')

		# Box the string reference
		self.visit(cil.Allocate(dest = None, ttype = "String"))		# Create new String object
		self.write_info('move $v1 $v0')

		# Box string's length
		self.visit(cil.Allocate(dest = None, ttype = "Int")	)		# Create new Int object

		self.write_info('lw $a1 12($fp)')			# self
		self.write_info('lw $a1 0($a1)')
		self.write_info('mul $a1 $a1 4')			# self's class tag
		self.write_info('addu $a1 $a1 $s1')			# class name table entry address
		self.write_info('lw $a1 0($a1)')				# Get class name address

		self.write_info('move $a2 $0')				# Compute string's length
		self.write_info('move $t2 $a1')
		self.write_info('_str_len_clsname_:', tabbed=False)
		self.write_info('lb $a0 0($t2)')
		self.write_info('beq $a0 $0 _end_clsname_len_')
		self.write_info('addiu $a2 $a2 1')
		self.write_info('addiu $t2 $t2 1')
		self.write_info('j _str_len_clsname_')
		self.write_info('_end_clsname_len_:', tabbed=False)

		self.write_info('sw $a2, 12($v0)')			# Store string's length

		self.write_info('sw $v0, 12($v1)')			# Fill String attributes
		self.write_info('sw $a1, 16($v1)')

		self.write_info('move $v0 $v1')
		self.write_info('jr $ra')
		self.write_info('')


	#----- STRING METHODS

	def string_length(self):
		self.write_info('function_String_length:', tabbed=False)
		# Set up stack frame
		self.write_info(f'move $fp, $sp')

		self.write_info('lw $a0 12($fp)')			# Self
		self.write_info('lw $v0 12($a0)')
		self.write_info('jr $ra')
		self.write_info('')

	def string_concat(self):
		self.write_info('function_String_concat:', tabbed=False)
		# Set up stack frame
		self.write_info(f'move $fp, $sp')

		self.visit(cil.Allocate(dest = None, ttype = "Int"))		# Create new Int object
		self.write_info('move $v1 $v0')												# Save new Int Object

		self.visit(cil.Allocate(dest = None, ttype = "String"))		# Create new String object
		self.write_info('move $t3 $v0')			# Store new String object

		self.write_info('lw $a1 12($fp)')		# Self
		self.write_info('lw $a2 16($fp)')		# Boxed String to concat

		self.write_info('lw $t1 12($a1)')		# Self's length Int object
		self.write_info('lw $t1 12($t1)')		# Self's length

		self.write_info('lw $t2 12($a2)')		# strings to concat's length Int object
		self.write_info('lw $t2 12($t2)')		# strings to concat's length

		self.write_info('addu $t0 $t2 $t1') 		# New string's length
		self.write_info('sw $t0 12($v1)')			# Store new string's length into box

		self.write_info('lw $a1 16($a1)')		# Unbox strings
		self.write_info('lw $a2 16($a2)')

		self.write_info('addiu $t0 $t0 1')		# Add space for \0
		self.allocate_memory('$t0', register=True)	# Allocate memory for new string
		self.write_info('move $t5 $v0')					# Keep the string's reference in v0 and use t7


		# a1: self's string		a2: 2nd string			t1: length self     t2: 2nd string length
		#									v1: new string's int object

		self.write_info('move $t4 $a1')			# Index for iterating the self string
		self.write_info('addu $a1 $a1 $t1')		# self's copy limit
		self.write_info('_strcat_copy_:', tabbed=False)
		self.write_info('beq $t4 $a1 _end_strcat_copy_')	# No more characters to copy

		self.write_info('lb $a0 0($t4)')			# Copy the character
		self.write_info('sb $a0 0($t5)')

		self.write_info('addiu $t5 $t5 1')		# Advance indices
		self.write_info('addiu $t4 $t4 1')
		self.write_info('j _strcat_copy_')
		self.write_info('_end_strcat_copy_:', tabbed=False)

		# Copy 2nd string

		self.write_info('move $t4 $a2')			# Index for iterating the strings
		self.write_info('addu $a2 $a2 $t2')		# self's copy limit
		self.write_info('_strcat_copy_snd_:', tabbed=False)
		self.write_info('beq $t4 $a2 _end_strcat_copy_snd_')	# No more characters to copy

		self.write_info('lb $a0 0($t4)')			# Copy the character
		self.write_info('sb $a0 0($t5)')

		self.write_info('addiu $t5 $t5 1')		# Advance indices
		self.write_info('addiu $t4 $t4 1')
		self.write_info('j _strcat_copy_snd_')
		self.write_info('_end_strcat_copy_snd_:', tabbed=False)

		self.write_info('sb $0 0($t5)')			# End string with \0

		# $v0: reference to new string			$v1: length int object
		# 						$t3: new string object
		# -> Create boxed string

		self.write_info('sw $v1 12($t3)')		# New length
		self.write_info('sw $v0 16($t3)')		# New string

		self.write_info('move $v0 $t3')			# Return new String object in $v0
		self.write_info('jr $ra')
		self.write_info('')

	def string_substr(self):
		self.write_info('function_String_substr:', tabbed=False)
		# Set up stack frame
		self.write_info(f'move $fp, $sp')
		self.write_info(f'lw $t5 12($fp)') # self param
		self.write_info(f'lw $a1 16($fp)') # reference of object int that represent i
		self.write_info(f'lw $a1 12($a1)') # value of i
		self.write_info(f'lw $a2 20($fp)') # reference of object int that represent j
		self.write_info(f'lw $a2 12($a2)') # value of j that is length to copy
		self.write_info(f'blt $a1 $0 _index_negative') # index i is negative
		self.write_info(f'blt $a2 $0 _index_negative') # length j is negative
		self.write_info(f'add $a2 $a1 $a2') # finish index
		self.write_info(f'lw $a3 12($t5)')
		self.write_info(f'lw $a3 12($a3)') # length of string
		self.write_info(f'bgt $a2 $a3 _index_out') # j > lenght

		# not errors
		self.visit(cil.Allocate(dest = None, ttype = "String"))
		self.write_info(f'move $v1 $v0') # new string

		self.visit(cil.Allocate(dest = None, ttype = "Int"))
		self.write_info(f'move $t0 $v0') # lenght of string
		self.write_info(f'move $t7 $a2')
		self.write_info(f'subu $t7 $t7 $a1')
		self.write_info(f'sw $t7 12($t0)') # save number that represent lenght of new string

		self.allocate_memory('$a2', register=True)	# $v0 -> address of the string

		self.write_info(f'sw $t0 12($v1)') # store length
		self.write_info(f'sw $v0 16($v1)') # store address of new string to String object

		# generate substring
		self.write_info('move $t1 $v0')				# Index for iterating the new string	
		
		self.write_info('lw $t5 16($t5)')			# Index for iterating the self string
		self.write_info('move $t4 $t5')
		self.write_info('addu $t4 $t4 $a1') # self's copy start
		self.write_info('addu $t5 $t5 $a2')	# self's copy limit

		self.write_info('_substr_copy_:', tabbed=False)
		self.write_info('bge $t4 $t5 _end_substr_copy_')	# No more characters to copy

		self.write_info('lb $a0 0($t4)')			# Copy the character
		self.write_info('sb $a0 0($t1)')

		self.write_info('addiu $t1 $t1 1')		# Advance indices
		self.write_info('addiu $t4 $t4 1')
		self.write_info('j _substr_copy_')

		# errors sections
		self.write_info(f'_index_negative:',tabbed=False)
		self.write_info(f'la $a0 _index_negative_msg')	
		self.write_info(f'b _subst_abort')

		self.write_info(f'_index_out:',tabbed=False)
		self.write_info(f'la $a0 _index_out_msg')	
		self.write_info(f'b _subst_abort')

		# abort execution 
		self.write_info(f'_subst_abort:',tabbed=False)
		self.write_info(f'li $v0 4') 
		self.write_info(f'syscall')
		self.write_info('la	$a0 _abort_msg')
		self.write_info(f'li $v0 4')
		self.write_info(f'syscall')
		self.write_info(f'li $v0 10')
		self.write_info(f'syscall') # exit

		# successful execution 
		self.write_info('_end_substr_copy_:', tabbed=False)

		self.write_info('move $v0 $v1')
		self.write_info('jr $ra')
		self.write_info('')

	#----- IO

	def io_in_int(self):
		self.write_info('function_IO_in_int:', tabbed=False)
		# Set up stack frame
		self.write_info(f'move $fp, $sp')

		self.visit(cil.Allocate(dest = None, ttype = "Int"))			# Create new Int object

		self.write_info('move $t0 $v0')				# Save Int object

		self.write_info('li $v0 5')					# Read int
		self.write_info('syscall')

		self.write_info('sw $v0 12($t0)')			# Store int

		self.write_info('move $v0 $t0')
		self.write_info('jr $ra')
		self.write_info('')

	def io_in_string(self):
		self.write_info('function_IO_in_string:', tabbed=False)
		# Set up stack frame
		self.write_info(f'move $fp, $sp')

		self.visit(cil.Allocate(dest = None, ttype = "Int"))		# Create new Int object for string's length
		self.write_info('move $v1 $v0')			# $v1: Int pbject

		self.visit(cil.Allocate(dest = None, ttype = "String"))			# Create new String object
		self.write_info('sw $v1 12($v0)')
		self.write_info('move $t5 $v0')			# $t5: String object

		# Read String and store in a temp buffer
		self.write_info('la $a0 str_buffer')
		self.write_info('li $a1 1025')
		self.write_info('li $v0 8')					# Read string
		self.write_info('syscall')

		# Compute string's length
		self.write_info('move $a0 $0')
		self.write_info('la $t2 str_buffer')
		self.write_info('_in_string_str_len_:', tabbed=False)
		self.write_info('lb $t0 0($t2)')
		self.write_info('beq $t0 $0 _end_in_string_str_len_')
		self.write_info('beq $t0 10 _end_in_string_str_len_')
		self.write_info('addiu $a0 $a0 1')
		self.write_info('addiu $t2 $t2 1')
		self.write_info('j _in_string_str_len_')
		self.write_info('_end_in_string_str_len_:', tabbed=False)

		# Store string's length into Integer class
		self.write_info('sw $a0 12($v1)')

		# Allocate size in $a0 ... string's length
		self.allocate_memory()

		# $a0: string's length 			$v0: string's new address			$t5: String object

		# Copy string from buffer to new address
		self.write_info('la $t4 str_buffer')			# Index for iterating the string buffer
		self.write_info('move $t1 $v0')					# Index for iterating new string address

		self.write_info('_in_str_copy_:', tabbed=False)
		self.write_info('lb $t0 0($t4)')			# Load a character
		self.write_info('beq $t0 $0 _end_in_str_copy_')	# No more characters to copy
		self.write_info('beq $t0 10 _end_in_str_copy_')	# No more characters to copy

		self.write_info('sb $t0 0($t1)')			# Copy the character

		self.write_info('addiu $t4 $t4 1')		# Advance indices
		self.write_info('addiu $t1 $t1 1')
		self.write_info('j _in_str_copy_')
		self.write_info('_end_in_str_copy_:', tabbed=False)

		# Store string
		self.write_info('sw $v0 16($t5)')	

		# Clean string buffer
		self.write_info('la $t4 str_buffer')			# Index for iterating the string buffer
		self.write_info('_in_str_clean_:', tabbed=False)
		self.write_info('lb $t0 0($t4)')			# Load a character
		self.write_info('beq $t0 $0 _end_in_str_clean_')	# No more characters to clean

		self.write_info('sb $0 0($t4)')			# Clean the character

		self.write_info('addiu $t4 $t4 1')		# Advance indices
		self.write_info('j _in_str_clean_')
		self.write_info('_end_in_str_clean_:', tabbed=False)

		# Return new string in $v0
		self.write_info('move $v0 $t5')
		self.write_info('jr $ra')
		self.write_info('')

	def io_out_int(self):
		self.write_info('function_IO_out_int:', tabbed=False)
		# Set up stack frame
		self.write_info(f'move $fp, $sp')

		self.write_info('lw $a0 16($fp)')			# Get Int object
		self.write_info('lw $a0 12($a0)')

		self.write_info('li $v0 1')					# Print int
		self.write_info('syscall')

		self.write_info('lw $v0 12($fp)')			# Return self
		self.write_info('jr $ra')
		self.write_info('')

	def io_out_string(self):
		self.write_info('function_IO_out_string:', tabbed=False)
		# Set up stack frame
		self.write_info(f'move $fp, $sp')

		self.write_info('lw $a0 16($fp)')			# Get String object
		self.write_info('lw $a0 16($a0)')

		self.write_info('li $v0 4')					# Print string
		self.write_info('syscall')

		self.write_info('lw $v0 12($fp)')				# Return self
		self.write_info('jr $ra')
		self.write_info('')

	#------ CONFORMS

	def conforms(self):
		self.write_info(f'function___conforms:', tabbed=False)
		# Set up stack frame
		self.write_info(f'move $fp, $sp')

		self.write_info(f'lw $t0 12($fp)')		# First arg's class tag
		self.write_info(f'lw $t1 16($fp)')		# Second arg's class tag

		# 2nd arg == Object -> return true
		self.write_info(f'beq $t1 {self.type_index.index("Object")} _conforms_ret_true_')	

		self.write_info('_conforms_loop_:', tabbed=False)

		# current == 2nd arg -> return true
		self.write_info('beq $t0 $t1 _conforms_ret_true_')	

		# current == Object -> return false
		self.write_info(f'beq $t0 {self.type_index.index("Object")} _conforms_ret_false_')		

		# Query parents's class tag from $s2 ... class parent table
		self.write_info('mul $t0 $t0 4')
		self.write_info('addu $t0 $t0 $s2')		
		self.write_info('lw $t0 0($t0)')			# current = current.parent
		self.write_info('j _conforms_loop_')
		
		self.write_info('_conforms_ret_true_:', tabbed=False)
		self.write_info('li $v0 1')
		self.write_info('j _conforms_ret_')

		self.write_info('_conforms_ret_false_:', tabbed=False)
		self.write_info('li $v0 0')
		
		# No need to store result in a Bool class
		self.write_info('_conforms_ret_:')
		self.write_info('jr $ra')
		self.write_info('')
	
	#------ ISVOID

	def isvoid(self):
		self.write_info(f'function__isvoid:', tabbed=False)
		# Set up stack frame
		self.write_info(f'move $fp, $sp')

		self.visit(cil.Allocate(dest = None, ttype = "Bool"))
		# $v0 contains new Bool object

		self.write_info(f'lw $t0 12($fp)')					# 1st arg is an object address
		self.write_info(f'la $t1 type_void')

		self.write_info(f'beq $t0 $t1 _is_void_true_')	# arg == void type
		self.write_info(f'sw $0 12($v0)')					# return False
		self.write_info(f'j _is_void_end_')

		self.write_info(f'_is_void_true_:', tabbed=False)
		self.write_info(f'li $t0 1')
		self.write_info(f'sw $t0 12($v0)')					# return True
		self.write_info(f'_is_void_end_:', tabbed=False)

		# Return Bool object in $v0
		self.write_info(f'jr $ra')
		self.write_info(f'')

############################# COMPARISONS ####################################

	def visit_Equal(self, node: cil.Equal):
		self.write_info('lw $t0 {}($fp)'.format(self.offset[node.left]))
		self.write_info('lw $t1 {}($fp)'.format(self.offset[node.right]))
		self.write_info(f'beq $t0 $zero _eq_false_{node.id}_')  # $t0 can't also be void
		self.write_info(f'beq $t1 $zero _eq_false_{node.id}_') # $t1 can't also be void
		self.write_info('lw $a0 0($t0)')	# get object 1 tag
		self.write_info('lw $a1 0($t1)')	# get object 2 tag
		self.write_info(f'bne $a0 $a1 _eq_false_{node.id}_')	# compare tags
		self.write_info('li $a2 {}'.format(self.type_index.index("Int")))	# load int tag
		self.write_info(f'beq $a0 $a2 _eq_int_bool_{node.id}')	# Integers
		self.write_info('li $a2 {}'.format(self.type_index.index("Bool")))	# load bool tag
		self.write_info(f'beq $a0 $a2 _eq_int_bool_{node.id}')	# Booleans
		self.write_info('li $a2 {}'.format(self.type_index.index("String")))   # load string tag
		self.write_info(f'bne $a0 $a2 _not_basic_type_{node.id}_') # Not a primitive type

		# equal strings
		# verify len of the strings
		self.write_info(f'_eq_str_{node.id}_:', tabbed = False) 	# handle strings
		self.write_info('lw	$t3 12($t0)')  # get string_1 size
		self.write_info('lw	$t3 12($t3)')  # unbox string_1 size
		self.write_info('lw	$t4, 12($t1)') # get string_2 size
		self.write_info('lw	$t4, 12($t4)') # unbox string_2 size
		self.write_info(f'bne $t3 $t4 _eq_false_{node.id}_') # string size are distinct
		self.write_info(f'beq $t3 $0 _eq_true_{node.id}_')	  # if strings are empty

		# Verify ascii secuences
		self.write_info('addu $t0 $t0 16')	# Point to start of string s1
		self.write_info('lw $t0 0($t0)')
		self.write_info('addu $t1 $t1 16') 	# Point to start of string s2
		self.write_info('lw $t1 0($t1)')
		self.write_info('move $t2 $t3')		# Keep string length as counter
		self.write_info(f'_verify_ascii_sequences_{node.id}_:', tabbed = False)
		self.write_info('lb $a0 0($t0)')	# get char of s1
		self.write_info('lb $a1 0($t1)')	# get char of s2
		self.write_info(f'bne $a0 $a1 _eq_false_{node.id}_') # char s1 /= char s2
		self.write_info('addu $t0 $t0 1')
		self.write_info('addu $t1 $t1 1')
		self.write_info('addiu $t2 $t2 -1')	# Decrement counter
		self.write_info(f'bnez $t2 _verify_ascii_sequences_{node.id}_')
		self.write_info(f'b _eq_true_{node.id}_')		# end of strings

		self.write_info(f'_not_basic_type_{node.id}_:', tabbed = False)
		self.write_info(f'bne $t0 $t1 _eq_false_{node.id}_')
		self.write_info(f'b _eq_true_{node.id}_')

		# equal int or boolf
		self.write_info(f'_eq_int_bool_{node.id}:', tabbed = False)	# handles booleans and ints
		self.write_info('lw $a3 12($t0)')	# load value variable_1
		self.write_info('lw $t4 12($t1)') # load variable_2
		self.write_info(f'bne $a3 $t4 _eq_false_{node.id}_') # value of int or bool are distinct

		#return true
		self.write_info(f'_eq_true_{node.id}_:', tabbed = False)
		self.write_info('li $a0 1')
		self.write_info('sw $a0 {}($fp)'.format(self.offset[node.dest]))
		self.write_info(f'b end_equal_{node.id}_')

		#return false
		self.write_info(f'_eq_false_{node.id}_:', tabbed = False)
		self.write_info('li $a0 0')
		self.write_info('sw $a0 {}($fp)'.format(self.offset[node.dest]))
		self.write_info(f'end_equal_{node.id}_:', tabbed = False)


	def visit_EqualOrLessThan(self, node: cil.EqualOrLessThan):
		self.write_info('# <=')
		self.write_info('lw $a1, {}($fp)'.format(self.offset[node.left]))
		self.write_info('lw $a2, {}($fp)'.format(self.offset[node.right]))
		self.write_info('sle $a0, $a1, $a2'.format(self.offset[node.right]))
		self.write_info('sw $a0, {}($fp)'.format(self.offset[node.dest]))
		self.write_info('')

	def visit_LessThan(self, node: cil.LessThan):
		self.write_info('# <')
		self.write_info('lw $a1, {}($fp)'.format(self.offset[node.left]))
		self.write_info('lw $a2, {}($fp)'.format(self.offset[node.right]))
		self.write_info('slt $a0, $a1, $a2'.format(self.offset[node.right]))
		self.write_info('sw $a0, {}($fp)'.format(self.offset[node.dest]))
		self.write_info('')

	def visit_Goto(self, node: cil.Goto):
		self.write_info('# GOTO')
		self.write_info('j _cil_label_{}'.format(node.label))
		self.write_info('')

	def visit_IfGoto(self, node: cil.IfGoto):
		self.write_info('# IF GOTO')
		self.write_info('lw $a0, {}($fp)'.format(self.offset[node.condition]))
		self.write_info('bnez $a0, _cil_label_{}'.format(node.label))
		self.write_info('')

############################## ASSIGNMENT ####################################

	def visit_Assign(self, node: cil.Assign):
		self.write_info('# ASSIGN')
		self.write_info('lw $a0, {}($fp)'.format(self.offset[node.source]))
		self.write_info('sw $a0, {}($fp)'.format(self.offset[node.dest]))
		self.write_info('')

	def visit_Label(self, node: cil.Label):
		self.write_info('_cil_label_{}:'.format(node.name), tabbed=False)

############################# ARITHMETICS ####################################

	def visit_Plus(self, node: cil.Plus):
		self.write_info('# +')
		self.write_info('lw $a0, {}($fp)'.format(self.offset[node.left]))
		self.write_info('lw $a1, {}($fp)'.format(self.offset[node.right]))
		self.write_info('add $a0, $a0, $a1')
		self.write_info('sw $a0, {}($fp)'.format(self.offset[node.dest]))
		self.write_info('')


	def visit_Minus(self, node: cil.Minus):
		self.write_info('# -')
		if isinstance(node.left, int):
			self.write_info('li $a0 {}'.format(node.left))
		else:
			self.write_info('lw $a0, {}($fp)'.format(self.offset[node.left]))
		self.write_info('lw $a1, {}($fp)'.format(self.offset[node.right]))
		self.write_info('sub $a0, $a0, $a1')
		self.write_info('sw $a0, {}($fp)'.format(self.offset[node.dest]))
		self.write_info('')

	def visit_Mult(self, node: cil.Mult):
		self.write_info('# *')
		self.write_info('lw $a0, {}($fp)'.format(self.offset[node.left]))
		self.write_info('lw $a1, {}($fp)'.format(self.offset[node.right]))
		self.write_info('mul $a0, $a0, $a1')
		self.write_info('sw $a0, {}($fp)'.format(self.offset[node.dest]))
		self.write_info('')

	def visit_Div(self, node: cil.Div):
		self.write_info('# /')
		self.write_info('lw $a0, {}($fp)'.format(self.offset[node.left]))
		self.write_info('lw $a1, {}($fp)'.format(self.offset[node.right]))
		self.write_info(f'beqz $a1 _div_error_{node.id}_')
		self.write_info('div $a0, $a0, $a1')
		self.write_info('sw $a0, {}($fp)'.format(self.offset[node.dest]))
		self.write_info(f'b _div_end_{node.id}_')
		self.write_info(f'_div_error_{node.id}_:',tabbed=False)
		self.write_info('la $a0 _div_zero_msg')
		self.write_info('li $v0 4')
		self.write_info('syscall')
		self.write_info('la $a0 _abort_msg')
		self.write_info('li $v0 4')
		self.write_info('syscall')
		self.write_info('li $v0 10')
		self.write_info('syscall')
		self.write_info(f'_div_end_{node.id}_:',tabbed=False)


############################# COMPARISONS ####################################

	def visit_LessThan(self, node: cil.LessThan):
		self.write_info('# <')
		self.write_info('lw $a1, {}($fp)'.format(self.offset[node.left]))
		self.write_info('lw $a2, {}($fp)'.format(self.offset[node.right]))
		self.write_info('slt $a0, $a1, $a2'.format(self.offset[node.right]))
		self.write_info('sw $a0, {}($fp)'.format(self.offset[node.dest]))
		self.write_info('')

