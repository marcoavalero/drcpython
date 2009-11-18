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
import drcdbe as query

yacc.yacc(module=drcdef)

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h:d", ["help", "debug"])
    except getopt.GetoptError:
        sys.exit(2)
    debug = False
    dbname = "metadata.db"
    dbtree = initializeDB(dbname)
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
            try:
                t.print_node()
            except:
                pass
            print "Syntax Error"
            continue
        try:
            if (t.nodeType == 'DBNode'):
                dbtree.print_node()
            else:
                if (t.nodeType == 'USEDB'):
                    dbtree = initializeDB(t.predicateName)
                else:
                    if debug:
                        free.set_free_variables(t)
                        limit.set_limits(t)
                        safe.safety_check(t)
                    elif not debug:
                        t.check_tables(dbtree)
                        free.set_free_variables(t)
                        limit.set_limits(t)
                        safe.safety_check(t)
                    t.print_node()
        except DrcError, e:
            if debug:
                t.print_node()
            print "\n*********************************************************************************************"
            print "%s: %s" %(type(e), str(e)) 
            print "*********************************************************************************************\n"
            continue
        
main()
