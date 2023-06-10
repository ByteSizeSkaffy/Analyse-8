import sqlite3
import datetime
import random
import re
import Validation
import Trainer
import sys
import Logging
import SuperFunc
import Hashing

#creates databases if they don't exist
super_usersdb = sqlite3.connect('super_users.db')
super_users = super_usersdb.cursor()
trainersdb = sqlite3.connect('trainers.db')
trainerdb = trainersdb.cursor()

membersdb = sqlite3.connect('members.db')
memberdb = membersdb.cursor()

super_users.execute('CREATE TABLE IF NOT EXISTS super_users (id INTEGER PRIMARY KEY, firstname TEXT, lastname TEXT, username TEXT, password TEXT, registrationdate TEXT)')
trainerdb.execute('CREATE TABLE IF NOT EXISTS trainers (id INTEGER PRIMARY KEY, firstname TEXT, lastname TEXT, username TEXT, password TEXT, registrationdate TEXT)')
memberdb.execute('CREATE TABLE IF NOT EXISTS members (id INTEGER PRIMARY KEY, firstname TEXT, lastname TEXT, age INTEGER, gender TEXT, weight INTEGER, Address TEXT, email TEXT, phonenumber INTEGER, password TEXT)')

super_usersdb.commit()
trainersdb.commit()
membersdb.commit()

# Populates super user database with a super user if the table is empty
super_users.execute("SELECT COUNT(*) FROM super_users")
result = super_users.fetchone()

if result[0] == 0:
    suprim = Validation.create_member_id()  # Assuming you have the implementation for create_member_id()
    trainerprim = Validation.create_member_id()  # Assuming you have the implementation for create_member_id()

    super_users.execute("INSERT INTO super_users (id, firstname, lastname, username, password, registrationdate) VALUES (?, ?, ?, ?, ?, ?)", (suprim, 'admin', 'adminson', 'super_admin', Hashing.hashPW('admin_123!'), '21/9/2023'))
    trainerdb.execute("INSERT INTO trainers (id, firstname, lastname, username, password, registrationdate) VALUES (?, ?, ?, ?, ?, ?)", (trainerprim, 'joe', 'bolsum', Hashing.hashPW('thisguy123'), 'trainer', '20/10/2011'))
    memberdb.execute("INSERT INTO members (id, firstname, lastname, age, gender, weight, Address, email, phonenumber, password) VALUES (?,?,?,?,?,?,?,?,?,?)",(212328742,'Mike', 'Thomson', 12, 'man', 123, '123 fake street', 'thompson@hotmale.com', 3198762716, Hashing.hashPW("member")))
 
    trainersdb.commit()
    super_usersdb.commit()
    membersdb.commit()

super_users.close()
trainerdb.close()
membersdb.close()

while True:
  print("Welcome to the Member Database")

  print("1. log in as a trainer")
  print("2. Log in as Admin")

print("1. Add a member")
print("2. log in as a trainer")


userinput = input("Enter your choice: ")
if(userinput == "1"):
    Validation.create_member()
elif(userinput == "2"):
    Trainer.start_trainer_menu()
