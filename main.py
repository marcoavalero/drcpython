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
import drctyp as tych
import drcdbe as query

yacc.yacc(module=drcdef)

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h:d", ["help", "debug"])
    except getopt.GetoptError:
        sys.exit(2)
    debug = False
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
                    if debug:
                        free.set_free_variables(t)
                        limit.set_limits(t)
                        safe.safety_check(t)
                        t.print_node()
                    elif not debug:
                        t.assign_type_to_nodes(dbtree,1)
                        t.assign_type_to_nodes(dbtree,2)
                        free.set_free_variables(t)
                        limit.set_limits(t)
                        safe.safety_check(t)
    	                query.gen_query(t,dbtree)
                        t.query = t.children[0].query
                        print "\nSQL QUERY:\n"
                        print t.query
                        print "\nRESULTS:\n"
                        query.execute_query(t,dbname)
        except DrcError, e:
            if debug:
                t.print_node()
            print "\n*********************************************************************************************"
            print "%s: %s" %(type(e), str(e)) 
            print "*********************************************************************************************\n"
            continue
        
main()
