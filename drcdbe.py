from drcarg import *
from drcobj import *

from sqlite3 import dbapi2 as sqlite

def initializeDB():

    dbname = "metadata.db"
    connection = sqlite.connect(dbname)
    cursor = connection.cursor()
    cursor1 = connection.cursor()
    cursor2 = connection.cursor()
    tablenames = []
    columnshash = {}
    argumenthash = {}

    cursor.execute( "select tbl_name from sqlite_master where type = 'table'" )
    listoftables = cursor.fetchall()
    for tablename in listoftables :
        tablenames.append(tablename[0])

    for tablename in tablenames :
        cursor1.execute("pragma table_info("+tablename+")")
        columns = cursor1.fetchall()
        columnshash[tablename] = len(columns)

    children = DRC("EMPTY")
    for tablename in tablenames :
        drcobject  = DRC("Predicate")
        drcobject.set_predicate(tablename)
        drcobject.set_children(children)
        cursor2.execute("pragma table_info("+tablename+")")
        for columninfo in cursor2:
            #        print columninfo[2]
            if(columninfo[2] == "INTEGER"):
                argg = Int_Con(data=columninfo[1])
            else:
                argg = Str_Con(data=columninfo[1])
            drcobject.set_arglist(argg)
        children = drcobject
    
    connection.close()
    return children

def gen_query(drctree,dbtree):
    print "GENERATING QUERY:"
    gen_predicate_query(drctree,dbtree)
    gen_internal_query(drctree,dbtree)

def gen_predicate_query(drctree,dbtree):
    SQUE = ""
    SQUEtemp = ""
    SFROM = ""
    SWHERE = ""
    S1WHERE = ""
    if drctree.nodeType == "Predicate":
           table = find_table(drctree.predicateName,dbtree)

           count = 0

           S1=set(drctree.argList)
           
           for variable in drctree.argList:
               if type(variable) == DRC_Var and variable in S1:
                   S1.remove(variable)
                   if variable in drctree.freeVariables :
                       if count == 0:
                           SQUE = table.argList[drctree.argList.index(variable)].data + " " + variable.idid
                       else:
                           SQUEtemp = table.argList[drctree.argList.index(variable)].data + " " + variable.idid
                           SQUE = ",".join([SQUE, SQUEtemp])
                       count = count + 1
               else:
                   if variable in S1:
                       SWHERE = SWHERE + " and " + table.argList[drctree.argList.index(variable)].data + " = " + str(variable.data)

           # To compare duplicate variables
           S=set(drctree.argList)
           while len(S) > 0:
               R = []	
               a = S.pop()
               count = 0 
               for item in drctree.argList:
                   if item == a:
                       R.append(count)
                   count = count + 1
               #print R  
               if len(R) > 1:
                   for i in range(1,len(R)):
                       S1WHERE = S1WHERE + " and " + table.argList[R[0]].data + " = " + table.argList[R[i]].data
                   #print S1WHERE

           SFROM = drctree.predicateName
           string_query = " ".join(["select distinct", SQUE, "from", SFROM, "where 1=1", SWHERE, S1WHERE])  
           print string_query
           drctree.query = string_query
    else:
        count = 0
        for item in drctree.children:
            gen_predicate_query(drctree.children[count],dbtree)     
            count = count + 1

def find_table(name, dbtree):
    if dbtree.nodeType != "EMPTY":
        if dbtree.predicateName == name:
            return dbtree
        else:
           return find_table(name, dbtree.children[0]) 
    else:
        print "Error finding table"


def gen_internal_query(drctree,dbtree):
    for item in drctree.children:
        if item.query == "":
            gen_internal_query(item,dbtree)     
            
        if drctree.nodeType == "exists":
            gen_exists_query(drctree)
        if drctree.nodeType == "or":
            gen_or_query(drctree)
        if drctree.nodeType == "and":
            print "and function"

def gen_exists_query(drctree):
    FREEVAR = ""
    SFROM = ""
    flag = 0
    for variable in drctree.freeVariables:
        if flag == 0:
            FREEVAR = FREEVAR + "TEMP"+  str(drctree.children[0].nodenumber) + "."+ variable.idid
            flag = 1
        else:
            FREEVAR = FREEVAR + ", TEMP"+ str(drctree.children[0].nodenumber) + "."+ variable.idid
    SFROM = SFROM + "(" + drctree.children[0].query + ")"
    SFROM = SFROM + " TEMP" + str(drctree.children[0].nodenumber)

    if variable in drctree.freeVariables :
        string_query = " ".join(["select distinct", FREEVAR, "from", SFROM, "where 1=1"])  
    #print string_query
    drctree.query = string_query

def gen_or_query(drctree):
    QUERY = ""
    flag = 0
    for child in drctree.children:
        if flag == 0:
            QUERY = QUERY + child.query
            flag = 1
        else:
            QUERY = QUERY + " UNION " + child.query
    string_query =  QUERY 
    #print string_query
    drctree.query = string_query
