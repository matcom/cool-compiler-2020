from .visitor_helper import *
from .ast import *


class FormatVisitor(object):
    @on('node')
    def visit(self, node, tabs):
        pass
    
    @when(ProgramNode)
    def visit(self, node, tabs=0):  
        buff = ""
        buff += "ProgramNode"
        for child in node.classes:
            buff += "\n"
            buff += self.visit(child, tabs + 1)
        
        return buff
    
    @when(ClassNode)
    def visit(self, node, tabs=0):
        buff = ""
        for i in range(0, tabs):
            buff += "    "
        buff += "ClassNode"
        buff += " " + node.typeName
        
        for feature in node.features:
            buff += "\n"
            buff += self.visit(feature, tabs + 1)
        
        return buff
    
    @when(AttributeFeatureNode)
    def visit(self, node, tabs=0):
        buff = ""
        for i in range(0, tabs):
            buff += "    "
        buff += "AttributeFeatureNode"

        return buff + " " + node.id

    @when(FunctionFeatureNode)
    def visit(self, node, tabs=0):
        buff = ""
        for i in range(0, tabs):
            buff += "    "
        buff += "FunctionFeatureNode"

        return buff + " " + node.id
