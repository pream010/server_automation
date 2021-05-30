#!/usr/bin/python3

#Change record creation
#Get the server schedule details from MySQL db and create changes in SNOW

import mysql.connector
import os

try:
    connection = mysql.connector.connect(host='localhost',
                                         database='patching_reporting',
                                         user='root',
                                         password='Patch@123')

    sql_select_Query = """SELECT ci.hostname,
    ci.ip_address,
    ci.environment,
    ci.os,
    ci.os_version,
    mw.frequency,
    mw.schedule_day,
    YEAR(cs.date) as year,
    MONTHNAME(cs.date) as month,
    CONCAT(cs.date," ",mw.start_time) as schedule_start_time,
    ADDTIME(CONCAT(cs.date," ",mw.start_time),duration) as schedule_end_time,
    ci.sys_id
    FROM `patching_reporting`.`cmdb_ci_server` as ci
    INNER JOIN `patching_reporting`.`mw_schedule` as mw ON ci.hostname=mw.hostname AND YEAR(mw.start_time)=YEAR(CURDATE())
    INNER JOIN `patching_reporting`.`cal_schedule` as cs ON mw.schedule_day=cs.nth_day_week
    WHERE cs.date > CURDATE() AND cs.date < DATE_ADD(CURDATE(), INTERVAL 15 DAY)"""
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)

    # get all records
    records = cursor.fetchall()

    for row in records:
        hostname = row[0]
        schedule_start_time = row[9]
        schedule_end_time = row[10]
        ci_sys_id = row[11]
        cmd = "./chg_auto_creation.py" " '" +schedule_start_time+ "' '" +schedule_end_time+ "' '" +ci_sys_id +"'"
        print(os.system(cmd))

except mysql.connector.Error as e:
    print("Error reading data from MySQL table", e)
finally:
    if connection.is_connected():
        connection.close()
        cursor.close()
