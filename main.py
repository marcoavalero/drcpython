import sys
import drcdef
import warnings
import ply.yacc as yacc
from drcdef import *
from drcerr import *
from drcobj import *
import drcfre as free
import drcsaf as safe
import drclim as limit

yacc.yacc(module=drcdef)

def main():
    while True:
        try:
            s = raw_input('DRC> ')
        except EOFError:
            break
        try:
            t = yacc.parse(s)
        except DrcError:
            continue
        try:
            free.set_free_variables(t)
            limit.set_limits(t)
            safe.safety_check(t)
        except DrcError:
            continue
        t.print_node()
        
main()
