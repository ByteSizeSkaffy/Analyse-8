import sqlite3
import datetime
import random
import re
import Validation
import Trainer
#creates databases if they don't exist

super_usersdb = sqlite3.connect('super_users.db')
super_users = super_usersdb.cursor()

trainers = sqlite3.connect('trainers.db')
trainerdb = trainers.cursor()

members = sqlite3.connect('members.db')
memberdb = members.cursor()

memberdb.execute('CREATE TABLE IF NOT EXISTS members (id INTEGER PRIMARY KEY, firstname TEXT, Last name TEXT, age INTEGER, gender TEXT, weight INTEGER, Address TEXT, email TEXT, phonenumber INTEGER, password TEXT)')
super_users.execute('CREATE TABLE IF NOT EXISTS super_users (id INTEGER PRIMARY KEY, firstname TEXT, lastname TEXT,username TEXT, password TEXT, registrationdate TEXT)')
trainerdb.execute('CREATE TABLE IF NOT EXISTS trainers (id INTEGER PRIMARY KEY, firstname TEXT, lastname TEXT,username TEXT, password TEXT, registrationdate TEXT)')

#populates super user database with super user if database is empty
super_users.execute("SELECT COUNT(*) FROM super_users")

result = super_users.fetchone()
if result[0]==0:
  super_users.execute("INSERT INTO super_users (name, age, username, registrationdate, password) VALUES ('admin', 20, 'super_admin', '21/9/2023', 'admin_123!')")
  trainerdb.execute("INSERT INTO trainers (name, age, username, registrationdate, password) VALUES ('joe', 20, 'trainer', '20/10/2011','trainer')")
  memberdb.execute('''INSERT INTO members (
    id INTEGER PRIMARY KEY, 
    firstname TEXT, Last name TEXT, 
    age INTEGER, gender TEXT, weight INTEGER, 
    Address TEXT, email TEXT, phonenumber INTEGER, 
    password TEXT) 
        VALUES (
      212328742,
      'Mike', 
      'Thomson', 
      'man',
      '',
      123,
      '123 fake street',
      'thompson@hotmale.com',
      3198762716, 
      'member')''') 
  trainerdb.commit()
  super_users.commit()
  memberdb.commit()

super_users.close()
trainerdb.close()
memberdb.close()


print("Welcome to the Member Database")

print("1. Add a member")
print("2. log in as a trainer")


userinput = input("Enter your choice: ")
if(userinput == "1"): 
  #Add a member
  Validation.create_member()
  print("Member added successfully")
elif(userinput == "2"):
  #login as a trainer
  trainerloggedin = Trainer.login_trainer()
if(trainerloggedin):
  print("1. Add a member")
  print("2. Search for a member")
  print("3. Update your password")
  print("4. modify a member")
if(userinput == "1"):
  Trainer.create_member()
elif(userinput == "2"):
  searchquery = input("Enter your search query: ")
  Validation.search_members(searchquery)
