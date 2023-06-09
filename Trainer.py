import sqlite3
import Validation
import Hashing
import Logging


#login as a trainer
def login_trainer():
  trainers = sqlite3.connect('trainers.db')
  trainerdb = trainers.cursor()
  username = input("Enter your username: ")
  password = input("Enter your password: ")
  
  #needs to be compared to hash
  trainerdb.execute("SELECT * FROM trainers WHERE username = ? AND password = ?", (username, password))
  result = trainerdb.fetchone()
  if result:
    print("Login successful")
    #close the connection
    Logging.logLoginAttempt(username, True, False, additionalInfo="Trainer Login")
    trainerdb.close()
    trainers.close()
    return True
  else:
    print("Login unsuccessful")
    #close the connection
    Logging.logLoginAttempt(username, False, True, additionalInfo="Trainer Login")
    trainerdb.close()
    trainers.close()    
    return False
trainerloggedin = False

def start_trainer_menu():
  #lets see if you are who you say you are
  tries = 0
  passed = False
  while tries <3 and not passed:
    passed = login_trainer()
    if passed: 
      break
    else:
      print("Please try again. \n these tries will be logged.")
      tries+=1
  
  if tries == 3:
    return
  #if you are who you say you are, then you can do stuff
  trainerloggedin = True
  while(trainerloggedin):
    print("[1] search a member (retrieve member info)")
    print("[2] add a member")
    print("[3] update/modify a member")
    print("[4] alter your own password")
    print("[5] logout")
    answer = input()
    if answer == "1":
      Validation.search_member(input("Enter the member's name: "))
    elif answer == "2":
      Validation.create_member()
    elif answer == "3":
      Validation.create_member()
    elif answer == "4":
      print("Not implemented yet")
    elif answer == "5":
      print("Logging out")
      trainerloggedin = False
      

    

  


  

