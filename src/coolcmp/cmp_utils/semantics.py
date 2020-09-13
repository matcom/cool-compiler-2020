from coolcmp.cmp_utils.errors import *
from coolcmp.cmp_utils.my_ast import *
from coolcmp.cmp_utils.visitor import Visitor
from coolcmp.cmp_utils.environment import Environment

class SemanticAnalyzer:
    def __init__(self, ast_root):
        self.ast_root = ast_root

    def build_inheritance_tree(self, native_classes):
        cls_refs = {}

        for cls in native_classes:
            cls_refs[cls.type.value] = cls

        for cls in self.ast_root.cls_list:
            if cls.type.value in cls_refs:
                raise SemanticError(cls.type.line, cls.type.col, f'Tried to redefine class "{cls.type.value}"')

            cls_refs[cls.type.value] = cls

        for cls in native_classes:
            self.ast_root.cls_list.append(cls)

        for cls in self.ast_root.cls_list:
            for feature in cls.feature_list:
                if isinstance(feature, Method):
                    if feature.id.value in cls.methods:
                        raise SemanticError(feature.id.line, feature.id.col, f'Tried to redefine method "{feature.id.value}" in class "{cls.type.value}"')

                    cls.methods[feature.id.value] = feature

                else:
                    if feature.id.value in cls.attrs:
                        raise SemanticError(feature.id.line, feature.id.col, f'Tried to redefine attribute "{feature.id.value}" in class "{cls.type.value}"')

                    cls.attrs[feature.id.value] = feature

            if cls.type.value == 'Object':
                continue

            name = (cls.opt_inherits or Type('Object')).value

            if name not in cls_refs:
                assert cls.opt_inherits
                raise SemanticError(cls.opt_inherits.line, cls.opt_inherits.col, f'Tried to inherit from unexistent class "{cls.opt_inherits.value}"')

            parent = cls_refs[name]

            if not parent.can_inherit:
                raise SemanticError(cls.opt_inherits.line, cls.opt_inherits.col, f'Tried to inherit from class "{cls.opt_inherits.value}"')

            parent.children.append(cls)

        if 'Main' not in cls_refs:
            raise SemanticError(1, 1, 'Class "Main" doesnt exist')

        main_class = cls_refs['Main']

        if 'main' not in main_class.methods:
            raise SemanticError(main_class.type.line, main_class.type.col, 'Couldnt find method "main" on "Main" class')

        return cls_refs

    def check_cycles(self):
        seen = {}
        up = {}

        for cls in self.ast_root.cls_list:
            if cls.type.value not in seen:
                self._dfs(cls, seen, up)

    def _dfs(self, u, seen, up):
        seen[u.type.value] = up[u.type.value] = True

        for v in u.children:
            if v.type.value not in seen:
                self._dfs(v, seen, up)

            elif up[v.type.value]:
                raise SemanticError(v.type.line, v.type.col, f'Inheritance cycle detected at class "{v.type.value}" inheriting from "{u.type.value}"')

        up[u.type.value] = False