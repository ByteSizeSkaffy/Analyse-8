import datetime
import sqlite3
import Validation
import Hashing
import Logging
import json
#infoObject properties: 
#id, firstname, lastname, username, Hpassword(hashed)
def AdminMenuing():
    print("Welcome to The admin Menu, Please log in first")
    LoggedInAdmin=False
    lockout=0
    while LoggedInAdmin==False:
        if lockout>=3:
            print("Login failed three times. Exiting")
            Logging.LogWarning()
            exit()
        LoggedInAdmin=AdminLogin()
        if LoggedInAdmin==False:
            print("Error, Invalid Login attempt. Please check your username and password and try again")
            lockout+=1
        elif LoggedInAdmin!=False:
            break
    print(f"Welcome{LoggedInAdmin.name}, What would you like to do?")
    userInput=input("")
    


def AdminLogin():
    admins = sqlite3.connect('super_users.db')
    admindb = admins.cursor()
    username = input("Enter your username: ")
    valUSR=Validation.check_username(username)
    password = input("Enter your password: ")
    valPW=Validation.check_password(password)
    result=False
    if not (valUSR or valPW):
        result=False
    else:
    #needs to be compared to hash
        admindb.execute("SELECT * FROM super_users WHERE username = ? AND password = ?", (username, Hashing.hashPW(password)))
        result = admindb.fetchone()
    if result:
        print("Login successful")
        #close the connection
        Logging.logLoginAttempt(username, True, False, additionalInfo="Admin Login")
        admindb.close()
        admins.close()
        return admin(result[0],result[3])
    else:
        print("Login unsuccessful")
        #close the connection
        Logging.logLoginAttempt(username, False, True, additionalInfo="Trainer Login")
        admindb.close()
        admins.close()    
        return False

class admin:
    def __init__(self,Name,ID):
        self.name=Name
        self.ID=ID
    #admin class makes admin funcs only callable if there is an active admin object
    #do same for trainer? ask mees
    #add: Trainer functions (copy)
    #add trainer
    #modify trainer
    #delete trainer
    #Reset trainer password


    def readLogs():
        with open('logs.json', 'r') as file:
            data=json.load(file)
            for item in data:
                print(f'{data[item]["Username"]} performed action: {data[item]["action"]} on {data[item]["date"]}, which was ' +( "Successful" if data[item]["passed"] else "unsuccessful")+("| Warning! possible suspicious activity" if data[item]["sussy"] else "")+". Additional info: " + (data[item]["additionalInfo"] if data[item]["additionalInfo"] != "" else "none"))


    
class Super(admin):

    def CreateAdmin():
        id=Validation.create_member_id()
        print("This will create an admin user")
        firstname=input("Input First name of user: ")
        lastname=input("Input last Name of user: ")
        username=input("input Username: ")
        password=Hashing.hashPW(input("Input user password"))

    def InsertAdmin(infoObject):
        regDate=str(datetime.datetime.now())
        super_usersdb = sqlite3.connect('super_users.db')
        super_users=super_usersdb.cursor()
        super_users.execute("INSERT INTO super_users (id, firstname, lastname, username, password, registrationdate) VALUES (?, ?, ?, ?, ?, ?)", 
                            (infoObject["id"], infoObject["firstname"], infoObject["lastname"], infoObject["username"], infoObject["Hpassword"], '21/9/2023'))