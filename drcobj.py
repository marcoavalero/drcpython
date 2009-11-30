from drcarg import *
from drcerr import *
from copy import *
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
        self.nodenumber = 0
        self.query = ""

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
        self.operator = operator 

    def set_free_variables(self, varlist):
        self.freeVariables = varlist
        
    def print_node(self):
        if self.nodeType != "EMPTY":
            print "------------DRCNode:", self.nodeType, "------------"
            print "Node Number:", self.nodenumber
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
            #if self.query != "":
            #    print "Query: ", self.query

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
        self.reduce_tree(4)

    def check_node_reduction(self):
        if self.nodeType == "and":
            self.reduce_and()     
        if self.nodeType == "or":
            self.reduce_or() 



            
            


            

## ========= REDUCTION ROUTINES ===================##

    def reduce_tree(self,action):
        if action == 1:
            self.check_node_reduction()
        if action == 2:
            self.demorgan_reduction()            
        if action == 3:
            self.double_not_reduction() 
        if action == 4:
            self.compare_not_reduction()
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

    def compare_not_reduction(self):
        for item in self.children:
            if self.nodeType == "not" and item.nodeType == "Comparison":
                o = []
                l = copy(item.leftOperand)
                r = copy(item.rightOperand)
                if item.operator == '<>':
                    o = '='
                elif item.operator == '=':
                    o = '<>'
                elif item.operator == '>':
                    o = '<='
                elif item.operator == '<':
                    o = '>='
                elif item.operator == '>=':
                    o = '<'
                elif item.operator == '<=':
                    o = '>'
                self.set_leftop(l)
                self.set_rightop(r)
                self.set_operator(o)
                self.set_type("Comparison")
                self.del_children(item)

## =============== TYPE CHECK ROUTINES ======== ##

#    def type_check(self):
#        allVariable= self.get_free_from_children()
#        eachVariable = []
#        byVariable = set(allVariable)
#        print map(str, byVariable) #debug line
#       print map(str, allVariable) #debug line
#        truthTable = [(verify(x,y)) for x in byVariable for y in allVariable]
#        truthTable = filter((lambda a: a == False), truthTable)
#        if len(truthTable) > 0:
#            return False
#        else:
#            return True
 
    def type_check(self):
        if self.nodeType == 'and':
            self.type_check_and()

    def type_check_and(self):
        for item in self.children:
            pass
        
## ============ Usefull Subroutines ==============##

    def get_free_from_children(self):
        allVariable = []
        for item in self.children:
            allVariable.extend(item.freeVariables)
        return allVariable

    def numbernodes(self,number):
        self.nodenumber = number
        count = 0
        for item in self.children:
            number = self.children[count].numbernodes(number + 1)
            count = count + 1
        return number


    def check_tablename(self,predicatenode):
        if self.nodeType != "EMPTY":
            if self.predicateName == predicatenode.predicateName:
                #print "Table %s found" % predicatenode.predicateName
                tablelen = len(self.argList)
                predicatelen = len(predicatenode.argList)
                if  tablelen !=  predicatelen:
                #    print "Number of columns do NOT MATCH"
                    raise ColumnsError("Error on table %s " % predicatenode.predicateName)
                else:
                    #print "Number of columns MATCHED"
                    count = 0
                    for arguments in self.argList:
                        if predicatenode.argList[count].type != "UKNOWN":
                            if not type_check(self.argList[count],predicatenode.argList[count]):
                                raise TypeMatchingError("Error on table %s " % predicatenode.predicateName)
                        else:
                            predicatenode.argList[count].type = self.argList[count].type
                            #print "ASSIGNED TYPE" , self.argList[count].type
                        count = count + 1
            else:
                self.children[0].check_tablename(predicatenode)
        else:
            raise TableNameError( "Table %s not found" % predicatenode.predicateName)


    def assign_type_to_nodes(self,dbtree,action):
        if action == 1 :
            #print "Assigning types to predicate nodes"
            if self.nodeType == "Predicate":
                dbtree.check_tablename(self)
            count = 0
            for item in self.children:
                self.children[count].assign_type_to_nodes(dbtree,action)     
                count = count + 1
        if action == 2:
            if self.nodeType == "and":
                #print "Assigning types to comparison nodes: "
                count = 0
                for item in self.children:
                    if self.children[count].nodeType == "Comparison":
                        #print "Before"
                        #print self.children[count].rightOperand
                        #print self.children[count].leftOperand
                        self.assign_comparison_type(self.children[count])
                        #print "After"
                        #print self.children[count].rightOperand
                        #print self.children[count].leftOperand
                    count = count + 1
            count = 0
            for item in self.children:
                self.children[count].assign_type_to_nodes(dbtree,action)     
                count = count + 1

    def assign_comparison_type(self,comparison_node):
        for predicatenode in self.children:
            if predicatenode.nodeType == "Predicate":
                for argument in predicatenode.argList:
                    if comparison_node.rightOperand[0] == argument:
                        comparison_node.rightOperand[0].type = argument.type
                    if comparison_node.leftOperand[0] == argument:
                        comparison_node.leftOperand[0].type = argument.type
