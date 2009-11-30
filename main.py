import sys, getopt
import drcdef
import warnings
import readline
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
        opts, args = getopt.getopt(sys.argv[1:], "hd:u:p:b", ["help", "database=", "debug"])
    except getopt.GetoptError:
        sys.exit(2)
    debug = False
    printing = False
    dbname = "modb"
    username = ''
    password = ''
    host_serv = 'localhost'

    for o, a in opts:
        if o in ('-h', '--help'):
            print "DRC Parser version 1.0 (by Marco Valero & John Daigle)\n\nCommand\t\t\tDescription\n-------\t\t\t----------\n-h, --help\t\tprint this message and exit\n-d db_name,\t\tchoose a starting database\n--database=db_name\t\t\n'-b'\t\t\tEnables debug mode\n'-p=password'\t\trequire password\n'-u username'\t\tset username\n"
            sys.exit()
        if o in ('-b'):
            debug = True
        if o in ('-d', '--database='):
            dbname=str(a)
        if o in ('-u'):
            username = str(a)
        if o in ('-p'):
            password = str(a)
    dbtree = initializeDB(dbname, host_serv, username, password)
    while True:
        try:
            s = ''
            a = True
            while a == True:
                s = s + raw_input('DRC> ')
                if s.startswith('{'):
                    while not ('}') in s:
                        s = s + raw_input('DRC> ')
                    a = False
                else:
                    a = False
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
                if (t.nodeType == 'USEDB' or t.nodeType == 'HELP' or t.nodeType == 'DEBUG' or t.nodeType == 'NODEBUG' or t.nodeType == 'PRINTING'):
                    if (t.nodeType == 'USEDB'):
                        dbname = t.predicateName
                        dbtree = initializeDB(dbname, host_serv, username, password)
                    if (t.nodeType == 'PRINTING'):
                        printing = not printing
                        print "Printing mode " , printing
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
                        if printing: 
                            t.print_node()
                            print "\nSQL QUERY:\n"
                            print t.query
                        print "\nRESULTS:\n"
                        query.execute_query(t,dbname, host_serv, username, password)
                        t.nodeType = 'null'
        except DrcError, e:
            if debug:
                t.print_node()
            print "\n*********************************************************************************************"
            print "%s: %s" %(type(e), str(e)) 
            print "*********************************************************************************************\n"
            continue


       

main()


