class DRC(object):
    def __init__(self, nodeType):
        self.nodeType = nodeType
        #print "%s DRCNode created" % self.nodeType
        self.predicateName = "none"
        self.children = []
        self.argList = []
        self.varList = []
        self.leftOperand = []
        self.leftOperandType = []
        self.operator = []
        self.rightOperand = []
        self.rightOperandType = []

#    def __del__(self):
        #print "%s DRCNode removed" % self.nodeType

    def set_type(self, nodeType):
        self.nodeType = nodeType

    def set_predicate(self, pName):
        self.predicateName = pName

    def set_children(self, child):
        self.children.append(child)

    def add_children(self, children):
        self.children = self.children + children

    def del_children(self, child):
        self.children.remove(child)

    def set_arglist(self, arglist):
        self.argList.append(arglist)

    def set_varlist(self, varlist):
        self.varList.append(varlist)

    def set_leftop(self, leftop):
        self.leftOperand.append(leftop)

    def set_leftop_type(self, leftop_type):
        self.leftOperandType.append(leftop_type)

    def set_rightop(self, rightop):
        self.rightOperand.append(rightop)

    def set_rightop_type(self, rightop_type):
        self.rightOperandType.append(rightop_type)

    def set_operator(self, operator):
        self.operator.append(operator)

        
    def print_node(self):
        print "------------DRCNode------------"
        print "Node type: ", self.nodeType
        if self.nodeType == "Predicate":
            print "Predicate name:", self.predicateName
        if len(self.varList) > 0:
            print "Variables list:", self.varList 
        if len(self.argList) > 0:
            print "Arguments list:", self.argList
        if len(self.children) > 0:
            print "Children:"
            count = 0
            for item in self.children:
                print self.children[count].nodeType
                count = count + 1               
        if self.nodeType == "Comparison":
            print "Left operand:", self.leftOperand
            print "Operator:", self.operator
            print "Right operand:", self.rightOperand

        print "-------------------------------\n"
        count = 0
        for item in self.children:
            self.children[count].print_node()
            count = count + 1        



    def reduceand(self):
       if self.children[1].children[1].nodeType == "and":
           print "Reducing Again"
           self.children[1].reduceand()
           self.copy_my_child_children()
       else:
           self.copy_my_child_children()

    def copy_my_child_children(self):
       count = 0
       for item in self.children[1].children:
           print "Copying child %d " % count
           print self.children[1].children[count].argList
           print ""
           self.children.append(self.children[1].children[count])
           count = count + 1
       print "Removing child " + self.children[1].nodeType
       self.del_children(self.children[1])
       print "Returning to function"

    def checknodereduction(self):
        print "I am " + self.nodeType
        if self.nodeType == "and" and self.children[1].nodeType == "and":
            print "Reducing and"
            self.reduceand()     
        if self.nodeType == "or" and self.children[1].nodeType == "or":
            print "Reducing or"
            self.reduceand() 

    def reducetree(self):
        self.checknodereduction()
        count = 0
        for item in self.children:
            self.children[count].reducetree()     
            count = count +1
            

