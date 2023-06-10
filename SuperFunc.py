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
    print("1. update your password\n 2. check user list\n 3. add new trainer to system\n 4. modify or delete a Trainer account\n 5. Manage Backups")
    userInput=int(input("7. see the logs\n add a member to the system\n 9. modify a member's information\n 10. Delete a member\n 11. seach and retrieve member information"+
                        ("12. add new Admin to the system\n 13. modify or delete admin account\n 14. reset admin password" if type(LoggedInAdmin)==SAdm else "")))
    Validation.validateMenuInput(userInput, 7)
    


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
    if result[3]=="super_admin":
        print("Login successful")
        #close the connection
        Logging.logLoginAttempt(username, True, False, additionalInfo="Admin Login")
        admindb.close()
        admins.close()
        return SAdm(result[0],result[3])
    elif result:
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


    
class SAdm(admin):

    def CreateAdmin(self):
        print("This will create an admin user")
        firstname=input("Input First name of user: ")
        lastname=input("Input last Name of user: ")
        username=input("input Username: ")
        password=Hashing.hashPW(input("Input user password"))
        infoObject={
            "id": Validation.create_member_id(),
            "firstname": firstname,
            "lastname": lastname,
            "username": username,
            "Hpassword": password,
            "registrationdate":str(datetime.datetime.now())
        }
        self.InsertAdmin()

    def InsertAdmin(self,infoObject):
        Logging.logInsert(infoObject,self)
        super_usersdb = sqlite3.connect('super_users.db')
        super_users=super_usersdb.cursor()
        super_users.execute("INSERT INTO super_users (id, firstname, lastname, username, password, registrationdate) VALUES (?, ?, ?, ?, ?, ?)", 
                            (infoObject["id"], infoObject["firstname"], infoObject["lastname"], infoObject["username"], infoObject["Hpassword"], infoObject["registrationdate"]))
        super_usersdb.commit()
        super_usersdb.close
    
    def checkUserList():
        trainerDB= sqlite3.connect('trainers.db')
        superDB= sqlite3.connect('super_users.db')
        train=trainerDB.cursor()
        soup=superDB.cursor()
        print("Listing Trainers: ")
        res=train.execute("SELECT * FROM trainers")
        stuff=res.fetchall()
        for item in stuff:
            print(item)
        
        print("Listing Trainers: ")
        res=soup.execute("SELECT * FROM super_users")
        stuff=res.fetchall()
        for item in stuff:
            print(item)
