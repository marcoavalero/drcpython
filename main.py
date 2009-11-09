import sys, getopt
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
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h:d", ["help", "debug"])
    except getopt.GetoptError:
        sys.exit(2)
    debug = False
    dbtree = initializeDB()
    for opt, arg in opts:
        if opt in ("-h, help"):
            usage()
            sys.exit()
        elif opt in ('-d'):
            debug = True
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
                if not debug:
                    t.check_tables(dbtree)
                t.print_node()
        except DrcError:
            continue
        
main()
