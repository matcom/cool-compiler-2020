from .AST_definitions import *
from compiler.utils.visitors_definitions import NodeVisitor
from compiler.utils.errors import error


class TypeCollectorVisitor(NodeVisitor):
    
	def visit_NodeProgram(self, node: NodeProgram):
		errors = []
		for nodeClass in node.class_list:
			result= self.visit(nodeClass)
			if type (result) is error: # This ugly return is because we only need a one error, this is the panic mode!
				errors.append(result)
				return errors
		

	def visit_NodeClass(self, node: NodeClass):
		# When we create a type, we store it in the context, if there is no errors
		return self.programContext.createType(node)
