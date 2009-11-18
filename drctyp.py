from drcarg import *
from drcerr import *
from drcobj import *
from copy import *

def type_check(t):
    if t.nodeType == "Predicate":
        type_check_predicate(t)
    else:
        for item in t.children:
            type_check(item)

def type_check_predicate(t):
    x = [copy(a) for a in t.argList if type(a) == DRC_Var]
    while len(x) > 1:
        i = x.pop()
        for j in x:
            if i == j and i.type != j.type:
                raise TypeMatchingError("%s,%s" %(i,j))
