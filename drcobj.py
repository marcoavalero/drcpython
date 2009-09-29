class DRC(object):
    def __init__(self, nodeType):
        self.nodeType = nodeType
        print "%s DRCNode created" % self.nodeType
        self.predicateName = "tablename"
        self.children = []
        self.argList = []
        self.varList = []
        self.leftOperand = []
        self.leftOperandType = []
        self.operator = []
        self.rightOperand = []
        self.rightOperandType = []

    def set_predicate(self, pName):
        self.predicateName = pName

    def set_children(self, child):
        self.children.append(child)

    def set_arglist(self, arglist):
        self.argList.append(arglist)

    def set_varlist(self, varlist):
        self.varList.append(varlist)

    def set_arglist(self, leftop):
        self.leftOperand.append(leftop)

    def set_arglist(self, leftop_type):
        self.leftOperandType.append(leftop_type)

    def set_arglist(self, rightop):
        self.rightOperand.append(rightop)

    def set_arglist(self, rightop_type):
        self.rightOperandType.append(rightop_type)

    def set_arglist(self, operator):
        self.operator.append(operator)
