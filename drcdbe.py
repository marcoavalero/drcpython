from drcarg import *
from drcobj import *

from sqlite3 import dbapi2 as sqlite
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
        if(columninfo[2] == "TEXT"):
            argg = Str_Con(data=columninfo[1])
        if(columninfo[2] == "INTEGER"):
            argg = Int_Con(data=columninfo[1])
        else:
            argg = DRC_Var(idid=columninfo[1])
        drcobject.set_arglist(argg)
    children = drcobject
    
children.print_node() 
    
connection.close()
