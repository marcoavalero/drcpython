from drcarg import *
from drcerr import *
from drcobj import *

def set_limits(t):
  if t.nodeType == "Predicate":
        pass
  elif t.nodeType == "Comparison":
      limit_comparison(t)
  elif t.nodeType == "not":
      limit_not(t)
      for item in t.children:
          set_limits(item)
  elif t.nodeType == "exists":
      for item in t.children:
          set_limits(item)
  elif t.nodeType == "and" or t.nodeType == "or":
      for item in t.children:
          set_limits(item)
  elif t.nodeType == "Query":
      for item in t.children:
          set_limits(item)



def limit_comparison(t):
    if t.operator[0] == '=' and (type(t.rightOperand[0]) == DRC_Var and type(t.leftOperand[0]) == DRC_Var):
        for i in t.freeVariables:
            i.limited = False

def limit_not(t):
    for i in t.freeVariables:
        i.limited = False
    
