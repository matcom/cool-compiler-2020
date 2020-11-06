import sys
sys.path.append('/..')
from .nodesIL.node_il import *
from .nodesIL.allocate_node_il import *
from .nodesIL.assignmet_node_il import *
from .nodesIL.methods_node_il import *
from .nodesIL.operation_node_il import *
from ..visitors import visitor

class codeVisitor:

    def __init__(self):
        #code IL
        self.code = []
        self.data = []

        self