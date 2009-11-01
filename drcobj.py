from drcarg import *
from drcerr import *
#from drcdbe import *


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
            return self.argList
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
        elif self.nodeType == "and" or self.nodeType == "or":
            for item in self.children:
                item.set_free_variables()
            return self.variable_check_and_or()
        elif self.nodeType == "Query":
            for item in self.children:
                item.set_free_variables()
            return self.variable_check_query()
            
            

    def safety_check(self):
        for item in self.children:
            if (item.nodeType == "not" or item.nodeType == "Comparison") and self.nodeType != "and":
                print "%s-node requires and-node as parent" %(item.nodeType)
                raise SafetyError
        if self.nodeType == "Query":
            self.safety_check_query()
        elif self.nodeType == "or":
            self.safety_check_or()
        elif self.nodeType == "and":
            self.safety_check_and()
        for item in self.children:
            item.safety_check()
            

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

    def safety_check_query(self):
        for item in self.freeVariables:
            if item not in self.varList:
                print "Unmatched Free Variable in Query %s" %(item)
                raise UnmatchedVariableError
        for item in self.varList:
            if item not in self.freeVariables:
                print "Unmatched Argument in Query %s" %(item)
                raise UnmatchedVariableError
            
    def safety_check_or(self):
        byVariable = set(self.freeVariables)
        for item in self.children:
            vars = item.freeVariables
            if len(byVariable) == len(vars) and byVariable - set(vars) == set([]):
                continue
            else:
                mySet = byVariable - set(vars)
                mySet = map((lambda a: a.idid), mySet)
                print "Unmatched Variable in Predicate: %s" % (mySet)
                raise UnmatchedVariableError

    def safety_check_and(self):
        for item in self.freeVariables:
            if item.limited == False:
                print "non-limited free variable in and-node"
                raise SafetyError

## =============== TYPE CHECK ROUTINES ======== ##

    def type_check(self):
        allVariable= self.get_free_from_children()
        eachVariable = []
        byVariable = set(allVariable)
#        print map(str, byVariable) #debug line
 #       print map(str, allVariable) #debug line
        truthTable = [(verify(x,y)) for x in byVariable for y in allVariable]
        truthTable = filter((lambda a: a == False), truthTable)
        if len(truthTable) > 0:
            return False
        else:
            return True
               
        
## ============ Usefull Subroutines ==============##

    def get_free_from_children(self):
        allVariable = []
        for item in self.children:
            allVariable.extend(item.freeVariables)
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
        free = []
        for item in self.children:
            free.extend(item.get_free_variables())
        for item in free:
            if item in self.varList:
                free.remove(item)
        return free

    def variable_check_and_or(self):
        free = []
        for item in self.children:
            x = []
            x.extend(item.get_free_variables())
            for i in x:
                if i.type == "UNKNOWN" and i in free:
                    x.remove(i)
            free = self.balance(free, x)
        return free

    def balance(self,f,x):
        if len(x) == 0:
            return f
        else:
            i = x.pop(0)
            if i not in f:
                f.append(i)
            else:
                j = f[f.index(i)]
                f.remove(i)
                if self.nodeType == "and":
                    if j.limited == True or i.limited == True:
                        j.limited, i.limited = True, True
                    else:
                        j.limited, i.limited = False, False
                elif self.nodeType=="or":
                    if j.limited == True and i.limited == True:
                        j.limited, i.limited = True, True
                    else:
                        j.limited, i.limited = False, False
                if verify(j,i):
                    f.append(j)
                else:
                    if j.type == "UNKNOWN":
                        f.append(i)
                    else:
                        print "Types do not Match: %s, %s" %(i,j)
                        raise TypeMatchingError
            return self.balance(f,x)

    def variable_check_query(self):
        free = []
        for item in self.children:
            x = []
            x.extend(item.get_free_variables())
            free.extend(x)
        return free

    def check_tablename(self,predicatenode):
        if self.nodeType != "EMPTY":
            if self.predicateName == predicatenode.predicateName:
                print "Table %s found" % predicatenode.predicateName
                tablelen = len(self.argList)
                predicatelen = len(predicatenode.argList)
                if  tablelen !=  predicatelen:
                    print "Number of columns do NOT MATCH"
                else:
                    print "Number of columns MATCHED"
                    count = 0
                    for arguments in self.argList:
                        if predicatenode.argList[count].type != "UKNOWN":
                            print type_check(self.argList[count],predicatenode.argList[count])
                        else:
                            predicatenode.argList[count].type = self.argList[count].type
                        count = count + 1
            else:
                self.children[0].check_tablename(predicatenode)
        else:
            print "Table %s NOT found" % predicatenode.predicateName
            


    def check_tables(self,dbtree):
        if self.nodeType == "Predicate":
            dbtree.check_tablename(self)
        count = 0
        for item in self.children:
            self.children[count].check_tables(dbtree)     
            count = count + 1

    def printdb(self,dbtree):
        print "******************DATABASE TREE*****************************"
        dbtree.print_node() 


