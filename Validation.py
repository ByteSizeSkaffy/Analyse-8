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
  search_pattern = '%' + search_key + '%'
  cursor.execute("SELECT * FROM members WHERE firstname LIKE ? OR address LIKE ? OR email LIKE ? OR id LIKE ? OR lastname LIKE ?",
               (search_pattern, search_pattern, search_pattern, search_pattern, search_pattern))
  results = cursor.fetchall()


  # Display the search results
  if results:
    print("Search Results:")
    i=1
    for row in results:
      print(f"row: [{i}] Member ID: {row[0]}, First Name: {row[1]}, Last Name: {row[2]}, Email: {row[7]}, Age: {row[3]}, gender: {row[4]}, Weight: {row[5]} Address: {row[6]}, Phone number:{row[8]}")
      
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

  firstname = input("Enter first name: ")
  lastname = input("Enter last name: ")
  age = input("Enter age: ")
  phonenumber = input("Enter phone number: ")
  gender = input("Enter gender: ")
  weight = input("Enter weight: ")
  address = input("Enter address: ")
  email = input("Enter email: ")
  print(" *----------------\n**Building Member ID**\n    ----------------*")
  member_id = create_member_id()
  
  #hier Password Hash call
  password = Hashing.hashPW(input("Enter password: "))
  member_id = Validation.create_member_id()

  #TODO: check the input for injection attacks
  
  memberdb.execute('''
  INSERT INTO members (
    id, 
    firstname, 
    Lastname, 
    age, 
    gender, 
    weight, 
    Address,
    email,
    phonenumber, 
    password 
    ) 
    VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (
    member_id, 
    firstname, 
    lastname, 
    age, 
    gender, 
    weight, 
    address,
    email, 
    phonenumber, 
    password))
  members.commit()
  print("Member created successfully")
  members.close()


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
  results = search_member(input("Please enter which user you'd like to alter:"))
    
  if results:
    row = int(input("Which user would you like to alter? \nPlease enter the number of the row they're in: "))
       
    if 1 <= row <= len(results):
      selected_user = results[row - 1]
            
      print("Selected User:")
            
    field = int(input("Which field would you like to modify?\n"
    "[1] First Name\n"
    "[2] Last Name\n"
    "[3] Age\n"
    "[4] Phone Number\n"
    "[5] Gender\n"
    "[6] Weight\n"
    "[7] Address\n"
    "[8] Email\n"
    "[9] Password\n"
    "Enter the corresponding number: "))
            
    if 1 <= field <= 9:
     #
     #TODO: check input for injection attacks
     new_value = input("Enter the new value: ")
                
      # Update the selected field for the selected user
    if field == 1:
      memberdb.execute("UPDATE members SET firstname = ? WHERE id = ?", (new_value, selected_user[0]))
    elif field == 2:
      memberdb.execute("UPDATE members SET lastname = ? WHERE id = ?", (new_value, selected_user[0]))
    elif field == 3:
      memberdb.execute("UPDATE members SET age = ? WHERE id = ?", (new_value, selected_user[0]))
    elif field == 4:
      memberdb.execute("UPDATE members SET phonenumber = ? WHERE id = ?", (new_value, selected_user[0]))
    elif field == 5:
      memberdb.execute("UPDATE members SET gender = ? WHERE id = ?", (new_value, selected_user[0]))
    elif field == 6:
      memberdb.execute("UPDATE members SET weight = ? WHERE id = ?", (new_value, selected_user[0]))
    elif field == 7:
      memberdb.execute("UPDATE members SET Address = ? WHERE id = ?", (new_value, selected_user[0]))
    elif field == 8:
      memberdb.execute("UPDATE members SET email = ? WHERE id = ?", (new_value, selected_user[0]))
    elif field == 9:
      #TODO: Password Hash call
      memberdb.execute("UPDATE members SET password = ? WHERE id = ?", (new_value, selected_user[0]))
    members.commit()
    print("User updated successfully!")
  else:
      print("Invalid field number. Please try again.")
  members.close()



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
    random_digits = [str(random.randint(0, 9)) for _ in range(7)]
    checksum = (sum(int(digit) for digit in random_digits) + last_digit_year) % 10
    member_id = current_year + ''.join(random_digits) + str(checksum)
    return member_id