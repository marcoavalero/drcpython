from drcarg import *
from drcerr import *
class DRC(object):
    def __init__(self, nodeType):
        self.nodeType = nodeType
        #print "%s DRCNode created" % self.nodeType
        self.predicateName = "none"
        self.children = []
        self.argList = []
        self.varList = []
        self.leftOperand = ""
        self.operator = []
        self.rightOperand = ""
        self.freeVariables = []

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
        self.leftOperand = leftop

    def set_rightop(self, rightop):
        self.rightOperand = rightop

    def set_operator(self, operator):
        self.operator.append(operator)

        
    def print_node(self):
        print "------------DRCNode:", self.nodeType, "------------"
        if self.nodeType == "Predicate":
            print "Predicate name:", self.predicateName
        if len(self.varList) > 0:
            print "Variables list:", self.varList 
        if len(self.argList) > 0:
            print "Arguments list:", (map(str,self.argList))
        if len(self.children) > 0:
            print "Children:"
            count = 0
            for item in self.children:
                print self.children[count].nodeType
                count = count + 1
        if len(self.freeVariables) > 0:
            print "Free Variables: ", self.freeVariables
        if self.nodeType == "Comparison":
            print "Left operand:", self.leftOperand
            print "Operator:", self.operator
            print "Right operand:", self.rightOperand

        print "-------------------------------\n"
        count = 0
        for item in self.children:
            self.children[count].print_node()
            count = count + 1        

## ========= CONTROL ROUTINES ==================== ##
            
    def prune_tree(self):
        self.reduce_tree(3)
        self.reduce_tree(1)
        self.reduce_tree(2)
        self.reduce_tree(3)

    def check_node_reduction(self):
        if self.nodeType == "and":
            self.reduce_and()     
        if self.nodeType == "or":
            self.reduce_or() 
            self.safety_check_or()
            self.type_check()

    def set_free_variables(self):
        self.freeVariables = self.get_free_variables()

    def get_free_variables(self):
        if self.nodeType == "Predicate":
            return varList
        elif self.nodeType == "Comparison":
            return self.variable_check_comparison()
        elif self.nodeType == "not":
            for item in self.children:
                item.set_free_variables()
            return self.variable_check_not()
        elif self.nodeType == "exists":
            for item in self.children:
                item.set_free_variables()
            return self.variable_check_exists()
        elif self.nodeType == "Query":
            for item in self.children:
                item.set_free_variables()
            return self.get_free_from_subtree()    
            

    def safety_check(self):
        return True
            

## ========= REDUCTION ROUTINES ===================##

    def reduce_tree(self,action):
        if action == 1:
            self.check_node_reduction()
        if action == 2:
            self.demorgan_reduction()            
        if action == 3:
            self.double_not_reduction() 
        count = 0
        for item in self.children:
            self.children[count].reduce_tree(action)     
            count = count + 1

    def reduce_or(self):
        newNode = self.children.pop()
        if newNode.nodeType != "or":
            self.children.append(newNode)
        else:
            self.children.extend(newNode.reduce_or())
        return self.children
        
    def reduce_and(self):
        newNode = self.children.pop()
        if newNode.nodeType != "and":
            self.children.append(newNode)
        else:
            self.children.extend(newNode.reduce_and())
        return self.children


    def demorgan_reduction(self):
        if self.nodeType == "not" and self.children[0].nodeType == "or":
            count = 0
            for item in self.children[0].children:
                notnode  = DRC("not")  
                notnode.set_children(self.children[0].children[count])
                self.children.append(notnode)
                count = count + 1
            self.del_children(self.children[0])
            self.set_type("and")


    def double_not_reduction(self):
        count = 0
        for item in self.children:
            if self.children[count].nodeType == "not":
                if self.children[count].children[0].nodeType == "not":
                    self.children.append(self.children[count].children[0].children[0])
                    self.del_children(self.children[count]) 
                    self.double_not_reduction()
            count = count + 1

## =============== SAFETY CHECKS ============== ##

    def safety_check_or(self):
        allVariable = self.get_free_from_subtree()
        byVariable = set(allVariable)
        for item in self.children:
            vars = filter((lambda a: type(a) == DRC_Var and a.free == True), item.argList)
            if len(byVariable) == len(vars) and byVariable - set(vars) == set([]):
                continue
            else:
                mySet = byVariable - set(vars)
                mySet = map((lambda a: a.idid), mySet)
                print "Unmatched Variable in Predicate: %s" % (mySet)
                raise UnmatchedVariableError

## =============== TYPE CHECK ROUTINES ======== ##

    def type_check(self):
        allVariable= self.get_free_from_subtree()
        eachVariable = []
        byVariable = set(allVariable)
        print map(str, byVariable) #debug line
        print map(str, allVariable) #debug line
        truthTable = [(verify(x,y)) for x in byVariable for y in allVariable]
        truthTable = filter((lambda a: a == False), truthTable)
        if len(truthTable) > 0:
            return False
        else:
            return True
               
        
## ============ Usefull Subroutines ==============##

    def get_free_from_subtree(self):
        allVariable = []
        for item in self.children:
            for arg in item.argList:
                if type(arg) == DRC_Var and arg.free == True:
                    allVariable.append(arg)
                elif type(arg) == DRC:
                    allVariable.extend(arg.get_free_from_subtree())
        return allVariable

    def variable_check_comparison(self):
        k = self.leftOperand + self.rightOperand
        if type(self.rightOperand[0]) != DRC_Var and type(self.leftOperand[0]) != DRC_Var:
            print "Left and Right operands of comparison statement cannot both be constants"
            raise ComparingConstantsError 
        elif self.operator[0] != '=' or (type(self.rightOperand[0]) == DRC_Var and type(self.leftOperand[0]) == DRC_Var):
            for i in k:
                if type(i) == DRC_Var:
                    i.limited = False
        if type(self.rightOperand[0]) != type(self.leftOperand[0]):
            v = filter(lambda a: type(a) == DRC_Var, k)
            c = filter(lambda a: type(a) != DRC_Var, k)
            if type(c[0]) == Str_Con:
                v[0].type = "STRING"
            else:
                v[0].type = "NUMBER"
        return [x for x in k if type(x)==DRC_Var]

    def variable_check_not(self):
        x = []
        for item in self.children:
            x.append(item.get_free_variables())
        for i in x:
            if type(i) == DRC_Var:
                i.limited = False
        return x

    def variable_check_exists(self):
        print self.varList
        free = []
        for item in self.children:
            free.extend(item.get_free_variables())
        for item in free:
            if item in self.varList:
                free.remove(item)
        return free
