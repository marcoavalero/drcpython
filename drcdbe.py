from drcarg import *
from drcobj import *

from sqlite3 import dbapi2 as sqlite

def initializeDB(dbname):

#    dbname = "metadata.db"
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
        tablenames.append(tablename[0].lower())

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
            if(columninfo[2] == "INTEGER" or columninfo[2] == "NUMBER" or columninfo[2] == "integer"):
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
    gen_comparison_query(drctree)
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
        if drctree.nodeType == "not":
            gen_not_query(drctree)
        if drctree.nodeType == "and":
            gen_and_query(drctree)
            

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

def gen_not_query(drctree):
    QUERY = ""
    flag = 0
    QUERY = "not in (" + drctree.children[0].query + ") "
    string_query =  QUERY 
    #print string_query
    drctree.query = string_query

def gen_comparison_query(drctree):
    if drctree.nodeType == "Comparison":
        QUERY = ""
        flag = 0
        QUERY = " " + drctree.operator + " " + str(drctree.rightOperand[0].data)
        string_query =  QUERY 
        #print string_query
        print "HERE!!!!"
        drctree.query = string_query
    else:
        count = 0
        for item in drctree.children:
            gen_comparison_query(drctree.children[count])     
            count = count + 1

def gen_and_query(drctree):
    FREEVAR = ""
    SFROM = ""
    WHERE = ""

###### FREE VARIABLES #################
    flag = 0
    for variable in drctree.freeVariables:
        if flag == 0:
            FREEVAR = FREEVAR + "TEMP" +  set_queryvar_for_and_node(drctree,variable) + "."+ variable.idid
            flag = 1
        else:
            FREEVAR = FREEVAR + ", TEMP"+ set_queryvar_for_and_node(drctree,variable) + "."+ variable.idid
###### FREE VARIABLES #################


###### FROM: REPEAT FOR EACH CHILD #################
    count = 0
    flag = 0
    for child in drctree.children:
        if (drctree.children[count].nodeType == "Predicate" or drctree.children[count].nodeType == "exists" or drctree.children[count].nodeType == "or"):
            if flag == 0:
                SFROM = SFROM + "(" + drctree.children[count].query + ")"
                SFROM = SFROM + " TEMP" + str(drctree.children[count].nodenumber)
                flag = 1
            else:
                SFROM = SFROM + ", (" + drctree.children[count].query + ")"
                SFROM = SFROM + " TEMP" + str(drctree.children[count].nodenumber)
        count = count + 1
###### FROM: REPEAT FOR EACH CHILD #################

###### WHERE: FOR COMPARISON###################
###### WHERE: FOR COMPARISON###################


###### WHERE: FOR NOT###################
    count = 0
    for child in drctree.children:
        if (drctree.children[count].nodeType == "not"):
            WHERE = " and (" + drctree.children[count].query + ")"
        count = count + 1
###### WHERE: FOR NOT###################

###### WHERE: JOIN CONDITIONS###################
###### WHERE: JOIN CONDITIONS###################

    string_query = " ".join(["select distinct", FREEVAR, "from", SFROM, "where 1=1",WHERE])  
    #print string_query
    drctree.query = string_query


def set_queryvar_for_and_node(drctree,variable):
    count = 0
    for child in drctree.children:
        if (drctree.children[count].nodeType == "Predicate" or drctree.children[count].nodeType == "exists" or drctree.children[count].nodeType == "or"):
            if variable in drctree.children[count].argList:
                    return str(drctree.children[count].nodenumber)
        count = count + 1

    return "-err"
