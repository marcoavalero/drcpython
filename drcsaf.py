from drcarg import *
from drcerr import *
from drcobj import *

def safety_check(t):
    for item in t.children:
        if (item.nodeType == "not" or item.nodeType == "Comparison") and t.nodeType != "and":
            print "%s-node requires and-node as parent" %(item.nodeType)
            raise SafetyError
    if t.nodeType == "Query":
        safety_check_query(t)
    elif t.nodeType == "or":
        safety_check_or(t)
    elif t.nodeType == "and":
        safety_check_and(t)
    elif t.nodeType == 'exists':
        safety_check_exists(t)
    for item in t.children:
        safety_check(item)

def safety_check_query(t):
    s = set(t.argList)
    if len(s) != len (t.argList):
        print "repeated variable in exists node"
        raise SafetyError
    for item in t.freeVariables:
        if item not in t.varList:
            print "Unmatched Free Variable in Query %s" %(item)
            raise UnmatchedVariableError
    for item in t.varList:
        if item not in t.freeVariables:
            print "Unmatched Argument in Query %s" %(item)
            raise UnmatchedVariableError

def safety_check_or(t):
    byVariable = set(t.freeVariables)
    for item in t.children:
        vars = item.freeVariables
        if len(byVariable) == len(vars) and byVariable - set(vars) == set([]):
            continue
        else:
            mySet = byVariable - set(vars)
            mySet = map((lambda a: a.idid), mySet)
            print "Unmatched Variable in Predicate: %s" % (mySet)
            raise UnmatchedVariableError

def safety_check_and(t):
    for item in t.freeVariables:
        if item.limited == False:
            print "non-limited free variable in and-node"
            raise SafetyError


def safety_check_exists(t):
    s = set(t.varList)
    if len(s) != len (t.varList):
        print "repeated variable in exists node"
        raise SafetyError
