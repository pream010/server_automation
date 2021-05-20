#!/usr/bin/python

# importing module 
import mysql.connector as mysql

#connection estrablish from mysql database
try:
    mysqldb = mysql.connect(host='<IP>', database='<DB_SCHEMA>', user='<DB_USER>', password='<DB_PASS>')

    #Test the connection to print db info
    print("MySQL Databse version is:", mysqldb.get_server_info())
    
except mysql.connector.Error as err: 
    print("There is a problem with MySQL", err)
    
mysqldb.close()

#END_OF_SCRIPT
