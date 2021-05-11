from ..ast import ClassDeclarationNode, ProgramNode
from ..errors import SemanticError
from ..utils import on, when
from .semantic_utils import Context, SemanticException


class COOL_TYPE_COLLECTOR(object):
    def __init__(self, errors=[]):
        self.context = None
        self.errors = errors
        self._mapper = dict()
        self._graph = dict()
        self._to = []

    def _order(self, actual):
        actual._visited = True
        for son in self._graph[actual.id]:
            son_node = self._mapper[son]
            if son_node._visited:
                continue
            self._order(son_node)
        self._to.append(actual)

    def check_cyclic(self, obj, parents):
        stack = [obj.id]
        while True:
            actual = stack[-1]
            parent = parents.get(actual, None)
            if parent is None:
                break
            else:
                if parent in stack:
                    self.errors.append(
                        SemanticError(
                            obj.line,
                            obj.column,
                            f"Cyclic inheritance in the hierarchy of {obj.id}.",
                        )
                    )
                    break
                else:
                    stack.append(parent)

    def define_basic_types(self):
        self.context.create_type("Object")
        self.context.create_type("IO")
        self.context.create_type("Int")
        self.context.create_type("String")
        self.context.create_type("Bool")

    @on("node")
    def visit(self, node):
        pass

    @when(ProgramNode)
    def visit(self, node: ProgramNode):  # noqa:F811
        self.context = Context()
        self.define_basic_types()
        for class_def in node.classes:
            class_def._visited = False  # type:ignore
            self._graph[class_def.id] = []
            self.visit(class_def)

        if len(self.errors) == 0:
            for class_def in node.classes:
                if (
                    class_def.parent is not None
                    and class_def.parent in self._graph.keys()
                ):
                    self._graph[class_def.id].append(class_def.parent)

            for class_def in node.classes:
                if class_def._visited:  # type:ignore
                    continue
                else:
                    self._order(class_def)

            # Check for ciclyc inheritance
            parents = dict()
            for class_def in node.classes:
                parents[class_def.id] = class_def.parent
                self.check_cyclic(class_def, parents)

            node.classes = self._to

        return self.context

    @when(ClassDeclarationNode)
    def visit(self, node: ClassDeclarationNode):  # noqa:F811
        try:
            self.context.create_type(node.id)
            self._mapper[node.id] = node
        except SemanticException as e:
            self.errors.append(SemanticError(node.line, node.column, e.text))
