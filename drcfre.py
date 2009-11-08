from drcarg import *
from drcerr import *
from drcobj import *


def set_free_variables(t):
    t.set_free_variables(get_free_variables(t))

def get_free_variables(t):
    if t.nodeType == "Predicate":
        return filter(lambda a: type(a) == DRC_Var, t.argList)
    elif t.nodeType == "Comparison":
        return variable_check_comparison(t)
    elif t.nodeType == "not":
        for item in t.children:
            set_free_variables(item)
        return variable_check_not(t)
    elif t.nodeType == "exists":
        for item in t.children:
            set_free_variables(item)
        return variable_check_exists(t)
    elif t.nodeType == "and" or t.nodeType == "or":
        for item in t.children:
            set_free_variables(item)
        return variable_check_and_or(t)
    elif t.nodeType == "Query":
        for item in t.children:
            set_free_variables(item)
        return variable_check_query(t)    
        
def variable_check_comparison(t):
    k = t.leftOperand + t.rightOperand
    if type(t.rightOperand[0]) != DRC_Var and type(t.leftOperand[0]) != DRC_Var:
        print "Left and Right operands of comparison statement cannot both be constants"
        raise ComparingConstantsError 
    elif t.operator[0] == '=' and (type(t.rightOperand[0]) == DRC_Var and type(t.leftOperand[0]) == DRC_Var):
        for i in k:
            if type(i) == DRC_Var:
                i.limited = False
    if type(t.rightOperand[0]) != type(t.leftOperand[0]):
        v = filter(lambda a: type(a) == DRC_Var, k)
        c = filter(lambda a: type(a) != DRC_Var, k)
        if type(c[0]) == Str_Con:
            v[0].type = "STRING"
        else:
            v[0].type = "NUMBER"
    return [x for x in k if type(x)==DRC_Var]

def variable_check_not(t):
    free = []
    for item in t.children:
        free.extend(get_free_variables(item))
    return free

def variable_check_exists(t):
    free = []
    for item in t.children:
        free.extend(get_free_variables(item))
    for item in free:
        if item in t.varList:
            free.remove(item)
    return free

def variable_check_and_or(t):
    free = []
    for item in t.children:
        x = []
        x.extend(get_free_variables(item))
        for i in x:
            if i.type == "UNKNOWN" and i in free:
                x.remove(i)
        free = balance(t,free, x)
    return free

def balance(t,f,x):
    if len(x) == 0:
        return f
    else:
        i = x.pop(0)
        if i not in f:
            f.append(i)
        else:
            j = f[f.index(i)]
            f.remove(i)
            if t.nodeType == "and":
                if j.limited == True or i.limited == True:
                    j.limited, i.limited = True, True
                else:
                    j.limited, i.limited = False, False
            elif t.nodeType=="or":
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
        return balance(t,f,x)

def variable_check_query(t):
    free = []
    for item in t.children:
        x = []
        x.extend(get_free_variables(item))
        free.extend(x)
    return free
