import sqlite3
import Hashing
import Logging
#login as a trainer
def login_trainer():
  trainers = sqlite3.connect('trainers.db')
  trainerdb = trainers.cursor()
  username = input("Enter your username: ")
  password = input("Enter your password: ")
  trainerdb.execute("SELECT * FROM trainers WHERE username = ? AND password = ?", (username, Hashing.hashPW(password)))
  result = trainerdb.fetchone()
  if result:
    print("Login successful")
    Logging.logLoginAttempt(username, True, False, additionalInfo="Trainer Login")
    return True
  else:
    print("Login unsuccessful")
    Logging.logLoginAttempt(username, False, True, additionalInfo="Trainer Login")
    return False
trainerloggedin = False 
