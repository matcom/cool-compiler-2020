from coolcmp.cmp_utils.errors import *
from coolcmp.cmp_utils.my_ast import *
from coolcmp.cmp_utils.native import native_classes
from coolcmp.cmp_utils.visitor import Visitor
from coolcmp.cmp_utils.environment import Environment

#check for class main at type-checking

class SemanticAnalyzer:
    def __init__(self, ast_root):
        self.ast_root = ast_root

    def build_inheritance_tree(self):
        native_names = [ cls.type.value for cls in native_classes ]
        cls_names = {}

        for cls in self.ast_root.cls_list:
            if cls.type.value in native_names:
                raise SemanticError(cls.type.line, cls.type.col, 'Tried to redefine a native class "{}"'.format(cls.type.value))

            if cls.type.value in cls_names:
                raise SemanticError(cls.type.line, cls.type.col, 'Tried to redefine class "{}"'.format(cls.type.value))

            cls_names[cls.type.value] = cls

        for cls in native_classes:
            cls_names[cls.type.value] = cls

        for cls in self.ast_root.cls_list:
            name = (cls.opt_inherits or Type('Object')).value

            if not name in cls_names:
                raise SemanticError(cls.opt_inherits.line, cls.opt_inherits.col, 'Tried to inherit from class "{}" that doesnt exists'.format(name))

            parent = cls_names[name]

            if not parent.can_inherit:
                raise SemanticError(cls.opt_inherits.line, cls.opt_inherits.col, 'Cant inherit from class "{}"'.format(name))
            
            parent.children.append(cls)

        for cls in native_classes:
            self.ast_root.cls_list.append(cls)

    def check_cycles(self):
        for cls in self.ast_root.cls_list:
            self._dfs(cls)

    def _dfs(self, u, seen={}, up={}):
        seen[u.type.value] = up[u.type.value] = True

        for v in u.children:
            if v.type.value not in seen:
                self._dfs(v, seen, up)

            elif up[v.type.value]:
                raise SemanticError(v.type.line, v.type.col, 'Inheritance cycle detected at class "{}" inheriting from "{}"'.format(v.type.value, u.type.value))

        up[u.type.value] = False