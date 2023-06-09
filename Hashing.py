import sqlite3
def hashPW(password):
    result=hash(password)
    #hash a password and put it in a database

    return result

#returns True if input password matches the hashed password taen from the database.
def GetPW(dbpw,password):
    #database call for the hashed password
    #passwordEncrypted=Databasing.GetUserInfo(username)
    if dbpw==hash(password):
        return True
    else:
        return False
    #get hashed password from database

