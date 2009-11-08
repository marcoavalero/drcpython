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
    dbtree = initializeDB()
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
            if (t.nodeType == 'DBNode'):
                dbtree.print_node()
            else:
                free.set_free_variables(t)
    	        limit.set_limits(t)
                safe.safety_check(t)
                t.check_tables(dbtree)
                t.print_node()
        except DrcError:
            continue
        
main()
