from .AST_definitions import *
from compiler.utils.visitors_definitions import NodeVisitor
from compiler.utils.errors import error


class TypeInheritanceVisitor(NodeVisitor):
		

	def visit_NodeProgram(self, node: NodeProgram):
		errors = []
		
		for nodeClass in node.class_list:
			result = self.programContext.checkGoodInheritance(nodeClass)
			if type(result) is error:
				errors.append(result)

		# This is because we need only one error to pass the tests.
		if errors:
			return [errors.pop()]

		self.programContext.actualizeChildren()
		node.class_list= self.orderClassesByInhertiance('Object', node.class_list,
		{node.idName: False for node in node.class_list})

		for nodeClass in node.class_list:
			result = self.visit(nodeClass)
			if type(result) is error:
				errors.append(result)
		return [errors.pop()] if errors else []

	def visit_NodeClass(self, node: NodeClass):

		if node.idName == 'Object':
			return
		
		for nodeAttr in node.attributes:
			resultVisitAttr= self.visit(nodeAttr, idType= node.idName)
			if type(resultVisitAttr) is error:
				return resultVisitAttr
		
		for nodeClassMethod in node.methods:
			resultVisitClassMethod= self.visit(nodeClassMethod, idType= node.idName)
			if type(resultVisitClassMethod) is error:
				return resultVisitClassMethod
		
		self.programContext.actualizeInherits(node)    
	
	
	def visit_NodeAttr(self, node: NodeAttr, idType):
		return self.programContext.checkNotOverwriteAttr(node, idType)
		

	def visit_NodeClassMethod(self, node: NodeClassMethod, idType):
		return self.programContext.checkGoodOverwriteMethod(node, idType)
		
	def orderClassesByInhertiance(self, typeName, classList, visitedDict):
		order = [self.returnClassByIdName(typeName, classList)]
		for child in self.programContext.types[typeName].children:
			if not visitedDict[typeName]:
				order += self.orderClassesByInhertiance(child, classList, visitedDict)
		
		visitedDict[typeName]= True
		return order
		
	def returnClassByIdName(self, typeName, classList):
		return next((_class for _class in classList if _class.idName == typeName), None)

