#!/usr/bin/python3

# importing module
import mysql.connector as mysql
import csv
import pandas as pd

##########START_OF_MySQL Block##########
#connection estrablish from mysql database
try:
    mysqldb = mysql.connect(host='<ip>', database='<DB_NAME>', user='<USER_NAME>', password='<PWD>')
    try:
        # MySQL select query
        mysqlquery = """<SQL_QUERY>"""

        # fetching all records
        records = pd.read_sql_query(mysqlquery, mysqldb)

        #Save it as csv file in folder:
        records.to_csv('<PATH>', index=False)

    except Exception as mysqlqueryerr:
        print("There is issue with : ", mysqlqueryerr)

except mysql.connector.Error as mysqlerr:
    print("There is a problem with MySQL", mysqlerr)

finally:
    if mysqldb:
        mysqldb.close()

##########END_OF_MySQL Block##########
