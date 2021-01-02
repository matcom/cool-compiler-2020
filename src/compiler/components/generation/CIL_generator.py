from compiler.components.visitors_definitions import NodeVisitor
from ..semantic.AST_definitions import *
import compiler.components.generation.CIL_definitions as cil
from compiler.components.generation.context import NameMap
from compiler.utils.errors import error

class CILVisitor(NodeVisitor):
	def __init__(self, programContext, mapExpr):
		super().__init__(programContext= programContext)
		self.mapExpr= mapExpr

		# Type declarations of the program
		self.dottype= []
		# String declarations of the program
		self.dotdata= []
		# Function declarations of the program
		self.dotcode= []

		# Data of the class being visited
		self.currentClassName= ""

		# Data of the function being visited
		self.currentFunctionName= ""
		self.localvars= []
		self.instructions= []

		# Attributes index map[][]
		self.attrIndexMap= {}

		# Methods index map
		self.mthMap= {}

		# Counters to make variable's names unique
		self.internalVarCount = 0			# LOCAL variables
		self.internalLabelCount = 0			# LABELs


		# Add static code
		self.addBuiltIns()
  
		# Class depth dictionary used to analyze Case expressions
		self.classDepth = {}

	def addBuiltIns(self):
		# Add static types, functions and string constants
		self.emptyString = self.registerData("")

		self.dottype.append(cil.Type('void', [], []))
  
  	#---------- LABELs
	def defineInternalLabel(self):
		label = f'LABEL_{self.internalLabelCount}'
		self.internalLabelCount += 1
		return label

	#---------- .TYPE
	def registerType(self, ttype):
		self.dottype.append(ttype)

	#---------- .DATA
	def registerData(self, value):
		vname = f'data_{len(self.dotdata)}'
		sameData = [data for data in self.dotdata if data.value == value]
		if sameData != []:
			return sameData[0].dest

		dataNode = cil.Data(vname, value)
		self.dotdata.append(dataNode)
		return dataNode.dest

	#---------- .CODE

	def buildInternalVname(self, vname):
		vname = f'_{vname}_{self.internalVarCount}'
		return vname

	def registerInternalLocal(self):
		return self.registerLocal('internal')

	def registerLocal(self, vname):
		vname = self.buildInternalVname(vname)
		self.localvars.append(cil.LocalDeclaration(vname))
		self.internalVarCount +=1
		return vname

	def registerInstruction(self, instructionType, *args):
		instruction = instructionType(*args)
		self.instructions.append(instruction) 
		return instruction

	def registerFunction(self, function):
		self.dotcode.append(function)

	def buildNewObject(self, dest, ttype):
		self.registerInstruction(cil.Allocate, dest, ttype)
		self.registerInstruction(cil.PushParam, dest)
		self.registerInstruction(cil.Call, dest, f'{ttype}_{"_init"}')
		self.registerInstruction(cil.PopParam, dest)

	def inspectInitializers(self, typeName):
		parentName = self.programContext.types[typeName].parent if typeName == "Object" or self.programContext.types[typeName].parent else 'Object'
		initializers = []
		while parentName:
			initializers.append(f'{parentName}_{"_init"}')
			parentName= self.programContext.types[parentName].parent
		
		return initializers
		
	def buildClassDepth(self, node: NodeProgram):
		# Initialize class depth dictionary
		for c in node.class_list:
			self.classDepth[c.idName] = 0

		for _class in node.class_list:
			if _class.parent:
				# Build the class depth dictionary
				self.classDepth[_class.idName] = self.classDepth[_class.parent] + 1

	def visit_NodeProgram(self, node: NodeProgram):
		self.buildClassDepth(node)
		for nodeClass in node.class_list:
			newType= self.visit(nodeClass, 
								initializers= self.inspectInitializers(nodeClass.idName))
			self.registerType(newType)
			
		for func in self.dotcode:
			for inst in func.body:
				if isinstance(inst, cil.VCall):
					inst.f = self.mthMap[inst.f]
				if (isinstance(inst, cil.SetAttrib) or isinstance(inst, cil.GetAttrib)) \
					and isinstance(inst.attribute, str):
					inst.attribute = self.attrIndexMap[inst.attribute]
		
		return cil.Program(self.dottype, self.dotdata, self.dotcode)
	
	def visit_NodeClass(self, node: NodeClass, initializers):
		
		self.currentClassName = node.idName
		# Ovewritting attrs it's not allowed, so the first attrs of the class are the inhertited
		if node.idName != 'Object':
			parentName= 'Object' if not node.parent else node.parent
			inhAttributes = [cil.Attribute(f'{parentName}_{attrName}') for attrName in
                    self.programContext.types[node.idName].inheritsAttr]
			
			methods= [cil.Method(methodName, f'{parentName}_{methodName}') for methodName in
             self.programContext.types[parentName].inheritsMethods.keys()]
			methods += [cil.Method(methodName, f'{parentName}_{methodName}') for methodName in
               self.programContext.types[parentName].methods.keys() if not methodName in methods]
			
			for i in range(len(inhAttributes)):
				self.attrIndexMap[f'{self.currentClassName}_{inhAttributes[i].name}']= i
			for i in range(len(methods)):
				self.mthMap[f'{self.currentClassName}_{methods[i].name}']= i
		else:
			inhAttributes = []
			methods = []
		# Translate all the properties (COOL) into attributes (CIL)
		# and build an initializer function
		self.localvars= []
		self.instructions= []
		self.internalVarCount= 0
		self.currentFunctionName= f'{self.currentClassName}_{"_init"}'

		# Build the initializer function and attributes list        
		for initializer in initializers:
			self.registerInstruction(cil.PushParam, "__self")
			self.registerInstruction(cil.Call, None, initializer)	# Call superclasses's initializers
			self.registerInstruction(cil.PopParam, None)

		ind= len(inhAttributes)
		naturalAttrs= []
		for nodeAttr in node.attributes:
			self.currentIndex= ind
			naturalAttrs.append(self.visit(nodeAttr))
			ind += 1
			
		# Register the initializer function
		self.registerInstruction(cil.Return, '__self')
		func = cil.Function(self.currentFunctionName,
							[cil.ArgDeclaration('__self')], 
							self.localvars, self.instructions)
		
		self.registerFunction(func)
		
		# Translate all Class Methods (COOL) into Type Methods (CIL)
		# and the functions associated will be automatically registered by the visitor
		ind = len(methods)
		for nodeClassMethod in node.methods:
			# Check if this method is being redefined
			
			if nodeClassMethod.idName in methods:
				# If it's being redefined, use the offset of the function already defined
				index = methods.index(nodeClassMethod.idName)
				del methods[i]
				ind -= 1

			else:
				index= ind
			self.currentIndex= index
			method = self.visit(nodeClassMethod)
			methods.insert(index, method)
			ind += 1

		return cil.Type(node.idName, inhAttributes + naturalAttrs, methods)
		
		
	def visit_NodeAttr(self, node: NodeAttr):
		if node.expr:
			rname = self.visit(node.expr)
			self.registerInstruction(cil.SetAttrib, "__self", self.currentIndex, rname)
		elif node._type == "prim_zero_slot":
			self.registerInstruction(cil.SetAttrib, "__self", self.currentIndex, 0)
		elif node._type == "prim_empty_slot":
			
			self.registerInstruction(cil.SetAttrib,
									 "__self",
									 self.currentIndex,
									 self.emptyString)
		else:
			_temp = self.registerInternalLocal()
			if node._type == 'Int':
				self.buildNewObject(_temp, 'Int')
			elif node._type == 'Bool':
				self.buildNewObject(_temp, 'Bool')
			elif node._type == 'String':
				self.buildNewObject(_temp, 'String')
			else:
				self.registerInstruction(cil.Allocate, _temp, 'void')
			self.registerInstruction(cil.SetAttrib, "__self", self.currentIndex, _temp)

		self.attrIndexMap[f'{self.currentClassName}_{node.idName}']= self.currentIndex
		return cil.Attribute(f'{self.currentClassName}_{node.idName}')
	
	def visit_NodeClassMethod(self, node: NodeClassMethod):
		self.localvars= []
		self.instructions= []
		self.internalVarCount= 0
		self.currentFunctionName= f"{self.currentClassName}_{node.idName}"
		
		self.nameMap = NameMap()
		
		arguments = [cil.ArgDeclaration("__self")]

		for formal_param in node.formal_param_list:
			arguments.append(self.visit(formal_param))

		if not self.currentClassName in self.programContext.basics:
			returnVal = self.visit(node.body)
			self.registerInstruction(cil.Return, returnVal)

		#----- Register the function and return the corresponding method node
		func= cil.Function(self.currentFunctionName, arguments, 
					  self.localvars, self.instructions)

		self.registerFunction(func)
  
		self.mthMap[func.name]= self.currentIndex

		return cil.Method(node.idName, func.name)
	
	def visit_NodeFormalParam(self, node: NodeFormalParam):
		self.nameMap.define_variable(node.idName, f'_{node.idName}')
		return cil.ArgDeclaration(f'_{node.idName}')

	################################## INSTANCES ##############################
	def visit_NodeObject(self, node: NodeObject):
		if node.idName == 'self': return '__self'
		objVname = self.nameMap.get_cil_name(node.idName)
		if objVname:
			return objVname
		else:
			vname = self.registerLocal(node.idName)
			attributeCilName = f'{self.currentClassName}_{node.idName}'
			self.registerInstruction(cil.GetAttrib,
							vname,
							'__self',
							attributeCilName)

			return vname

	def visit_NodeSelf(self, node: NodeSelf):
		return '__self'


	################################## CONSTANTS ##############################
	
	def visit_NodeInteger(self, node: NodeInteger):
		boxedInt = self.registerInternalLocal()
		self.registerInstruction(cil.Allocate, boxedInt, 'Int')
		self.registerInstruction(cil.SetAttrib, boxedInt, 0, node.content)
		return boxedInt

	def visit_NodeString(self, node: NodeString):
		dataVname= self.registerData(node.content)
		boxedString = self.registerInternalLocal()
		boxedInt = self.registerInternalLocal()
		self.registerInstruction(cil.Allocate, boxedInt, 'Int')
		self.registerInstruction(cil.SetAttrib, boxedInt, 0, len(node.content))

		self.registerInstruction(cil.Allocate, boxedString, 'String')
		self.registerInstruction(cil.SetAttrib, boxedString, 0, boxedInt)
		self.registerInstruction(cil.SetAttrib, boxedString, 1, dataVname)
		return boxedString

	def visit_NodeBoolean(self, node: NodeBoolean):
		boxedBool = self.registerInternalLocal()
		self.registerInstruction(cil.Allocate, boxedBool, 'Bool')
		if node.content:
			self.registerInstruction(cil.SetAttrib, boxedBool, 0, 1)
		else:
			self.registerInstruction(cil.SetAttrib, boxedBool, 0, 0)
		return boxedBool

	################################## EXPRESSIONS ##############################
	
	def visit_NodeNewObject(self, node: NodeNewObject):
		vname = self.registerInternalLocal()
		_temp = self.registerInternalLocal()
		self.registerInstruction(cil.Allocate, vname, node.type)
		self.registerInstruction(cil.PushParam, vname)
		self.registerInstruction(cil.Call, _temp, f'{node.type}_{"_init"}')
		self.registerInstruction(cil.PopParam, vname)
		return vname

	def visit_NodeIsVoid(self, node: NodeIsVoid):
		value = self.registerInternalLocal()
		exprVal = self.visit(node.expr)
		self.registerInstruction(cil.PushParam, exprVal)
		self.registerInstruction(cil.Call, value, "_isvoid")
		self.registerInstruction(cil.PopParam, exprVal)
		return value

	def visit_NodeAssignment(self, node: NodeAssignment):
		rname = self.visit(node.expr)
		cilName = self.nameMap.get_cil_name(node.nodeObject.idName)
		if cilName:
			self.registerInstruction(cil.Assign, cilName, rname)
		else:
			attributeCilName = f'{self.currentClassName}_{node.nodeObject.idName}'
			self.registerInstruction(cil.SetAttrib, 
							 '__self', attributeCilName, rname)
		return rname

	def visit_NodeBlock(self, node: NodeBlock):
		blockValue = None
		for expr in node.expr_list:
			blockValue = self.visit(expr)
		return blockValue

	def visit_NodeLetComplex(self, node: NodeLetComplex):
		self.nameMap = self.nameMap.create_child_scope()
		for nodeLet in node.nestedLets:
			self.visit(nodeLet)

		res_vname = self.visit(node.body)
		self.nameMap.exit_child_scope()

		return res_vname

	def visit_NodeLet(self, node: NodeLet):
		varName = ""
		if node.body:
   			varName = self.visit(node.body)
		else:
			varName = self.registerLocal(node.idName)
			if node.type == 'Int':
				self.registerInstruction(cil.SetAttrib, '__self', self.currentIndex, 0)
				self.buildNewObject(varName, 'Int')
			elif node.type == 'Bool':
				self.registerInstruction(cil.SetAttrib, '__self', self.currentIndex, 0)
				self.buildNewObject(varName, 'Bool')
			elif node.type == 'String':
				self.registerInstruction(cil.SetAttrib, '__self', self.currentIndex, self.emptyString)
				self.buildNewObject(varName, 'String')
			elif node.type == '__prim_zero_slot':
   				self.register_instruction(cil.SetAttrib, '__self', self.currentIndex, 0)
			elif node.type == '__prim_empty_slot':
				self.register_instruction(cil.SetAttrib, '__self', self.currentIndex, self.emptyString)	
			else:
				self.registerInstruction(cil.Allocate, varName, 'Void')
	
		self.nameMap.define_variable(node.idName, varName)
	
	def visit_NodeIf(self, node: NodeIf):
		# LOCAL <if.value>
		# 	<condition.locals>
		# 	<else.locals>
		# 	<then.locals>
		# 		...
		# 	<condition.body>
		# condition-unboxed = GetAttr <condition.value> _value
		# if condition-unboxed GOTO then_lbl
		# 	<else.code>
		# <if.value> = <else.value>
		# GOTO continue_lbl
		# LABEL then_lbl:
		# 	<then.code>
		# <if.value> = <then.value>
		# LABEL continue_lbl:

		# <.locals>
		ifValue = self.registerInternalLocal()
		conditionUnboxed = self.registerInternalLocal()
		thenLbl = self.defineInternalLabel()
		continueLbl = self.defineInternalLabel()

		# <.body>
		conditionValue = self.visit(node.predicate)
		self.registerInstruction(cil.GetAttrib, conditionUnboxed, conditionValue, 0)
		self.registerInstruction(cil.IfGoto, conditionUnboxed, thenLbl)
		elseValue = self.visit(node.else_body)
		self.registerInstruction(cil.Assign, ifValue, elseValue)
		self.registerInstruction(cil.Goto, continueLbl)
		self.registerInstruction(cil.Label, thenLbl)
		thenValue = self.visit(node.then_body)
		self.registerInstruction(cil.Assign, ifValue, thenValue)
		self.registerInstruction(cil.Label, continueLbl)

		return ifValue
	
	def visit_NodeWhileLoop(self, node: NodeWhileLoop):
		# LOCAL <while.value>
		# 	<condition.locals>
		# 	<body.locals>
		#  	...
		# LABEL start_lbl
		# 	<condition.code>
		# condition-unboxed = GetAttr <condition.value> _value
		# if condition-unboxed GOTO body_lbl
		# GOTO continue_lbl
		# LABEL body_lbl
		# 	<body.code>
		# GOTO start_lbl
		# LABEL continue_lbl
		# <while.value> = 'VOID_TYPE'

		# <.locals>
		whileValue = self.registerInternalLocal()
		conditionUnboxed = self.registerInternalLocal()
		startLbl = self.defineInternalLabel()
		bodyLbl = self.defineInternalLabel()
		continueLbl = self.defineInternalLabel()

		# <.code>
		self.registerInstruction(cil.Label, startLbl)
		conditionValue = self.visit(node.predicate)		# Generate <condition.body> and <condition.locals>
		self.registerInstruction(cil.GetAttrib, conditionUnboxed, conditionValue, 0)
		self.registerInstruction(cil.IfGoto, conditionUnboxed, bodyLbl)
		self.registerInstruction(cil.Goto, continueLbl)
		self.registerInstruction(cil.Label, bodyLbl)
		self.visit(node.body)
		self.registerInstruction(cil.Goto, startLbl)
		self.registerInstruction(cil.Label, continueLbl)
		self.registerInstruction(cil.Allocate, whileValue, 'Void')

		return whileValue

	def visit_NodeCase(self, node: NodeCase):
		# Sort types by their depths in the class hierarchy
		actions = list(node.actions)
		actions.sort(key = lambda x: self.classDepth[x.type], reverse = True)

		# <.locals>
		_temp = self.registerInternalLocal()
		exprType = self.registerLocal("expression_type")
		caseValue = self.registerInternalLocal()
		
		# Labels
		labels = []
		for _ in node.actions:
			labels.append(self.defineInternalLabel())
		endLabel = self.defineInternalLabel()

		# <.code>
		exprValue = self.visit(node.expr)
		self.registerInstruction(cil.TypeOf, exprType, exprValue)

		for i in range(len(actions)):
			self.registerInstruction(cil.PushParam, actions[i].type)
			self.registerInstruction(cil.PushParam, exprType)
			# Call conforms function : (typex, typey) -> typex <= typey
			self.registerInstruction(cil.Call, _temp, "__conforms")
			self.registerInstruction(cil.PopParam, None)
			self.registerInstruction(cil.PopParam, None)
			self.registerInstruction(cil.IfGoto, _temp, labels[i])

		for i in range(len(actions)):
			self.registerInstruction(cil.Label, labels[i])
			self.nameMap.define_variable(actions[i].idName, exprValue)
			self.nameMap = self.nameMap.create_child_scope()
			expr_i = self.visit(actions[i])
			self.nameMap.exit_child_scope()
			self.registerInstruction(cil.Assign, caseValue, expr_i)
			self.registerInstruction(cil.Goto, endLabel)
   
		self.registerInstruction(cil.Label, endLabel)
		return caseValue

	def visit_NodeCaseAction(self, node: NodeCaseAction):
			return self.visit(node.expr)
  
	################################# DISPATCHS #######################################
	
	def visit_NodeDynamicDispatch(self, node: NodeDynamicDispatch):
		instanceVname = self.visit(node.expr)
		ttype = self.registerInternalLocal()
		result = self.registerInternalLocal()

		# Save the params to do Pop after calling the function
		pops = []
		for i in range(len(node.arguments)-1, -1, -1):
			param = node.arguments[i]
			paramVname = self.visit(param)
			self.registerInstruction(cil.PushParam, paramVname)
			pops.append(paramVname)

		# Instance
		self.registerInstruction(cil.PushParam, instanceVname)

		# Compute instance's type
		self.registerInstruction(cil.TypeOf, ttype, instanceVname)
		methodPrefix= self.mapExpr[(node.line, node.column)]
		# Call the function
		methodName = f'{methodPrefix}_{node.method}'
		self.registerInstruction(cil.VCall, result, ttype, methodName)
		self.registerInstruction(cil.PopParam, instanceVname)

		# Pop the arguments
		for i in range(len(pops)-1, -1, -1):
			self.registerInstruction(cil.PopParam, pops[i])

		return result

	def visit_NodeStaticDispatch(self, node: NodeStaticDispatch):
		instanceVname = self.visit(node.expr)
		result = self.registerInternalLocal()

		# Save the params to do Pop after calling the function
		pops = []
		for i in range(len(node.arguments)-1, -1, -1):
			param = node.arguments[i]
			paramVname = self.visit(param)
			self.registerInstruction(cil.PushParam, paramVname)
			pops.append(paramVname)

		# Instance
		self.registerInstruction(cil.PushParam, instanceVname)

		# Call the function
		method_name = f'{node.expr.type}_{node.method}'
		self.registerInstruction(cil.VCall, result, node.dispatch_type, method_name)
		self.registerInstruction(cil.PopParam, instanceVname)


		# Pop the arguments
		for i in range(len(pops)-1, -1, -1):
			self.registerInstruction(cil.PopParam, pops[i])

		return result

	def visit_NodeIntegerComplement(self, node: NodeIntegerComplement):
		# <.locals>
		unboxedVal = self.registerInternalLocal()
		_temp = self.registerInternalLocal()
		result = self.registerInternalLocal()

		# <.code>
		boxedVal = self.visit(node.integer_expr)
		self.registerInstruction(cil.GetAttrib, unboxedVal, boxedVal, 0)
		self.registerInstruction(cil.Minus, _temp, 0, unboxedVal)
		self.registerInstruction(cil.Allocate, result, "Int")
		self.registerInstruction(cil.SetAttrib, result, 0, _temp)
		return result

	def visit_NodeBooleanComplement(self, node: NodeBooleanComplement):
		# <.locals>
		unboxedVal = self.registerInternalLocal()
		_temp = self.registerInternalLocal()
		result = self.registerInternalLocal()

		# <.code>
		boxedVal = self.visit(node.boolean_expr)
		self.registerInstruction(cil.GetAttrib, unboxedVal, boxedVal, 0)
		self.registerInstruction(cil.Minus, _temp, 1, unboxedVal)
		self.registerInstruction(cil.Allocate, result, 'Bool')
		self.registerInstruction(cil.SetAttrib, result, 0, _temp)
		return result

	################################ BINARY OPERATIONS ##################################
	
	def visit_NodeAddition(self, node: NodeAddition):
		# <.locals>
		_temp = self.registerInternalLocal()
		firstVal = self.registerInternalLocal()
		secondVal = self.registerInternalLocal()
		result = self.registerInternalLocal()

		# <.code>
		firstBoxed = self.visit(node.first)
		secondBoxed = self.visit(node.second)
		self.registerInstruction(cil.GetAttrib, firstVal, firstBoxed, 0)
		self.registerInstruction(cil.GetAttrib, secondVal, secondBoxed, 0)
		self.registerInstruction(cil.Plus, _temp, firstVal, secondVal)
		self.registerInstruction(cil.Allocate, result, 'Int')
		self.registerInstruction(cil.SetAttrib, result, 0, _temp)
		return result
	
	def visit_NodeSubtraction(self, node: NodeSubtraction):
		# <.locals>
		_temp = self.registerInternalLocal()
		firstVal = self.registerInternalLocal()
		secondVal = self.registerInternalLocal()
		result = self.registerInternalLocal()

		# <.code>
		firstBoxed= self.visit(node.first)
		secondBoxed= self.visit(node.second)
		self.registerInstruction(cil.GetAttrib, firstVal, firstBoxed, 0)
		self.registerInstruction(cil.GetAttrib, secondVal, secondBoxed, 0)
		self.registerInstruction(cil.Minus, _temp, firstVal, secondVal)
		self.registerInstruction(cil.Allocate, result, "Int")
		self.registerInstruction(cil.SetAttrib, result, 0, _temp)
		return result

	def visit_NodeMultiplication(self, node: NodeMultiplication):
		# <.locals>
		_temp = self.registerInternalLocal()
		firstVal = self.registerInternalLocal()
		secondVal = self.registerInternalLocal()
		result = self.registerInternalLocal()

		# <.code>
		firstBoxed = self.visit(node.first)
		secondBoxed = self.visit(node.second)
		self.registerInstruction(cil.GetAttrib, firstVal, firstBoxed, 0)
		self.registerInstruction(cil.GetAttrib, secondVal, secondBoxed, 0)
		self.registerInstruction(cil.Mult, _temp, firstVal, secondVal)
		self.registerInstruction(cil.Allocate, result, 'Int')
		self.registerInstruction(cil.SetAttrib, result, 0, _temp)
		return result

	def visit_NodeDivision(self, node: NodeDivision):
		# <.locals>
		_temp = self.registerInternalLocal()
		firstVal = self.registerInternalLocal()
		secondVal = self.registerInternalLocal()
		result = self.registerInternalLocal()

		# <.code>
		firstBoxed = self.visit(node.first)
		secondBoxed = self.visit(node.second)
		self.registerInstruction(cil.GetAttrib, firstVal, firstBoxed, 0)
		self.registerInstruction(cil.GetAttrib, secondVal, secondBoxed, 0)
		self.registerInstruction(cil.Div, _temp, firstVal, secondVal)
		self.registerInstruction(cil.Allocate, result, "Int")
		self.registerInstruction(cil.SetAttrib, result, 0, _temp)
		return result

	def visit_NodeEqual(self, node: NodeEqual):
   		# <.locals>
		_temp = self.registerInternalLocal()
		result = self.registerInternalLocal()

		# <.code>
		first_val = self.visit(node.first)
		second_val = self.visit(node.second)
		self.registerInstruction(cil.Equal, _temp, first_val, second_val)
		self.registerInstruction(cil.Allocate, result, 'Bool')
		self.registerInstruction(cil.SetAttrib, result, 0, _temp)
		return result

	def visit_NodeLessThan(self, node: NodeLessThan):
		# <.locals>
		_temp = self.registerInternalLocal()
		first_val = self.registerInternalLocal()
		second_val = self.registerInternalLocal()
		result = self.registerInternalLocal()

		# <.code>
		first_boxed = self.visit(node.first)
		second_boxed = self.visit(node.second)
		self.registerInstruction(cil.GetAttrib, first_val, first_boxed, 0)
		self.registerInstruction(cil.GetAttrib, second_val, second_boxed, 0)
		self.registerInstruction(cil.LessThan, _temp, first_val, second_val)
		self.registerInstruction(cil.Allocate, result, "Int")
		self.registerInstruction(cil.SetAttrib, result, 0, _temp)
		return result

	def visit_NodeLessThanOrEqual(self, node: NodeLessThanOrEqual):
   		# <.locals>
		_temp = self.registerInternalLocal()
		firstVal = self.registerInternalLocal()
		secondVal = self.registerInternalLocal()
		result = self.registerInternalLocal()

		# <.code>
		firstBoxed = self.visit(node.first)
		secondBoxed = self.visit(node.second)
		self.registerInstruction(cil.GetAttrib, firstVal, firstBoxed, 0)
		self.registerInstruction(cil.GetAttrib, secondVal, secondBoxed, 0)
		self.registerInstruction(cil.EqualOrLessThan, _temp, firstVal, secondVal)
		self.registerInstruction(cil.Allocate, result, "Int")
		self.registerInstruction(cil.SetAttrib, result, 0, _temp)
		return result
