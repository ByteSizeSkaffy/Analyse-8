import sys
import json
import datetime

#how to log:
# make method with inputs of your choice
# made logObject using logLoginattempt as template
# call LogGeneric
def FileExistsCheck():
    try:
        with open("logs.json","r"):
            pass
    except:
        with open("logs.json","w+") as file:
            addObject={
                f"Beginning of file at {datetime.datetime.now()}":{
                    "Username":"none",
                    "action":"FileCreation",
                    "passed":True,
                    "sussy":True,
                    "additionalInfo":"Log file was created because it wasn't found or did not exist",
                    "date":str(datetime.datetime.now())
                }
            }
            file.write(json.dumps(addObject))

def logInsert(infoObject,admin):
    action="Created new Admin account"
    logObject={
        "action":action,
        "Username":admin.name,
        "passed":True,
        'sussy':False,
        'additionalInfo':"Username of created account: "+ infoObject["username"],
        "date":str(datetime.datetime.now())
    }
    logGeneric(infoObject)

def logLoginAttempt(Username, passed, sussy, additionalInfo=""):
    action="login"
    logObject={
        "action":action,
        "Username":Username,
        "passed":passed,
        'sussy':sussy,
        'additionalInfo':additionalInfo,
        "date":str(datetime.datetime.now())

    }
    logGeneric(logObject)

def LogWarning():
    logGeneric({
        "action":"Admin Login",
        "Username":"A user",
        "passed":False,
        'sussy':True,
        'additionalInfo':"Login Failed Three times. Exiting.",
        "date":str(datetime.datetime.now())
    })

def logGeneric(logObject):
    FileExistsCheck()
    with open('logs.json', 'r+') as file:
        data=json.loads(file.read())
        file.seek(0)
        
        addObject={
            "Username":logObject['Username'],
            "action":logObject["action"],
            "passed":logObject["passed"],
            "sussy":logObject["sussy"],
            "additionalInfo":logObject["additionalInfo"],
            "date":logObject['date']
            }
        
        data[f"{logObject['Username']} at {logObject['date']}"]=(addObject)
        json_object = json.dumps(data, indent=4)
        file.write(json_object)

def readLogs():
    with open('logs.json', 'r') as file:
        data=json.load(file)
        for item in data:
            print(f'{data[item]["Username"]} performed action: {data[item]["action"]} on {data[item]["date"]}, which was ' +( "Successful" if data[item]["passed"] else "unsuccessful")+("| Warning! possible suspicious activity" if data[item]["sussy"] else "")+". Additional info: " + (data[item]["additionalInfo"] if data[item]["additionalInfo"] != "" else "none"))