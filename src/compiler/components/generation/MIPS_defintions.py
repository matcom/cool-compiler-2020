class MIPSNode:
    pass

class MIPSProgramNode(MIPSNode):
    def __init__(self, dotdata, dottext):
        self.dotdata = dotdata
        self.dottext = dottext

class MIPSDataNode(MIPSNode):
    pass

class MIPSProcedureNode(MIPSNode):
    def __init__(self, label):
        self.label = label
        self.instructions = []

class MIPSInstructionNode(MIPSNode):
    pass

class MIPSDataTypedNode(MIPSDataNode):
    def __init__(self, vname, data_type, values):
        self.vname = vname
        self.data_type = data_type
        self.values = values

    def __str__(self):
        values = ""
        for value in self.values:
            values += f", {value}"
        return f"{self.vname} : {self.data_type}{values}"

class MIPSConstantNode(MIPSDataNode):
    def __init__(self, vname, value):
        self.vname = vname
        self.value = value

class MIPSArithmeticAndLogicNode(MIPSInstructionNode) :
    def __init__(self, destination, left, right):
        self.destination = destination
        self.left = left
        self.right = right

class MIPSAddNode(MIPSArithmeticAndLogicNode):
    def __str__(self):
        return f"add {self.destination}, {self.left}, {self.right}"

class MIPSSubstractNode(MIPSArithmeticAndLogicNode):
    def __str__(self):
        return f"sub {self.destination}, {self.left}, {self.right}"

class MIPSAddInmediateNode(MIPSArithmeticAndLogicNode):
    def __str__(self):
        return f'addi {self.destination}, {self.left}, {self.right}'

class MIPSAddUnsigned(MIPSArithmeticAndLogicNode):
    pass

class MIPSSubstractUnsignedNode(MIPSArithmeticAndLogicNode):
    pass

class MIPSAddInmediateUnsignedNode(MIPSArithmeticAndLogicNode):
    pass

class MIPSMultiplyWithoutOverflow(MIPSArithmeticAndLogicNode):
    pass

class MIPSAndNode(MIPSArithmeticAndLogicNode):
    pass

class MIPSOrNode(MIPSArithmeticAndLogicNode):
    pass

class MIPSAndInmediateNode(MIPSArithmeticAndLogicNode):
    pass

class MIPSOrInmediateNode(MIPSArithmeticAndLogicNode):
    pass

class MIPSShiftLeftNode(MIPSArithmeticAndLogicNode):
    pass

class MIPSShiftRightNode(MIPSArithmeticAndLogicNode):
    pass

class MIPSHiLoOperationNode(MIPSInstructionNode):
    def __init__(self,left,right):
        self.left = left
        self.right = right

class MIPSMultiplyNode(MIPSHiLoOperationNode):
     def __str__(self):
        return f'mult {self.left}, {self.right}'

class MIPSDivideNode(MIPSHiLoOperationNode):
     def __str__(self):
        return f'div {self.left}, {self.right}'

class MIPSDataTransferNode(MIPSInstructionNode):
    pass
class MIPSDataTransferWithOffsetNode(MIPSDataTransferNode):
    def __init__(self, source, offset, destination):
        self.source = source
        self.offset = offset
        self.destination = destination

class MIPSLoadWordNode(MIPSDataTransferWithOffsetNode):
    def __str__(self):
        return f'lw {self.source}, {str(self.offset)}({self.destination})'

class MIPSLoadByteNode(MIPSDataTransferWithOffsetNode):
    def __str__(self):
        return f'lb {self.source}, {str(self.offset)}({self.destination})'

class MIPSStoreWordNode(MIPSDataTransferWithOffsetNode):
    def __str__(self):
        return f'sw {self.source}, {str(self.offset)}({self.destination})'

class MIPSStoreByteNode(MIPSDataTransferWithOffsetNode):
    def __str__(self):
        return f'sb {self.source}, {str(self.offset)}({self.destination})'

class MIPSLoadNode(MIPSDataTransferNode):
    def __init__(self, destination, source):
        self.destination = destination
        self.source = source

class MIPSLoadUpperInmediateNode(MIPSLoadNode):
    pass

class MIPSLoadAdressNode(MIPSLoadNode):
    def __str__(self):
        return f'la {self.destination}, {self.source}'

class MIPSLoadInmediateNode(MIPSLoadNode):
    def __str__(self):
        return f'li {self.destination}, {str(self.source)}'

class MIPSMoveFromNode(MIPSDataTransferNode):
    def __init__(self, destination):
        self.destination = destination

class MIPSMoveNode(MIPSDataTransferNode):
    def __init__(self, destination, source):
        self.destination = destination
        self.source = source

    def __str__(self):
        return f"move {self.destination} {self.source}"

class MIPSConditionalBranchNode(MIPSInstructionNode):
    def __init__(self, r1, r2, jump):
        self.r1 = r1
        self.r2 = r2
        self.jump = jump

class MIPSBranchOnEqualNode(MIPSConditionalBranchNode):
    def __str__(self):
        return f"beq {self.r1}, {self.r2}, {self.jump}"

class MIPSBranchNeqZero(MIPSInstructionNode):
    def __init__(self, r, label):
        self.r = r
        self.label = label

    def __str__(self):
        return f"bnez {self.r}, {self.label}"

class MIPSBranchOnNotEqualNode(MIPSConditionalBranchNode):
    def __str__(self):
        return f"bne {self.r1}, {self.r2}, {self.jump}"

class MIPSBranchOnGTNode(MIPSConditionalBranchNode):
    def __str__(self):
        return f"bgt {self.r1}, {self.r2}, {self.jump}"

class MIPSBranchOnGTENode(MIPSConditionalBranchNode):
    pass

class MIPSBranchOnLTNode(MIPSConditionalBranchNode):
    def __str__(self):
        return f"blt {self.r1}, {self.r2}, {self.jump}"

class MIPSBranchOnLTENode(MIPSConditionalBranchNode):
    pass

class MIPSComparissonNode(MIPSInstructionNode):
    def __init__(self, result_register, value1, value2):
        self.result_register = result_register
        self.value1 = value1
        self.value2 = value2

class MIPSSetOnLTNode(MIPSComparissonNode):
    def __str__(self):
        return f'slt {self.result_register}, {self.value1}, {self.value2}'

class MIPSSetOnLTENode(MIPSComparissonNode):
    def __str__(self):
        return f'sleu {self.result_register}, {self.value1}, {self.value2}'

class MIPSSetOnENode(MIPSComparissonNode):
    def __str__(self):
        return f'seq {self.result_register}, {self.value1}, {self.value2}'

class MIPSSetOnLTInmediateNode(MIPSComparissonNode):
    def __str__(self):
        return f'slti {self.result_register}, {self.value1}, {self.value2}'

class MIPSUnconditionalJumpNode(MIPSInstructionNode):
    def __init__(self, jump):
        self.jump = jump

class MIPSJumpNode(MIPSUnconditionalJumpNode):
    def __str__(self):
        return f"j {self.jump}"

class MIPSJumpRegisterNode(MIPSUnconditionalJumpNode):
    def __str__(self):
        return f"jr {self.jump}"

class MIPSJumpAndLinkNode(MIPSUnconditionalJumpNode):
    def __str__(self):
        return f"jal {self.jump}"

class MIPSJumpAndLinkRegNode(MIPSInstructionNode):
    def __init__(self, r):
        self.r = r

    def __str__(self):
        return f"jalr {self.r}"

class MIPSLabelNode(MIPSInstructionNode):
    def __init__(self, label):
        self.label = label

    def __str__(self):
        return f"{self.label}:"

class MIPSEmptyInstruction(MIPSInstructionNode):
     def __str__(self):
        return ""

class MIPSCommentNode(MIPSNode):
    def __init__(self, comment):
        self.comment = comment

    def __str__(self):
        return f"#{self.comment}"

class MIPSSyscallNode(MIPSInstructionNode):
    def __str__(self):
        return "syscall"

class MIPSMLONode(MIPSInstructionNode):
    def __init__(self,destiny):
        self.destiny = destiny
    def __str__(self):
        return f"mflo {self.destiny}"
