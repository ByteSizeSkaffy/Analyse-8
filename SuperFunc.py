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
    while True:
        print(f"Welcome{LoggedInAdmin.name}, What would you like to do?")
        print("pick an option by typing a number and pressing ENTER")
        print("1. update your password\n 2. check user list\n 3. add new trainer to system\n 4. modify a Trainer account\n 5. Delete a Trainer account\n 6. Manage Backups")
        userInput=int(input("7. see the logs\n 8. add a member to the system\n 9. modify a member's information\n 10. Delete a member\n 11. seach and retrieve member information"+
                            ("12. add new Admin to the system\n 13. modify or delete admin account\n 14. reset admin password" if type(LoggedInAdmin)==SAdm else "")))
        Validation.validateMenuInput(userInput, 14 if type(LoggedInAdmin)==SAdm else 11)
        if userInput==1:
            LoggedInAdmin.ChangeAdminPassword(LoggedInAdmin.ID)
        elif userInput==2:
            LoggedInAdmin.checkUserList()
        elif userInput==3:
            LoggedInAdmin.createTrainer()
        elif userInput==4:
            LoggedInAdmin.ModifyTrainer()
        elif userInput==5:
            LoggedInAdmin.deleteTrainer()
        elif userInput==6:
            LoggedInAdmin.manageBackups()
        elif userInput==7:
            Logging.readLogs()
        elif userInput==8:
            Validation.create_member()
        elif userInput==9:
            Validation.modifymember()
        elif userInput==10:
            LoggedInAdmin.deleteMember()
        elif userInput==11:
            Validation.search_member(input("Enter the member's name: "))
        elif userInput==12 and type(LoggedInAdmin)==SAdm:
            LoggedInAdmin.CreateAdmin()
        elif userInput==13 and type(LoggedInAdmin)==SAdm:
            LoggedInAdmin.modifyAdmin()
        elif userInput==14 and type(LoggedInAdmin)==SAdm:
            LoggedInAdmin.ChangeAdminPassword(LoggedInAdmin.ID)

    


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
    def createTrainer(self):
        superdb = sqlite3.connect('super_users.db')
        supDbC = superdb.cursor()

        firstname = input("Enter first name: ")
        lastname = input("Enter last name: ")
        age = input("Enter age: ")
        phonenumber = input("Enter phone number: ")
        gender = input("Enter gender: ")
        weight = input("Enter weight: ")
        address = input("Enter address: ")
        email = input("Enter email: ")
        print(" *----------------\n**Building Member ID**\n    ----------------*")
        member_id = Validation.create_member_id()
        
        #hier Password Hash call
        password = Hashing.hashPW(input("Enter password: "))
        

        #TODO: check the input for injection attacks
        
        supDbC.execute('''
        INSERT INTO superdb (
            id, 
            firstname, 
            Lastname, 
            age, 
            gender, 
            weight, 
            Address,
            email,
            phonenumber, 
            password 
            ) 
            VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (
            member_id, 
            firstname, 
            lastname, 
            age, 
            gender, 
            weight, 
            address,
            email, 
            phonenumber, 
            password))
        superdb.commit()
        print("Member created successfully")
        superdb.close()
    
    def ModifyTrainer(self):
        raise NotImplemented
    
    def deleteTrainer(self):
        raise NotImplemented

    def manageBackups(self):
        raise NotImplemented
    
    def deleteMember(self):
        raise NotImplemented
    
    def modifyAdmin(self):
        raise NotImplemented

    def checkUserList(self):
        trainerDB= sqlite3.connect('trainers.db')
        superDB= sqlite3.connect('super_users.db')
        train=trainerDB.cursor()
        soup=superDB.cursor()
        print("Listing Trainers: ")
        res=train.execute("SELECT * FROM trainers")
        stuff=res.fetchall()
        for item in stuff:
            print(f"name: {item[1]}, Role: Trainer, username: {item[3]}, Last name: {item[2]}")
        
        print("Listing Admins: ")
        res=soup.execute("SELECT * FROM super_users")
        stuff=res.fetchall()
        for item in stuff:
            print (f"name: {item[1]}, Role: You (Super admin), username: {item[3]}, Last name: {item[2]}") if item[3]=="super_admin" else f"name: {item[1]}, Role: Admin, username: {item[3]}, Last name: {item[2]}"    

    def ChangeAdminPassword(self,ID):
        trainers = sqlite3.connect('super_users.db')
        trainerdb = trainers.cursor()
        print("Changing your password")
        #TODO: make sure the password is strong enough
        password = input("Enter your new password: ")
        #TOdo: hash the password
        trainerdb.execute("UPDATE super_users SET password = ? WHERE id = ?", (Hashing.hashPW(password), ID))
        trainers.commit()
        print("Password changed successfully")
        trainerdb.close()
        trainers.close()

    def readLogs(self):
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
