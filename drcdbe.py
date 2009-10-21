from drcarg import *
from drcobj import *

from pysqlite2 import dbapi2 as sqlite
dbname = "metadata.db"
connection = sqlite.connect(dbname)
cursor = connection.cursor()
cursor1 = connection.cursor()
cursor2 = connection.cursor()
tablenames = []
columnshash = {}
argumenthash = {}

cursor.execute( "select tbl_name from sqlite_master where type = 'table'" )
list_tables = cursor.fetchall()
for table_name in list_tables :
    tablenames.append(table_name[0])

for tables in tablenames :
    cursor1.execute("pragma table_info("+tables+")")
    columns = cursor1.fetchall()
    print '-'*60
    print tables
    print len(columns)
    columnshash[tables] = len(columns)
    cursor2.execute("pragma table_info("+tables+")")
    for row in cursor2:
        print 'Name: ', row[1], ' Type: ', row[2]
print columnshash
    
connection.close()
