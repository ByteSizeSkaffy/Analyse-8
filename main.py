import sqlite3
import datetime
import random
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
  trainerdb.commit()
  super_users.commit()

#creates a member id
def create_member_id():
    current_year = datetime.datetime.now().strftime("%Y")
    last_digit_year = (datetime.datetime.now().strftime("%Y"))%10
    print(last_digit_year)
    random_digits = [str(random.randint(0, 9)) for _ in range(7)]
    checksum = (sum(int(digit) for digit in random_digits) + last_digit_year) % 10
    member_id = current_year + ''.join(random_digits) + str(checksum)
    return member_id

#creates a member
def create_member():
  firstname = input("Enter your first name: ")
  lastname = input("Enter your last name: ")
  age = input("Enter your age: ")
  phonenumber = input("Enter your phone number: ")
  gender = input("Enter your gender:")
  weight = input("Enter your weight: ")
  address = input("Enter your address: ")
  email = input("Enter your email: ")
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
    ) 
    VALUES (
      member_id,
      firstname, 
      lastname,
      age,
      phonenumber,
      weight,
      address
      ) ''')
  memberdb.commit()
#search user

def search_members(search_key):

  # Connect to the SQLite database
  conn = sqlite3.connect('members.db')
  cursor = conn.cursor()

  # Search for members using partial keys
  cursor.execute("SELECT * FROM members WHERE name LIKE ? OR address LIKE ? OR email LIKE ? OR phone LIKE ? OR member_id LIKE ?",
               ('%' + search_key + '%', '%' + search_key + '%', '%' + search_key + '%', '%' + search_key + '%' + '%' + search_key + '%'))
  results = cursor.fetchall()

  # Display the search results
  if results:
    print("Search Results:")
    for row in results:
      print(f"Member ID: {row[0]}, Name: {row[1]}, Address: {row[3]}, Email: {row[4]}, Phone: {row[5]}")
  else:
    print("No matching members found.")

    # Close the database connection
    cursor.close()
    conn.close()

#login as a trainer
def login_trainer():
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

print("Welcome to the Member Database")

print("1. Add a member")
print("2. log in as a trainer")


userinput = input("Enter your choice: ")
if(userinput == "1"): 
  #Add a member
  create_member()
  print("Member added successfully")
elif(userinput == "2"):
  #login as a trainer
  trainerloggedin = login_trainer()

if(trainerloggedin):
  print("1. Add a member")
  print("2. Search for a member")
  print("3. Update your password")
  print("4. modify a member")
if(userinput == "1"):
  create_member()
elif(userinput == "2"):
  searchquery = input("Enter your search query: ")
  search_members(searchquery)
