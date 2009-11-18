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
#    dbname = "metadata.db"
    dbname = "dbs/modb.sql"
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
                if (t.nodeType != 'null'):
                    t.print_node()
            except:
                pass
            print "Syntax Error"
            continue
        try:
            if (t.nodeType == 'DBNode'):
                dbtree.print_node() 
                t.nodeType = 'null'
            else:
                if (t.nodeType == 'USEDB' or t.nodeType == 'HELP' or t.nodeType == 'DEBUG' or t.nodeType == 'NODEBUG'):
                    if (t.nodeType == 'USEDB'):
                        dbtree = initializeDB(t.predicateName)
                    if (t.nodeType == 'DEBUG'):
                        debug = True
                    if (t.nodeType == 'NODEBUG'):
                        debug = False
                    t.nodeType = 'null'
                else:
                    free.set_free_variables(t)
                    limit.set_limits(t)
                    safe.safety_check(t)
                    if not debug:
                        t.check_tables(dbtree)
    	                query.gen_query(t,dbtree)
                    t.print_node()
        except DrcError, e:
            if debug:
                t.print_node()
            print "\n*********************************************************************************************"
            print "%s: %s" %(type(e), str(e)) 
            print "*********************************************************************************************\n"
            continue
        
main()
