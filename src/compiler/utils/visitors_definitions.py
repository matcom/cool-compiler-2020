from ..components.semantic.AST_definitions import *


from compiler.utils.errors import error


class NodeVisitor:
	def __init__(self, programContext):
		self.programContext= programContext
	
	def visit(self, node: Node, **args):
		if self.__class__.__name__ == 'TypeCheckerVisitor':
			if issubclass(type(node), NodeBinaryOperation):
				return self.visit_NodeBinaryOperation(node, **args)
			
		visitor_method_name = 'visit_' + node.clsname
		visitor = getattr(self, visitor_method_name, self.not_implemented)        
		return visitor(node, **args) # Return the new context result from the visit

	def not_implemented(self, node: Node, **args):
		raise Exception('Not implemented visit_{} method'.format(node.clsname))


