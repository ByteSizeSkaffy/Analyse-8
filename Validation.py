import re
import datetime
import random
import Validation
import sqlite3
import Hashing
#search user
def search_member(search_key):

  # Connect to the SQLite database
  conn = sqlite3.connect('members.db')
  cursor = conn.cursor()

  # Search for members using partial keys should be sql injection safe but im not a cryptographer
  cursor.execute("SELECT * FROM members WHERE name LIKE ? OR address LIKE ? OR email LIKE ? OR phone LIKE ? OR member_id LIKE ?",
               ('%' + search_key + '%', '%' + search_key + '%', '%' + search_key + '%', '%' + search_key + '%' + '%' + search_key + '%'))
  results = cursor.fetchall()

  # Display the search results
  if results:
    print("Search Results:")
    for row in results:
      print(f"Member ID: {row[0]}, Name: {row[1]}, Address: {row[3]}, Email: {row[4]}, Phone: {row[5]}")
      
    # Close the connection    
    cursor.close()
    conn.close()
    return results
  else:
    print("No matching members found.")

    # Close the connection
    cursor.close()
    conn.close()
    return False

#creates a member
def create_member():
  members = sqlite3.connect('members.db')
  memberdb = members.cursor()

  firstname = input("Enter  first name: ")
  lastname = input("Enter  last name: ")
  age = input("Enter  age: ")
  phonenumber = input("Enter  phone number: ")
  gender = input("Enter  gender:")
  weight = input("Enter  weight: ")
  address = input("Enter  address: ")
  email = input("Enter  email: ")
  #hier Password Hash call
  password = Hashing.hashPW(input("Enter password"))
  member_id = Validation.create_member_id()

  
  
  memberdb.execute('''
  INSERT INTO members (
    id INTEGER PRIMARY KEY, 
    firstname TEXT, 
    Last name TEXT, 
    age INTEGER, 
    gender TEXT, 
    weight INTEGER, 
    Address TEXT,
    email TEXT,
    phonenumber INTEGER, 
    password TEXT 
    ) 
    VALUES (
      member_id, 
      firstname, 
      lastname, 
      age, 
      gender, 
      weight, 
      address,
      email, 
      phonenumber, 
      password
      ) ''')
  memberdb.commit()
  memberdb.close()


#checks if username complies with standards laid out in the assignment

def check_username(string):
    # Check if the string length is between 8 and 12 characters
    if len(string) < 8 or len(string) > 12:
      print("Username must be between 8 and 12 characters long")
      return False
    
    # Check if the string starts with a letter or underscore
    if not re.match(r'^[a-zA-Z_]', string):
      print("Username must start with a letter or underscore")
      return False

    # Check if the string contains valid characters
    if not re.match(r'^[a-zA-Z0-9_\'\.]+$', string):
      print("Username must only contain letters, numbers, underscores, apostrophes, and periods")
      return False

    # Convert the string to lowercase for uniqueness *check
    string = string.lower()

    # Check if the string is unique
    unique_set = set()
    for char in string:
        if char in unique_set:
            return False
        unique_set.add(char)
    return True

def modifymember():
   members = sqlite3.connect('members.db')
   memberdb = members.cursor()
   results = search_member(input("please enter which user you'd like to alter:"))




def check_password(string):
    # Check if the string length is between 12 and 30 characters
    if len(string) < 12 or len(string) > 30:
        return False

    # Check if the string contains at least one lowercase letter
    if not re.search(r'[a-z]', string):
        return False

    # Check if the string contains at least one uppercase letter
    if not re.search(r'[A-Z]', string):
        return False

    # Check if the string contains at least one digit
    if not re.search(r'\d', string):
        return False

    # Check if the string contains at least one special character
    if not re.search(r'[~!@#$%&_\-=\\|()\[\]{}:;\'<>,.?/]', string):
        return False

    return True

#creates a member id
def create_member_id():
    current_year = datetime.datetime.now().strftime("%Y")
    last_digit_year = int((datetime.datetime.now().strftime("%Y")))%10
    print(last_digit_year)
    random_digits = [str(random.randint(0, 9)) for _ in range(7)]
    checksum = (sum(int(digit) for digit in random_digits) + last_digit_year) % 10
    member_id = current_year + ''.join(random_digits) + str(checksum)
    return member_id