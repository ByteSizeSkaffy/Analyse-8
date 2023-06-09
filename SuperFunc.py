import datetime
import sqlite3
import Validation
import Hashing
#infoObject properties: 
#id, firstname, lastname, username, Hpassword(hashed)
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