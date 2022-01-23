from fastapi import FastAPI
import requests
import time
import threading

app = FastAPI()
incidents = {}
password = ('elevateinterviews', 'ElevateSecurityInterviews2021')

@app.on_event("startup")
def startup_event():
    print("loading data first time")
    refresh_incidents()
    print("starting refresh job ever 1 minute")
    threading.Timer(60, refresh_incidents).start()

@app.get("/incidents")
def get_incidents(): 
    return incidents

def refresh_incidents():
    print("refreshing data")
    current_incidents = {}
    request = requests.get('https://incident-api.use1stag.elevatesecurity.io/identities', auth=password)
    ip_to_employeeId = request.json() 

    denials = safely_get_data("https://incident-api.use1stag.elevatesecurity.io/incidents/denial/")  
    addIncidents(current_incidents, denials, 'reported_by', False, ip_to_employeeId, "denial")

    intrusions = safely_get_data("https://incident-api.use1stag.elevatesecurity.io/incidents/intrusion/")
    addIncidents(current_incidents, intrusions, 'internal_ip', True, ip_to_employeeId, "intrusion")
     
    executables = safely_get_data('https://incident-api.use1stag.elevatesecurity.io/incidents/executable/')
    addIncidents(current_incidents, executables, None, True, ip_to_employeeId, "executable")

    misuse = safely_get_data('https://incident-api.use1stag.elevatesecurity.io/incidents/misuse/')
    addIncidents(current_incidents, misuse, 'employee_id', False, ip_to_employeeId, "misuse") 
 
    unauthorized = safely_get_data('https://incident-api.use1stag.elevatesecurity.io/incidents/unauthorized/')
    addIncidents(current_incidents, unauthorized, 'employee_id', False, ip_to_employeeId, "unauthorized") 

    probing = safely_get_data('https://incident-api.use1stag.elevatesecurity.io/incidents/probing/')
    addIncidents(current_incidents, probing, None, True, ip_to_employeeId, "probing") 
    
    other = safely_get_data('https://incident-api.use1stag.elevatesecurity.io/incidents/other/')
    addIncidents(current_incidents, other, 'identifier', False, ip_to_employeeId, "other")        

    global incidents

    incidents = current_incidents 


def addIncidents(incidents, incidents_being_added, key, translateIpToEmployeeId, ip_to_employeeId, type):
    for incident in incidents_being_added:
        incident['type'] = type
        if (translateIpToEmployeeId):
            ip_address = "" 
            internal_ip = incident.get('internal_ip')
            machine_ip = incident.get('machine_ip')
            ip = incident.get('ip')
            if (internal_ip is not None):
                ip_address = internal_ip
            elif (machine_ip is not None): 
                ip_address = machine_ip
            elif (ip is not None):
                ip_address = ip
            employeeId = ip_to_employeeId[ip_address] 
        elif key == "identifier": 
            identifier = incident[key]
            if isinstance(identifier, int):
               employeeId = identifier
               del incident[key] 
            else:
               employeeId = ip_to_employeeId[identifier]
        else: 
            employeeId = incident[key]
            del incident[key]  
        employeeInfo = getOrInitEmployeeInfo(incidents, employeeId)
        priority = incident['priority'] 
        groupedByPriority = employeeInfo[priority]
        groupedByPriority["count"] = groupedByPriority["count"] + 1        
        whereToInsert = 0
        for prior in groupedByPriority["incidents"]:
            if prior['timestamp'] > incident['timestamp']:
                break
            whereToInsert = whereToInsert + 1
        groupedByPriority["incidents"].insert(whereToInsert, incident)
        del incident['priority'] 

def getOrInitEmployeeInfo(incidents, employeeId):
    employeeInfo = incidents.get(employeeId)
    if (employeeInfo == None): 
        employeeInfo = {"low":       {"count":0, "incidents":[] },
                        "medium":    {"count":0, "incidents":[] },
                        "high":      {"count":0, "incidents":[] }, 
                        "critical" : {"count":0, "incidents":[] } } 
        incidents[employeeId] = employeeInfo
    return employeeInfo

def safely_get_data(link): 
   max_tries = 3
   tries = 0
   while (tries < max_tries): 
       try:
           request = requests.get(link, auth=password) 
           return request.json()['results']
       except Exception as e:
           print(e)
       tries = tries + 1
       time.sleep(tries * 0.5)  
            

