import sqlite3
import datetime
import random
super_users = sqlite3.connect('super_users.db')
super_usersdb = super_users.cursor()

members = sqlite3.connect('members.db')
memberdb = members.cursor()

def create_member_id():
    current_year = datetime.datetime.now().strftime("%Y")
    last_digit_year = int(current_year[-1])
    print(last_digit_year)
    random_digits = [str(random.randint(0, 9)) for _ in range(7)]
    checksum = (sum(int(digit) for digit in random_digits) + last_digit_year) % 10

    member_id = current_year + ''.join(random_digits) + str(checksum)
    return member_id
print(create_member_id())
memberdb.execute('CREATE TABLE IF NOT EXISTS members (id INTEGER PRIMARY KEY, name TEXT, age INTEGER, Address TEXT, email TEXT, phone INTEGER, password TEXT)')
super_usersdb.execute('CREATE TABLE IF NOT EXISTS super_users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER, Address TEXT, email TEXT, phone INTEGER, password TEXT)')
print("Welcome to the Member Database")

print("1. Add a member")

userinput = input("Enter your choice: ")
if(userinput == "1"): 
    name = input("Enter your name: ")
    age = input("Enter your age: ")
    Address = input("Enter your Address: ")
    email = input("Enter your email: ")
    phone = input("Enter your phone: ")
    password = input("Enter your password: ")
    memberdb.execute("INSERT INTO members (name, age, Address, email, phone, password) VALUES (?, ?, ?, ?, ?, ?)", (name, age, Address, email, phone, password))
    members.commit()
    print("Member added successfully")