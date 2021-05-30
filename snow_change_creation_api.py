#!/usr/bin/python3

#Create standard change in ServiceNow using Python API

import requests
import sys
import json
import time

# request parameters
snow_url = '<snow_url>'
tmpt_id = '<standard change template id>'
user = '<user_id>'
pwd = '<pwd>'
schdl_start_time = '<schedule start time> e.g.,2021-06-01 18:00:00'
schdl_end_time = '<schedule start time> e.g.,2021-06-02 18:00:00'
cmdb_ci_sys_id = '<ci_sys_id>,<ci_sys_id>'

# Headers
headers = {"Accept":"application/json", "Content-Type":"application/json"}

#create change request using standard template
sn_url = snow_url + "/api/sn_chg_rest/change/standard/" + tmpt_id

# Do the HTTP request
response = requests.post(sn_url, auth=(user, pwd), headers=headers )

# Check the respose code and proceed further
if response.status_code != 200:
    print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:', response.content)
    exit()
else :
    #Get Change Sys ID
    chg_sys_id_ft = response.json()['result']['sys_id']['value']
    chg_sys_id = chg_sys_id_ft.strip('"')
    chg_nu_ft = response.json()['result']['number']['value']
    chg_nu = chg_nu_ft.strip('"')

    #Get change task details
    chg_tsk_url = snow_url + "/api/sn_chg_rest/change/" + chg_sys_id + "/task"

    tsk_response = requests.get(chg_tsk_url, auth=(user, pwd), headers=headers )

    # Check the respose code and proceed further
    if tsk_response.status_code != 200:
        print('Status-Task:', tsk_response.status_code, 'Headers:', tsk_response.headers, 'Error Response:', tsk_response.content)
        exit()
    else :
        #Get Change Task ID
        chg_sys_tsk = tsk_response.json()
        task_one = chg_sys_tsk['result'][0]['sys_id']['value']
        task_two = chg_sys_tsk['result'][1]['sys_id']['value']

#####################################################

    #Update schedule in change tasks
    chg_tsk_one_sch_url = snow_url + "/api/sn_chg_rest/change/" + chg_sys_id + "/task/" + task_one

    data = {"planned_start_date": schdl_start_time,"planned_end_date": schdl_end_time }
    tsk_one_sch_response = requests.patch(chg_tsk_one_sch_url, auth=(user, pwd), headers=headers, json=data )

    if tsk_one_sch_response.status_code != 200:
        print('Status-Task-Schedule1:', tsk_one_response.status_code, 'Headers:', tsk_one_response.headers, 'Error Response:', tsk_one_response.content)
        exit()

    chg_tsk_two_sch_url = snow_url + "/api/sn_chg_rest/change/" + chg_sys_id + "/task/" + task_two

    tsk_two_sch_response = requests.patch(chg_tsk_two_sch_url, auth=(user, pwd), headers=headers, json=data )

    if tsk_two_sch_response.status_code != 200:
        print('Status-Task-Schedule2:', tsk_two_response.status_code, 'Headers:', tsk_two_response.headers, 'Error Response:', tsk_two_response.content)
        exit()

######################################################

    #Update schedule in change
    chg_sch_url = snow_url + "/api/sn_chg_rest/change/standard/" + chg_sys_id

    data_chg = {"start_date": schdl_start_time,"end_date": schdl_end_time}
    chg_sch_response = requests.patch(chg_sch_url, auth=(user, pwd), headers=headers, json=data_chg )

    if chg_sch_response.status_code != 200:
        print('Status-Change-Schedule:', chg_sch_response.status_code, 'Headers:', chg_sch_response.headers, 'Error Response:', chg_sch_response.content)
        exit()
    else :
######################################################

        #Add Affected CI into the change record
        chg_ci_url = snow_url + "/api/sn_chg_rest/change/" + chg_sys_id + "/ci"

        data_ci = {"cmdb_ci_sys_ids": cmdb_ci_sys_id, "association_type": "affected"}
        chg_ci_response = requests.post(chg_ci_url, auth=(user, pwd), headers=headers, json=data_ci)

        if chg_ci_response.status_code != 202 :
            print('Status-Change-CI:', chg_ci_response.status_code, 'Headers:', chg_ci_response.headers, 'Error Response:', chg_ci_response.content)
            exit()
        else :
######################################################
            time.sleep(30)
            #Risk Analysis
            chg_risk_url = snow_url + "/api/sn_chg_rest/change/" + chg_sys_id + "/risk"

            chg_risk_response = requests.patch(chg_risk_url, auth=(user, pwd), headers=headers )

            if chg_risk_response.status_code != 200 :
                print('Status-Change-Risk:', chg_risk_response.status_code, 'Headers:', chg_risk_response.headers, 'Error Response:', chg_risk_response.content)
                exit()
            else :
######################################################

                #Conflict Anaysis
                chg_conf_url = snow_url + "/api/sn_chg_rest/change/" + chg_sys_id + "/conflict"

                chg_conf_response = requests.post(chg_conf_url, auth=(user, pwd), headers=headers )

                if chg_conf_response.status_code != 202 :
                    print('Status-Change-Conflict:', chg_conf_response.status_code, 'Headers:', chg_conf_response.headers, 'Error Response:', chg_conf_response.content)
                    exit()
                else :
                    print(chg_nu)

###########################
#END_OF_SCRIPT
