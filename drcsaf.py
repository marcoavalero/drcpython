from drcarg import *
from drcerr import *
from drcobj import *

def safety_check(t):
    for item in t.children:
        if (item.nodeType == "not" or item.nodeType == "Comparison") and t.nodeType != "and":
            raise SafetyError("%s node (%d) requires and node as parent" %(item.nodeType, item.nodenumber))
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
        raise SafetyError("repeated variable in %s node (%d)" %(item, t.nodeType, t.nodenumber))
    for item in t.freeVariables:
        if item not in t.varList:
            raise UnmatchedVariableError("Unmatched Free Variable %s in %s node (%d)" %(item, t.nodeType, t.nodenumber))
    for item in t.varList:
        if item not in t.freeVariables:
            raise UnmatchedVariableError("Unmatched Free Variable %s in %s node (%d)" %(item, t.nodeType, t.nodenumber))

def safety_check_or(t):
    byVariable = set(t.freeVariables)
    for item in t.children:
        vars = item.freeVariables
        if len(byVariable) == len(vars) and byVariable - set(vars) == set([]):
            continue
        else:
            mySet = byVariable - set(vars)
            mySet = map((lambda a: a.idid), mySet)
            raise UnmatchedVariableError("Unmatched Variable %s in disjunct for %s node (%d)" % (mySet, t.nodeType, t.nodenumber))

def safety_check_and(t):
    for item in t.freeVariables:
        if item.limited == False:
            raise SafetyError("variable %s not limited in %s node (%d)" %(item, t.nodeType, t.nodenumber))


def safety_check_exists(t):
    s = set(t.varList)
    if len(s) != len (t.varList):
        raise SafetyError("repeated variable in %s node (%d)" %(t.nodeType, t.nodenumber))
