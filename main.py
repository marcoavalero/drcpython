import sys
import drcdef
import warnings
import ply.yacc as yacc
from drcdef import *
from drcerr import *
from drcobj import *

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
 
            if (t.nodeType == 'DBNode'):
                dbtree.print_node()
            else:
                t.check_tables(dbtree)
                t.print_node()

        except DrcError:
            continue

        
main()
