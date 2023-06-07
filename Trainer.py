import sqlite3
#login as a trainer
def login_trainer():
  trainers = sqlite3.connect('trainers.db')
  trainerdb = trainers.cursor()
  username = input("Enter your username: ")
  password = input("Enter your password: ")
  trainerdb.execute("SELECT * FROM trainers WHERE username = ? AND password = ?", (username, password))
  result = trainerdb.fetchone()
  if result:
    print("Login successful")
    return True
  else:
    print("Login unsuccessful")
    return False
trainerloggedin = False 
