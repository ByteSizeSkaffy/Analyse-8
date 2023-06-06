import sqlite3
import datetime
import random
#creates databases if they don't exist

super_users = sqlite3.connect('super_users.db')
super_usersdb = super_users.cursor()

members = sqlite3.connect('members.db')
memberdb = members.cursor()

memberdb.execute('CREATE TABLE IF NOT EXISTS members (id INTEGER PRIMARY KEY, firstname TEXT, Last name TEXT, age INTEGER, gender TEXT, weight INTEGER, Address TEXT, email TEXT, phonenumber INTEGER, password TEXT)')
super_usersdb.execute('CREATE TABLE IF NOT EXISTS super_users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER, Address TEXT, email TEXT, phonenumber INTEGER, password TEXT)')

#populates super user database with super user if database is empty
super_users.execute("SELECT COUNT(*) FROM super_users")
result = super_users.fetchone()
if result[0]==0:
  super_users.execute("INSERT INTO super_users (name, age, Address, email, phonenumber, password) VALUES ('admin', 20, 'admin', 'admin', 1234567890, 'admin')")
  super_users.commit()


def create_member_id():
    current_year = datetime.datetime.now().strftime("%Y")
    last_digit_year = int(current_year[-1])
    print(last_digit_year)
    random_digits = [str(random.randint(0, 9)) for _ in range(7)]
    checksum = (sum(int(digit) for digit in random_digits) + last_digit_year) % 10
    member_id = current_year + ''.join(random_digits) + str(checksum)
    return member_id



print("Welcome to the Member Database")

print("1. Add a member")

userinput = input("Enter your choice: ")
if(userinput == "1"): 
    #Add a member
    firstname = input("Enter your first name: ")
    lastname = input("Enter your last name: ")
    age = input("Enter your age: ")
    phonenumber = input("Enter your phone number: ")
    gender = input("Enter your gender:")
    weight = input("Enter your weight: ")
    address = input("Enter your address: ")
    email = input("Enter your email: ")
    password = input("Enter your password: ")
    member_id = create_member_id()
    memberdb.execute('''
    INSERT INTO members (
      id INTEGER PRIMARY KEY,
      firstname TEXT, Last name TEXT,
      age INTEGER, 
      gender TEXT, 
      weight INTEGER, 
      Address TEXT, 
      email TEXT, 
      phonenumber INTEGER, 
      password TEXT) 
    VALUES (
      member_id,
      firstname, 
      lastname,
      age,
      phonenumber,
      weight,
      address,
      password) ''')
    print("Member added successfully")