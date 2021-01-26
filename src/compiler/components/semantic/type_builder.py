from .AST_definitions import *
from compiler.utils.visitors_definitions import NodeVisitor
from compiler.utils.errors import error


class TypeBuilderVisitor(NodeVisitor):
	def __init__(self, programContext):
		super().__init__(programContext)
		self.currentTypeName = ''

	def visit_NodeProgram(self, node: NodeProgram):
		errors = []
		for nodeClass in node.class_list:
			errors += self.visit(nodeClass)
		return errors

	def visit_NodeClass(self, node: NodeClass):
		errors= []
		self.currentTypeName= node.idName
		
		for nodeAttr in node.attributes:
			errors += self.visit(nodeAttr)
		for nodeClassMethod in node.methods:
			errors += self.visit(nodeClassMethod)
		return errors

	def visit_NodeAttr(self, node: NodeAttr):
		resultOp= self.programContext.defineAttrInType(self.currentTypeName,
		node)
		
		if type (resultOp) is error:
			return [resultOp]
		
		return []

	def visit_NodeClassMethod(self, node: NodeClassMethod):
		return [definition for definition in
		[self.programContext.getType(node.returnType, (node.line, node.column))] +
		[self.programContext.getType(idName = formal_param._type, row_and_col= (formal_param.line, formal_param.column)) for formal_param in node.formal_param_list] +
		[self.programContext.defineMethod(
			typeName = self.currentTypeName,
			node= node
			)]
		if type(definition) is error
		]

